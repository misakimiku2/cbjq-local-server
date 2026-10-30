# 尘白禁区 · 本地服整合方案

一站式《尘白禁区》(Snowbreak: Containment Zone) 本地私人服务器方案：
一键启动、网页控制台、GM 工具、全量数据本地保存。

> ⚠️ 本项目仅供学习与研究，请于 24 小时内自行删除，勿用于任何商业用途。
> 与游戏官方（西山居 / Seasun）无任何关联。

## 组件架构

```
┌─────────────┐   hosts 接管    ┌──────────────┐
│  尘白禁区客户端 │ ───────────▶ │ https_mock    │
│ (不修改任何文件) │              │ (127.0.0.1)  │
└─────────────┘              └──────┬───────┘
                                    ▼
┌─────────────┐   HTTP/WS    ┌──────────────┐
│ 浏览器控制台   │ ◀─────────  │  launcher.py  │
│ GM 工具/状态灯 │              │ (一键编排)    │
└─────────────┘              └──────┬───────┘
                                    ▼
                            ┌──────────────┐
                            │ acacia-rs     │
                            │ 游戏服务器(AGPL)│
                            └──────────────┘
```

- **launcher/** — 一键启动器（PyInstaller 打包为桌面 exe）：拉起 mock 与游戏服务器、
  打开网页控制台（http://127.0.0.1:8899）、提供 GM 工具（超级大礼包/全解锁/满级等）
- **mock/** — HTTPS 地址接管（`cbjq-serverlist.xoyocdn.com` → 127.0.0.1），
  证书为本地自签名，需自行生成（见 mock/README）
- **runtime/** — 战斗滚轮镜头缩放 Mod 的外部滚轮嗅探器（详见 [cbjq-mods 仓库](https://github.com/…/cbjq-mods)）
- **tools/** — repak 使用说明与 unlock_tower 等实用脚本（repak 本体请从官方 release 下载）
- **convert_tables.py** — 游戏数据表 → JSON 缓存转换（生成 `convert_cache/`，不入库）
- **docs/** — 商城协议逆向交接文档等研究笔记

## 快速开始

1. 按 [acacia-rs](https://github.com/ahalpha/acacia-rs) 上游说明编译游戏服务器
   （本仓库含本地修改的 fork 见 …）
2. `mock/` 内生成自签名证书并导入系统信任区
3. hosts 添加 `127.0.0.1 cbjq-serverlist.xoyocdn.com`
4. `python launcher/launcher.py`（或打包为 exe 后双击）
5. 正常启动游戏即可连入本地服

## 目录结构

```
cbjq-local-server/
├── launcher/        # 一键启动器 + Web 控制台 + GM 工具
├── mock/            # HTTPS 地址接管
├── runtime/         # 滚轮嗅探器脚本（配套镜头 Mod）
├── tools/           # 辅助工具
├── experiment/      # 抓包分析实验记录
├── docs/            # 逆向研究交接文档
└── convert_tables.py
```

## 致谢

- [ahalpha/acacia-rs](https://github.com/ahalpha/acacia-rs) — 游戏服务端模拟器（AGPL-3.0）
- [ahalpha/Snowbreak-AnitAmend](https://github.com/ahalpha/Snowbreak-AnitAmend) — 模组思路参考
- [repak](https://github.com/trumank/repak) — Unreal .pak 打包工具

## 许可

本仓库自有代码部分按现状提供，不含任何游戏官方资源；acacia-rs 部分遵循 AGPL-3.0。
