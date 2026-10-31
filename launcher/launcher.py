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

# ============ 游戏目录（MOD 管理用，可在控制台里改）============
# 默认值只是兜底；真正的目录从 launcher/game_config.json 读取，读不到就自动探测。
GAME_CONFIG = os.path.join(ROOT, 'launcher', 'game_config.json')
GAME_ROOT = r'E:\SeasunCBJQos'
GAME_EXE = os.path.join(GAME_ROOT, 'SeasunGame.exe')
PAKS_DIR = os.path.join(GAME_ROOT, r'Game\cbjq\game\Game\Content\Paks')
PAKS_DISABLED = os.path.join(PAKS_DIR, '_disabled')
# 游戏自带的官方 pak 前缀；其余 Patch_*.pak 一律视为自制 MOD
OFFICIAL_PAK_PREFIX = ('Patch_UFS-', 'Patch_NonUFS-', 'Patch_ShaderPatch-')

# ============ 输入嗅探器（拍照模式 MOD 的输入源）============
# 随本启动器启停：本进程已是管理员（UAC 自提权），拉起嗅探器继承权限，
# 用户不再需要单独的 UAC 弹窗；启动器退出/关闭全部服务时嗅探器跟着退出。
PYW = r'C:\Users\MisakiMiku\.workbuddy\binaries\python\versions\3.13.12\pythonw.exe'
SNIFFER_PY = os.path.join(ROOT, 'runtime', 'wheel_sniffer.py')
SNIFFER_PID = os.path.join(ROOT, 'runtime', 'sniffer.pid')

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
_stopping = False          # 置 True 后 hosts 守护线程退出，允许清理 hosts 再关进程


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


