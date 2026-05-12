# 团子竞速模拟器

当前版本：v2.7

基于《鸣潮》团子活动规则的回合制竞速模拟器，支持上半场/下半场两种模式，多个团子组别，单次过程回放和多次统计分析。

## 游戏规则

6 个普通团子 + 1 个 Boss 团子在 32 格环形赛道上竞速，上半场最先跑完一圈（进度 ≥ 32）、下半场最先跑完两圈（进度 ≥ 64）的团子获胜。

### 基础规则

- 首回合先随机决定初始堆叠顺序（起点自上而下排列），行动顺序为该顺序的**逆序**
- 首回合普通团子从上到下移动时，**不会带动**头上的其他团子
- 第 2 回合起所有普通团子按随机顺序行动，布大王从第 3 回合开始加入随机顺序
- 普通团子骰子范围 **1-3**，Boss 骰子范围 **1-6**
- 同一格上的团子形成堆叠，底层团子移动时整组带走
- 布大王第 3 回合在终点（cell 0）出场，之后沿终点往起点方向移动，**每走一格**会将该格上所有团子从下往上摞到头上，剩余步数带着头上团子继续移动

### 地图装置

| 装置      | 格子            | 效果        |
| ------- | ------------- | --------- |
| 🚀 推进装置 | 3, 11, 16, 23 | 前进 1 格    |
| 🪤 阻遏装置 | 10, 28        | 后退 1 格    |
| 🌪 时空裂隙 | 6, 20         | 当前格堆叠随机重排 |

***

## 团子技能

### A 组

#### 达妮娅 — 连掷激励

> 投骰子时，若投出和上一次相同的点数，则额外前进 **2 格**。
> 第一回合无上次点数，不触发。

#### 菲比 — 幸运掷骰

> **50%** 概率额外前进 **1 格**。

#### 西格莉卡 — 标记指令

> 每回合投骰后，标记排名紧邻自身且更高的至多 **2 个**团子。
> 被标记者本回合移动 **-1 格**（最低 1 格）。

#### 绯雪 — 追击之魂

> 与布大王相遇后，**永久**获得每次移动额外 **+1 格**。

#### 陆·赫斯 — 装置精通

> 触发推进装置时总共 **+4 格**（默认 1 + 额外 3）。
> 触发阻遏装置时总共 **-2 格**（默认 1 + 额外 1）。

#### 卡提希娅 — 绝境逆袭

> 每场比赛最多触发 **1 次**。
> 自身移动结束后若处于最后一名，剩余回合 **60%** 概率额外前进 **2 格**。

### B 组

#### 千咲 — 最小激励

> 投骰子时，若投出的结果为本轮所有点数**最小之一**，则额外前进 **2 格**。

#### 莫宁 — 循环骰子

> 投骰子时，点数将固定在 **3 → 2 → 1** 循环出现（忽略随机投骰结果）。

#### 琳奈 — 波动步伐

> 每回合中，有 **60%** 概率按照双倍点数移动，但有 **20%** 概率当回合**无法移动**。

#### 爱弥斯 — 中点传送

> 每圈**一次**，当该团子经过赛程中点（每圈 progress % 32 跨过 16）后，若前方存在其他非布大王的团子，则会传送到**最近**团子顶端。
> 第一圈中点 progress 16，第二圈中点 progress 48，各自独立触发。

#### 守岸人 — 稳定投掷

> 骰子只会掷出 **2 或 3**。

#### 珂莱塔 — 双倍冲刺

> **28%** 概率以骰子的双倍点数前进。

### C 组

#### 奥古斯塔 — 顶端蛰伏

> 回合开始时，若该团子处于堆叠最顶端，则**本回合不行动**，且在下回合中**最后一个行动**。

#### 尤诺 — 排名聚合

> 每场比赛**一次**，当该团子经过赛程中点后，若排名前后有其他非布大王团子，则将这些团子传送至自己的格子。堆叠顺序与传送前的排名顺序一致。

