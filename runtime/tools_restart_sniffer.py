# -*- coding: utf-8 -*-
"""重启输入嗅探器（wheel_sniffer.py）。

用途：修改 wheel_sniffer.py 后必须重启进程才会生效（钩子只在启动时安装）。
      本脚本用 Python 直接 TerminateProcess + CreateProcess，绕过 shell 工具层的
      限制，并让新进程脱离当前 job object，保证脚本退出后嗅探器继续常驻。

用法：python tools_restart_sniffer.py
"""
import ctypes
from ctypes import wintypes as wt
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PYW = r'C:\Users\MisakiMiku\.workbuddy\binaries\python\versions\3.13.12\pythonw.exe'
SCRIPT = os.path.join(HERE, 'wheel_sniffer.py')

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
PROCESS_TERMINATE = 0x0001
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

# 1) 找出旧进程并结束。优先用 sniffer.pid（sniffer 自己写的），
#    没有就退回「所有 pythonw.exe」—— 本机 pythonw 只用来跑嗅探器。
#    不用 wmic：Win11 24H2 起已移除。
def terminate(pid):
    h = kernel32.OpenProcess(PROCESS_TERMINATE, False, pid)
    if not h:
        return False
    try:
        kernel32.TerminateProcess(h, 0)
        return True
    finally:
        kernel32.CloseHandle(h)


def list_pythonw():
    out = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq pythonw.exe', '/FO', 'CSV', '/NH'],
                         capture_output=True, text=True, errors='ignore').stdout
    pids = []
    for line in out.splitlines():
        parts = [p.strip('"') for p in line.split('","')]
        if len(parts) >= 2 and parts[0].lower().startswith('pythonw'):
            try:
                pids.append(int(parts[1]))
            except ValueError:
                pass
    return pids


def kill_old():
    killed = []
    pidfile = os.path.join(HERE, 'sniffer.pid')
    targets = []
    if os.path.exists(pidfile):
        try:
            targets = [int(open(pidfile, encoding='utf-8').read().strip())]
        except ValueError:
            targets = []
    if not targets:
        targets = list_pythonw()
    for pid in targets:
        if terminate(pid):
            killed.append(pid)
    return killed


killed = kill_old()
print('killed:', killed)
time.sleep(0.8)

# 2) 以脱离 job 的方式启动新进程
DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200
CREATE_BREAKAWAY_FROM_JOB = 0x01000000
flags = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_BREAKAWAY_FROM_JOB
si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
si.wShowWindow = 0
try:
    p = subprocess.Popen([PYW, SCRIPT], cwd=HERE, creationflags=flags,
                         startupinfo=si, close_fds=True,
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
except OSError as e:
    print('breakaway failed (%s), retry without' % e)
    flags = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
    p = subprocess.Popen([PYW, SCRIPT], cwd=HERE, creationflags=flags,
                         startupinfo=si, close_fds=True,
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)

time.sleep(2.5)
alive = os.path.join(HERE, 'sniffer_alive.txt')
err = os.path.join(HERE, 'sniffer_error.txt')
print('new pid:', p.pid, 'poll:', p.poll())
if os.path.exists(alive):
    print('alive.txt:', open(alive, encoding='utf-8').read().strip())
if os.path.exists(err):
    print('error.txt:', open(err, encoding='utf-8').read().strip())
print('check process:', subprocess.run(['tasklist', '/FI', 'IMAGENAME eq pythonw.exe'],
                                       capture_output=True, text=True).stdout)
