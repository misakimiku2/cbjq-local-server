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
import math
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
WM_MOUSEMOVE = 0x0200
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
GAME_PROCS = ('game.exe', 'games.exe', 'game-win64-shipping.exe')
# ⚠ 'games.exe' 是实测补上的：本机游戏本体叫 Games.exe（游戏目录 ...\Game\Binaries\Win64）。
#   少了它 game_running() 恒 False，会连锁毁掉一整套判定：
#     overlay 以为游戏没跑 → 每 2s 把 on 置 0 → UI 周期消失、_ovl_on=0 →
#     钩子不拦方向键 / 不转发点击（v6~v8 鼠标点不通的真正原因也是这个）。
#   进程名以游戏安装目录为准，换版本时先用 tasklist 核一遍。
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
                    0x5A: 'Z', 0x58: 'X',
                    # F9：景深滑块面板开关（v19；嗅探器内部消费，Lua 侧 blockList
                    # 也加了 120，游戏收不到）。
                    0x78: 'F9',
                    # ESC：拍照模式下 UI 全隐藏，ESC 直接退出自由相机（Lua v18）。
                    # Lua 同时把 27 写进 blockList —— 键盘钩子「先记后吞」，
                    # fp_key.txt 照样收到、游戏菜单不弹；拍照模式外 ESC 照常进菜单。
                    0x1B: 'ESC'}

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
user32.GetAsyncKeyState.restype = ctypes.c_short
user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
user32.GetCursorPos.argtypes = [ctypes.c_void_p]
user32.PostMessageW.restype = wt.BOOL
user32.PostMessageW.argtypes = [wt.HWND, ctypes.c_uint, wt.WPARAM, wt.LPARAM]
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
kernel32.QueryFullProcessImageNameW.restype = wt.BOOL
kernel32.QueryFullProcessImageNameW.argtypes = [wt.HANDLE, wt.DWORD, wt.LPWSTR,
                                                ctypes.POINTER(wt.DWORD)]

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
_gone = [0]              # 连续多少拍看不到游戏（清理 freecam_on 的防抖计数）
# pid 快照会间歇性抽风（见过 game_pids 忽空），但 pid 本身在一次游戏会话里
# 是稳定的 —— 用「曾经见过」的集合做前台判定，不受抽风影响。
# （残留风险：pid 被系统回收复用给别的程序时可能误判一次；黑名单本身有
#   3s 死人开关 + 只在游戏前台生效，出错的代价被限制在很短的窗口内）
_game_pids_ever = set()
_launcher_pids_ever = set()
_launcher_pid = 0       # 启动器（本地服）pid：非 0 时随启动器退出自尽
_launcher_miss = [0]    # 启动器失联连续计数（3 次 = 确认退出）
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


def pid_image_alive(pid, name_hints):
    """pid 是否活着且映像名含任一提示串（防 pid 被系统回收复用后误判）。"""
    h = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not h:
        return False
    try:
        buf = ctypes.create_unicode_buffer(300)
        size = wt.DWORD(300)
        if kernel32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(size)):
            n = (buf.value or '').replace('/', '\\').lower()
            return any(x in n for x in name_hints)
        return True      # 查不到名字（权限抖动）按活着算，保守
    except Exception:
        return True
    finally:
        kernel32.CloseHandle(h)


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
        # 鼠标一律不参与面板交互（v9 起彻底放弃）：分层窗口叠在游戏上方时，
        # 无论切 WS_EX_TRANSPARENT 还是钩子转发，实机都收不到可靠点击 /
        # 拖动会跟游戏视角打架。面板改为纯键盘（方向键）操作，见 adj_dof()。
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
            # ---- 方向键调景深（v9）----
            # 拍照模式 + 面板展开时，方向键只归滑块：直接改内存并吞掉，
            # 游戏收不到（它在这时也没什么用 —— HUD 全隐藏）。
            # 按住会持续 repeat，天然支持连续微调。
            if vk in _DIRKEYS and _ovl_on[0] and DOF['show']:
                adj_dof(vk)
                return 1
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
                    if vk == 0x78:            # F9：收起 / 展开景深面板（默认展开）
                        DOF['show'] = not DOF['show']
                        DOF['dirty'] = True
            # 记录完再吞：Q/E 要先进 keys_held.txt 给相机升降用，再挡住游戏
            if vk in _block:
                return 1
        except Exception:
            pass
    elif nCode == 0 and wParam in (WM_KEYUP, WM_SYSKEYUP):
        try:
            kb = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
            vk = int(kb.vkCode)
            # 方向键的 KEYUP 也吞掉：KEYDOWN 已经拦下，别让游戏收到孤立的抬起
            if vk in _DIRKEYS and _ovl_on[0] and DOF['show']:
                return 1
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


# ── 自由相机操作提示 v2（精装键帽版）────────────────────────────
# 键帽 = 白色描边圆角矩形 + 键帽字母 + 黑色投影；整窗无底板（透明浮在画面上）。
# 渲染在 overlay_thread() 里用 GDI+ 完成（纯 GDI 做不出抗锯齿圆角和半透明投影）。
OVL_HEADER = '自 由 相 机'
# ('cap', 文本) = 键帽；('label', 文本) = 说明；('gap', 像素) = 组间距
OVL_ROWS = [
    [('cap', '鼠标'), ('label', '转视角')],
    [('cap', 'W'), ('cap', 'A'), ('cap', 'S'), ('cap', 'D'), ('label', '移动')],
    [('cap', 'E'), ('label', '上升'), ('gap', 18), ('cap', 'Q'), ('label', '下降')],
    [('cap', '滚轮'), ('label', '变焦 FOV')],
    [('cap', 'V'), ('label', '定格时间')],
    [('cap', 'B'), ('label', '进入 / 退出'), ('gap', 18), ('cap', 'ESC'), ('label', '退出')],
]