#### 弗洛洛 — 底层突破

> 回合开始时，若该团子处于堆叠最底层，则在移动时额外前进 **3 格**。

#### 长离 — 蓄势待发

> 如果下方堆叠其他团子，下一个回合有 **65%** 概率最后一个行动。

#### 今汐 — 凌越巅峰

> 如果头顶堆叠其他团子，有 **40%** 的概率移动到所有团子的最上方。

#### 卡卡罗 — 末位追击

> 开始移动时，如果在最后一名，额外前进 **3 格**。

### 布大王 (Boss) — 噩梦之主

> 第 3 回合起在终点（cell 0）出场，参与每回合随机投骰与行动顺序。
> 行动前不参与团子堆叠排序，但一定处于堆叠底部。
> 骰子 1-6，赛道内所有装置机制均对其生效。
> 沿终点往起点方向移动，**逐步移动**：每经过一格，若该格上有团子存在，则将其全部摞到头上（从下往上），剩余步数带着头上团子继续跑。
> 每回合结束后，若布大王已与**全部 6 名**普通团子相遇过，则**传送回终点**（cell 0）并重置相遇记录，开始新一轮巡回。

***

## 安装

```bash
git clone https://github.com/suching8848/Wuthering_Waves_dango_simulator.git
cd Wuthering_Waves_dango_simulator
```

仅需 Python 3.10+，无外部依赖。

## 使用

### 上半场单次模拟

模拟一局完整的上半场比赛，输出每回合的投骰结果、技能触发、移动过程、装置触发、排名变化及最终结果。

```bash
python main.py single                           # A组，随机种子
python main.py single --seed 42                 # A组，固定种子
python main.py single --seed 42 --fixed-order   # A组，固定初始堆叠
python main.py single --group B                 # B组
python main.py single --group C                 # C组
python main.py single --group B --seed 42       # B组，固定种子
```

### 上半场多次模拟 — 统计胜率

运行大量上半场对局，统计各团子获胜次数、胜率、平均/最小/最大回合数。

```bash
python main.py multi                     # A组，默认 1000 次
python main.py multi -n 10000            # A组，自定义次数
python main.py multi --group B           # B组
python main.py multi --group C           # C组
python main.py multi --group B -n 100 --seed 42
```

### 下半场模拟 — 从上半场局势预测下半场胜者

在上半场命令后加 `-s` 指定快照文件即可切换为下半场。**同组续跑**时继承上半场位置和技能状态；**异组新跑**时从 cell 0 全新起跑。布大王在下半场第 3 回合重新入场。

```bash
# 下半场单次
python main.py single -s presets/a_early.json --group A        # A组续跑（同组，继承位置/技能）
python main.py single -s presets/a_early.json --group B        # B组新跑（异组，cell 0 起跑）
python main.py single -s presets/b_finish.json --group B       # B组续跑（同组，B组预设）

# 下半场多次
python main.py multi -s presets/b_finish.json --group B -n 100 --seed 42  # 多次预测
```

**JSON 状态文件格式：**

```json
{
  "round": 8,
  "dangos": {
    "daniya":    {"cell": 0,  "progress": 32},
    "phoebe":    {"cell": 31, "progress": 31},
    "siglica":   {"cell": 31, "progress": 31},
    "feixue":    {"cell": 30, "progress": 30, "state": {"metBoss": true}},
    "luhesi":    {"cell": 30, "progress": 30},
    "katixiya":  {"cell": 29, "progress": 29, "state": {"skill_activated": true}}
  },
  "stacks": {
    "0":  ["budaiwang", "daniya"],
    "31": ["siglica", "phoebe"],
    "30": ["luhesi", "feixue"]
  },
  "boss": {
    "cell": 0,
    "progress": 24,
    "spawned": true
  },
  "seed": 42
}
```