def restore_hosts():
    """退出启动器时清掉我们写的 hosts 条目。

    不清的话，之后去连正式服客户端仍会被解析到 127.0.0.1（本地服已关，直接连接失败）。
    """
    try:
        try:
            with open(HOSTS_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.read().splitlines()
        except Exception:
            return False
        kept = [l for l in lines if HOSTS_DOMAIN not in l]
        if len(kept) == len(lines):
            return True
        with open(HOSTS_FILE, 'w', encoding='ascii', errors='ignore', newline='') as f:
            f.write('\r\n'.join(kept) + '\r\n')
        subprocess.run('ipconfig /flushdns', shell=True, capture_output=True,
                       creationflags=CREATE_NO_WINDOW)
        _hosts_note('已清理 hosts 条目（退出启动器）')
        return True
    except Exception as e:
        _hosts_note('清理 hosts 失败：%s' % e)
        return False


def hosts_guard():
    """常驻守护：加速器（雷神/UU 等）会把自己的 hosts 保护重写、把第三方条目注释掉，
    这里每 2 秒回抢一次，保证客户端始终解析到 127.0.0.1。

    另外每 10 秒做一次「应用层解析」校验：某些 VPN/TUN 会改 DNS 而不改 hosts，
    单看文件看不出问题，必须看客户端真正解析到什么。"""
    global _hosts_ok, _resolve_ip
    last_note = 0.0
    tick = 0
    while not _stopping:
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
_mock_srv = None


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
    global _mock_srv
    if _mock_srv is not None:
        return
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(CERT, KEY)
    srv = http.server.ThreadingHTTPServer(('0.0.0.0', 443), MockHandler)
    srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    _mock_srv = srv
    log_mock('地址接管服务已启动（监听 443）')


def stop_mock():
    """关掉 443 接线员。serve_forever 在 daemon 线程里，主线程 shutdown 是安全的。"""
    global _mock_srv
    srv, _mock_srv = _mock_srv, None
    if srv is None:
        return
    try:
        srv.shutdown()
        srv.server_close()
    except Exception as e:
        log_mock('地址接管服务停止异常：%s' % e)
    log_mock('地址接管服务已停止')


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


# ============ 输入嗅探器启停 ============
def start_sniffer():
    """拉起输入嗅探器（wheel_sniffer.py）。

    - 继承本进程的管理员令牌（游戏也是管理员完整性，UIPI 要求嗅探器必须管理员）
    - --launcher-pid：嗅探器探测到本进程退出后自动自尽，生命周期与本地服一致
    - 先杀旧实例：嗅探器有单实例互斥量，旧的活着新的会直接退出
    """
    stop_sniffer()
    time.sleep(0.6)
    try:
        if not os.path.exists(PYW) or not os.path.exists(SNIFFER_PY):
            SERVER_LOGS.append(f'[{ts()}] 嗅探器未拉起（缺 pythonw 或 wheel_sniffer.py）')
            return
        base_flags = 0x00000008 | 0x00000200        # DETACHED_PROCESS | 新进程组
        args = [PYW, SNIFFER_PY, '--launcher-pid', str(os.getpid())]
        kw = dict(cwd=os.path.dirname(SNIFFER_PY), close_fds=True,
                  stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                  stderr=subprocess.DEVNULL)
        try:
            subprocess.Popen(args, creationflags=base_flags | 0x01000000, **kw)  # +脱离job
        except OSError:
            subprocess.Popen(args, creationflags=base_flags, **kw)
        SERVER_LOGS.append(f'[{ts()}] 输入嗅探器已随启动器拉起（管理员）')
    except Exception as e:
        SERVER_LOGS.append(f'[{ts()}] 嗅探器拉起失败: {e}')


def stop_sniffer():
    """关停嗅探器：先按 sniffer.pid 精确终止，失败退回 taskkill pythonw。"""
    try:
        pid = int(open(SNIFFER_PID, encoding='ascii').read().strip())
        k = ctypes.windll.kernel32
        h = k.OpenProcess(0x0001, False, pid)          # PROCESS_TERMINATE
        if h:
            k.TerminateProcess(h, 0)
            k.CloseHandle(h)
    except Exception:
        pass
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'pythonw.exe'],
                       capture_output=True, creationflags=CREATE_NO_WINDOW)
    except Exception:
        pass


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
    """把命令转发给游戏服务器。服务端会回 {ok, error, ms}，
    这里把 player-offline / unknown-command 翻成人话，避免"点了没反应还提示成功"。"""
    t0 = time.time()
    try:
        req = urllib.request.Request(
            f'http://127.0.0.1:{GM_PORT}/gm/script',
            data=json.dumps({"pid": PLAYER_PID, "code": code}).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST')
        resp = urllib.request.urlopen(req, timeout=300)
        raw = resp.read().decode('utf-8', errors='replace')
        try:
            body = json.loads(raw)
        except Exception:
            body = {}
        if body.get('ok'):
            return {"ok": True, "ms": body.get('ms') or int((time.time() - t0) * 1000)}
        err = str(body.get('error') or raw or 'unknown')
        if err.startswith('player-offline'):
            return {"ok": False, "error": '游戏未在线——请先进入游戏大厅，再回来点这个按钮'}
        if err.startswith('unknown-command'):
            return {"ok": False, "error": '服务端不认识这条命令（游戏服务器可能是旧版）'}
        if err.startswith('run-failed:'):
            return {"ok": False, "error": err[len('run-failed:'):]}
        return {"ok": False, "error": err}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ============ 游戏目录配置（可换盘、可换安装位置）============
def apply_game_root(root):
    """切换游戏根目录 —— 之后 MOD 列表、启动游戏、pak 目录全部跟着换。"""
    global GAME_ROOT, GAME_EXE, PAKS_DIR, PAKS_DISABLED
    GAME_ROOT = root
    GAME_EXE = os.path.join(root, 'SeasunGame.exe')
    PAKS_DIR = os.path.join(root, r'Game\cbjq\game\Game\Content\Paks')
    PAKS_DISABLED = os.path.join(PAKS_DIR, '_disabled')


def detect_game_root():
    """找 SeasunGame.exe：先查常见安装目录，再扫各盘符根下的一层文件夹。"""
    for base in (r'E:\SeasunCBJQos', r'D:\SeasunCBJQos', r'C:\SeasunCBJQos', r'F:\SeasunCBJQos'):
        if os.path.isfile(os.path.join(base, 'SeasunGame.exe')):
            return base
    for letter in 'CDEFGH':
        base = letter + ':\\'
        try:
            names = os.listdir(base)
        except OSError:
            continue
        for name in names:
            path = os.path.join(base, name)
            try:
                if os.path.isdir(path) and os.path.isfile(os.path.join(path, 'SeasunGame.exe')):
                    return path
            except OSError:
                continue
    return ''


def save_game_config():
    try:
        os.makedirs(os.path.dirname(GAME_CONFIG), exist_ok=True)
        with open(GAME_CONFIG, 'w', encoding='utf-8') as f:
            json.dump({'game_root': GAME_ROOT}, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        SERVER_LOGS.append(f'[{ts()}] 保存游戏目录配置失败: {e}')
        return False


def load_game_config():
    """优先用配置文件；配置缺失或目录已失效时自动探测一次并落盘。"""
    root = ''
    try:
        with open(GAME_CONFIG, 'r', encoding='utf-8') as f:
            root = (json.load(f) or {}).get('game_root') or ''
    except Exception:
        root = ''
    if root and os.path.isdir(root):
        apply_game_root(root)
        return
    found = detect_game_root()
    if found:
        apply_game_root(found)
        save_game_config()


def game_info():
    return {
        'root': GAME_ROOT,
        'exe': GAME_EXE,
        'exe_found': os.path.isfile(GAME_EXE),
        'paks_dir': PAKS_DIR,
        'paks_found': os.path.isdir(PAKS_DIR),
    }


def set_game_root(raw_root):
    root = str(raw_root or '').strip().strip('"').rstrip('\\/')
    if not root:
        return False, '路径为空'
    if not os.path.isdir(root):
        return False, '目录不存在：%s' % root
    if not os.path.isfile(os.path.join(root, 'SeasunGame.exe')):
        return False, '这个目录下没有 SeasunGame.exe，请选游戏根目录'
    apply_game_root(root)
    save_game_config()
    return True, ''


# ============ 服务总控（可停可启，不退出启动器）============
def services_running():
    return port_listening(443) or port_listening(5200)


def start_all_services():
    start_mock()
    start_server()
    start_sniffer()


def stop_all_services():
    """只停服务，保留本进程。网页控制台必须活着，才能显示“已停止”并支持再次启动。"""
    stop_server()
    stop_sniffer()
    stop_mock()


# ============ MOD 管理 ============
def _is_mod(name):
    """只认自制 MOD：Patch_ 开头、非官方前缀、.pak 结尾。

    游戏本体的 pak 是 APP_* / App_* / PAK_* / FixConnectionPatch_* 这些，
    官方热更补丁是 Patch_UFS- / Patch_NonUFS- / Patch_ShaderPatch-，
    我们自己的 MOD 一律是 Patch_<名字>-Windows_100_P.pak。
    """
    low = name.lower()
    return low.startswith('patch_') and low.endswith('.pak') and not name.startswith(OFFICIAL_PAK_PREFIX)


def ensure_mod_dirs():
    try:
        os.makedirs(PAKS_DISABLED, exist_ok=True)
    except Exception as e:
        SERVER_LOGS.append(f'[{ts()}] 创建 _disabled 目录失败: {e}')


def list_mods():
    items = []
    for enabled, folder in ((True, PAKS_DIR), (False, PAKS_DISABLED)):
        if not os.path.isdir(folder):
            continue
        try:
            names = os.listdir(folder)
        except OSError:
            continue
        for name in names:
            if not _is_mod(name):
                continue
            path = os.path.join(folder, name)
            try:
                st = os.stat(path)
            except OSError:
                continue
            items.append({
                'name': name,
                'size': st.st_size,
                'mtime': datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M'),
                'enabled': enabled,
            })
    items.sort(key=lambda x: (not x['enabled'], x['name'].lower()))
    return items


def toggle_mod(raw_name, enable):
    """启用 / 禁用 = 在 Paks 与 Paks/_disabled 之间移动文件。

    UE4 只加载 `.pak` 扩展名，移出 Paks 目录即视为不加载；
    用移动而不是改名，是为了不破坏 pak 的加载顺序（按文件名排序）。
    """
    name = os.path.basename(str(raw_name or '').strip())
    if not name or not _is_mod(name) or name in ('.', '..'):
        return False, '非法文件名'
    src_dir, dst_dir = (PAKS_DISABLED, PAKS_DIR) if enable else (PAKS_DIR, PAKS_DISABLED)
    src = os.path.join(src_dir, name)
    dst = os.path.join(dst_dir, name)
    if not os.path.isfile(src):
        return False, '文件不存在（可能已被移动或删除）'
    if os.path.exists(dst):
        return False, '目标目录已有同名文件'
    try:
        os.makedirs(dst_dir, exist_ok=True)
        os.replace(src, dst)
    except Exception as e:
        return False, str(e)
    return True, ''


def launch_game():
    if not os.path.isfile(GAME_EXE):
        return False, '找不到游戏启动器：%s' % GAME_EXE
    try:
        subprocess.Popen([GAME_EXE], cwd=GAME_ROOT, close_fds=True)
    except Exception as e:
        return False, str(e)
    return True, ''


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
.sub { font-size: 13px; color: #666; margin-bottom: 16px; }
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
button.tiny { border: 3px solid #111; border-radius: 10px; padding: 8px 14px; font-size: 13px; font-weight: 900;
              font-family: inherit; cursor: pointer; box-shadow: 3px 3px 0 #111; background: #E9ECEF; }
button.tiny:active { transform: translate(3px, 3px); box-shadow: 0 0 0 #111; }
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
.hint { font-size: 12.5px; color: #555; line-height: 1.9; }
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
.svc-bar { display: none; font-size: 13.5px; font-weight: 700; margin-top: 14px; padding: 11px 14px;
           border: 3px solid #111; border-radius: 10px; background: #FFC078; box-shadow: 4px 4px 0 #111; line-height: 1.7; }
/* ---- 视图切换 ---- */
.tabs { display: flex; gap: 12px; margin-bottom: 18px; flex-wrap: wrap; }
.tab { border: 3px solid #111; border-radius: 12px; padding: 12px 24px; font-size: 15px; font-weight: 900;
       font-family: inherit; cursor: pointer; background: #fff; box-shadow: 4px 4px 0 #111; }
.tab.active { background: #FFD93D; }
.tab:active { transform: translate(4px, 4px); box-shadow: 0 0 0 #111; }
.view { display: none; }
.view.active { display: block; }
/* ---- MOD 管理 ---- */
.path-row { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 12px; }
.path-text { flex: 1; min-width: 240px; font-family: Consolas, monospace; font-size: 12px; color: #333;
             background: #EFEFEF; border-left: 6px solid #111; border-radius: 6px; padding: 10px 12px; word-break: break-all; }
.mods-list { margin: 14px 0; }
.mod-row { display: flex; align-items: center; gap: 12px; border: 3px solid #111; border-radius: 12px;
           padding: 12px 14px; background: #fff; box-shadow: 4px 4px 0 #111; margin-bottom: 10px; }
.mod-row.off { background: #F2F2F2; border-color: #888; box-shadow: 3px 3px 0 #bbb; }
.mod-main { flex: 1; min-width: 0; }
.mod-name { font-size: 14px; font-weight: 900; word-break: break-all; }
.mod-meta { font-size: 12px; color: #666; margin-top: 4px; font-family: Consolas, monospace; }
.mod-state { font-size: 12px; font-weight: 900; padding: 5px 12px; border: 2px solid #111; border-radius: 999px; white-space: nowrap; }
.mod-state.on { background: #A8E6A3; }
.mod-state.off { background: #E9ECEF; }
.mod-btn { border: 3px solid #111; border-radius: 10px; padding: 9px 18px; font-weight: 900; font-size: 13px;
           font-family: inherit; cursor: pointer; background: #FFD93D; box-shadow: 3px 3px 0 #111; white-space: nowrap; }
.mod-btn.disable { background: #FFA8A8; }
.mod-btn:active { transform: translate(3px, 3px); box-shadow: 0 0 0 #111; }
.empty { font-size: 13px; color: #666; padding: 18px; text-align: center; border: 3px dashed #bbb; border-radius: 12px; }
.actions { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 14px; }
.actions button.big { width: auto; min-width: 200px; }
.bye { max-width: 660px; margin: 80px auto; border: 3px solid #111; border-radius: 14px; background: #fff;
       box-shadow: 8px 8px 0 #111; padding: 28px 32px; }
.bye h1 { font-size: 22px; margin-bottom: 16px; }
.bye p { font-size: 14px; line-height: 2; color: #333; }
.bye .tag { display: inline-block; font-size: 12px; font-weight: 900; padding: 4px 12px; border: 2px solid #111;
            border-radius: 999px; background: #FFA8A8; margin-bottom: 14px; }
</style>
</head>
<body>
<h1>尘白禁区 · 本地服控制台</h1>
<div class="sub">启动器常驻 · 服务可随时启停 · 保持本页面即可管理一切</div>

<div class="tabs">
  <button class="tab active" id="tab-console" onclick="switchView('console')">🎛 控制台</button>
  <button class="tab" id="tab-mods" onclick="switchView('mods')">🧩 MOD 管理</button>
</div>

<!-- ==================== 控制台 ==================== -->
<div class="view active" id="view-console">
  <div class="card">
    <div class="row">
      <div class="status-item"><div class="name">① 地址接管（接线员）</div><div class="val" id="s-mock"><span class="dot off"></span>检查中...</div></div>
      <div class="status-item"><div class="name">② 游戏服务器（内容屋）</div><div class="val" id="s-server"><span class="dot off"></span>检查中...</div></div>
      <div class="status-item"><div class="name">③ 游戏连接</div><div class="val" id="s-player"><span class="dot off"></span>检查中...</div></div>
      <div class="status-item"><div class="name">④ 域名接管（hosts）</div><div class="val" id="s-hosts"><span class="dot off"></span>检查中...</div></div>
    </div>
    <div class="svc-bar" id="svc-bar">⚠️ 本地服务已停止 —— 游戏此时连不上。点下方「▶ 启动全部服务」即可恢复，不用重开启动器。</div>
    <div class="hosts-warn" id="hosts-warn">⚠️ 域名接管失效：加速器（雷神 / UU 等）把 hosts 里的本地服记录注释掉了，客户端会直接连到<b>正式服</b>。点下方「立即修复域名接管」可立刻抢回。</div>
    <div class="net-info" id="net-info">网络环境检测中...</div>
  </div>

  <div class="card">
    <h2>🎮 游戏启动与目录</h2>
    <div class="path-row">
      <code class="path-text" id="game-root">读取中...</code>
      <button class="tiny" onclick="detectGame()">🔍 自动检测</button>
      <button class="tiny c-green" onclick="launchGame()">🎮 启动游戏</button>
    </div>
    <input class="cmd" id="game-root-input" placeholder="换目录时在这里粘贴游戏根目录（需包含 SeasunGame.exe），例如 E:\SeasunCBJQos">
    <button class="big c-gray" style="width:240px" onclick="saveGameRoot()">💾 保存新目录</button>
    <div class="hint" style="margin-top:10px">换盘 / 重装游戏后改这里即可 —— MOD 列表和「启动游戏」都会跟着新目录走。</div>
  </div>

  <div class="card">
    <h2>⚡ 一键 GM 工具（点击即生效）</h2>
    <div class="playing-tip" id="playing-tip">💡 检测到游戏在线，命令将立即生效；执行后到游戏中切换界面 / 重登即可看到效果。</div>
    <div class="grid">
      <button class="big super-pkg" onclick="runSuper()">🎁 超级大礼包（一键全搞定）
        <span class="b-sub">全进度通关 + 全领奖 + 全角色 Lv.80 + 全物品 + 全卡池 + 好感度 + 货币 + 经验</span></button>
      <button class="big c-green" onclick="runComplete()">🏁 一键全进度通关 + 全领奖
        <span class="b-sub">全部关卡满星通关 + 首通奖励补发 + 章节星级奖励全领</span></button>
      <button class="big c-pink" onclick="runHouseUnlock()">🏠 宿舍家具 / 好感度全解锁
        <span class="b-sub">角色房间家具 + 按摩房 / 温泉 / 沙滩 家具 + 全员好感度</span></button>
      <button class="big c-purple" onclick="runGiveFurniture()">🪑 补发全部宿舍家具
        <span class="b-sub">324 件 dorm_gift × 99（含嵌入式展示柜）</span></button>
      <button class="big c-blue" onclick="run('GM.MaxAllGirl()')">⭐ 全角色 / 武器满级 Lv.80<span class="b-sub">一键拉满</span></button>
      <button class="big c-orange" onclick="run('GM.AddAllItem()')">🎒 全部物品礼包<span class="b-sub">角色/皮肤/武器/后勤/材料/家具</span></button>
      <button class="big c-purple" onclick="run('GM.Gacha.UnLockAllPool()')">🎰 全部卡池解锁<span class="b-sub">所有抽卡池开放</span></button>
      <button class="big c-pink" onclick="run('GM.House.AddAllGirlLoveNum(9999)')">💗 全员好感度 +9999<span class="b-sub">宿舍好感一次拉满</span></button>
      <button class="big c-green" onclick="run('GM.Riki.GMUnLockRiki(1)')">🧭 图鉴全解锁<span class="b-sub">Riki 系统全开</span></button>
      <button class="big c-orange" onclick="runMoney()">💰 货币大礼包<span class="b-sub">五种货币各 +99999999</span></button>
      <button class="big c-blue" onclick="run('GM.Add(GM.AddExp, {9999999})')">🚀 账号经验 +9999999<span class="b-sub">分析员快速升级</span></button>
    </div>
  </div>

  <div class="card">
    <h2>⌨️ 自定义命令</h2>
    <input class="cmd" id="cmd-input" placeholder='示例：GM.SetAttr({22, 10124, 1}) / GM.House.SkipTaskGuide() / GM.PassAll()'>
    <button class="big c-gray" style="width:220px" onclick="runCustom()">执行命令</button>
  </div>

  <div class="card">
    <h2>📋 服务器日志（实时）</h2>
    <div class="logbox" id="logbox">加载中...</div>
  </div>

  <div class="card">
    <h2>🔧 系统操作</h2>
    <div class="hint">
      · 玩游戏期间保持本页面即可（页面关掉也能用 http://127.0.0.1:8899 回来）<br>
      · 启停按钮是<b>同一个位置切换</b>：服务开着显示「停止全部服务」，停了就变成「启动全部服务」<br>
      · 「停止全部服务」只停游戏服务，<b>控制台会留着</b>，可随时再启动<br>
      · 「退出启动器」才会真正关闭本进程（443 / 5200 / 8899 全释放，hosts 条目一并清理）
    </div>
    <div class="actions">
      <button class="big c-green" id="btn-start" onclick="startAll()" style="display:none">▶ 启动全部服务</button>
      <button class="big c-red" id="btn-stop" onclick="stopAll()">⏹ 停止全部服务</button>
      <button class="big c-blue" onclick="restartServer()">🔄 重启游戏服务器</button>
      <button class="big c-orange" onclick="fixHosts()">🔧 立即修复域名接管</button>
      <button class="big c-gray" onclick="exitLauncher()">🚪 退出启动器</button>
    </div>
  </div>
</div>

<!-- ==================== MOD 管理 ==================== -->
<div class="view" id="view-mods">
  <div class="card">
    <h2>🧩 MOD 管理器</h2>
    <div class="path-row">
      <code class="path-text" id="mods-dir">读取中...</code>
      <button class="tiny" onclick="openModsFolder()">📂 打开目录</button>
    </div>
    <div class="hint">
      · 只列自制 MOD（游戏自带 <code>Patch_UFS-*</code> / <code>Patch_NonUFS-*</code> / <code>Patch_ShaderPatch-*</code> 已隐藏）<br>
      · 「禁用」= 把 pak 移到 <code>_disabled</code> 子目录，游戏不再加载它（不动文件名，不影响其余 pak 的加载顺序）<br>
      · 启用 / 禁用后<b>必须重启游戏</b>才生效；正在运行的游戏进程不会被改动，重启时按新配置加载
    </div>
    <div id="mods-list" class="mods-list"><div class="empty">读取中...</div></div>
    <div class="actions">
      <button class="big c-blue" onclick="loadMods(true)">🔄 刷新列表</button>
      <button class="big c-gray" onclick="switchView('console')">🎮 去控制台启动游戏</button>
    </div>
  </div>
</div>

<div id="toast"></div>

<script>
let currentView = 'console';

function esc(s) {
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function toast(msg, isErr) {
  const d = document.createElement('div');
  d.className = 'toast-item' + (isErr ? ' err' : '');
  d.textContent = msg;
  document.getElementById('toast').appendChild(d);
  setTimeout(() => d.remove(), 4200);
}
function switchView(name) {
  currentView = name;
  document.getElementById('view-console').classList.toggle('active', name === 'console');
  document.getElementById('view-mods').classList.toggle('active', name === 'mods');
  document.getElementById('tab-console').classList.toggle('active', name === 'console');
  document.getElementById('tab-mods').classList.toggle('active', name === 'mods');
  if (name === 'mods') loadMods();
}

async function refresh() {
  try {
    const r = await fetch('/status');
    const s = await r.json();
    document.getElementById('s-mock').innerHTML = '<span class="dot ' + (s.mock ? 'on' : 'off') + '"></span>' + (s.mock ? '运行中' : '已停止');
    document.getElementById('s-server').innerHTML = '<span class="dot ' + (s.server ? 'on' : 'off') + '"></span>' + (s.server ? '运行中' : '已停止');
    document.getElementById('s-player').innerHTML = '<span class="dot ' + (s.player ? 'on' : 'warn') + '"></span>' + (s.player ? '已连接（在线）' : '未连接（请进游戏大厅）');
    document.getElementById('s-hosts').innerHTML = '<span class="dot ' + (s.hosts ? 'on' : 'warn') + '"></span>'
      + (s.hosts ? '已接管 → 127.0.0.1' : (s.hosts_admin ? '失效（正被改写）' : '失效（缺管理员）'));
    document.getElementById('hosts-warn').style.display = s.hosts ? 'none' : 'block';
    const svcDown = !s.mock || !s.server;
    document.getElementById('svc-bar').style.display = svcDown ? 'block' : 'none';
    document.getElementById('btn-start').style.display = svcDown ? 'inline-block' : 'none';
    document.getElementById('btn-stop').style.display = svcDown ? 'none' : 'inline-block';
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
async function runComplete() {
  toast('🏁 正在补写全进度（约 10~30 秒，请勿关闭页面）...');
  const ok = await run('GM.CompleteAll()', true);
  if (ok) toast('🎉 全部关卡已通关满星，章节星级奖励已领取');
  else toast('⚠️ 执行失败，请确认游戏在线（先进到大厅）', true);
}
async function runHouseUnlock() {
  toast('🏠 正在解锁宿舍家具与好感度（约 5~15 秒）...');
  const ok = await run('GM.House.UnlockAll()', true);
  if (ok) toast('🎉 宿舍家具 / 好感度已解锁');
  else toast('⚠️ 执行失败，请确认游戏在线（先进到大厅）', true);
}
async function runGiveFurniture() {
  toast('🪑 正在发放 324 件宿舍家具...');
  const ok = await run('GM.House.GiveAllFurniture()', true);
  if (ok) toast('🎉 全部宿舍家具已到账（各 ×99）');
  else toast('⚠️ 执行失败，请确认游戏在线（先进到大厅）', true);
}
async function runSuper() {
  toast('🎁 超级大礼包开始发放...');
  const list = [
    ['GM.CompleteAll()', '全进度+全领奖'],
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

async function startAll() {
  toast('▶ 正在启动本地服务...');
  await fetch('/start_all', { method: 'POST' });
  setTimeout(refresh, 1500);
}
async function stopAll() {
  if (!confirm('停止全部服务？游戏会断线，但本控制台会保留，可随时再启动。')) return;
  toast('⏹ 正在停止服务...');
  await fetch('/stop_all', { method: 'POST' });
  setTimeout(refresh, 900);
}
async function exitLauncher() {
  if (!confirm('退出启动器？443 / 5200 / 8899 会全部关闭，hosts 条目也会清理，下次需要双击桌面图标重新启动。')) return;
  await fetch('/exit_launcher', { method: 'POST' });
  clearInterval(_timer);
  document.body.innerHTML = `
    <div class="bye">
      <div class="tag">已停止</div>
      <h1>启动器已退出</h1>
      <p>· 地址接管（443）、游戏服务器（5200）、本控制台（8899）全部已释放</p>
      <p>· hosts 里的本地服条目已清理，可以正常连接正式服了</p>
      <p>· 本页面已失效，可直接关闭标签页；下次使用请双击桌面「尘白禁区-本地服」</p>
    </div>`;
}
async function restartServer() {
  await fetch('/restart_server', { method: 'POST' });
  toast('🔄 游戏服务器重启中...');
  setTimeout(refresh, 2500);
}
async function fixHosts() {
  const r = await fetch('/fix_hosts', { method: 'POST' });
  const j = await r.json();
  if (j.ok) toast('✅ 域名接管已抢回（' + j.at + '），可直接启动游戏');
  else toast('⚠️ 修复失败：请以管理员身份运行启动器', true);
  refresh();
}

/* ---------------- MOD 管理 ---------------- */
async function loadMods(manual) {
  const box = document.getElementById('mods-list');
  try {
    const r = await fetch('/mods/list');
    const j = await r.json();
    document.getElementById('mods-dir').textContent = j.dir;
    if (!j.dir_found) {
      box.innerHTML = '<div class="empty">找不到 Paks 目录：' + esc(j.dir) + '</div>';
      return;
    }
    if (!j.mods || !j.mods.length) {
      box.innerHTML = '<div class="empty">没有检测到自制 MOD<br><span style="font-size:12px">（只显示 Paks 目录里非官方的 Patch_*.pak）</span></div>';
      return;
    }
    box.innerHTML = j.mods.map(m => `
      <div class="mod-row ${m.enabled ? '' : 'off'}">
        <div class="mod-main">
          <div class="mod-name">${esc(m.name)}</div>
          <div class="mod-meta">${(m.size / 1024).toFixed(0)} KB · ${esc(m.mtime)}</div>
        </div>
        <div class="mod-state ${m.enabled ? 'on' : 'off'}">${m.enabled ? '启用中' : '已禁用'}</div>
        <button class="mod-btn ${m.enabled ? 'disable' : ''}" data-name="${esc(m.name)}" data-enable="${!m.enabled}">
          ${m.enabled ? '禁用' : '启用'}
        </button>
      </div>`).join('');
    box.querySelectorAll('.mod-btn').forEach(btn => {
      btn.onclick = () => toggleMod(btn.dataset.name, btn.dataset.enable === 'true');
    });
    if (manual) toast('🔄 已刷新，共 ' + j.mods.length + ' 个 MOD');
  } catch (e) {
    box.innerHTML = '<div class="empty">读取失败：' + esc(e.message) + '</div>';
  }
}
async function toggleMod(name, enable) {
  const r = await fetch('/mods/toggle', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ name, enable })
  });
  const j = await r.json();
  if (j.ok) {
    toast((enable ? '✅ 已启用：' : '⛔ 已禁用：') + name + '（重启游戏生效）');
    loadMods();
  } else {
    toast('⚠️ 操作失败：' + (j.error || '未知错误'), true);
  }
}
async function openModsFolder() {
  const r = await fetch('/mods/open_folder', { method: 'POST' });
  const j = await r.json();
  if (!j.ok) toast('⚠️ 打开失败：' + (j.error || ''), true);
}
async function launchGame() {
  toast('🎮 正在启动游戏...');
  const r = await fetch('/game/launch', { method: 'POST' });
  const j = await r.json();
  if (j.ok) toast('🎮 游戏启动中，等待进大厅');
  else toast('⚠️ 启动失败：' + (j.error || ''), true);
}
async function loadGameInfo() {
  try {
    const r = await fetch('/game/info');
    const j = await r.json();
    const box = document.getElementById('game-root');
    box.textContent = j.root + (j.exe_found ? '' : '   ⚠️ 该目录下没有 SeasunGame.exe');
    document.getElementById('game-root-input').placeholder =
      '当前：' + j.root + '　——　粘贴新路径后点「保存新目录」';
  } catch (e) {}
}
async function saveGameRoot() {
  const v = document.getElementById('game-root-input').value.trim();
  if (!v) { toast('先在输入框里填写游戏根目录', true); return; }
  const r = await fetch('/game/config', {
    method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ root: v })
  });
  const j = await r.json();
  if (j.ok) {
    toast('✅ 已切换到：' + j.info.root);
    document.getElementById('game-root-input').value = '';
    loadGameInfo();
    loadMods();
  } else {
    toast('⚠️ ' + (j.error || '保存失败'), true);
  }
}
async function detectGame() {
  toast('🔍 正在扫描盘符寻找 SeasunGame.exe...');
  const r = await fetch('/game/detect', { method: 'POST' });
  const j = await r.json();
  if (j.ok) { toast('✅ 已定位：' + j.root); loadGameInfo(); loadMods(); }
  else toast('⚠️ ' + (j.error || '没找到'), true);
}

const _timer = setInterval(refresh, 2000);
refresh();
loadMods();
loadGameInfo();
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
        elif self.path == '/game/info':
            self._send(200, json.dumps(game_info()))
        elif self.path == '/mods/list':
            self._send(200, json.dumps({
                "dir": PAKS_DIR,
                "disabled_dir": PAKS_DISABLED,
                "game_exe": GAME_EXE,
                "game_found": os.path.isfile(GAME_EXE),
                "dir_found": os.path.isdir(PAKS_DIR),
                "mods": list_mods(),
            }))
        else:
            self._send(404, json.dumps({"err": "not found"}))

    def do_POST(self):
        global _hosts_ok, _stopping
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
        elif self.path == '/start_all':
            start_all_services()
            self._send(200, json.dumps({"ok": True}))
        elif self.path == '/stop_all' or self.path == '/stop_app':
            # 只停服务，不退出本进程 —— 控制台要留下来显示“已停止”并允许重新启动。
            # /stop_app 是旧页面的入口，保留别名以免缓存页面点了 404。
            stop_all_services()
            self._send(200, json.dumps({"ok": True}))
        elif self.path == '/exit_launcher':
            # 先让 hosts 守护线程停下，再清 hosts，最后退出——否则守护线程会把条目又写回去
            _stopping = True
            stop_all_services()
            restore_hosts()
            self._send(200, json.dumps({"ok": True}))
            threading.Timer(0.8, lambda: os._exit(0)).start()
        elif self.path == '/mods/toggle':
            try:
                payload = json.loads(raw.decode('utf-8'))
            except Exception:
                payload = {}
            ok, err = toggle_mod(payload.get('name', ''), bool(payload.get('enable')))
            self._send(200, json.dumps({"ok": True} if ok else {"ok": False, "error": err}))
        elif self.path == '/mods/open_folder':
            try:
                os.makedirs(PAKS_DIR, exist_ok=True)
                os.startfile(PAKS_DIR)
                self._send(200, json.dumps({"ok": True}))
            except Exception as e:
                self._send(200, json.dumps({"ok": False, "error": str(e)}))
        elif self.path == '/game/launch':
            ok, err = launch_game()
            self._send(200, json.dumps({"ok": True} if ok else {"ok": False, "error": err}))
        elif self.path == '/game/config':
            try:
                payload = json.loads(raw.decode('utf-8'))
            except Exception:
                payload = {}
            ok, err = set_game_root(payload.get('root', ''))
            self._send(200, json.dumps({"ok": True, "info": game_info()} if ok else {"ok": False, "error": err}))
        elif self.path == '/game/detect':
            found = detect_game_root()
            if not found:
                self._send(200, json.dumps({"ok": False, "error": '没找到 SeasunGame.exe，请手动填路径'}))
            else:
                ok, err = set_game_root(found)
                self._send(200, json.dumps({"ok": True, "root": found} if ok else {"ok": False, "error": err}))
        elif self.path == '/fix_hosts':
            _hosts_ok = repair_hosts()
            self._send(200, json.dumps({"ok": _hosts_ok, "at": _hosts_last_fix}))
        else:
            self._send(404, json.dumps({"err": "not found"}))


# ============ 单实例互斥（重复双击只保留一个启动器）============
MUTEX_NAME = 'Local\\cbjq-local-launcher'
_mutex_handle = None


def acquire_single_instance():
    """抢命名互斥量。True = 我是唯一实例；False = 已经有一个在跑。

    比原来的「探测 8899 端口」可靠：端口被别的程序占用时不会误判成"已在运行"，
    也不会因为 TIME_WAIT 而漏判。
    """
    global _mutex_handle
    try:
        k32 = ctypes.WinDLL('kernel32', use_last_error=True)
        handle = k32.CreateMutexW(None, False, MUTEX_NAME)
        err = ctypes.get_last_error()
        if not handle:
            return True                      # 创建失败就不要把用户挡在外面
        if err == 183:                       # ERROR_ALREADY_EXISTS
            k32.CloseHandle(handle)
            return False
        _mutex_handle = handle
        return True
    except Exception:
        return True


# ============ 主流程 ============
def main():
    global _hosts_ok, _resolve_ip

    # 单实例：已有启动器在跑，就只把控制台打开，不再起第二套服务
    if not acquire_single_instance():
        webbrowser.open(f'http://127.0.0.1:{WEB_PORT}')
        sys.exit(0)

    # 游戏目录（MOD 管理器 / 启动游戏用）；配置缺失或失效时自动探测并落盘
    load_game_config()

    # 端口兜底检测
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
    # 2.5 输入嗅探器（拍照模式 MOD 输入源；随本启动器启停）
    start_sniffer()
    # 2.6 MOD 目录（确保 _disabled 存在，MOD 管理器才有地方放被禁用的 pak）
    ensure_mod_dirs()
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
