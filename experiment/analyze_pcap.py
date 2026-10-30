import struct, sys, collections, datetime, time

FN = r'D:\test\cbjq-re\experiment\cbjq_capture.pcapng'
OUT = r'D:\test\cbjq-re\experiment\pcap_analysis.txt'

TARGET = bytes([42, 192, 24, 211])  # 42.192.24.211

tcp_sess = collections.Counter()
tcp_bytes = collections.Counter()
udp_sess = collections.Counter()
target_pkts = []          # 42.192.24.211 相关包
dns_rr = collections.defaultdict(set)   # qname -> set(ip)
dns_timeline = []         # (ts_sec, qname)
syn_events = []           # (ts_sec, dst_ip, dport)
ip_pkt_count = collections.Counter()    # dst ip -> count

n = 0
link_type = 1
tsresol = 6
first_ts = None
t0 = time.time()

def ip2s(b):
    return '.'.join(str(x) for x in b)

def parse_dns_name(payload, off, depth=0):
    labels = []
    jumps = 0
    while off < len(payload) and jumps < 30:
        if off >= len(payload): break
        l = payload[off]
        if l == 0:
            off += 1
            break
        if (l & 0xc0) == 0xc0:
            if off+1 >= len(payload): break
            ptr = struct.unpack('>H', payload[off:off+2])[0] & 0x3fff
            off2 = ptr
            sub, _ = parse_dns_name(payload, off2, depth+1) if depth < 3 else ('', ptr)
            if sub: labels.append(sub)
            off += 2
            return '.'.join(labels), off
        if l > 63: break
        labels.append(payload[off+1:off+1+l].decode('ascii', 'replace'))
        off += 1 + l
        jumps += 1
    return '.'.join(labels), off

def analyze_dns(payload, is_resp, ts):
    try:
        if len(payload) < 12: return
        tid, flags, qd, an, ns, ar = struct.unpack('>HHHHHH', payload[:12])
        off = 12
        qnames = []
        for _ in range(qd):
            name, off = parse_dns_name(payload, off)
            if off+4 > len(payload): break
            qtype, qclass = struct.unpack('>HH', payload[off:off+4])
            off += 4
            if name: qnames.append(name)
        if qnames and not is_resp:
            dns_timeline.append((ts, qnames[0]))
        # 解析 answers
        if is_resp and an > 0:
            for _ in range(min(an, 20)):
                if off >= len(payload): break
                # name
                if (payload[off] & 0xc0) == 0xc0:
                    off += 2
                else:
                    _, off = parse_dns_name(payload, off)
                if off+10 > len(payload): break
                rtype, rclass, ttl, rdlen = struct.unpack('>HHIH', payload[off:off+10])
                off += 10
                if rtype == 1 and rdlen == 4:  # A record
                    ip = ip2s(payload[off:off+4])
                    if qnames:
                        dns_rr[qnames[0]].add(ip)
                off += rdlen
    except Exception:
        pass

with open(FN, 'rb') as f:
    while True:
        hdr = f.read(8)
        if len(hdr) < 8: break
        btype, blen = struct.unpack('<II', hdr)
        if blen < 12 or blen > 16_000_000:
            break
        body = f.read(blen - 12)
        f.read(4)  # trailing length
        n += 1
        if n % 200000 == 0:
            print(f'  ... {n} blocks, {time.time()-t0:.0f}s', flush=True)

        if btype == 1:  # IDB
            if len(body) >= 8:
                link_type = struct.unpack('<H', body[0:2])[0]
        elif btype == 6:  # EPB
            if len(body) < 20: continue
            iface, tsh, tsl, caplen, origlen = struct.unpack('<IIIII', body[0:20])
            data = body[20:20+caplen]
            ts64 = (tsh << 32) | tsl
            ts_sec = ts64 / 1e6
            if first_ts is None: first_ts = ts_sec

            off = 14 if link_type == 1 else 0
            if link_type == 1:
                if len(data) < 14: continue
                eth_type = struct.unpack('>H', data[12:14])[0]
                if eth_type != 0x0800:
                    continue
            if len(data) < off + 20: continue
            ihl = (data[off] & 0x0f) * 4
            proto = data[off + 9]
            src = data[off + 12:off + 16]
            dst = data[off + 16:off + 20]
            l4 = data[off + ihl:]

            if proto == 6 and len(l4) >= 20:
                sport, dport = struct.unpack('>HH', l4[0:4])
                flags = l4[13]
                key = (ip2s(src), ip2s(dst), sport, dport)
                tcp_sess[key] += 1
                tcp_bytes[key] += origlen
                ip_pkt_count[ip2s(dst)] += 1
                if (flags & 0x02) and not (flags & 0x10):  # SYN without ACK
                    syn_events.append((ts_sec, ip2s(dst), dport))
                if src == TARGET or dst == TARGET:
                    if len(target_pkts) < 400:
                        target_pkts.append((ts_sec, ip2s(src), sport, ip2s(dst), dport, flags, origlen))
            elif proto == 17 and len(l4) >= 8:
                sport, dport = struct.unpack('>HH', l4[0:4])
                udp_sess[(ip2s(src), ip2s(dst), sport, dport)] += 1
                if 53 in (sport, dport):
                    is_resp = (sport == 53)
                    analyze_dns(l4[8:], is_resp, ts_sec)