| 字段 | 说明 |
|------|------|
| `round` | 上半场结束时的回合数（必填），下半场从此回合+1 开始 |
| `dangos` | 各团子的 cell、progress（必填），可选 `state` 继承上半场技能状态 |
| `stacks` | 同格团子的堆叠顺序（底→顶），含 Boss 的堆叠需显式列出 Boss 在底部 |
| `boss` | Boss 状态：`cell`、`progress`、`spawned` |
| `seed` | 可选随机种子，命令行 `--seed` 参数优先级更高 |

### 参数一览

| 参数 | 适用模式 | 说明 |
|------|----------|------|
| `--group` | 全部 | 选择团子组别 A/B/C（上半场默认 A，下半场默认 B） |
| `--seed` | 全部 | 固定随机种子 |
| `--fixed-order` | single | 固定初始堆叠顺序 |
| `-s, --state` | single/multi | 上半场结束状态的 JSON 文件路径（指定后切换为下半场） |
| `-n, --num-simulations` | multi | 模拟次数，默认 1000 |

***

## 快速示例

```bash
# 上半场 A 组单次模拟
python main.py single --seed 42 --fixed-order

# 上半场 B 组多次统计
python main.py multi --group B -n 100 --seed 42

# 下半场 A 组续跑（同组继承位置）
python main.py single -s presets/a_early.json --group A --seed 42

# 下半场 B 组全新起跑（异组，cell 0 起跑）
python main.py single -s presets/a_early.json --group B --seed 42

# 下半场 B 组续跑（同组，继承位置/技能）
python main.py single -s presets/b_finish.json --group B --seed 42

# 下半场 B 组多次预测
python main.py multi -s presets/b_finish.json --group B -n 100 --seed 42
```

***

## 更新内容

### v2.7

- 新增: **C 组** 6 个团子及技能（奥古斯塔、尤诺、弗洛洛、长离、今汐、卡卡罗）。
- 新增: 引擎 `_act_last` 机制 — 技能可推迟团子到下回合最后行动（奥古斯塔、长离）。
- 重做: 布大王移动逻辑改为**逐步移动** — 每经过一格，若该格上有团子存在则全部从下往上摞到头上，剩余步数带着头上团子继续跑。
- 更新: CLI `--group` 参数支持 `C`，交互式菜单同步支持 C 组。

### v2.61

- 新增: `menu.py` 交互式菜单界面，无需记忆命令，逐级选择即可运行。

### v2.6

- 统一: CLI 命令统一为 `single`/`multi`，加 `-s` 文件即下半场，移除 `second`/`predict` 子命令。
- 修改: 爱弥斯「中点传送」从整局一次改为每圈触发一次（第一圈跨过 progress 16、第二圈跨过 progress 48 均可触发）。
- 新增: `presets/` 目录统一存放下半场预设配置文件，包含 A 组早期/后期、B 组终点等场景。
- 优化: 预设文件去除固定种子，默认随机种子运行，仅 CLI `--seed` 参数可固定。

### v2.51

- 修复: 爱弥斯「中点传送」传送到较高圈数团子时 progress 可能倒退的问题（`move_to_cell` 跨圈数修正）。
- 验证: 全部 13 个团子技能逐项检查，确认正确生效。

### v2.5

- 重构: 上半场/下半场两种模式分离，`single`/`multi` 为上半场，新增 `second` 为下半场（`predict` 保留为别名）。
- 新增: 所有模式均支持 `--group A|B` 参数，任意组别可用于任意模式。
- 新增: 下半场同组续跑 — 使用 `--group A` 时从快照恢复 A 组团子的位置、堆叠和技能状态。
- 新增: B 组六个团子及技能（千咲、莫宁、琳奈、爱弥斯、守岸人、珂莱塔）。
- 修复: 布大王在下半场第 3 回合重新入场（而非立即出场）。
- 重构: 模块化团子组系统，`config/default_config.py` 中按注释指引即可添加新组。

### v2.32

- 新增: 下半场技能状态继承 — JSON 中每个团子可通过 `state` 字段指定上半场结束时的技能状态（如绯雪的 `metBoss`、卡提希娅的 `skill_activated`），下半场直接沿用，无需重新触发激活条件。

