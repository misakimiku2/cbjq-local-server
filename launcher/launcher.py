# -*- coding: utf-8 -*-
"""
尘白禁区 · 本地服务器 一键启动器
================================
双击桌面快捷方式"尘白禁区-本地服"即可：
  1. 自动启动「地址接管服务」（Mock, 443端口）—— 接线员
  2. 自动启动「游戏服务器」（acacia, 5200端口）—— 内容屋
  3. 自动打开「网页控制台」—— 查看状态 + 一键 GM 工具

关闭方式：在网页控制台点击「关闭全部服务」。
"""
import os
import sys
import json
import ssl
import time
import socket
import ctypes
import threading
import subprocess
import webbrowser
import collections
import http.server
import urllib.request
import urllib.error
from datetime import datetime

# ============ 路径配置 ============
if getattr(sys, 'frozen', False):
    # 打包为 exe 后：使用固定工作路径
    ROOT = r'D:\test\cbjq-re'
    # 无控制台模式：重定向标准输出，避免 print 异常
    try:
        sys.stdout = open(os.devnull, 'w', encoding='utf-8')
        sys.stderr = sys.stdout
    except Exception:
        pass
else:
    BASE = os.path.dirname(os.path.abspath(__file__))
    ROOT = os.path.dirname(BASE)
MOCK_DIR = os.path.join(ROOT, 'mock')
SERVER_DIR = os.path.join(ROOT, 'server2')
SERVER_EXE = os.path.join(SERVER_DIR, 'acacia-game-server.exe')
SERVER_LOG = os.path.join(SERVER_DIR, 'server.log')
CERT = os.path.join(MOCK_DIR, 'server.crt')
KEY = os.path.join(MOCK_DIR, 'server.key')

WEB_PORT = 8899
GM_PORT = 1234
PLAYER_PID = 10001
CREATE_NO_WINDOW = 0x08000000


def ts():
    return datetime.now().strftime('%H:%M:%S')


# ============ hosts 地址接管（需管理员；游戏加速器会改写，故守护）============
HOSTS_FILE = r'C:\Windows\System32\drivers\etc\hosts'
HOSTS_DOMAIN = 'cbjq-serverlist.xoyocdn.com'
HOSTS_LINE = '127.0.0.1 ' + HOSTS_DOMAIN
HOSTS_MARK = '# cbjq-local-server'
HOSTS_GUARD_INTERVAL = 2.0

_hosts_ok = False
_hosts_last_fix = ''
_hosts_events = collections.deque(maxlen=15)
_resolve_ip = ''


def is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def relaunch_as_admin():
    """写 hosts 需要管理员权限：非管理员时用 UAC 重启自身，成功返回 True"""
    try:
        if getattr(sys, 'frozen', False):
            exe, params = sys.executable, ''
        else:
            exe = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
            if not os.path.exists(exe):
                exe = sys.executable
            params = '"%s"' % os.path.abspath(__file__)
        rc = ctypes.windll.shell32.ShellExecuteW(None, 'runas', exe, params, ROOT, 1)
        return rc > 32                      # >32 表示已成功拉起提权实例
    except Exception:
        return False


def _hosts_note(msg):
    line = '[%s] %s' % (ts(), msg)
    _hosts_events.append(line)
    print('[hosts]', line, flush=True)


def resolve_target():
    """应用层实际解析结果 —— 客户端 getaddrinfo 真正拿到的 IP"""
    try:
        return socket.gethostbyname(HOSTS_DOMAIN)
    except Exception:
        return ''


def net_probe():
    """环境探针：系统代理状态（仅展示，TUN/系统代理都不影响回环连接）"""
    info = {'sysproxy': False, 'proxy_server': '', 'resolve': _resolve_ip}
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r'Software\Microsoft\Windows\CurrentVersion\Internet Settings') as k:
            info['sysproxy'] = bool(winreg.QueryValueEx(k, 'ProxyEnable')[0])
            try:
                info['proxy_server'] = str(winreg.QueryValueEx(k, 'ProxyServer')[0])
            except Exception:
                info['proxy_server'] = ''
    except Exception:
        pass
    return info