total = time.time() - t0

def fmt_ts(ts):
    return datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S.%f')[:-3] if ts else '?'

lines = []
A = lines.append
A(f'=== pcap 分析报告（共 {n} 个块，耗时 {total:.0f}s）===')
A(f'链路类型: {link_type}，首包时间: {fmt_ts(first_ts)}')
A('')
A(f'=== [1] DNS 记录（若命中重点域名列出全部，其余列出解析到非公网/可疑的）===')
kw = ('xoyo', 'xgsdk', 'cbjq', 'seasun', 'amazing', 'jxsj', 'snowbreak', 'qcloud', 'myqcloud', 'unreal')
for qname, ips in sorted(dns_rr.items()):
    if any(k in qname.lower() for k in kw):
        A(f'  {qname} -> {sorted(ips)}')
A('')
A('其它 DNS 解析（全部域名，去重）:')
other = {q: ips for q, ips in dns_rr.items() if not any(k in q.lower() for k in kw)}
for qname, ips in sorted(other.items()):
    A(f'  {qname} -> {sorted(ips)}')
A('')
A('=== [2] 42.192.24.211 的连接建立过程 ===')
A(f'  目标相关包数（前400条）: {len(target_pkts)}')
for (ts, s, sp, d, dp, fl, ln) in target_pkts[:60]:
    flg = ''.join(x for x, b in [('S',2),('A',0x10),('F',1),('R',4),('P',8)] if fl & b)
    A(f'  {fmt_ts(ts)}  {s}:{sp} -> {d}:{dp}  flags={flg} len={ln}')
A('')
A('=== [3] 连接 42.192.24.211 之前的连接建立时间线（SYN 事件，倒序找最近的）===')
# 找 42.192.24.211 的第一个 SYN 时间
t_first = None
for (ts, d, dp) in syn_events:
    if d == '42.192.24.211':
        t_first = ts
        break
if t_first:
    A(f'  首次连接 42.192.24.211 的 SYN: {fmt_ts(t_first)}')
    window_start = t_first - 15
    A(f'  --- 该时刻前 15 秒内的所有新建连接 (SYN) ---')
    for (ts, d, dp) in syn_events:
        if window_start <= ts <= t_first + 5:
            A(f'    {fmt_ts(ts)}  -> {d}:{dp}')
    A(f'  --- 该时刻前 15 秒内的 DNS 查询 ---')
    for (ts, q) in dns_timeline:
        if window_start <= ts <= t_first + 5:
            A(f'    {fmt_ts(ts)}  {q}')
else:
    A('  未发现直接连 42.192.24.211 的 SYN（可能被截断或走别的路径）')
A('')
A('=== [4] TCP 会话排行（按包数 Top 30）===')
for key, cnt in tcp_sess.most_common(30):
    s, d, sp, dp = key
    A(f'  {cnt:>7} pkts  {tcp_bytes[key]/1e6:>9.2f} MB  {s}:{sp} -> {d}:{dp}')
A('')
A('=== [5] 目标 IP 流量聚合（按目的 IP，Top 30）===')
for ip, cnt in ip_pkt_count.most_common(30):
    A(f'  {cnt:>7} pkts  -> {ip}')

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f'分析完成 -> {OUT}')