# 操作提示状态：Lua 进自由相机写 1，退出写 0
OVLIPC = os.path.join(BASE, 'freecam_on.txt')

# ── 景深滑块面板（v19；v6 overlay 起常显）──────────────────────
# v6 起面板**随拍照 UI 常显**，不再需要 F9 才出现：
#   * show —— 是否绘制面板。默认 True；F9 仅作「收起 / 展开」的可选开关，
#     每次进入拍照模式都重置为 True（用户要求：进相机就有滑块）。
#   * edit —— 交互态，**由 ALT 按住驱动**，与 show 解耦。原先 edit 跟 panel
#     开关绑在一起，面板一常显就等于 WASD 永远被滑块吃掉、相机走不动。
#     现在：按住 ALT（游戏本来就用它呼出鼠标指针）= 冻结走位 + 可拖拽滑块；
#     松开 ALT 立刻把 WASD 还给相机。
# 参数写 dof.txt 给 Lua 应用："fstop focus edit"，Lua 每 20 帧同步。
DOFIPC = os.path.join(BASE, 'dof.txt')
DOF = {'show': True, 'sel': 0, 'fstop': 2.8, 'focus': 800.0,
       'dirty': False}      # 首帧由 paint() 直接画，无需再置脏
# (下限, 上限, 单步)
DOF_RANGE = {'fstop': (1.4, 16.0, 0.2), 'focus': (100.0, 8000.0, 120.0)}

# overlay 是否正在显示（钩子只在显示时拦截方向键）
_ovl_on = [0]
# 交互诊断（每 400ms 落一次）：on/edit/dofsel/值 够定位「按键没进钩子 / 进了没改值」
OVLSTATE = os.path.join(BASE, 'overlay_state.txt')

# ── 方向键调参（v9）──────────────────────────────────────────
# 用户实测：鼠标拖拽这条路走不通（分层窗口在游戏上方收不到点击，两版都没解决），
# 改为**纯键盘**：↑↓ 选参数、←→ 调数值。方向键在拍照模式下由钩子直接吞掉，
# 不写 fp_key.txt（避免 Lua 侧误判），也不进 blockList（不用改 pak）。
DIR_VK = {'up': 0x26, 'down': 0x28, 'left': 0x25, 'right': 0x27}
_DIRKEYS = frozenset(DIR_VK.values())
# 最近一次方向键调参结果（钩子写、overlay 线程读，用于诊断文件）
LASTKEY = ['-']


def adj_dof(vk):
    """方向键改景深参数。只在钩子线程调用：**不动磁盘**，只改内存 + 置脏，
    由 overlay 线程序列化（避免在低级钩子里做文件 IO，那会拖到钩子超时）。"""
    if vk == DIR_VK['up']:
        DOF['sel'] = (DOF['sel'] - 1) % 2
    elif vk == DIR_VK['down']:
        DOF['sel'] = (DOF['sel'] + 1) % 2
    else:
        dkey = 'fstop' if DOF['sel'] == 0 else 'focus'
        lo, hi, step = DOF_RANGE[dkey]
        v = DOF[dkey] + (step if vk == DIR_VK['right'] else -step)
        if v < lo:
            v = lo
        if v > hi:
            v = hi
        if v == DOF[dkey]:
            return
        DOF[dkey] = float('%.2f' % v)
    DOF['dirty'] = True
    LASTKEY[0] = 'vk=%d sel=%d fstop=%.1f focus=%.0f' % (
        vk, DOF['sel'], DOF['fstop'], DOF['focus'])


def write_dof():
    # 第 3 字段（edit / 冻结相机走位）v9 起恒 0：方向键调参不占用 WASD，
    # 没有理由为了调滑块把相机锁住。
    try:
        with open(DOFIPC, 'w', encoding='ascii') as f:
            f.write('%.2f %.0f 0' % (DOF['fstop'], DOF['focus']))
    except OSError:
        pass


def read_held_vks():
    try:
        with open(HELDIPC, encoding='ascii') as f:
            return set(int(x) for x in f.read().split() if x.isdigit())
    except (OSError, ValueError):
        return set()