### v2.31 [测试版]

- 修正: 布大王传送机制 — 从"与最后一名不在同格即传送"改为"与全部 6 名团子相遇后才传送回终点，同时重置相遇记录"。Boss 需要在赛道上逐轮移动并与各团子相遇，集齐 6 次相遇后才触发传送，更贴合实际游戏行为。

### v2.3

- 新增: 下半场预测功能（测试版），支持从上半场结束局势模拟下半场。通过 JSON 文件输入各团子位置、进度、堆叠关系及 Boss 状态，使用 `python main.py predict -s state.json` 运行。
  - 下半场**继承**上半场回合数，不重新计数。
  - 下半场胜者条件为跑完**第二圈**（progress ≥ 64），未完成第一圈的团子继续跑完第一圈后冲刺第二圈，上半场胜者正常参与下半场竞速。
  - 新增多次预测模式 `python main.py predict -s state.json -n 100`，统计下半场各团子胜率。
- 新增: 布大王传送机制 — 与全部 6 名团子相遇后传送回终点（cell 0）并重置相遇记录。
- 新增: 布大王详细机制描述（不参与堆叠排序、装置对其生效、始终处于堆叠底部）。
- 修复: Pylance 严格模式下 `list[str] = None` 类型标注报错，统一改为 `list[str] | None`。

### v2.21

- 修正西格莉卡「标记指令」首回合不应生效的问题：第 1 回合投骰后不再标记目标。

### v2.2

- 修复卡提希娅「绝境逆袭」全平局误判：`_is_last_place` 增加 `min < max` 判定，全平局时不再激活。
- 修复 Boss 携带普通团子倒退时报错：被带走的普通团子改用 `advance(-steps)`。
- 修复 `_apply_group_displacement` 中 Boss 对装置触发的方向处理缺失。
- 修复 `_check_device_trigger` 中 `final_cell` 未使用装置后位置的问题。
- 清理死代码：`move_to_cell` 的 `progress < 0` 分支、`boss_skill.py` 的 `_get_last_place_dango` / `_teleport_boss_to_start`。

### v2.1

- 修复卡提希娅「绝境逆袭」激活判定 Bug：`_is_last_place` 比较符号从 `>` 修正为 `<`，现在正确地在最后一名时激活而非第一名。
- 布大王默认携带上方堆叠团子移动 (`boss_carries_upper_stack = True`)。
- 修正 `advance_backward` 实现：Boss 逆向进度保持正向递增，cell 通过 `(-progress) % length` 计算，避免 progress 出现负值。
- 单次模拟新增技能触发提示：每个团子行动时如技能生效，会输出 `[技能]` 前缀的提示语。

### v2.0

- 模块化重写：技能系统抽象为 `BaseSkill` 基类 + 独立技能文件，游戏引擎与模拟器解耦。
- 引入堆叠管理器 (`StackManager`) 统一管理环形赛道上的堆叠状态。
- 新增多次模拟统计功能 (`python main.py multi`)。

### v1.6

- 修正西格莉卡技能时机：改为在投骰阶段、她自己投完骰子后立刻结算并锁定本回合减速目标。
- 修正西格莉卡标记不会在移动阶段前再次重算，保证当前回合名次变化不会影响已发动的技能效果。

### v1.5

- 修正布大王反向移动时的堆叠携带与装置位移逻辑，被带走的普通团子会被正确往回拖动。
- 修正绯雪技能判定：只要绯雪位置大于等于布大王位置，即视为已经相遇，并永久获得每次移动额外 +1 步。

### v1.4

- 修正布大王出场与展示逻辑：第 3 回合才在终点出场，并在每回合日志中显示状态。
- 修正布大王行动参与：从第 3 回合开始加入随机投骰与随机顺序，但不计入最终排名。

### v1.3

- 修正布大王出场逻辑：不再开局就占据起点，而是在第 3 回合正式从终点出场。
- 修正布大王反向移动建模：其位置按"从终点往起点逆向巡场"计算，并与普通团子方向相反。

