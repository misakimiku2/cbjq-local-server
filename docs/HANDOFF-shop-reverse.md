# 尘白禁区本地服 · 商店商品列表逆向交接

> 状态：**未解决，待逆向**。2026-10-30 记录。
> 接手前请先读完「已确认事实」和「已排除方案」，能省掉几轮编译。

## 一、目标

让游戏内**货币商店**（常规物资 / 活动兑换 / 循环中心 / 数据百货 / 甄选好物）正常显示商品并可购买。

注意：不是氪金商店。氪金商品在 `purchase/ibgoods.json`（566 条，`GoodsTag: com.kingsoft.*`），是另一套。

## 二、当前状态

| 项 | 状态 |
|---|---|
| 商品数据接入 | ✅ 已完成（489 条，按 ShopId 能正确查出） |
| 客户端请求 | ✅ 正常收到，参数正确 |
| 商品渲染 | ❌ **空白**（客户端解析不了响应结构） |
| 页签 / 刷新倒计时 / 刷新费用 / 可重置次数 | ✅ 正常（全部来自客户端本地配置） |
| 购买功能 | ❌ 未开始 |

## 三、已确认事实（不用再验证）

### 1. 客户端请求

```
ShopLogic_GetGoodsList  param={"nShopId":12}
```

- 商店 ID 来自 `shop/shop_tab.json` 的 `ShopId`
- 实测出现：12（常规物资，60 个商品）、13（14 个）、23（13 个）
- 服务端已能按 ShopId 正确返回（`shopId=12 -> 60 个商品`）

### 2. 数据源与字段含义

`Kei-Luna/MikuSB-Resource` → `shop/goods.json`（489 条）+ `shop/shop_tab.json`（16 条）

| 字段 | 含义 |
|---|---|
| `ShopId` / `GoodsId` | 商店 ID / 商品 ID（如 12 / 1198） |
| `GDPLN` | 商品内容 `[genre, detail, particular, level, num]` |
| `Price1` | 价格 `[货币类型, 单价]`，例：`{3,20000}` |
| `Price2` | 第二价格，空表示单一货币 |
| `LimitType` / `LimitNum` | 限购规则（shopId=12 全部是 2 / 1） |
| `Class` / `Weight` | 分类（`ordinary`）/ 权重（10/25/50/100） |

已转换为 `server2/data/settings/shop/goods.txt`，表 `shop_goods`，index `shop_id_1`。

### 3. 客户端本地有完整商店配置

`shop_tab` 里的数值和界面显示**完全一致**：

- `RefreshFee = [50,50,50,50,50]` → 界面「刷新 50」
- `RefreshLimits = 5` → 「可重置次数 0/5」
- `RefreshTime = [0400]` → 倒计时指向每天 04:00

**结论：页签、刷新规则、费用全部由客户端本地渲染**，服务器只负责「有哪些商品、买了多少次」。

### 4. 四种响应结构全部失败

| # | `goodsList` 形式 | 界面表现 |
|---|---|---|
| 1 | `[]` | 正常（本地值 50 / 0-5），商品空白 |
| 2 | `[{对象数组，含 nGoodsId / tbGDPLN / price1 等多种键名}]` | 同 1 |
| 3 | `{"1198": 0, ...}`（映射，值为数字） | **数值错乱**：刷新 6000、可重置 22、倒计时 23:12 天 |
| 4 | `{"1198": {完整对象}, ...}` | 回到 1（正常本地值，商品空白） |

**从这四次能推出的结论：**

- 第 3 次有反应 → 客户端**确实遍历 `goodsList`**，并把 value 当数字参与运算
- 第 4 次无反应 → value 是 table 时客户端直接放弃（异常被 `pcall` 吞掉）
- 所以 `goodsList` 的 value 大概率**期望数字**（已购次数 / 库存 / 数量）
- 但第 3 次错乱显示的是「刷新费用/可重置次数」→ 这些数字被用在了刷新相关的位置，
  语义可能不是「购买次数」，或者客户端用某种累加/取首值的方式处理
- **商品详情（图标、价格）应该是客户端本地拿的**，服务器真正要给的只有状态数字

### 5. 为什么拿不到客户端 Lua

- `PAK_Game_Script_0` 加密，pak 主密钥运行时读取、被 ACE 拦截
  （见 `work/HANDOFF.md` 第 759–760 行，已确认解不出来）
- `Game.log` 里没有相关 Lua 报错 —— 客户端用 `or {}` 之类兜底，**静默失败**

## 四、下一步方案

### 方案 A：UnLua 运行时探测（推荐先做）