def overlay_thread():
    """自由相机的操作提示面板 v2（GDI+ 逐像素 alpha 分层窗，鼠标穿透，不进任务栏）。

    为什么不是游戏内 UMG：用户不想让它进截图；且 NewObject 的 TextBlock
    拿不到字体，渲染不出来（两次踩坑后放弃）。

    v2（2026-10-30，用户需求「精装」）：
      * 去掉底部色板 —— 整窗透明，键帽/文字直接浮在画面上
      * 按键 = 白色描边圆角矩形 + 键帽字母 + 黑色投影（键帽样式）
      * 全部文字带黑色投影，亮/暗场景都可读
    实现：GDI+（gdiplusflat）画进 PARGB 位图 → UpdateLayeredWindow。
    纯 GDI 做不到：圆角无抗锯齿，且 GDI 不写 alpha 字节（半透明投影不可能）。

    ⚠ 64 位 ctypes 的坑（每个都实测踩过）：
      * Python 3.13 的 wintypes 没有 WNDCLASS / HCURSOR，要手工定义
      * 所有句柄必须显式 argtypes/restypes，否则按 32 位截断直接 OverflowError
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
        gd = ctypes.WinDLL('gdiplus')

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

        class RectF(ctypes.Structure):
            _fields_ = [('X', ctypes.c_float), ('Y', ctypes.c_float),
                        ('W', ctypes.c_float), ('H', ctypes.c_float)]

        class GPRECT(ctypes.Structure):
            _fields_ = [('X', ctypes.c_int), ('Y', ctypes.c_int),
                        ('W', ctypes.c_int), ('H', ctypes.c_int)]

        class BitmapData(ctypes.Structure):
            _fields_ = [('Width', ctypes.c_uint), ('Height', ctypes.c_uint),
                        ('Stride', ctypes.c_int), ('Scan0', ctypes.c_void_p),
                        ('Reserved', ctypes.c_size_t)]

        class SIZE(ctypes.Structure):
            _fields_ = [('cx', wt.LONG), ('cy', wt.LONG)]

        class BLENDFUNCTION(ctypes.Structure):
            _fields_ = [('BlendOp', ctypes.c_ubyte), ('BlendFlags', ctypes.c_ubyte),
                        ('SourceConstantAlpha', ctypes.c_ubyte),
                        ('AlphaFormat', ctypes.c_ubyte)]

        class BITMAPINFOHEADER(ctypes.Structure):
            _fields_ = [('biSize', wt.DWORD), ('biWidth', wt.LONG), ('biHeight', wt.LONG),
                        ('biPlanes', wt.WORD), ('biBitCount', wt.WORD),
                        ('biCompression', wt.DWORD), ('biSizeImage', wt.DWORD),
                        ('biXPelsPerMeter', wt.LONG), ('biYPelsPerMeter', wt.LONG),
                        ('biClrUsed', wt.DWORD), ('biClrImportant', wt.DWORD)]

        class BITMAPINFO(ctypes.Structure):
            _fields_ = [('bmiHeader', BITMAPINFOHEADER),
                        ('bmiColors', ctypes.c_uint32 * 3)]

        class GdiplusStartupInput(ctypes.Structure):
            _fields_ = [('GdiplusVersion', ctypes.c_uint32),
                        ('DebugEventCallback', ctypes.c_void_p),
                        ('SuppressBackgroundThread', wt.BOOL),
                        ('SuppressExternalCodecs', wt.BOOL)]

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
        u.ShowWindow.argtypes = [wt.HWND, ctypes.c_int]
        u.SetTimer.argtypes = [wt.HWND, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p]
        u.PostQuitMessage.argtypes = [ctypes.c_int]
        u.BeginPaint.argtypes = [wt.HWND, ctypes.c_void_p]
        u.BeginPaint.restype = wt.HDC
        u.EndPaint.argtypes = [wt.HWND, ctypes.c_void_p]
        u.GetDC.restype = wt.HDC
        u.GetDC.argtypes = [wt.HWND]
        u.ReleaseDC.argtypes = [wt.HWND, wt.HDC]
        u.UpdateLayeredWindow.restype = wt.BOOL
        u.UpdateLayeredWindow.argtypes = [wt.HWND, wt.HDC, ctypes.c_void_p, ctypes.c_void_p,
                                          wt.HDC, ctypes.c_void_p, ctypes.c_uint,
                                          ctypes.c_void_p, ctypes.c_uint]
        g.CreateCompatibleDC.restype = wt.HDC
        g.CreateCompatibleDC.argtypes = [wt.HDC]
        g.DeleteDC.argtypes = [wt.HDC]
        g.DeleteObject.argtypes = [wt.HANDLE]
        g.SelectObject.restype = wt.HANDLE
        g.SelectObject.argtypes = [wt.HDC, wt.HANDLE]
        g.CreateDIBSection.restype = wt.HBITMAP
        g.CreateDIBSection.argtypes = [wt.HDC, ctypes.c_void_p, ctypes.c_uint,
                                       ctypes.POINTER(ctypes.c_void_p), wt.HANDLE,
                                       ctypes.c_uint]
        # StretchBlt(HALFTONE)：2x → 1x 降采样（GDI+ DrawImage 本机 AV，纯 Python 盒
        # 滤波 0.4s/帧拖不动滑块，GDI 拉伸 ~30ms）
        g.SetStretchBltMode.argtypes = [wt.HDC, ctypes.c_int]
        g.StretchBlt.restype = wt.BOOL
        g.StretchBlt.argtypes = [wt.HDC, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                 ctypes.c_int, wt.HDC, ctypes.c_int, ctypes.c_int,
                                 ctypes.c_int, ctypes.c_int, wt.DWORD]
        u.GetWindowLongPtrW.restype = ctypes.c_ssize_t
        u.GetWindowLongPtrW.argtypes = [wt.HWND, ctypes.c_int]
        u.SetWindowLongPtrW.restype = ctypes.c_ssize_t
        u.SetWindowLongPtrW.argtypes = [wt.HWND, ctypes.c_int, ctypes.c_ssize_t]

        # ---- GDI+ flat 绑定：句柄一律 c_void_p、状态码 c_int（64 位截断的教训）----
        P, I, F = ctypes.c_void_p, ctypes.c_int, ctypes.c_float
        SZT = ctypes.c_size_t
        PP = ctypes.POINTER

        def gp(name, restype, *argtypes):
            # 约定：gp(名字, 返回类型, *参数类型) —— 返回类型恒为 GpStatus(I)
            fn = getattr(gd, name)
            fn.restype = restype
            fn.argtypes = list(argtypes)
            return fn

        gdi_startup = gp('GdiplusStartup', I, PP(SZT), P, P)
        bmp_new = gp('GdipCreateBitmapFromScan0', I, I, I, I, I, P, PP(P))
        #                                                └ w  h  stride fmt scan0 out
        gfx_of = gp('GdipGetImageGraphicsContext', I, P, PP(P))
        smooth = gp('GdipSetSmoothingMode', I, P, I)
        texthint = gp('GdipSetTextRenderingHint', I, P, I)
        gfx_del = gp('GdipDeleteGraphics', I, P)
        img_del = gp('GdipDisposeImage', I, P)
        brush_new = gp('GdipCreateSolidFill', I, ctypes.c_uint32, PP(P))
        brush_del = gp('GdipDeleteBrush', I, P)
        pen_new = gp('GdipCreatePen1', I, ctypes.c_uint32, F, I, PP(P))
        pen_del = gp('GdipDeletePen', I, P)
        path_new = gp('GdipCreatePath', I, I, PP(P))
        path_arc = gp('GdipAddPathArc', I, P, F, F, F, F, F, F)
        path_close = gp('GdipClosePathFigure', I, P)   # ⚠ flat API 叫 ClosePathFigure，
                                                       # 没有 GdipCloseFigure（托管 API 才是 CloseFigure）
        path_fill = gp('GdipFillPath', I, P, P, P)
        path_draw = gp('GdipDrawPath', I, P, P, P)
        path_del = gp('GdipDeletePath', I, P)
        fam_new = gp('GdipCreateFontFamilyFromName', I, wt.LPCWSTR, P, PP(P))
        font_new = gp('GdipCreateFont', I, P, F, I, I, PP(P))
        font_del = gp('GdipDeleteFont', I, P)
        fam_del = gp('GdipDeleteFontFamily', I, P)
        fmt_new = gp('GdipCreateStringFormat', I, I, I, PP(P))
        fmt_align = gp('GdipSetStringFormatAlign', I, P, I)
        fmt_line = gp('GdipSetStringFormatLineAlign', I, P, I)
        fmt_del = gp('GdipDeleteStringFormat', I, P)
        # ⚠ GdipMeasureString 在这台机器的 gdiplus.dll 上对全有效句柄也会 fail-fast
        #   （0xC0000409，探针 1-4：裸调用/argtypes/NULL-format/交换参数全试过，
        #   同参数的 DrawString/GetFontHeight 都正常）—— 测宽彻底弃用字体度量，
        #   键帽宽度按内容硬编码（见下方 estw/draw_cap），GDI+ 只负责画。
        str_draw = gp('GdipDrawString', I, P, wt.LPCWSTR, I, P, PP(RectF), P, P)
        bits_lock = gp('GdipBitmapLockBits', I, P, PP(GPRECT), ctypes.c_uint, I,
                       PP(BitmapData))
        bits_unlock = gp('GdipBitmapUnlockBits', I, P, PP(BitmapData))
        gdi_getdc = gp('GdipGetDC', I, P, PP(wt.HDC))
        gdi_reldc = gp('GdipReleaseDC', I, P, wt.HDC)
        gfx_from_hdc = gp('GdipCreateFromHDC', I, wt.HDC, PP(P))

        token = SZT()
        gsi = GdiplusStartupInput()
        gsi.GdiplusVersion = 1
        if gdi_startup(ctypes.byref(token), ctypes.byref(gsi), None) != 0:
            fail('GdiplusStartup failed')
            return

        WM_DESTROY, WM_PAINT, WM_TIMER = 0x0002, 0x000F, 0x0113
        WM_ERASEBKGND = 0x0014

        # ---- 渲染倍率 ----
        # 目标物理尺寸 (W1,H1)，超采样位图严格 2x (Wk,Hk)=(2W1,2H1)，绘制倍率
        # K = Wk/560。所有绘制坐标按 1x 逻辑值书写乘 K 落到超采样位图，画完做
        # 2x2 盒滤波降采样回物理尺寸 —— 键帽圆角与文字边缘多一轮四点滤波，
        # 明显更顺滑（修「字体/按钮锯齿多」）。
        # DPI 感知已在 main() 开头声明；钩子不涉及屏幕坐标，不受影响。
        _dpi = 96
        try:
            _dpi = int(u.GetDpiForSystem()) or 96
        except Exception:
            _dpi = 96
        S = _dpi / 96.0                       # 物理像素 / 逻辑像素
        W1 = max(1, int(round(560 * S)))      # 物理目标尺寸
        H1 = max(1, int(round(400 * S)))
        Wk, Hk = W1 * 2, H1 * 2               # 精确 2x 超采样（盒滤波要求整倍数）
        K = Wk / 560.0                        # 实际绘制倍率

        # ---- 字体（雅黑 UI 优先，失败退雅黑/黑体）----
        fam = P()
        for nm in ('Microsoft YaHei UI', 'Microsoft YaHei', 'SimHei'):
            if fam_new(nm, None, ctypes.byref(fam)) == 0 and fam:
                break
        if not fam:
            fail('no CJK font family')
            return
        UNIT_PX = 2
        fKey = P(); font_new(fam, 15.0 * K, 1, UNIT_PX, ctypes.byref(fKey))    # 键帽字母 Bold
        fLab = P(); font_new(fam, 14.0 * K, 0, UNIT_PX, ctypes.byref(fLab))    # 说明 Regular
        fHead = P(); font_new(fam, 14.0 * K, 1, UNIT_PX, ctypes.byref(fHead))  # 标题 Bold

        # NoWrap|NoClip：文字不换行不裁剪；键帽字母水平+垂直居中
        # ⚠ GdipCreateStringFormat(attributes, language, &format) —— out 参在最后
        fmtC = P(); fmt_new(0x1000 | 0x4000, 0, ctypes.byref(fmtC))
        fmt_align(fmtC, 2); fmt_line(fmtC, 2)
        fmtL = P(); fmt_new(0x1000 | 0x4000, 0, ctypes.byref(fmtL))
        fmt_line(fmtL, 2)

        # ARGB（0xAARRGGBB）
        brKey = P(); brush_new(0xFFFFFFFF, ctypes.byref(brKey))   # 键帽字母：白
        brKeyS = P(); brush_new(0xB4000000, ctypes.byref(brKeyS))  # 字母投影：黑
        brLab = P(); brush_new(0xF0FFFFFF, ctypes.byref(brLab))   # 说明：白
        brLabS = P(); brush_new(0x99000000, ctypes.byref(brLabS))  # 说明投影：黑
        brHead = P(); brush_new(0xF2A8DCFF, ctypes.byref(brHead))  # 标题：淡蓝
        brHeadS = P(); brush_new(0x99000000, ctypes.byref(brHeadS))
        brFill = P(); brush_new(0x590E1420, ctypes.byref(brFill))  # 键帽底：深色半透明
        brShdw = P(); brush_new(0x73000000, ctypes.byref(brShdw))  # 键帽投影：黑
        brDim = P(); brush_new(0x66FFFFFF, ctypes.byref(brDim))    # 版本标记：半透明白
        brSel = P(); brush_new(0x24A8DCFF, ctypes.byref(brSel))    # 滑块选中行底：淡蓝
        brTrack = P(); brush_new(0x55FFFFFF, ctypes.byref(brTrack))  # 滑轨：半透明白
        brFillHi = P(); brush_new(0xD9FFFFFF, ctypes.byref(brFillHi))  # 滑块填充：白
        penLine = P(); pen_new(0xF2FFFFFF, 2.0 * K, UNIT_PX, ctypes.byref(penLine))  # 白描边

        PARGB = 0x26200A
        gfx = None           # 当前 2x 绘制目标（paint() 里赋值，重绘时重建）

        # ---- 键帽/文本宽度：不再做字体测宽，按内容估算 ----
        # 历史教训（2026-10-31 实机两连击）：
        #   1) GdipMeasureString 在本机 gdiplus.dll 上对有效句柄也 fail-fast，不可用；
        #   2) GDI GetTextExtentPoint32W 与 GDI+ DrawString 的 em 口径不一致
        #      （nHeight 是字符高度不是 em），校准后仍差 40% —— 键帽被撑成扁宽
        #      「挤压变形」。键帽文字是固定集合，直接按设计给宽度，彻底绕开字体度量。
        # 宽度单位 1x 逻辑像素；CJK ≈ 15px/字、ASCII ≈ 8px/字、空格 5px。

        def estw(text):
            w = 0.0
            for ch in text:
                if ch == ' ':
                    w += 5.0
                elif ord(ch) > 0x2E7F:
                    w += 15.0
                else:
                    w += 8.0
            return w

        def rr_path(x, y, w, h, r):
            # 物理坐标（调用方负责 ×K）
            p = P(); path_new(0, ctypes.byref(p))
            d = 2.0 * r
            path_arc(p, x, y, d, d, 180.0, 90.0)
            path_arc(p, x + w - d, y, d, d, 270.0, 90.0)
            path_arc(p, x + w - d, y + h - d, d, d, 0.0, 90.0)
            path_arc(p, x, y + h - d, d, d, 90.0, 90.0)
            path_close(p)
            return p

        def draw_text(text, font, fmt, brush, shbrush, x, y, w, h):
            # 1x 逻辑坐标进，内部 ×K；先黑投影（+1K,+2K）后正文字
            x, y, w, h = x * K, y * K, w * K, h * K
            str_draw(gfx, text, len(text), font,
                     ctypes.byref(RectF(x + 1.0 * K, y + 2.0 * K, w, h)), fmt, shbrush)
            str_draw(gfx, text, len(text), font,
                     ctypes.byref(RectF(x, y, w, h)), fmt, brush)

        def draw_cap(x, y, text):
            # 1x 逻辑坐标进；宽度按内容定（单字母 36 / ESC 44 / 双汉字 50），
            # 返回 1x 逻辑宽给布局 —— 布局与绘制同源，保证窗口装得下
            w = max(36.0, estw(text) + 20.0)
            xk, yk, wk, hk, rk = x * K, y * K, w * K, 30.0 * K, 8.0 * K
            p = rr_path(xk, yk + 3.0 * K, wk, hk, rk)      # 黑色投影
            path_fill(gfx, brShdw, p); path_del(p)
            p = rr_path(xk, yk, wk, hk, rk)                # 半透明深底 + 白描边
            path_fill(gfx, brFill, p)
            path_draw(gfx, penLine, p)
            path_del(p)
            draw_text(text, fKey, fmtC, brKey, brKeyS, x, y, w, 30.0)
            return w

        CAP_H, ROW_GAP, HEAD_GAP = 30.0, 11.0, 10.0
        MX, MTOP, MBOT = 10.0, 6.0, 8.0

        def dof_frac(key):
            if key == 'fstop':
                lo, hi, _ = DOF_RANGE['fstop']
                return math.log(DOF[key] / lo) / math.log(hi / lo)
            lo, hi, _ = DOF_RANGE['focus']
            return (DOF[key] - lo) / (hi - lo)

        # ---- 固定物理尺寸的 DIB + memdc（repaint 复用；ULW 每次只换内容）----
        hdcScreen = u.GetDC(None)
        memdc = g.CreateCompatibleDC(hdcScreen)
        bi = BITMAPINFO()
        bi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bi.bmiHeader.biWidth = W1
        bi.bmiHeader.biHeight = -H1          # 负高 = top-down
        bi.bmiHeader.biPlanes = 1
        bi.bmiHeader.biBitCount = 32
        bi.bmiHeader.biCompression = 0       # BI_RGB
        pv = ctypes.c_void_p()
        hbmp = g.CreateDIBSection(hdcScreen, ctypes.byref(bi), 0, ctypes.byref(pv), None, 0)
        oldbmp = g.SelectObject(memdc, hbmp)
        # 2x 绘制 DIB：GDI+ 通过 HDC 直接画进来（GdipCreateFromHDC），
        # StretchBlt 再从它拉伸到窗口 DIB —— 全程 GDI 表面，避免 GDI+/GDI 交叉读。
        drawdc = g.CreateCompatibleDC(hdcScreen)
        bi2 = BITMAPINFO()
        bi2.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bi2.bmiHeader.biWidth = Wk
        bi2.bmiHeader.biHeight = -Hk
        bi2.bmiHeader.biPlanes = 1
        bi2.bmiHeader.biBitCount = 32
        bi2.bmiHeader.biCompression = 0
        pv2 = ctypes.c_void_p()
        hbmp2 = g.CreateDIBSection(hdcScreen, ctypes.byref(bi2), 0, ctypes.byref(pv2), None, 0)
        oldbmp2 = g.SelectObject(drawdc, hbmp2)
        blend = BLENDFUNCTION(0, 0, 255, 1)          # AC_SRC_OVER / 255 / AC_SRC_ALPHA
        ptSrc = wt.POINT(0, 0)
        HIT = []                       # 滑块行命中区（1x 逻辑坐标，仅布局自检用）
        SZ = {'wh': (0, 0)}            # 上次 ULW 传过的窗口尺寸（只在不一致时重设）
        SHOW = {'on': None}            # 上次的可见状态（None = 还没设置过）
        PTN = [0]                      # paint() 调用次数（诊断「UI 到底有没有重画」）

        def wndproc(hwnd, msg, wp, lp):
            if msg == WM_DESTROY:
                u.PostQuitMessage(0)
                return 0
            if msg == WM_ERASEBKGND:
                return 1
            if msg == WM_PAINT:              # ULW 内容不走 WM_PAINT，验证掉即可
                ps = PAINTSTRUCT()
                hdc = u.BeginPaint(hwnd, ctypes.byref(ps))
                u.EndPaint(hwnd, ctypes.byref(ps))
                return 0
            # v9：窗口不接收鼠标（永久 WS_EX_TRANSPARENT），滑块改方向键控制，
            # 这里不再需要任何鼠标消息分支。
            return u.DefWindowProcW(hwnd, msg, wp, lp)

        cb = [None]
        hwnd = [None]

        def paint():
            """绘制一帧并 ULW 上去。滑块面板常显，仅在内容变化时重画。"""
            nonlocal gfx
            PTN[0] += 1
            HIT.clear()
            ctypes.memset(pv2, 0, Wk * Hk * 4)     # 清空 2x 画布（透明）
            gfx = P()
            if gfx_from_hdc(drawdc, ctypes.byref(gfx)) != 0 or not gfx:
                fail('GdipCreateFromHDC failed')
                return
            smooth(gfx, 4)      # SmoothingModeAntiAlias
            texthint(gfx, 4)    # TextRenderingHintAntiAlias（灰度，透明底无彩边）

            x0, y, maxw = MX, MTOP, 0.0
            hw_, hh = estw(OVL_HEADER), 19.0
            draw_text(OVL_HEADER, fHead, fmtL, brHead, brHeadS, x0, y, hw_ + 12.0, hh)
            # 版本标记（半透明小字）：截图一眼确认跑的是哪版 overlay
            draw_text('v11', fLab, fmtL, brDim, brHeadS, x0 + hw_ + 18.0, y + 1.0,
                      32.0, hh)
            y += hh + HEAD_GAP
            if hw_ > maxw: maxw = hw_

            for row in OVL_ROWS:
                x = x0
                for item in row:
                    if item[0] == 'cap':
                        x += draw_cap(x, y, item[1]) + 7.0
                    elif item[0] == 'label':
                        tw = estw(item[1])
                        draw_text(item[1], fLab, fmtL, brLab, brLabS, x, y, tw + 8.0, CAP_H)
                        x += tw + 12.0
                    else:
                        x += float(item[1])
                if x - 7.0 > maxw: maxw = x - 7.0
                y += CAP_H + ROW_GAP
            bottom = y - ROW_GAP

            # ---- 景深滑块面板（常显；点击由钩子转发，窗口永久穿透）----
            if DOF['show']:
                py = bottom + 8.0
                # 选中行由滑块底色高亮表达，标题保持常态
                draw_text('景深', fHead, fmtL, brHead, brHeadS,
                          x0, py, estw('景深') + 10.0, 19.0)
                py += 24.0
                for i, (lbl, dkey) in enumerate((('光圈', 'fstop'), ('对焦', 'focus'))):
                    if i == DOF['sel']:
                        p = rr_path((x0 - 5.0) * K, (py - 4.0) * K,
                                    246.0 * K, 24.0 * K, 6.0 * K)
                        path_fill(gfx, brSel, p); path_del(p)
                    draw_text(lbl, fLab, fmtL, brLab, brLabS, x0, py, 34.0, 20.0)
                    tx, tw_, th, ty = x0 + 40.0, 150.0, 6.0, py + 7.0
                    p = rr_path(tx * K, ty * K, tw_ * K, th * K, 3.0 * K)
                    path_fill(gfx, brTrack, p); path_del(p)
                    frac = dof_frac(dkey)
                    fw = max(6.0, tw_ * frac)
                    p = rr_path(tx * K, ty * K, fw * K, th * K, 3.0 * K)
                    path_fill(gfx, brFillHi, p); path_del(p)
                    kx = tx + tw_ * frac - 7.0
                    p = rr_path(kx * K, (py + 2.0) * K, 14.0 * K, 14.0 * K, 7.0 * K)
                    path_fill(gfx, brKey, p)
                    path_draw(gfx, penLine, p)
                    path_del(p)
                    vtxt = ('%.1f' % DOF[dkey]) if dkey == 'fstop' else ('%.0f' % DOF[dkey])
                    draw_text(vtxt, fLab, fmtL, brKey, brKeyS, tx + tw_ + 10.0, py,
                              44.0, 20.0)
                    HIT.append((tx - 8.0, py - 4.0, tx + tw_ + 8.0, py + 20.0, dkey))
                    py += 26.0
                draw_text('↑↓ 选参数    ←→ 调数值', fLab, fmtL, brDim,
                          brHeadS, x0, py, estw('↑↓ 选参数    ←→ 调数值') + 8.0, 16.0)
                py += 17.0
                draw_text('F9 收起面板', fLab, fmtL, brDim,
                          brHeadS, x0, py, estw('F9 收起面板') + 8.0, 16.0)
                py += 18.0
                if 246.0 > maxw: maxw = 246.0
                bottom = py

            win_w = int(maxw + MX + 8.0)
            win_h = int(bottom + MBOT)

            # ---- 2x → 1x 降采样：GDI StretchBlt(HALFTONE)，DIB→DIB ----
            g.SetStretchBltMode(memdc, 4)      # HALFTONE
            g.StretchBlt(memdc, 0, 0, W1, H1, drawdc, 0, 0, Wk, Hk, 0x00CC0020)
            gfx_del(gfx)

            if hwnd[0] is None:
                cb[0] = WNDPROC(wndproc)
                wcx = WNDCLASSW()
                wcx.lpfnWndProc = cb[0]
                wcx.hInstance = k.GetModuleHandleW(None)
                wcx.lpszClassName = 'CamZoomFreeCamHelp'
                wcx.hbrBackground = None
                if not u.RegisterClassW(ctypes.byref(wcx)):
                    fail('RegisterClassW failed err=%d' % u.GetLastError())
                    return
                hwnd[0] = u.CreateWindowExW(
                    0x00080000 | 0x00000008 | 0x00000020 | 0x00000080,
                    # LAYERED | TOPMOST | TRANSPARENT | TOOLWINDOW
                    'CamZoomFreeCamHelp', 'FreeCam',
                    0x80000000,                          # WS_POPUP
                    int(48 * S), int(48 * S), int(win_w * S), int(win_h * S),
                    None, None, wcx.hInstance, None)
                if not hwnd[0]:
                    fail('CreateWindowExW failed err=%d' % u.GetLastError())
                    return
            # ⚠ v11：**每次都传 psize**。之前为了防闪烁做了「尺寸没变就传 NULL」的
            #   缓存，实机表现为「按方向键数值变了但面板纹丝不动，只有 F9 收起/展开
            #   （尺寸真的变了）才刷新」—— psize/pptDst 同时为 NULL 时这次 ULW
            #   并没有把新内容贴上去。传相同尺寸不会触发 resize，不会闪。
            size = SIZE(int(win_w * S), int(win_h * S))
            if not u.UpdateLayeredWindow(hwnd[0], hdcScreen, None, ctypes.byref(size),
                                         memdc, ctypes.byref(ptSrc), 0,
                                         ctypes.byref(blend), 2):
                fail('UpdateLayeredWindow err=%d' % u.GetLastError())

        paint()

        msg = wt.MSG()
        # 单定时器 80ms（滑块跟手）。原先每拍都无条件 ShowWindow —— SW_SHOWNA
        # 反复作用于已显示的分层窗口会让 DWM 重新合成，就是「周期性闪烁」的来源。
        # 现在显隐按 400ms 节流、且**只在状态真变化时** ShowWindow。
        # （试过 991/992 两个 SetTimer 分频，WM_TIMER 的 wParam 分支在实测里
        #   不可靠，索性用一个定时器 + 时间戳节流，逻辑更直白。）
        u.SetTimer(None, 991, 80, None)
        prev_on = False
        next_vis = 0.0
        GRACE = {'t': time.monotonic()}   # 最近一次确认游戏在跑的时刻（隐藏宽限用）
        while True:
            r = u.GetMessageW(ctypes.byref(msg), None, 0, 0)
            if r <= 0:
                break
            if (not msg.hWnd) and msg.message == WM_TIMER:
                now = time.monotonic()      # 单调时钟：系统时间被校准时不会被卡住
                if now >= next_vis:
                    next_vis = now + 0.4
                    # ---- 显隐（低频）：拍照模式开关 ----
                    try:
                        with open(OVLIPC, encoding='ascii') as f:
                            on = f.read().strip().startswith('1')
                    except OSError:
                        on = False
                    # 游戏已退（Alt+F4 等）→ 隐藏防 UI 残留。
                    # ⚠ 判定放宽：game_running() 靠进程名匹配，改版就容易失效；
                    #   启动器还在跑时一律认为「游戏可能还在」，绝不隐藏。
                    #   万一真退了，tick() 那边有连续 3 拍的兜底清理。
                    if game_running() or _launcher_pids:
                        GRACE['t'] = now
                    elif on and now - GRACE['t'] > 5.0:
                        on = False
                    if on != prev_on:
                        prev_on = on
                        _ovl_on[0] = 1 if on else 0
                        if hwnd[0]:
                            u.ShowWindow(hwnd[0], 8 if on else 0)  # SW_SHOWNA / SW_HIDE
                        if on:
                            DOF['show'] = True      # 每次进拍照模式都恢复「滑块常显」
                            DOF['dirty'] = True
                    # 诊断（400ms 一次）：够判断「方向键有没有进钩子 / 改没改到值」
                    try:
                        with open(OVLSTATE, 'w', encoding='ascii') as f:
                            f.write('t=%.1f on=%d show=%d sel=%d fstop=%.2f '
                                    'focus=%.0f paints=%d last=%s\n'
                                    % (now, 1 if prev_on else 0,
                                       1 if DOF['show'] else 0, DOF['sel'],
                                       DOF['fstop'], DOF['focus'], PTN[0],
                                       LASTKEY[0]))
                    except OSError:
                        pass
                # ---- 参数落盘 + 重绘 ----
                # 方向键在钩子线程里只改内存（低级钩子里做文件 IO 会拖到超时），
                # 统一由这里序列化：80ms 检查一次，变过才写盘 + 重画。
                if DOF['dirty']:
                    DOF['dirty'] = False
                    write_dof()
                    if hwnd[0]:
                        paint()
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
    # 游戏强退（Alt+F4 等）时 Lua 没机会写 0：清掉 freecam_on 残留，
    # 否则提示窗会一直挂在屏幕上。
    # ⚠ 必须防抖：refresh_pids 偶尔一拍看不到游戏（Toolhelp 快照/权限抖动），
    #   当场清 0 会让 overlay 在拍照模式中途「自己消失」（用户实测消失两次）。
    #   连续 3 拍确认游戏真的不在了才清。
    if game_running() or _launcher_pids:
        _gone[0] = 0
    else:
        _gone[0] += 1
    if _gone[0] >= 3:
        try:
            with open(OVLIPC, encoding='ascii') as f:
                stale_on = f.read().strip() == '1'
        except OSError:
            stale_on = False
        if stale_on:
            try:
                with open(OVLIPC, 'w', encoding='ascii') as f:
                    f.write('0')
            except OSError:
                pass
    # 启动器绑定：本地服启动器已退出（连续 3 次探测失联）→ 清理后自尽
    if _launcher_pid:
        if pid_image_alive(_launcher_pid, ('snowbreaklocalserver', '本地服')):
            _launcher_miss[0] = 0
        else:
            _launcher_miss[0] += 1
            if _launcher_miss[0] >= 3:
                remove_hooks()
                try:
                    with open(OVLIPC, 'w', encoding='ascii') as f:
                        f.write('0')
                except OSError:
                    pass
                write_state(False)
                os._exit(0)


def main():
    # DPI 感知必须先于任何窗口创建：不声明的话 DWM 会按虚拟化坐标拉伸分层窗口，
    # 键帽/文字在高分屏上发糊起锯齿。钩子不涉及屏幕坐标，感知模式对输入转发无影响。
    try:
        ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass
    # 启动器绑定：launcher.py 拉起时带 --launcher-pid，启动器退出 → 本进程自尽
    global _launcher_pid
    if '--launcher-pid' in sys.argv:
        try:
            _launcher_pid = int(sys.argv[sys.argv.index('--launcher-pid') + 1])
        except (ValueError, IndexError):
            _launcher_pid = 0
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
    write_dof()           # 初始化景深参数文件（Lua 侧读这个）
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