### v1.2

- 修复堆叠移除后位置索引未清理的问题，避免 Boss 等角色在日志中出现错误原位置。
- 修复最终堆叠输出包含空格子的显示问题，使结束态展示与实际堆叠一致。

## 配置

所有可调参数集中在 `config/default_config.py`，按注释指引即可添加新组：

```python
# 团子组定义 — 添加新组只需在 DANGO_GROUPS 中添加并配置对应团子
DANGO_GROUPS = {
    "A": DANGO_IDS_A,
    "B": DANGO_IDS_B,
    "C": DANGO_IDS_C,
}

# 技能参数
SKILL_CONFIG = {
    # A 组
    "daniya":   {"extra_steps_on_same_dice": 2},
    "phoebe":   {"extra_step_probability": 0.5},
    "siglica":  {"mark_count": 2, "mark_penalty": 1},
    "feixue":   {"extra_steps_after_meeting_boss": 1},
    "luhesi":   {"boost_extra_steps": 3, "trap_extra_steps": 1},
    "katixiya": {"activation_probability": 0.6, "extra_steps": 2},
    # B 组
    "qianxiao":  {"extra_steps_on_min_dice": 2},
    "moning":    {"dice_cycle": [3, 2, 1]},
    "linnai":    {"double_probability": 0.6, "skip_probability": 0.2},
    "aimisi":    {"midpoint": 16},
    "shouanren": {},
    "kelaite":   {"double_probability": 0.28},
    # C 组
    "aogusita": {},
    "younuo":   {"midpoint": 16},
    "fuluoluo": {"extra_steps": 3},
    "changli":  {"delay_probability": 0.65},
    "jinxi":    {"rise_probability": 0.4},
    "kakaluo":  {"extra_steps": 3},
}
```

***

## 项目结构

```
├── menu.py                  # 交互式菜单界面
├── main.py                  # CLI 入口
├── presets/                 # 下半场预设快照
│   ├── a_early.json         # A组上半场早期
│   ├── a_late.json          # A组上半场后期（达妮娅已胜）
│   └── b_finish.json        # B组终点局势
├── config/
│   └── default_config.py    # 默认配置（团子、技能、装置、组别）
├── core/
│   ├── game_engine.py       # 游戏引擎
│   ├── simulator.py         # 模拟器（单次/多次/下半场）
│   └── stack_manager.py     # 堆叠管理
├── models/
│   ├── dango.py             # 团子数据模型
│   ├── board.py             # 赛道模型
│   └── game_state.py        # 对局状态
├── skills/
│   ├── base_skill.py        # 技能基类（10 个生命周期钩子）
│   ├── daniya_skill.py      # A组: 达妮娅
│   ├── phoebe_skill.py      # A组: 菲比
│   ├── siglica_skill.py     # A组: 西格莉卡
│   ├── feixue_skill.py      # A组: 绯雪
│   ├── lu_hesi_skill.py     # A组: 陆·赫斯
│   ├── katixiya_skill.py    # A组: 卡提希娅
│   ├── qianxiao_skill.py    # B组: 千咲
│   ├── moning_skill.py      # B组: 莫宁
│   ├── linnai_skill.py      # B组: 琳奈
│   ├── aimisi_skill.py      # B组: 爱弥斯
│   ├── shouanren_skill.py   # B组: 守岸人
│   ├── kelaite_skill.py     # B组: 珂莱塔
│   ├── aogusita_skill.py    # C组: 奥古斯塔
│   ├── younuo_skill.py      # C组: 尤诺
│   ├── fuluoluo_skill.py    # C组: 弗洛洛
│   ├── changli_skill.py     # C组: 长离
│   ├── jinxi_skill.py       # C组: 今汐
│   ├── kakaluo_skill.py     # C组: 卡卡罗
│   └── boss_skill.py        # Boss: 布大王
└── utils/
    └── logger.py            # 日志输出
```

## License

MIT
