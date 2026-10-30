# -*- coding: utf-8 -*-
"""
地下清理（爬塔）进度一键拉满

做的事：
  1. 读 climb_tower_time 表，取当前周期的 Level1（基础区）与 Level2（进阶区）关卡组
  2. 通过 climb_tower_levelorder 把「爬塔关卡ID」映射成「实际关卡ID」
  3. 逐条调 GM.SetAttr 写入：
       属性(22, 实际关卡ID) = 1          通关记录 -> 首通奖励判定
       属性(3, 10000+爬塔关卡ID) = 511   9 星满星位图 -> 3/6/9 星档奖励判定
  4. 设置进阶难度与历史最高难度，让难度选择不被拦

用法：
  python tools/unlock_tower.py            # 基础区 + 进阶区
  python tools/unlock_tower.py --basic    # 只做基础区

注意：GM 命令需要玩家在线（客户端停在游戏内），否则服务器会静默跳过。
"""
import argparse
import json
import os
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLE_DIR = os.path.join(ROOT, 'server2', 'data', 'settings', 'challenge', 'climbtower')
GM_URL = 'http://127.0.0.1:1234/gm/script'
PLAYER_PID = 10001

ATTR_GID = 3
SID_DIFF = 4
SID_HISTORY_DIFF = 5
SID_TIME = 1
SID_LEVEL_STATE_BASE = 10000
FULL_STAR = 0x1FF  # 3 区域 × 3 星


def load_tsv(name):
    with open(os.path.join(TABLE_DIR, name), encoding='utf-8') as f:
        lines = f.read().splitlines()
    headers = lines[1].split('\t')
    rows = []
    for ln in lines[2:]:
        if not ln.strip():
            continue
        rows.append(dict(zip(headers, ln.split('\t'))))
    return rows


def parse_groups(cell):
    """'{3071,3072},{3073,3074}' -> [[3071,3072],[3073,3074]]"""
    cell = (cell or '').strip()
    if not cell or cell in ('{}', '""'):
        return []
    groups = []
    for chunk in cell.strip('{}').split('},{'):
        ids = [int(x) for x in chunk.strip('{}').split(',') if x.strip().isdigit()]
        if ids:
            groups.append(ids)
    return groups


def current_cycle(rows):
    import datetime as dt

    def parse_time(v):
        v = (v or '').strip().strip('[]')
        if len(v) != 12:
            return None
        try:
            return dt.datetime.strptime(v, '%Y%m%d%H%M')
        except ValueError:
            return None

    now = dt.datetime.utcnow()
    latest = None
    for r in rows:
        s, e = parse_time(r.get('StartTime')), parse_time(r.get('EndTime'))
        if not s or not e:
            continue
        if s <= now < e:
            return r
        if s <= now and (latest is None or s > parse_time(latest.get('StartTime'))):
            latest = r
    return latest


def gm(code):
    body = json.dumps({"pid": PLAYER_PID, "code": code}).encode('utf-8')
    req = urllib.request.Request(GM_URL, data=body,
                                 headers={'Content-Type': 'application/json'}, method='POST')
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=30) as r:
            r.read()
        return int((time.time() - t0) * 1000)
    except Exception as e:
        print(f"    [失败] {code} -> {e}")
        return -1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--basic', action='store_true', help='只拉基础区')
    args = ap.parse_args()

    times = load_tsv('climb_tower_time.txt')
    cycle = current_cycle(times)
    if not cycle:
        print('找不到当前周期，检查 climb_tower_time.txt')
        return 1

    cycle_id = cycle['ID']
    basic = parse_groups(cycle.get('Level1'))
    advanced = parse_groups(cycle.get('Level2'))
    print(f"当前周期 {cycle_id}：基础区 {len(basic)} 层，进阶区 {len(advanced)} 层")

    order = {r['ID']: r.get('LevelID') or r['ID'] for r in load_tsv('climb_tower_levelorder.txt')}

    groups = list(basic)
    if not args.basic:
        groups += advanced
    else:
        groups = basic

    # 收集所有爬塔关卡 ID
    tower_ids = []
    for g in groups:
        for tid in g:
            if tid not in tower_ids:
                tower_ids.append(tid)

    print(f"共 {len(tower_ids)} 个爬塔关卡，开始写属性（需玩家在线）...")

    # 周期与难度前置：历史难度给满，允许自由选难度
    gm(f"GM.SetAttr({{{ATTR_GID}, {SID_TIME}, {cycle_id}}})")
    gm(f"GM.SetAttr({{{ATTR_GID}, {SID_DIFF}, 1}})")
    gm(f"GM.SetAttr({{{ATTR_GID}, {SID_HISTORY_DIFF}, 3}})")

    ok = 0
    for i, tid in enumerate(tower_ids, 1):
        level_id = order.get(str(tid), tid)
        ms1 = gm(f"GM.SetAttr({{22, {level_id}, 1}})")
        ms2 = gm(f"GM.SetAttr({{{ATTR_GID}, {SID_LEVEL_STATE_BASE + tid}, {FULL_STAR}}})")
        if ms1 >= 0 and ms2 >= 0:
            ok += 1
        print(f"  [{i}/{len(tower_ids)}] 爬塔关卡 {tid} -> 实际关卡 {level_id}："
              f"通关={ms1}ms 满星={ms2}ms")
        time.sleep(0.05)

    print(f"\n完成：{ok}/{len(tower_ids)} 个关卡写入成功")
    if ok == 0:
        print('全部失败 —— 大概率是玩家不在线（GM 命令需要客户端连接着服务器）')
        return 1
    print('现在回到游戏打开奖励界面，各层奖励应当都可领取')
    return 0


if __name__ == '__main__':
    sys.exit(main())
