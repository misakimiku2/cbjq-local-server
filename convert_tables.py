# -*- coding: utf-8 -*-
"""
MikuSB-Resource (JSON) -> acacia TSV 转换器
从 GitHub 拉取 42 个游戏数据表，转换成 acacia 服务器需要的 TSV 格式
输出到 D:\test\cbjq-re\server2\data\settings\
"""
import json
import os
import re
import time
import urllib.request

BASE = 'https://raw.githubusercontent.com/Kei-Luna/MikuSB-Resource/main/'
CACHE = r'D:\test\cbjq-re\convert_cache'
OUTPUT = r'D:\test\cbjq-re\server2\data\settings'

os.makedirs(CACHE, exist_ok=True)

# 42 个表的映射（acacia path <- mikusb json path）
pairs = [
    ('activity/activities.txt', 'activity/activities.json'),
    ('activity/sign/signday.txt', 'activity/sign/signday.json'),
    ('activity/sign/signshort.txt', 'activity/sign/signshort.json'),
    ('activity/gacha_try/gacha_try.txt', 'activity/gacha_try/gacha_try.json'),
    ('activity/gacha_try/try_girl.txt', 'activity/gacha_try/try_girl.json'),
    ('item/templates/card.txt', 'item/templates/card.json'),
    ('item/templates/weapon.txt', 'item/templates/weapon.json'),
    ('item/templates/support_card.txt', 'item/templates/support_card.json'),
    ('item/templates/others.txt', 'item/templates/others.json'),
    ('item/templates/suplies.txt', 'item/templates/suplies.json'),
    ('item/templates/weapon_parts.txt', 'item/templates/weapon_parts.json'),
    ('item/templates/card_skin.txt', 'item/templates/card_skin.json'),
    ('item/templates/dorm_gift.txt', 'item/templates/dorm_gift.json'),
    ('item/templates/profile.txt', 'item/templates/profile.json'),
    ('item/templates/weapon_skin.txt', 'item/templates/weapon_skin.json'),
    ('item/templates/monster_card.txt', 'item/templates/monster_card.json'),
    ('item/templates/manifestation.txt', 'item/templates/manifestation.json'),
    ('item/templates/main_scene.txt', 'item/templates/main_scene.json'),
    ('item/templates/house_photo.txt', 'item/templates/house_photo.json'),
    ('item/templates/house_commonphoto.txt', 'item/templates/house_commonphoto.json'),
    ('item/templates/ar_item.txt', 'item/templates/ar_item.json'),
    ('item/templates/call_item.txt', 'item/templates/call_item.json'),
    ('item/templates/card_skin_parts.txt', 'item/templates/card_skin_parts.json'),
    ('item/break.txt', 'item/break.json'),
    ('item/skill/spine.txt', 'item/skill/spine.json'),
    ('item/skill/nodecondition.txt', 'item/skill/nodecondition.json'),
    ('item/cardbreak/break.txt', 'item/cardbreak/break.json'),
    ('item/cardbreak/breaknew.txt', 'item/cardbreak/breaknew.json'),
    ('item/support/affix_pool.txt', 'item/support/affix_pool.json'),
    ('house/gift.txt', 'house/gift.json'),
    ('house/gift_exchange.txt', 'house/gift_exchange.json'),
    ('house/FurniturePos.txt', 'house/FurniturePos.json'),
    ('house/support_furniture.txt', 'house/support_furniture.json'),
    ('house/open_girl.txt', 'house/open_girl.json'),
    ('player/rename.txt', 'player/rename.json'),
    ('cash/cash.txt', 'cash/cash.json'),
    ('battlepass/timelist.txt', 'battlepass/timelist.json'),
    ('chapter/level.txt', 'chapter/level.json'),
    ('daily/level.txt', 'daily/level.json'),
    ('chapter/chapter_main.txt', 'chapter/chapter_main.json'),
    ('chapter/chapter_branch.txt', 'chapter/chapter_branch.json'),
    ('drop/drop.txt', 'drop/drop.json'),
    ('drop/drop_grop.txt', 'drop/drop_grop.json'),
    ('riki/Riki.txt', 'riki/Riki.json'),
    ('dlc/rogue3d/server_01_difficult.txt', 'dlc/rogue3d/server_01_difficult.json'),
    ('challenge/bosspvp/boss_challenge.txt', 'challenge/bosspvp/boss_challenge.json'),
    ('challenge/climbtower/climb_tower_time.txt', 'challenge/climbtower/climb_tower_time.json'),
    ('challenge/climbtower/climb_tower_diff.txt', 'challenge/climbtower/climb_tower_diff.json'),
    ('challenge/climbtower/climb_tower_award.txt', 'challenge/climbtower/climb_tower_award.json'),
    ('challenge/climbtower/climb_tower_levelorder.txt', 'challenge/climbtower/climb_tower_levelorder.json'),
    ('shop/goods.txt', 'shop/goods.json'),
    ('shop/shop_tab.txt', 'shop/shop_tab.json'),
]


