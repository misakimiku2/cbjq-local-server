# -*- coding: utf-8 -*-
"""
尘白禁区 · 本地服务器地址接管服务（HTTPS Mock）
================================================
原理：
  游戏启动时会请求 https://cbjq-serverlist.xoyocdn.com/query?version=...&platform=...
  获取"官方服务器地址"。本服务配合 hosts 劫持，替代该请求的响应，
  把服务器地址指向你自己的本地服务器（默认 127.0.0.1:5200）。

用法：
  1. 需要先用 hosts 将 cbjq-serverlist.xoyocdn.com 指向 127.0.0.1
  2. 【以管理员身份】运行本脚本（因为要监听 443 端口）：
     "C:\\Users\\MisakiMiku\\.workbuddy\\binaries\\python\\envs\\default\\Scripts\\python.exe" https_mock.py
  3. 保持窗口开启，然后正常启动游戏

环境变量（可选）：
  MOCK_HOST      目标游戏服务器地址（默认 127.0.0.1）
  MOCK_GAME_PORT 目标游戏服务器端口（默认 5200）
"""
import http.server
import ssl
import json
import sys
import os
import re
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
CERT = os.path.join(BASE, 'server.crt')
KEY = os.path.join(BASE, 'server.key')

LISTEN_PORT = int(os.environ.get('MOCK_PORT', '443'))
TARGET_HOST = os.environ.get('MOCK_HOST', '127.0.0.1')
TARGET_PORT = int(os.environ.get('MOCK_GAME_PORT', '5200'))


def ts():
    return datetime.now().strftime('%H:%M:%S')


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def log_message(self, fmt, *args):
        # 覆盖默认日志，统一格式
        pass

    def do_GET(self):
        print(f'[{ts()}] 收到请求: GET {self.path}  (来自 {self.client_address[0]})', flush=True)
        if self.path.startswith('/query'):
            m = re.search(r'version=([^&]+)', self.path)
            v = m.group(1) if m else '3.6.0'
            m = re.search(r'platform=([^&]+)', self.path)
            p = m.group(1) if m else 'PC'
            # 返回伪造服务器列表：把官方地址替换为本地地址
            data = [{"platform": p, "version": v, "host": TARGET_HOST, "port": TARGET_PORT}]
            body = json.dumps(data, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            print(f'[{ts()}] 已响应: {body.decode()}  (-> 游戏将连接 {TARGET_HOST}:{TARGET_PORT})', flush=True)
        else:
            body = b'404 page not found'
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            print(f'[{ts()}] 已响应: 404 (未知路径)', flush=True)


def main():
    if not (os.path.exists(CERT) and os.path.exists(KEY)):
        print(f'[错误] 缺少证书文件: {CERT} / {KEY}')
        sys.exit(1)

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(CERT, KEY)

    try:
        srv = http.server.ThreadingHTTPServer(('0.0.0.0', LISTEN_PORT), Handler)
    except PermissionError:
        print('=' * 60)
        print(' [错误] 无法监听端口 %d：权限不足' % LISTEN_PORT)
        print(' 请关闭本窗口，然后【右键 -> 以管理员身份运行】本脚本')
        print('=' * 60)
        sys.exit(2)
    except OSError as e:
        print(f'[错误] 端口 {LISTEN_PORT} 被占用或不可用: {e}')
        print('（如果之前已经有一个 Mock 在运行，请先关掉它）')
        sys.exit(3)

    srv.socket = ctx.wrap_socket(srv.socket, server_side=True)

    print('=' * 60)
    print('  尘白禁区 · 本地服务器地址接管服务 已启动')
    print('=' * 60)
    print(f'  监听端口 : {LISTEN_PORT} (HTTPS)')
    print(f'  引导目标 : {TARGET_HOST}:{TARGET_PORT}')
    print()
    print('  现在可以正常启动游戏了。')
    print('  玩游戏期间保持本窗口开启，按 Ctrl+C 可退出。')
    print('=' * 60)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print('\n已退出。')
        srv.server_close()


if __name__ == '__main__':
    main()