def _bypass_covered(items, target):
    """判断 bypass 列表是否已覆盖目标（支持 127.* 这类通配与 <local>）"""
    t = target.lower()
    for it in items:
        s = it.lower()
        if s == t:
            return True
        if s.endswith('*') and t.startswith(s[:-1]):
            return True
        if s == '<local>' and '.' not in t:
            return True
    return False


def ensure_proxy_bypass():
    """把本地服地址加入「系统代理 bypass」。

    风险场景：开了 Clash / 其他 VPN 的系统代理后，若客户端读系统代理设置，
    域名会被代理端用自己的 DNS 解析（不读 hosts）→ 拿到正式服 IP。
    把 127.0.0.1 / localhost / 该域名加入 bypass 即可强制直连，不经过代理。
    幂等：只增不删，不影响用户已有配置。"""
    try:
        import winreg
        key = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0,
                            winreg.KEY_READ | winreg.KEY_WRITE) as k:
            try:
                cur = str(winreg.QueryValueEx(k, 'ProxyOverride')[0])
            except Exception:
                cur = ''
            items = [x.strip() for x in cur.split(';') if x.strip()]
            added = []
            for it in ('127.0.0.1', 'localhost', HOSTS_DOMAIN):
                if not _bypass_covered(items, it):
                    items.append(it)
                    added.append(it)
            if added:
                winreg.SetValueEx(k, 'ProxyOverride', 0, winreg.REG_SZ, ';'.join(items))
                # 通知 WinINET 立即重读，避免已启动的程序还用旧设置
                try:
                    ctypes.windll.wininet.InternetSetOptionW(0, 39, 0, 0)
                    ctypes.windll.wininet.InternetSetOptionW(0, 37, 0, 0)
                except Exception:
                    pass
                _hosts_note('系统代理 bypass 已补充：%s' % ', '.join(added))
                return True
        return True
    except Exception as e:
        _hosts_note('补充系统代理 bypass 失败：%s' % e)
        return False


