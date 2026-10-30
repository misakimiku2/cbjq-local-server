# -*- coding: utf-8 -*-
"""
输入嗅探器（CamZoom 兜底输入源）

两个全局低级钩子：
  1) WH_MOUSE_LL    —— 滚轮方向 → runtime/wheel.txt，内容 "seq dir"（1 上滚 / -1 下滚）
  2) WH_KEYBOARD_LL —— 游戏在前台时的按键 → runtime/fp_key.txt，内容 "seq vk"
                       （V=86 切换第一人称；B=66 预留）

三条硬性设计约束（都是实测踩出来的，改动前务必读懂）：

  A) **消息泵必须阻塞**。低级钩子是同步回调：系统投递输入事件后要等宿主线程
     处理完才继续。v69 曾把 GetMessageW 换成 `PeekMessage + sleep(0.02)` 轮询，
     结果宿主线程大部分时间在睡眠，每个鼠标事件都要排队等它醒来 —— 用户直接
     感觉到「鼠标有迟滞、影响正常用电脑」。**永远不要在这个循环里 sleep 轮询。**

  B) **没开游戏就不要挂钩子**。运行时用 SetTimer(1s) 检查 Game.exe 是否在跑：
     在跑才 SetWindowsHookEx，退出就 UnhookWindowsHookEx。平时上网/办公零影响。
     定时器用 SetTimer(None, id, 1000, None) 产生 WM_TIMER 投递到线程队列，
     GetMessageW 会正常返回它，不需要窗口。

  C) 键盘钩子必须做前台判定：全局钩子会捕捉任何窗口的按键，不加判定的话
     在聊天窗打字打出一个 v 就会切换视角。

为什么要外部进程：游戏本身没有滚轮轴映射（Input.ini 零条 AxisMapping），
Lua 侧拿不到滚轮；键盘的 PCKeyboardEvent 也不保证派发所有键。

用法：游戏经 SeasunGame.exe 以管理员权限启动（带 UAC），所以要用
      start_wheel_sniffer_admin.vbs（会弹一次 UAC）。平时不玩游戏时钩子会自动
      卸掉，不必手动关。重复启动会被自动去重（同名互斥量）。
"""
import ctypes
from ctypes import wintypes as wt
import os
import sys
import time

BASE = os.path.join(os.environ.get('PROGRAMDATA', r'C:\ProgramData'), 'CamZoomMod')
IPC = os.path.join(BASE, 'wheel.txt')
KEYIPC = os.path.join(BASE, 'fp_key.txt')
BEAT = os.path.join(BASE, 'sniffer_beat.txt')
STATE = os.path.join(BASE, 'sniffer_state.txt')
RAW = os.path.join(BASE, 'fp_key_raw.txt')
# 「按住中」的键集合。FreeCam 的 WASD/Q E 走位需要**持续状态**，而 fp_key.txt 只有
# 按下瞬间的一条事件 —— 所以单独出一份文件，Lua 每帧直接读当前按住哪些键。
HELDIPC = os.path.join(BASE, 'keys_held.txt')
# 「要吞掉的键」黑名单。FreeCam 进入时由 Lua 写入，退出写 0。
# 低级钩子里返回 1 = 该事件不再往后传，游戏就收不到 —— 这是唯一能挡住开火/瞄准/
# 大招的办法（pawn:DisableInput 对这款游戏无效，DisableInput=true 也照样开枪）。
# 约定：1=左键 2=右键 4=中键 10=滚轮，其余直接写 VK。
BLOCKIPC = os.path.join(BASE, 'block_vk.txt')

WH_MOUSE_LL = 14
WH_KEYBOARD_LL = 13
WM_MOUSEWHEEL = 0x020A
WM_LBUTTONDOWN, WM_LBUTTONUP = 0x0201, 0x0202
WM_RBUTTONDOWN, WM_RBUTTONUP = 0x0204, 0x0205
WM_MBUTTONDOWN, WM_MBUTTONUP = 0x0207, 0x0208
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_SYSKEYDOWN = 0x0104
WM_SYSKEYUP = 0x0105
WM_TIMER = 0x0113
TIMER_ID = 1
TICK_MS = 1000