1. 写探测脚本注入 `umg_main`（参考 `work/build_both.js` 的注入方式，一个 pak 装多个 mod）
2. 在游戏里 dump：
   - `s2c` 分发表的全部命令名 → 确认 `ShopLogic_GetGoodsList` 对应哪个处理函数
   - `package.loaded` 里名字含 `shop` / `mall` / `store` 的模块及其键名
   - 试 `debug.getinfo(fn).source` 拿到路径后 `io.open` 读源码（大概率失败，值得一试）
3. 输出用 `print`，从 `Game.log`（`E:\SeasunCBJQos\Game\cbjq\game\Saved\Logs\Game.log`）读

### 方案 B：错误注入探测（备选）

故意返回类型错误的数据让客户端抛 Lua 错误，从错误信息反推字段名与用法。
已知难点：多数异常被 `pcall` 吞掉，需要构造能穿透的错误。

### 方案 C：等社区

- MikuSB（`work/MikuSB-main`）**也没有** `ShopLogic_GetGoodsList`，只有 `IBLogic_BuyGoods`（氪金）
- 上游 `ahalpha/acacia-rs` 至今仍是 `"goodsList": [] // WIP`（2026-10-30 已核实）
- 可留意 GitHub 上其它尘白本地服项目的新分支

## 五、代码与数据位置

| 内容 | 路径 |
|---|---|
| handler | `acacia-rs/acacia-game-server/src/handlers/callgs/shop_logic.rs` |
| 表注册 | `acacia-rs/acacia-data/src/tables.rs`（`shop_goods`） |
| schema | `acacia-rs/acacia-data/src/schemas/others.rs`（`ShopGoodsData`） |
| 表转换 | `cbjq-re/convert_tables.py`（`shop/goods`、`shop/shop_tab` 两行） |
| 数据 | `server2/data/settings/shop/goods.txt` |
| 客户端日志 | `E:\SeasunCBJQos\Game\cbjq\game\Saved\Logs\Game.log` |

## 六、编译与部署（踩过的坑，务必照做）

**编译：**

```bash
cd D:/test/cbjq-re/acacia-rs
cargo build --release -p acacia-game-server --features full -j 4
```

> ⚠ **必须带 `-j 4`**。默认并行度会 jobserver 死锁：进程在、CPU 累计只有 0.3 秒、
> 几十分钟零产出。判断方法是对比两次采样 `Get-Process rustc | Select CPU` 是否增长。
> 正常约 3.5–4 分钟。

**部署：**

acacia 以管理员身份运行，普通 PowerShell `Stop-Process` 杀不掉；运行中的 exe
**不能覆盖但可以重命名**：

```powershell
Rename-Item 现 exe -> acacia-game-server.exe.old
Copy-Item   新 exe -> acacia-game-server.exe
POST http://127.0.0.1:8899/restart_server
```

重启会让玩家断线，需重新登录。属性已落库，不受影响。

## 七、当前代码状态（下次接手第一件事）

`shop_logic.rs` 现在返回的是**体积最大**的那个版本：

```json
{
  "shopId": 12, "nShopId": 12,
  "goodsList": { "1198": {完整商品对象}, ... },   // 60 条
  "tbGoods":     [对象数组],
  "tbGoodsList": [对象数组],
  "goods":       [对象数组]
}
```

四个键各带一份 60 条数据，**单次响应约 200KB**。界面能正常显示（客户端放弃了），
但每次打开商店都在传无用数据。建议下次开工先把 `GetGoodsList` 精简回：

```rust
arg: json!({"shopId": shop_id, "goodsList": []})
```

同时把诊断用的 `warn!` 降级为 `debug!`（当前每次开商店都会刷两行 WARN）。

## 八、购买功能（尚未开始）

- acacia 没有任何购买接口
- MikuSB 的 `IBLogic_BuyGoods` 是氪金商品逻辑（查 `IbGoodsData`），货币商店用不上
- 货币商店的购买接口名未知，建议和列表格式一起逆向时确认：
  在探测 mod 里 dump `s2c` 全表，就能看到客户端注册了哪些购买相关命令

## 九、收益评估（决定投入前先想清楚）

商店的实际收益是「用游戏币买东西」。当前可用替代方案：

- `GM.AddAllItem()` —— 全物品（角色/皮肤/武器/后勤/材料）
- `GM.Add(GM.AddMoney, {类型, 数量})` —— 刷货币

所以商店属于**锦上添花**，不影响核心玩法。逆向成本（动 pak + 多轮重启验证）明显高于收益，
这也是本轮选择搁置的原因。