def hosts_effective():
    """hosts 中是否存在「未被注释」的 127.0.0.1 cbjq-serverlist.xoyocdn.com"""
    try:
        with open(HOSTS_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                s = line.split('#', 1)[0].strip()   # 加速器常用 #lg_acc 之类前缀整行注释
                if not s:
                    continue
                parts = s.split()
                if len(parts) >= 2 and parts[0] == '127.0.0.1' \
                        and HOSTS_DOMAIN in [p.lower() for p in parts[1:]]:
                    return True
    except Exception:
        pass
    return False


def repair_hosts():
    """清掉该域名的全部条目（含被加速器注释的残留），追加一条干净的"""
    global _hosts_last_fix
    try:
        try:
            with open(HOSTS_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.read().splitlines()
        except Exception:
            lines = []
        kept = [l for l in lines if HOSTS_DOMAIN not in l]
        kept.append('%s  %s' % (HOSTS_LINE, HOSTS_MARK))
        # 必须显式用 \r\n + newline=''，否则 Windows 会写出 \r\n\r\n
        with open(HOSTS_FILE, 'w', encoding='ascii', errors='ignore', newline='') as f:
            f.write('\r\n'.join(kept) + '\r\n')
        subprocess.run('ipconfig /flushdns', shell=True, capture_output=True,
                       creationflags=CREATE_NO_WINDOW)
        _hosts_last_fix = datetime.now().strftime('%H:%M:%S')
        return True
    except Exception as e:
        _hosts_note('写入 hosts 失败：%s' % e)
        return False


def hosts_guard():
    """常驻守护：加速器（雷神/UU 等）会把自己的 hosts 保护重写、把第三方条目注释掉，
    这里每 2 秒回抢一次，保证客户端始终解析到 127.0.0.1。

    另外每 10 秒做一次「应用层解析」校验：某些 VPN/TUN 会改 DNS 而不改 hosts，
    单看文件看不出问题，必须看客户端真正解析到什么。"""
    global _hosts_ok, _resolve_ip
    last_note = 0.0
    tick = 0
    while True:
        ok = hosts_effective()
        if not ok:
            ok = repair_hosts()
            now = time.time()
            if now - last_note > 30:        # 节流，避免加速器反复改写时刷屏
                if ok:
                    _hosts_note('hosts 被改写（加速器？）→ 已自动抢回本地地址接管')
                else:
                    _hosts_note('hosts 被改写且修复失败，请以管理员身份运行启动器')
                last_note = now
        _hosts_ok = ok

        if ok and tick % 5 == 0:
            ip = resolve_target()
            _resolve_ip = ip
            if ip and ip != '127.0.0.1':
                now = time.time()
                if now - last_note > 30:
                    _hosts_note('域名解析异常：%s -> %s（应为 127.0.0.1，'
                                '可能是 VPN/加速器改写了 DNS）→ 已重新接管' % (HOSTS_DOMAIN, ip))
                    last_note = now
                repair_hosts()
        if tick % 15 == 0:                  # Clash 等重启会重写 bypass，定期补回
            ensure_proxy_bypass()
        tick += 1
        time.sleep(HOSTS_GUARD_INTERVAL)


# ============ 日志缓冲 ============
MOCK_LOGS = collections.deque(maxlen=60)
SERVER_LOGS = collections.deque(maxlen=200)
_serer_proc = None


def log_mock(msg):
    line = f'[{ts()}] {msg}'
    MOCK_LOGS.append(line)
    print('[接线员]', line, flush=True)


# ============ Mock 服务（地址接管）============
TARGET_HOST = '127.0.0.1'
TARGET_PORT = 5200


class MockHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path.startswith('/query'):
            import re
            m = re.search(r'version=([^&]+)', self.path)
            v = m.group(1) if m else '3.6.0'
            m = re.search(r'platform=([^&]+)', self.path)
            p = m.group(1) if m else 'PC'
            body = json.dumps([{"platform": p, "version": v, "host": TARGET_HOST, "port": TARGET_PORT}]).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            log_mock(f'游戏查询服务器地址 -> 已引导至 {TARGET_HOST}:{TARGET_PORT}')
        else:
            body = b'404'
            self.send_response(404)
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)


def start_mock():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(CERT, KEY)
    srv = http.server.ThreadingHTTPServer(('0.0.0.0', 443), MockHandler)
    srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    log_mock('地址接管服务已启动（监听 443）')


# ============ 游戏服务器（acacia）============
def start_server():
    global _serer_proc
    if _serer_proc and _serer_proc.poll() is None:
        return
    f = open(SERVER_LOG, 'wb')
    _serer_proc = subprocess.Popen(
        [SERVER_EXE], cwd=SERVER_DIR,
        stdout=f, stderr=subprocess.STDOUT,
        creationflags=CREATE_NO_WINDOW,
    )
    SERVER_LOGS.append(f'[{ts()}] 游戏服务器已启动 (PID {_serer_proc.pid})')


def stop_server():
    global _serer_proc
    if _serer_proc and _serer_proc.poll() is None:
        _serer_proc.kill()
        SERVER_LOGS.append(f'[{ts()}] 游戏服务器已停止')
    _serer_proc = None


def read_server_log():
    try:
        with open(SERVER_LOG, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()[-40:]
        return [l.rstrip() for l in lines]
    except Exception:
        return []


# ============ 状态检测 ============
def port_listening(port):
    try:
        with socket.create_connection(('127.0.0.1', port), timeout=0.6):
            return True
    except Exception:
        return False


def player_online():
    """游戏客户端连上 5200 的 ESTABLISHED 连接"""
    try:
        out = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True, timeout=8,
            creationflags=CREATE_NO_WINDOW,   # 关键：禁止弹出控制台窗口
        ).stdout
        text = out.decode('gbk', errors='replace')
        for line in text.splitlines():
            if ':5200' in line and 'ESTABLISHED' in line:
                return True
    except Exception:
        pass
    return False


# ============ GM 转发 ============
def gm_call(code):
    t0 = time.time()
    try:
        req = urllib.request.Request(
            f'http://127.0.0.1:{GM_PORT}/gm/script',
            data=json.dumps({"pid": PLAYER_PID, "code": code}).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST')
        resp = urllib.request.urlopen(req, timeout=300)
        _ = resp.read()
        return {"ok": True, "ms": int((time.time() - t0) * 1000)}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ============ 网页控制台 ============
PANEL_HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>尘白禁区 · 本地服控制台</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #FDF3DC; font-family: "Microsoft YaHei", system-ui, sans-serif; color: #111;
       padding: 22px; min-height: 100vh; }
h1 { font-size: 24px; font-weight: 900; letter-spacing: 1px; margin-bottom: 4px; }
.sub { font-size: 13px; color: #666; margin-bottom: 18px; }
.card { border: 3px solid #111; background: #fff; box-shadow: 6px 6px 0 #111; border-radius: 14px; padding: 16px 18px; margin-bottom: 18px; }
.row { display: flex; gap: 14px; flex-wrap: wrap; }
.status-item { flex: 1; min-width: 200px; border: 3px solid #111; border-radius: 12px; background: #fff; padding: 12px 16px; box-shadow: 4px 4px 0 #111; }
.status-item .name { font-size: 13px; color: #555; }
.status-item .val { font-size: 19px; font-weight: 900; margin-top: 4px; }
.dot { display: inline-block; width: 12px; height: 12px; border-radius: 50%; border: 2px solid #111; margin-right: 7px; vertical-align: 1px; }
.on { background: #3ECF6E; }
.off { background: #E5E5E5; }
.warn { background: #FFB800; }
h2 { font-size: 16px; font-weight: 900; margin-bottom: 12px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(215px, 1fr)); gap: 12px; }
button.big {
  border: 3px solid #111; border-radius: 12px; padding: 15px 10px; font-size: 15px; font-weight: 900;
  font-family: inherit; cursor: pointer; box-shadow: 5px 5px 0 #111; transition: none; text-align: left;
  background: #FFD93D; color: #111;
}
button.big:hover { filter: brightness(1.05); }
button.big:active { transform: translate(5px, 5px); box-shadow: 0 0 0 #111; }
button.big .b-sub { display: block; font-size: 11.5px; font-weight: 500; color: #444; margin-top: 5px; }
.c-green { background: #A8E6A3 !important; }
.c-blue  { background: #A5D8FF !important; }
.c-pink  { background: #FFB3C6 !important; }
.c-orange{ background: #FFC078 !important; }
.c-purple{ background: #D0BFFF !important; }
.c-red   { background: #FFA8A8 !important; }
.c-gray  { background: #E9ECEF !important; }
.super-pkg { grid-column: 1 / -1; background: #FFD93D; font-size: 18px; padding: 20px 16px; }
.logbox { background: #16181D; color: #B8F3C6; border: 3px solid #111; border-radius: 10px; padding: 12px 14px;
          font-family: Consolas, monospace; font-size: 12px; height: 170px; overflow-y: auto; white-space: pre-wrap; box-shadow: 4px 4px 0 #111; }
.logbox .warnline { color: #FFD93D; }
.hint { font-size: 12.5px; color: #555; line-height: 1.8; }
#toast { position: fixed; right: 24px; bottom: 24px; display: flex; flex-direction: column; gap: 10px; z-index: 99; }
.toast-item { border: 3px solid #111; border-radius: 10px; padding: 12px 16px; font-weight: 700; font-size: 14px;
              box-shadow: 5px 5px 0 #111; background: #A8E6A3; max-width: 380px; }
.toast-item.err { background: #FFA8A8; }
input.cmd { width: 100%; border: 3px solid #111; border-radius: 10px; padding: 12px 14px; font-size: 14px;
            font-family: Consolas, monospace; box-shadow: inset 2px 2px 0 #eee; margin-bottom: 10px; }
.playing-tip { font-size: 13px; font-weight: 700; margin-bottom: 12px; padding: 10px 14px; border: 3px solid #111;
               border-radius: 10px; background: #FFF3BF; display: none; }
.hosts-warn { display: none; font-size: 13px; font-weight: 700; margin-top: 14px; padding: 11px 14px;
              border: 3px solid #111; border-radius: 10px; background: #FFA8A8; box-shadow: 4px 4px 0 #111; line-height: 1.7; }
.net-info { font-size: 12.5px; color: #333; margin-top: 14px; padding: 9px 13px; border-left: 6px solid #111;
            background: #EFEFEF; border-radius: 6px; font-family: Consolas, "Microsoft YaHei", monospace; line-height: 1.6; }
</style>
</head>
<body>
<h1>尘白禁区 · 本地服控制台</h1>
<div class="sub">双击启动器后本页面会自动打开 · 保持此页面即可随时使用 GM 工具</div>

<div class="card">
  <div class="row">
    <div class="status-item"><div class="name">① 地址接管（接线员）</div><div class="val" id="s-mock"><span class="dot off"></span>检查中...</div></div>
    <div class="status-item"><div class="name">② 游戏服务器（内容屋）</div><div class="val" id="s-server"><span class="dot off"></span>检查中...</div></div>
    <div class="status-item"><div class="name">③ 游戏连接</div><div class="val" id="s-player"><span class="dot off"></span>检查中...</div></div>
    <div class="status-item"><div class="name">④ 域名接管（hosts）</div><div class="val" id="s-hosts"><span class="dot off"></span>检查中...</div></div>
  </div>
  <div class="hosts-warn" id="hosts-warn">⚠️ 域名接管失效：加速器（雷神 / UU 等）把 hosts 里的本地服记录注释掉了，客户端会直接连到<b>正式服</b>。点下方「立即修复域名接管」可立刻抢回。</div>
  <div class="net-info" id="net-info">网络环境检测中...</div>
</div>

<div class="card">
  <h2>⚡ 一键 GM 工具（点击即生效）</h2>
  <div class="playing-tip" id="playing-tip">💡 检测到游戏在线，命令将立即生效；执行后到游戏中切换界面 / 重登即可看到效果。</div>
  <div class="grid">
    <button class="big super-pkg" onclick="runSuper()">🎁 超级大礼包（一键全搞定）
      <span class="b-sub">全解锁 + 全角色 Lv.80 + 全物品 + 全卡池 + 好感度 + 货币 + 经验</span></button>
    <button class="big c-green" onclick="run('GM.PassGuide()')">🗺️ 解锁全部剧情关卡<span class="b-sub">补写全部关卡通过记录</span></button>
    <button class="big c-blue" onclick="run('GM.MaxAllGirl()')">⭐ 全角色 / 武器满级 Lv.80<span class="b-sub">一键拉满</span></button>
    <button class="big c-orange" onclick="run('GM.AddAllItem()')">🎒 全部物品礼包<span class="b-sub">角色/皮肤/武器/后勤/材料</span></button>
    <button class="big c-purple" onclick="run('GM.Gacha.UnLockAllPool()')">🎰 全部卡池解锁<span class="b-sub">所有抽卡池开放</span></button>
    <button class="big c-pink" onclick="run('GM.House.AddAllGirlLoveNum(9999)')">💗 全员好感度 +9999<span class="b-sub">宿舍好感一次拉满</span></button>
    <button class="big c-green" onclick="run('GM.Riki.GMUnLockRiki(1)')">🧭 图鉴全解锁<span class="b-sub">Riki 系统全开</span></button>
    <button class="big c-orange" onclick="runMoney()">💰 货币大礼包<span class="b-sub">五种货币各 +99999999</span></button>
    <button class="big c-blue" onclick="run('GM.Add(GM.AddExp, {9999999})')">🚀 账号经验 +9999999<span class="b-sub">分析员快速升级</span></button>
  </div>
</div>

<div class="card">
  <h2>⌨️ 自定义命令</h2>
  <input class="cmd" id="cmd-input" placeholder='示例：GM.AddItem 相关 / GM.SetAttr({22, 10124, 1}) / GM.Add(GM.AddMoney, {1, 999})'>
  <button class="big c-gray" style="width:220px" onclick="runCustom()">执行命令</button>
</div>

<div class="card">
  <h2>📋 服务器日志（实时）</h2>
  <div class="logbox" id="logbox">加载中...</div>
</div>

<div class="card">
  <h2>🔧 系统操作</h2>
  <div class="hint">
    · 玩游戏期间：保持本启动器运行即可（页面可关闭，服务不受影响，再次打开 http://127.0.0.1:8899 即可回到本页面）<br>
    · 若需彻底停止全部服务（接线员 + 游戏服务器）：<br>
  </div>
  <div style="margin-top:12px">
    <button class="big c-red" style="width:260px" onclick="stopAll()">⏹ 关闭全部服务</button>
    <button class="big c-blue" style="width:260px" onclick="restartServer()">🔄 重启游戏服务器</button>
    <button class="big c-orange" style="width:260px" onclick="fixHosts()">🔧 立即修复域名接管</button>
  </div>
</div>

<div id="toast"></div>

<script>
function toast(msg, isErr) {
  const d = document.createElement('div');
  d.className = 'toast-item' + (isErr ? ' err' : '');
  d.textContent = msg;
  document.getElementById('toast').appendChild(d);
  setTimeout(() => d.remove(), 4200);
}
async function refresh() {
  try {
    const r = await fetch('/status');
    const s = await r.json();
    document.getElementById('s-mock').innerHTML = '<span class="dot ' + (s.mock ? 'on' : 'off') + '"></span>' + (s.mock ? '运行中' : '未运行');
    document.getElementById('s-server').innerHTML = '<span class="dot ' + (s.server ? 'on' : 'off') + '"></span>' + (s.server ? '运行中' : '未运行');
    document.getElementById('s-player').innerHTML = '<span class="dot ' + (s.player ? 'on' : 'warn') + '"></span>' + (s.player ? '已连接（在线）' : '未连接（请进游戏大厅）');
    document.getElementById('s-hosts').innerHTML = '<span class="dot ' + (s.hosts ? 'on' : 'warn') + '"></span>'
      + (s.hosts ? '已接管 → 127.0.0.1' : (s.hosts_admin ? '失效（正被改写）' : '失效（缺管理员）'));
    document.getElementById('hosts-warn').style.display = s.hosts ? 'none' : 'block';
    const n = s.net || {};
    const ip = s.resolve || '未知';
    document.getElementById('net-info').textContent =
      '网络环境：系统代理 ' + (n.sysproxy ? ('开启（' + (n.proxy_server || '?') + '）') : '关闭')
      + '　·　域名实际解析 ' + ip
      + '　·　' + (ip === '127.0.0.1'
          ? '已指向本机，开 VPN / 加速器都不影响'
          : '未指向本机（客户端会连到正式服）');
    document.getElementById('playing-tip').style.display = s.player ? 'block' : 'none';
    const box = document.getElementById('logbox');
    box.textContent = s.server_log.join('\n') || '（暂无日志）';
    box.scrollTop = box.scrollHeight;
  } catch (e) {}
}
async function run(code, silent) {
  const r = await fetch('/gm', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({code}) });
  const j = await r.json();
  if (j.ok) { if (!silent) toast('✅ 执行成功（' + j.ms + 'ms）'); }
  else { toast('⚠️ 执行失败：' + (j.error || '未知错误'), true); }
  return j.ok;
}
async function runSuper() {
  toast('🎁 超级大礼包开始发放...');
  const list = [
    ['GM.PassGuide()', '解锁剧情'],
    ['GM.MaxAllGirl()', '满级'],
    ['GM.AddAllItem()', '全物品'],
    ['GM.Gacha.UnLockAllPool()', '全卡池'],
    ['GM.House.AddAllGirlLoveNum(9999)', '好感度'],
    ['GM.Riki.GMUnLockRiki(1)', '图鉴'],
    ['GM.Add(GM.AddExp, {9999999})', '经验'],
  ];
  for (const [c, name] of list) {
    const ok = await run(c, true);
    if (!ok) { toast('⚠️ [' + name + '] 失败，请确认游戏在线', true); return; }
  }
  await runMoney(true);
  toast('🎉 超级大礼包全部发放完成！回到游戏查看');
}
async function runMoney(silent) {
  for (let i = 1; i <= 5; i++) await run('GM.Add(GM.AddMoney, {' + i + ', 99999999})', true);
  if (!silent) toast('💰 货币已到账 ×5 种');
}
async function runCustom() {
  const v = document.getElementById('cmd-input').value.trim();
  if (!v) { toast('请先输入命令', true); return; }
  await run(v);
}
async function restartServer() {
  await fetch('/restart_server', { method: 'POST' });
  toast('🔄 游戏服务器重启中...');
}
async function fixHosts() {
  const r = await fetch('/fix_hosts', { method: 'POST' });
  const j = await r.json();
  if (j.ok) toast('✅ 域名接管已抢回（' + j.at + '），可直接启动游戏');
  else toast('⚠️ 修复失败：请以管理员身份运行启动器', true);
  refresh();
}
async function stopAll() {
  if (!confirm('确定要关闭全部服务吗？（游戏将断开连接）')) return;
  await fetch('/stop_app', { method: 'POST' });
  toast('已关闭全部服务，可关闭本页面');
}
setInterval(refresh, 2000); refresh();
</script>
</body>
</html>'''


class WebHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype='application/json; charset=utf-8'):
        if isinstance(body, str):
            body = body.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == '/' or self.path.startswith('/index'):
            self._send(200, PANEL_HTML, 'text/html; charset=utf-8')
        elif self.path == '/status':
            self._send(200, json.dumps({
                "mock": port_listening(443),
                "server": port_listening(5200),
                "player": player_online(),
                "hosts": bool(_hosts_ok),
                "hosts_admin": is_admin(),
                "hosts_fix": _hosts_last_fix,
                "hosts_events": list(_hosts_events),
                "resolve": _resolve_ip,
                "net": net_probe(),
                "server_log": read_server_log(),
            }))
        else:
            self._send(404, json.dumps({"err": "not found"}))

    def do_POST(self):
        ln = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(ln) if ln else b'{}'
        if self.path == '/gm':
            try:
                code = json.loads(raw.decode('utf-8')).get('code', '')
                result = gm_call(code)
            except Exception as e:
                result = {"ok": False, "error": str(e)}
            self._send(200, json.dumps(result))
        elif self.path == '/restart_server':
            stop_server()
            time.sleep(1)
            start_server()
            self._send(200, json.dumps({"ok": True}))
        elif self.path == '/stop_app':
            stop_server()
            self._send(200, json.dumps({"ok": True}))
            threading.Timer(0.8, lambda: os._exit(0)).start()
        elif self.path == '/fix_hosts':
            global _hosts_ok
            _hosts_ok = repair_hosts()
            self._send(200, json.dumps({"ok": _hosts_ok, "at": _hosts_last_fix}))
        else:
            self._send(404, json.dumps({"err": "not found"}))


# ============ 主流程 ============
def main():
    global _hosts_ok, _resolve_ip
    # 单实例检测
    try:
        probe = socket.socket()
        probe.settimeout(0.5)
        probe.connect(('127.0.0.1', WEB_PORT))
        probe.close()
        # 已有实例在跑：若本次以管理员启动而 hosts 已失效，顺手抢回再退出
        if is_admin() and not hosts_effective():
            repair_hosts()
        # 已有实例：打开控制台后退出
        webbrowser.open(f'http://127.0.0.1:{WEB_PORT}')
        sys.exit(0)
    except Exception:
        pass

    print('=' * 56)
    print('  尘白禁区 · 本地服启动器')
    print('=' * 56)

    # 0. 地址接管（hosts）—— 写 hosts 必须管理员，且要防加速器改写
    if not is_admin():
        print('[hosts] 需要管理员权限写 hosts，正在请求提权...')
        if relaunch_as_admin():
            os._exit(0)                 # 提权实例已启动，本进程退出
        print('[hosts] 提权被取消，将以普通权限运行（hosts 无法自动修复）')
    if hosts_effective():
        _hosts_ok = True
        _hosts_note('地址接管条目正常（%s -> 127.0.0.1）' % HOSTS_DOMAIN)
    else:
        _hosts_ok = repair_hosts()
        _hosts_note('已写入地址接管条目' if _hosts_ok else '写入失败（需管理员权限）')
    _resolve_ip = resolve_target()
    ensure_proxy_bypass()
    threading.Thread(target=hosts_guard, daemon=True).start()

    # 1. Mock
    start_mock()
    # 2. 游戏服务器
    start_server()
    # 3. Web 控制台
    web = http.server.ThreadingHTTPServer(('127.0.0.1', WEB_PORT), WebHandler)
    threading.Thread(target=web.serve_forever, daemon=True).start()
    print(f'[控制台] 已就绪: http://127.0.0.1:{WEB_PORT}')
    # 4. 打开浏览器
    time.sleep(1.2)
    webbrowser.open(f'http://127.0.0.1:{WEB_PORT}')
    # 保持运行
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