# 判定「游戏在跑」的进程名（决定要不要挂钩子）。
# 只放游戏本体，不要放启动器 SeasunGame.exe —— 它常驻，加了钩子就永远挂着。
GAME_PROCS = ('game.exe', 'game-win64-shipping.exe')
# 启动器：在前台时也接受键盘（避免刚点启动的那几秒丢键）
LAUNCHER_PROCS = ('seasungame.exe', 'seasunlauncher.exe')
# ⚠ 事故记录（2026-10-30）：黑名单曾经做成「全局吞」—— 不看前台窗口，
# 结果用户在自由相机里切到桌面/任务管理器时，鼠标点击照样被吞、键盘也被吞一部分，
# 连杀进程都点不动，只能重启电脑。**任何吞事件的逻辑都必须过这两道闸**：
#   1) 只在游戏前台时生效（foreground_is_game）
#   2) 死人开关：黑名单文件超过 3s 未更新即失效（见 load_block）
# 而且这个功能本身就未必有用：实测即使吞了，游戏照样能开枪（疑似走 Raw Input）。
#
# 关心的按键（VK 码）：钩子**只转发白名单内的键**，不在表里的会被静默丢弃。
# 曾经踩过：FreeCam 绑定 F7 时怎么按都没反应，排查半天才发现是这张表没放行。
# V=86 / B=66 / F5=116 / F6=117 / F7=118 / F8=119
KEYS_OF_INTEREST = {0x56: 'V', 0x42: 'B', 0x74: 'F5', 0x75: 'F6', 0x76: 'F7', 0x77: 'F8',
                    # W/A/S/D/Q/E：FreeCam 的走位键。自由相机模式下角色被
                    # SetIgnoreMoveInput 冻结，这几个键正好空出来给相机用。
                    0x57: 'W', 0x41: 'A', 0x53: 'S', 0x44: 'D', 0x51: 'Q', 0x45: 'E',
                    # Z/X：FreeCam 的升降。Q/E 被游戏占为大招，不能用。
                    0x5A: 'Z', 0x58: 'X'}

PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
TH32CS_SNAPPROCESS = 0x00000002

os.makedirs(BASE, exist_ok=True)

user32 = ctypes.WinDLL('user32', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# 单实例
kernel32.CreateMutexW.restype = wt.HANDLE
_mutex = kernel32.CreateMutexW(None, False, 'Global\\CamZoomWheelSniffer')
if kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
    sys.exit(0)


class MSLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ('pt', wt.POINT),
        ('mouseData', wt.DWORD),
        ('flags', wt.DWORD),
        ('time', wt.DWORD),
        ('dwExtraInfo', ctypes.c_void_p),
    ]


class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ('vkCode', wt.DWORD),
        ('scanCode', wt.DWORD),
        ('flags', wt.DWORD),
        ('time', wt.DWORD),
        ('dwExtraInfo', ctypes.c_void_p),
    ]


class PROCESSENTRY32W(ctypes.Structure):
    _fields_ = [
        ('dwSize', wt.DWORD),
        ('cntUsage', wt.DWORD),
        ('th32ProcessID', wt.DWORD),
        ('th32DefaultHeapID', ctypes.c_void_p),
        ('th32ModuleID', wt.DWORD),
        ('cntThreads', wt.DWORD),
        ('th32ParentProcessID', wt.DWORD),
        ('pcPriClassBase', ctypes.c_long),
        ('dwFlags', wt.DWORD),
        ('szExeFile', ctypes.c_wchar * 260),
    ]


HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_ssize_t, ctypes.c_int, wt.WPARAM, wt.LPARAM)
user32.CallNextHookEx.restype = ctypes.c_ssize_t
user32.CallNextHookEx.argtypes = [wt.HHOOK, ctypes.c_int, wt.WPARAM, wt.LPARAM]
user32.SetWindowsHookExW.restype = wt.HHOOK
user32.SetWindowsHookExW.argtypes = [ctypes.c_int, HOOKPROC, wt.HMODULE, wt.DWORD]
user32.UnhookWindowsHookEx.restype = wt.BOOL
user32.UnhookWindowsHookEx.argtypes = [wt.HHOOK]
user32.SetTimer.restype = ctypes.c_size_t
user32.SetTimer.argtypes = [wt.HWND, ctypes.c_size_t, wt.UINT, ctypes.c_void_p]
kernel32.GetModuleHandleW.restype = wt.HMODULE
kernel32.GetModuleHandleW.argtypes = [wt.LPCWSTR]
kernel32.OpenProcess.restype = wt.HANDLE
kernel32.QueryFullProcessImageNameW.restype = wt.BOOL
kernel32.CloseHandle.restype = wt.BOOL
kernel32.CreateToolhelp32Snapshot.restype = wt.HANDLE
kernel32.CreateToolhelp32Snapshot.argtypes = [wt.DWORD, wt.DWORD]
kernel32.Process32FirstW.restype = wt.BOOL
kernel32.Process32FirstW.argtypes = [wt.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
kernel32.Process32NextW.restype = wt.BOOL
kernel32.Process32NextW.argtypes = [wt.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]

_seq = [0]
_key_seq = [0]
_beat = [0]
_tick_n = [0]
_fg_cache = {'t': 0.0, 'v': False}
_state = {'mouse': None, 'key': None}
_cb = {}          # 回调对象必须长期持有，否则被 GC 回收后钩子回调会踩野指针
_game_pids = set()      # 游戏本体 pid（决定挂不挂钩子 + 键盘前台判定）
_launcher_pids = set()  # 启动器 pid（前台判定放行用）
_key_down = {}          # vk -> 按下时刻：防止按住时系统 repeat 反复触发
_held = set()           # 当前按住的 vk（供 keys_held.txt / FreeCam 持续走位用）
_block = set()          # 要吞掉的输入（block_vk.txt，由 Lua 在进出自由相机时写）
_last_game_seen = [0.0]  # 最近一次看到游戏进程的时刻（钩子装卸防抖用）
# pid 快照会间歇性抽风（见过 game_pids 忽空），但 pid 本身在一次游戏会话里
# 是稳定的 —— 用「曾经见过」的集合做前台判定，不受抽风影响。
# （残留风险：pid 被系统回收复用给别的程序时可能误判一次；黑名单本身有
#   3s 死人开关 + 只在游戏前台生效，出错的代价被限制在很短的窗口内）
_game_pids_ever = set()
_launcher_pids_ever = set()
_elevated = [0]         # 是否以管理员运行 —— UIPI 决定钩子能不能收到游戏的输入

# ⚠ UIPI（本轮最深的一个坑）：游戏经 SeasunGame.exe 启动，是**管理员完整性**。
# 普通权限进程安装的 WH_MOUSE_LL / WH_KEYBOARD_LL 收不到发往高完整性进程的输入。
# 表现极其反直觉：游戏在前台时滚轮/按键完全没反应，**把游戏切到后台反而生效**
# （因为那时事件目标是同权限的聊天窗口）。所以必须用 start_wheel_sniffer_admin.vbs。
try:
    _shell32 = ctypes.WinDLL('shell32')
    _shell32.IsUserAnAdmin.restype = wt.BOOL
    _elevated[0] = 1 if _shell32.IsUserAnAdmin() else 0
except Exception:
    _elevated[0] = 0


def write_dir(direction):
    _seq[0] += 1
    try:
        with open(IPC, 'w', encoding='ascii') as f:
            f.write('%d %d' % (_seq[0], direction))
    except OSError:
        pass


def write_key(vk):
    _key_seq[0] += 1
    try:
        with open(KEYIPC, 'w', encoding='ascii') as f:
            f.write('%d %d' % (_key_seq[0], vk))
    except OSError:
        pass


def write_held():
    """当前按住的键（空格分隔的 VK；没有就写 0）。FreeCam 每帧读它做持续走位。"""
    try:
        with open(HELDIPC, 'w', encoding='ascii') as f:
            f.write(' '.join(str(v) for v in sorted(_held)) if _held else '0')
    except OSError:
        pass


def write_beat():
    """心跳：Lua 侧靠这个判断嗅探器是否还活着（进程被收掉时文件会停更）。"""
    _beat[0] += 1
    try:
        with open(BEAT, 'w', encoding='ascii') as f:
            f.write(str(_beat[0]))
    except OSError:
        pass


def write_state(active):
    try:
        with open(STATE, 'w', encoding='utf-8') as f:
            f.write('hooks=%s pid=%d beat=%d elevated=%d game_pids=%s fg=%s\n'
                    % ('on' if active else 'off', os.getpid(), _beat[0],
                       _elevated[0], sorted(_game_pids), _fg_cache['v']))
    except OSError:
        pass


def write_raw(vk, fg, accepted, hwnd_pid):
    """诊断（追加写）：V/B/F5/Insert 只要进了钩子就留一行痕，用来区分
    「钩子收不到键」和「判定把它丢了」—— 这两个原因的修法完全不同。
    追加而不是覆盖：一次测试里按了好几次，覆盖写只会留下最后一次，等于白测。"""
    try:
        with open(RAW, 'a', encoding='utf-8') as f:
            f.write('%.1f vk=%d(%s) fg=%d acc=%d hwnd_pid=%d game_pids=%s\n'
                    % (time.time(), vk, KEYS_OF_INTEREST.get(vk, '?'),
                       1 if fg else 0, 1 if accepted else 0, hwnd_pid,
                       sorted(_game_pids)))
    except OSError:
        pass


MOUSE_NAME = {WM_LBUTTONDOWN: 'LMBdown', WM_LBUTTONUP: 'LMBup',
              WM_RBUTTONDOWN: 'RMBdown', WM_RBUTTONUP: 'RMBup',
              WM_MBUTTONDOWN: 'MMBdown', WM_MBUTTONUP: 'MMBup',
              WM_MOUSEWHEEL: 'wheel'}


def write_mouse(wParam, blk):
    """诊断（追加写）：鼠标按键/滚轮进钩子时留痕，带当时的黑名单。
    判读：有记录但游戏照样开枪 = 游戏走 Raw Input(WM_INPUT)，低级钩子吞不掉。"""
    try:
        with open(RAW, 'a', encoding='utf-8') as f:
            f.write('%.1f mouse=%s blk=%s\n'
                    % (time.time(), MOUSE_NAME.get(wParam, hex(wParam)), sorted(blk)))
    except OSError:
        pass


def load_block():
    """读黑名单。两道保险，缺一不可（教训见文件头事故记录）：

    1) **只在游戏前台时才吞**。吞事件是全局的，不加这道判定就会连桌面、
       任务管理器的点击一起吞掉 —— 用户切出去想杀进程都点不动，只能重启电脑。
    2) **死人开关**：文件超过 3s 没更新就当黑名单为空。Lua 崩了、游戏关了、
       忘了写 0，都会自动解禁，绝不会留下一个「重启才能解开」的状态。
    """
    try:
        st = os.stat(BLOCKIPC)
    except OSError:
        _block.clear()
        return
    if time.time() - st.st_mtime > 3.0:
        if _block:
            _block.clear()
        return
    if not foreground_is_game():
        if _block:
            _block.clear()
        return
    try:
        with open(BLOCKIPC, encoding='ascii') as f:
            s = f.read()
    except OSError:
        _block.clear()
        return
    new = set()
    for tok in s.split():
        if tok.isdigit():
            new.add(int(tok))
    if new != _block:
        _block.clear()
        _block.update(new)


def trim_raw():
    """把 raw 日志裁到最近 200 行，避免长期跑出个大文件。"""
    try:
        if not os.path.exists(RAW) or os.path.getsize(RAW) < 64 * 1024:
            return
        with open(RAW, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()[-200:]
        with open(RAW, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    except OSError:
        pass


def game_running():
    """游戏本体是否在运行（决定挂不挂钩子）。用刷新好的 pid 集合，零开销。"""
    return bool(_game_pids)


def refresh_pids():
    """一次进程快照同时刷新「游戏 pid」和「启动器 pid」。

    ⚠ 为什么不用 OpenProcess 读进程名：尘白的游戏进程有反作弊保护，
    低完整性进程 OpenProcess 会被拒（HANDOFF 早有记录：无法 OpenProcess、
    无法读命令行）。v70 的前台判定就是栽在这里 —— 判定恒为 False，
    所有按键被静默丢弃。pid 比对完全不需要进程句柄，绕开这条限制。
    """
    _game_pids.clear()
    _launcher_pids.clear()
    snap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if not snap or snap == ctypes.c_void_p(-1).value:
        return
    try:
        e = PROCESSENTRY32W()
        e.dwSize = ctypes.sizeof(e)
        ok = kernel32.Process32FirstW(snap, ctypes.byref(e))
        while ok:
            n = (e.szExeFile or '').lower()
            pid = int(e.th32ProcessID)
            if n in GAME_PROCS:
                _game_pids.add(pid)
                _game_pids_ever.add(pid)
            elif n in LAUNCHER_PROCS:
                _launcher_pids.add(pid)
                _launcher_pids_ever.add(pid)
            ok = kernel32.Process32NextW(snap, ctypes.byref(e))
    finally:
        kernel32.CloseHandle(snap)


def foreground_is_game():
    """前台窗口是否属于游戏/启动器（带 0.3s 缓存，钩子回调里不能太慢）。

    三重判定（任一命中即算）：
      1) 前台窗口的 pid 在「曾经见过的游戏/启动器 pid」里
      2) 前台窗口标题含「尘白禁区」——pid 快照会间歇抽风，标题不会
      3) 拿不到前台窗口但游戏进程在跑（独占全屏）——放行比丢输入合理
    """
    now = time.time()
    if now - _fg_cache['t'] < 0.3:
        return _fg_cache['v']
    ok = False
    try:
        hwnd = user32.GetForegroundWindow()
        if hwnd:
            pid = wt.DWORD(0)
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            if (pid.value in _game_pids_ever) or (pid.value in _launcher_pids_ever):
                ok = True
            else:
                buf = ctypes.create_unicode_buffer(128)
                user32.GetWindowTextW(hwnd, buf, 128)
                ok = ((buf.value or '').find('尘白禁区') >= 0)
        elif _game_pids:
            # 独占全屏偶尔拿不到前台窗口；钩子本来就只在游戏运行时挂着，
            # 这种情况下放行比丢掉所有输入更合理
            ok = True
    except Exception:
        ok = False
    _fg_cache['t'] = now
    _fg_cache['v'] = ok
    return ok


def _mouse_proc(nCode, wParam, lParam):
    # 快路径：非滚轮事件立刻放行，不做任何解析（鼠标移动是高频事件）
    if nCode == 0:
        blk = _block
        # 诊断：鼠标按键/滚轮到底有没有进钩子、吞没吞成。
        # 用来区分「钩子没收到」和「收到了但游戏走 Raw Input 不受影响」。
        if wParam in (WM_LBUTTONDOWN, WM_LBUTTONUP, WM_RBUTTONDOWN, WM_RBUTTONUP,
                      WM_MBUTTONDOWN, WM_MBUTTONUP, WM_MOUSEWHEEL):
            write_mouse(wParam, blk)
        if blk:
            # 返回 1 = 吞掉，游戏/其它程序都收不到
            if (wParam == WM_LBUTTONDOWN or wParam == WM_LBUTTONUP) and 1 in blk:
                return 1
            if (wParam == WM_RBUTTONDOWN or wParam == WM_RBUTTONUP) and 2 in blk:
                return 1
            if (wParam == WM_MBUTTONDOWN or wParam == WM_MBUTTONUP) and 4 in blk:
                return 1
        if wParam == WM_MOUSEWHEEL:
            try:
                ms = ctypes.cast(lParam, ctypes.POINTER(MSLLHOOKSTRUCT)).contents
                raw = (ms.mouseData >> 16) & 0xFFFF
                delta = ctypes.c_short(raw).value
                if delta != 0:
                    write_dir(1 if delta > 0 else -1)
            except Exception:
                pass
            # 先记后吞：我们拿滚轮控 FOV，别让游戏拿它切枪
            if 10 in blk:
                return 1
    return user32.CallNextHookEx(None, nCode, wParam, lParam)


def _key_proc(nCode, wParam, lParam):
    if nCode == 0 and wParam in (WM_KEYDOWN, WM_SYSKEYDOWN):
        try:
            kb = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
            vk = int(kb.vkCode)
            if vk in KEYS_OF_INTEREST:
                now = time.time()
                held = _key_down.get(vk)
                # 按住不放时系统会持续发 KEYDOWN（repeat），必须只在「首次按下」
                # 才触发一次 —— 否则按住 V 会把 FP 反复开关，镜头在原地抽搐。
                # held 超过 1.5s 视为丢了 KEYUP（切窗口时收不到），强制放行。
                repeat = held is not None and (now - held) < 1.5
                fg = foreground_is_game()
                # v72：**不再用前台判定筛掉按键**。钩子本来就只在游戏运行时
                # 才安装，场景已经限定住了；而前台窗口 pid 常常对不上游戏 pid
                # （实测 hwnd_pid=36568 vs game_pids=[48216]，游戏有独立的
                # 窗口/渲染进程），拿它筛等于把所有按键丢光 —— 这就是
                # 「V/B/F5/Insert 怎么按都没反应」的根因。fg 只写进诊断日志。
                accept = (not repeat)
                _key_down[vk] = now
                # 按住集合：只在真正变化时才落盘（按住不放时每秒有 ~30 次 repeat，
                # 每次都写文件纯属浪费）
                if vk not in _held:
                    _held.add(vk)
                    write_held()
                try:
                    hwnd = user32.GetForegroundWindow()
                    pid = wt.DWORD(0)
                    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                    hwnd_pid = pid.value
                except Exception:
                    hwnd_pid = 0
                write_raw(vk, fg, accept, hwnd_pid)
                if accept:
                    write_key(vk)
            # 记录完再吞：Q/E 要先进 keys_held.txt 给相机升降用，再挡住游戏
            if vk in _block:
                return 1
        except Exception:
            pass
    elif nCode == 0 and wParam in (WM_KEYUP, WM_SYSKEYUP):
        try:
            kb = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
            vk = int(kb.vkCode)
            if vk in KEYS_OF_INTEREST:
                _key_down.pop(vk, None)
                if vk in _held:
                    _held.discard(vk)
                    write_held()
            if vk in _block:
                return 1
        except Exception:
            pass
    return user32.CallNextHookEx(None, nCode, wParam, lParam)


def install_hooks():
    hm = kernel32.GetModuleHandleW(None)
    _state['mouse'] = user32.SetWindowsHookExW(WH_MOUSE_LL, _cb['mouse'], hm, 0)
    _state['key'] = user32.SetWindowsHookExW(WH_KEYBOARD_LL, _cb['key'], hm, 0)
    ok = bool(_state['mouse'] or _state['key'])
    write_state(ok)
    if not ok:
        try:
            with open(os.path.join(BASE, 'sniffer_error.txt'), 'w', encoding='utf-8') as f:
                f.write('SetWindowsHookEx failed, error=%d\n' % ctypes.get_last_error())
        except OSError:
            pass
    elif not _elevated[0]:
        # 钩子挂上了，但如果游戏是管理员完整性，UIPI 会让它收不到游戏窗口的输入
        # （症状：游戏在前台没反应，切到后台反而生效）—— 直接把结论写出来
        try:
            with open(os.path.join(BASE, 'sniffer_warn.txt'), 'w', encoding='utf-8') as f:
                f.write('非管理员运行：钩子已挂，但游戏是管理员完整性，\n'
                        'UIPI 会让钩子收不到发往游戏窗口的输入。\n'
                        '请关闭本进程并改用 start_wheel_sniffer_admin.vbs\n')
        except OSError:
            pass
    else:
        try:
            os.remove(os.path.join(BASE, 'sniffer_warn.txt'))
        except OSError:
            pass
    return ok


def remove_hooks():
    _block.clear()          # 钩子没了就绝不能再吞任何东西
    _held.clear()
    write_held()
    for k in ('mouse', 'key'):
        h = _state.get(k)
        if h:
            try:
                user32.UnhookWindowsHookEx(h)
            except Exception:
                pass
            _state[k] = None
    write_state(False)


OVERLAY_TEXT = (
    "【自由相机】\r\n"
    "鼠标        转视角\r\n"
    "W / S       沿视线前后\r\n"
    "A / D       左右平移\r\n"
    "E / Q       上升 / 下降\r\n"
    "滚轮        FOV（长焦↔广角）\r\n"
    "V           定格（时间冻结）\r\n"
    "B           退出自由相机"
)

# 操作提示状态：Lua 进自由相机写 1，退出写 0
OVLIPC = os.path.join(BASE, 'freecam_on.txt')


def overlay_thread():
    """自由相机的操作提示面板（纯 ctypes 置顶窗口，鼠标穿透，不进任务栏）。

    为什么不是游戏内 UMG：用户不想让它进截图；且 NewObject 的 TextBlock
    拿不到字体，渲染不出来（两次踩坑后放弃）。

    ⚠ 64 位 ctypes 的坑（每个都实测踩过）：
      * Python 3.13 的 wintypes 没有 WNDCLASS / HCURSOR / PAINTSTRUCT，要手工定义
      * 所有句柄必须显式 argtypes/restypes，否则按 32 位截断直接 OverflowError
      * FillRect / DrawTextW 在 user32 不在 gdi32
    出错时写 overlay_err.txt，不再静默失败。
    """
    ERRLOG = os.path.join(BASE, 'overlay_err.txt')
    def fail(msg):
        try:
            with open(ERRLOG, 'a', encoding='utf-8') as f:
                f.write('%.1f %s\n' % (time.time(), msg))
        except OSError:
            pass

    try:
        u = ctypes.windll.user32
        k = ctypes.windll.kernel32
        g = ctypes.windll.gdi32

        LRESULT = ctypes.c_longlong
        HCURSOR = ctypes.c_void_p
        HMENU = ctypes.c_void_p
        WNDPROC = ctypes.WINFUNCTYPE(LRESULT, wt.HWND, ctypes.c_uint, wt.WPARAM, wt.LPARAM)

        class PAINTSTRUCT(ctypes.Structure):
            _fields_ = [('hdc', wt.HDC), ('fErase', wt.BOOL), ('rcPaint', wt.RECT),
                        ('fRestore', wt.BOOL), ('fIncUpdate', wt.BOOL),
                        ('rgbReserved', ctypes.c_byte * 32)]

        class WNDCLASSW(ctypes.Structure):
            _fields_ = [
                ('style', ctypes.c_uint),
                ('lpfnWndProc', WNDPROC),
                ('cbClsExtra', ctypes.c_int),
                ('cbWndExtra', ctypes.c_int),
                ('hInstance', wt.HINSTANCE),
                ('hIcon', wt.HICON),
                ('hCursor', HCURSOR),
                ('hbrBackground', wt.HBRUSH),
                ('lpszMenuName', wt.LPCWSTR),
                ('lpszClassName', wt.LPCWSTR),
            ]

        u.CreateWindowExW.restype = wt.HWND
        u.CreateWindowExW.argtypes = [wt.DWORD, wt.LPCWSTR, wt.LPCWSTR, wt.DWORD,
                                      ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                      wt.HWND, HMENU, wt.HINSTANCE, wt.LPVOID]
        k.GetModuleHandleW.restype = wt.HMODULE
        u.DefWindowProcW.restype = LRESULT
        u.DefWindowProcW.argtypes = [wt.HWND, ctypes.c_uint, wt.WPARAM, wt.LPARAM]
        u.RegisterClassW.restype = ctypes.c_ushort
        u.RegisterClassW.argtypes = [ctypes.c_void_p]
        u.DestroyWindow.argtypes = [wt.HWND]
        u.UnregisterClassW.argtypes = [wt.LPCWSTR, wt.HINSTANCE]
        u.IsWindow.argtypes = [wt.HWND]
        u.IsWindowVisible.argtypes = [wt.HWND]
        u.ShowWindow.argtypes = [wt.HWND, ctypes.c_int]
        u.SetWindowPos.argtypes = [wt.HWND, wt.HWND, ctypes.c_int, ctypes.c_int,
                                   ctypes.c_int, ctypes.c_int, ctypes.c_uint]
        u.BeginPaint.argtypes = [wt.HWND, ctypes.c_void_p]
        u.BeginPaint.restype = wt.HDC
        u.EndPaint.argtypes = [wt.HWND, ctypes.c_void_p]
        u.GetClientRect.argtypes = [wt.HWND, ctypes.c_void_p]
        u.SetTimer.argtypes = [wt.HWND, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p]
        u.FillRect.argtypes = [wt.HDC, ctypes.c_void_p, wt.HBRUSH]
        u.DrawTextW.argtypes = [wt.HDC, wt.LPCWSTR, ctypes.c_int, ctypes.c_void_p, ctypes.c_uint]
        u.PostQuitMessage.argtypes = [ctypes.c_int]

        WM_DESTROY, WM_PAINT, WM_TIMER = 0x0002, 0x000F, 0x0113
        WM_ERASEBKGND = 0x0014
        font = g.CreateFontW(-15, 0, 0, 0, 400, 0, 0, 0, 1, 0, 0, 0, 0,
                             'Microsoft YaHei')

        def wndproc(hwnd, msg, wp, lp):
            if msg == WM_DESTROY:
                u.PostQuitMessage(0)
                return 0
            if msg == WM_ERASEBKGND:
                return 1
            if msg == WM_PAINT:
                ps = PAINTSTRUCT()
                hdc = u.BeginPaint(hwnd, ctypes.byref(ps))
                r = wt.RECT()
                u.GetClientRect(hwnd, ctypes.byref(r))
                brush = g.CreateSolidBrush(0x00182030)
                u.FillRect(hdc, ctypes.byref(r), brush)
                g.DeleteObject(brush)
                r.left += 14
                r.top += 12
                g.SetBkMode(hdc, 1)
                g.SetTextColor(hdc, 0x00FFD86A)
                old = g.SelectObject(hdc, font)
                u.DrawTextW(hdc, OVERLAY_TEXT, -1, ctypes.byref(r), 0x0000)
                g.SelectObject(hdc, old)
                u.EndPaint(hwnd, ctypes.byref(ps))
                return 0
            return u.DefWindowProcW(hwnd, msg, wp, lp)

        cb = WNDPROC(wndproc)
        wc = WNDCLASSW()
        wc.lpfnWndProc = cb
        wc.hInstance = k.GetModuleHandleW(None)
        wc.lpszClassName = 'CamZoomFreeCamHelp'
        wc.hbrBackground = None
        if not u.RegisterClassW(ctypes.byref(wc)):
            fail('RegisterClassW failed err=%d' % u.GetLastError())
            return
        hwnd = u.CreateWindowExW(
            0x00000008 | 0x00000020 | 0x00000080,   # TOPMOST | TRANSPARENT | TOOLWINDOW
            'CamZoomFreeCamHelp', 'FreeCam',
            0x80000000,                              # WS_POPUP
            48, 48, 380, 210, None, None, wc.hInstance, None)
        if not hwnd:
            fail('CreateWindowExW failed err=%d' % u.GetLastError())
            return

        msg = wt.MSG()
        u.SetTimer(None, 991, 300, None)
        while True:
            r = u.GetMessageW(ctypes.byref(msg), None, 0, 0)
            if r <= 0:
                break
            if (not msg.hWnd) and msg.message == WM_TIMER:
                try:
                    with open(OVLIPC, encoding='ascii') as f:
                        on = f.read().strip().startswith('1')
                except OSError:
                    on = False
                u.ShowWindow(hwnd, 8 if on else 0)   # SW_SHOWNA / SW_HIDE
                continue
            u.TranslateMessage(ctypes.byref(msg))
            u.DispatchMessageW(ctypes.byref(msg))
    except Exception as e:
        fail('EXCEPTION %r' % e)


def tick():
    """1s 一次：刷新 pid 集合 → 按游戏是否在跑装卸钩子 → 每 2s 写心跳。"""
    refresh_pids()
    # 防抖：pid 快照偶尔会一帧看不到游戏（Toolhelp 快照/权限），钩子跟着一开一关，
    # 表现出来就是「按一会儿有反应、一会儿完全没反应」。看过就保持 10s 有效。
    if _game_pids:
        _last_game_seen[0] = time.time()
    # 黑名单：带前台判定 + 死人开关，见 load_block()
    load_block()
    want = game_running() or bool(_launcher_pids) or (time.time() - _last_game_seen[0] < 10.0)
    live = bool(_state['mouse'] or _state['key'])
    if want and not live:
        install_hooks()
    elif not want and live:
        remove_hooks()
    _tick_n[0] += 1
    if _tick_n[0] % 2 == 0:
        write_beat()
    if _tick_n[0] % 60 == 0:
        trim_raw()
    # 兜底：切窗口/丢焦点时收不到 KEYUP，按住状态会永久卡住（相机一直飘）。
    # 按住时系统每 ~30ms 发一次 repeat，超过 2.5s 没动静就视为已松开。
    if _held:
        now = time.time()
        stale = [v for v in _held if now - _key_down.get(v, 0) > 2.5]
        if stale:
            for v in stale:
                _held.discard(v)
                _key_down.pop(v, None)
            write_held()


def main():
    _cb['mouse'] = HOOKPROC(_mouse_proc)
    _cb['key'] = HOOKPROC(_key_proc)

    # 操作提示面板：独立线程 + 独立消息泵，失败也不影响钩子
    try:
        import threading
        threading.Thread(target=overlay_thread, daemon=True).start()
    except Exception:
        pass

    write_dir(0)          # 初始化 IPC 文件
    write_key(0)
    write_beat()
    try:
        with open(OVLIPC, 'w', encoding='ascii') as f:
            f.write('0')
    except OSError:
        pass
    with open(os.path.join(BASE, 'sniffer.pid'), 'w', encoding='ascii') as f:
        f.write(str(os.getpid()))

    # 启动时先刷新 pid 再决定挂不挂钩子
    refresh_pids()
    if game_running():
        install_hooks()
    else:
        write_state(False)

    # 1s 定时器：阻塞式消息泵 + 定时器 = 空闲时 0 CPU、钩子回调零延迟
    user32.SetTimer(None, TIMER_ID, TICK_MS, None)

    msg = wt.MSG()
    while True:
        ret = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
        if ret <= 0:
            break
        if (not msg.hWnd) and msg.message == WM_TIMER:
            tick()
            continue
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageW(ctypes.byref(msg))
    return 0


if __name__ == '__main__':
    sys.exit(main())