def to_lua(v):
    """JSON 值 -> Lua 表字面量/标量文本"""
    if v is None:
        return ''
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, (int, float)):
        if isinstance(v, float) and v == int(v):
            return str(int(v))
        return str(v)
    if isinstance(v, str):
        return v.replace('\t', ' ').replace('\r', ' ').replace('\n', ' ').replace('"', "'")
    if isinstance(v, list):
        return '{' + ','.join(to_lua(x) for x in v) + '}'
    if isinstance(v, dict):
        # 数字键 dict（如 Node1Condition: {"1":1,"2":2}）-> {{k,v},...}
        try:
            pairs = sorted(((int(k), val) for k, val in v.items()), key=lambda x: x[0])
            return '{' + ','.join('{' + str(k) + ',' + to_lua(val) + '}' for k, val in pairs) + '}'
        except (ValueError, TypeError):
            return '{' + ','.join(f'{k}={to_lua(x)}' for k, x in v.items()) + '}'
    return str(v)


def download(jpath):
    """下载 JSON（带缓存）"""
    cache_file = os.path.join(CACHE, jpath.replace('/', '_'))
    if os.path.exists(cache_file) and os.path.getsize(cache_file) > 0:
        return open(cache_file, 'rb').read()
    url = BASE + jpath
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'table-converter'})
            data = urllib.request.urlopen(req, timeout=30).read()
            open(cache_file, 'wb').write(data)
            return data
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(1.5)
    raise RuntimeError('unreachable')


def convert(records):
    """JSON 数组 -> TSV 文本"""
    if not isinstance(records, list) or not records:
        return None
    # 表头：所有 key 的并集（保持首次出现顺序）
    headers = []
    seen = set()
    for rec in records:
        if isinstance(rec, dict):
            for k in rec.keys():
                if k not in seen:
                    seen.add(k)
                    headers.append(k)
    # 数据行
    lines = []
    # 第一行：占位（会被服务器丢弃）
    lines.append('xxx_0\t' + '\t'.join(['A'] * len(headers)))
    # 第二行：表头
    lines.append('\t'.join(headers))
    # 数据行
    for rec in records:
        if not isinstance(rec, dict):
            continue
        row = [to_lua(rec.get(h)) for h in headers]
        lines.append('\t'.join(row))
    return '\r\n'.join(lines) + '\r\n'


def main():
    ok, fail = 0, 0
    for txt_path, jpath in pairs:
        try:
            raw = download(jpath)
            records = json.loads(raw.decode('utf-8-sig'))
            tsv = convert(records)
            if tsv is None:
                print(f'  [跳过] {txt_path}: 空数据')
                fail += 1
                continue
            out_path = os.path.join(OUTPUT, txt_path.replace('/', os.sep))
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, 'w', encoding='utf-8', newline='') as f:
                f.write(tsv)
            n = tsv.count('\r\n') - 2
            print(f'  [OK] {txt_path}  ({n} 条记录)')
            ok += 1
        except Exception as e:
            print(f'  [失败] {txt_path}: {e}')
            fail += 1
    print(f'\n完成: 成功 {ok}, 失败 {fail}')

    # 验证关键表: (1,2,1,1) 是否存在
    card_file = os.path.join(OUTPUT, 'item', 'templates', 'card.txt')
    if os.path.exists(card_file):
        content = open(card_file, encoding='utf-8').read()
        hits = [l for l in content.split('\r\n') if l.startswith('1\t2\t1\t1\t')]
        print(f'\n验证 gdpl=[1,2,1,1] 的卡片: 找到 {len(hits)} 条')
        if hits:
            print('  示例:', hits[0][:100])


if __name__ == '__main__':
    main()
