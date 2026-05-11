# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

团子竞速模拟器 — a turn-based racing simulator for the Dango mini-game from _Wuthering Waves_ (鸣潮). 6 normal dangos + 1 boss dango race on a 32-cell circular track per half. Two groups of 6 dangos (A组 / B组). Python 3.10+, zero external dependencies.

## Commands

```bash
# === 上半场 (first half) — 全新比赛 ===
python main.py single                             # A组单次，完整过程回放
python main.py single --group B                   # B组单次
python main.py single --seed 42 --fixed-order     # 固定种子 + 固定初始堆叠

python main.py multi                              # A组多次统计 (默认1000局)
python main.py multi --group B -n 100 --seed 42   # B组100局统计

# === 下半场 (second half) — 加 -s 快照文件即可 ===
python main.py single -s presets/a_early.json --group A        # A组续跑 (同组，继承位置/技能)
python main.py single -s presets/a_early.json --group B        # B组新跑 (异组，cell 0 起跑)
python main.py single -s presets/b_finish.json --group B       # B组续跑 (同组，B组预设)
python main.py multi -s presets/b_finish.json --group B -n 100 --seed 42  # 多次预测
```

No build step, no test suite, no linter configured.

## Preset snapshots

`presets/` directory contains ready-to-use state files for second-half simulations:

| File | Group | Description |
|------|-------|-------------|
| `a_early.json` | A | Early first-half end (round 2, all dangos mid-race) |
| `a_late.json` | A | Late first-half end (daniya won, others scattered) |
| `b_finish.json` | B | B-group at finish line (kelaite at cell 0, boss below) |

These files contain no fixed `seed` — simulations use random seeds unless `--seed` is passed via CLI.

## Architecture

**Entry point:** `main.py` — argparse CLI with `single`/`multi` subcommands. Add `-s state.json` to either to switch from 上半场 to 下半场. All accept `--group A|B` (default: A for 上半场, B for 下半场). Assembles a `config` dict from defaults and CLI args, creates a `Simulator`, and runs it.

**Data flow:** `Simulator` → `GameEngine.create_game_state()` (上半场) or `create_game_state_from_snapshot()` (下半场) → loop `GameEngine.run_round()` until winner found.

**Two-mode group logic:** `create_game_state_from_snapshot(snapshot, rng, dango_group)` auto-detects whether to continue or start fresh:
- **同组** (snapshot dango IDs overlap with current group): restores positions, stacks, and skill states from snapshot. Boss always resets (`boss_spawned=False`, `boss_start_round = snapshot_round + 3`).
- **异组** (snapshot dango IDs don't overlap): current group starts fresh at cell 0 with random initial stack.

### Layers

- **`config/`** — `default_config.py` holds all tunable parameters: board layout (boost/trap/rift cells), dango definitions (A-group + B-group + boss), skill parameters, simulation settings. `DANGO_GROUPS` maps `"A"` / `"B"` to dango ID lists. Each dango config has a `group` field (`"A"`, `"B"`, or `"boss"`). Imported as a flat namespace via `__init__.py`.

- **`models/`** — Dataclasses with game logic methods:
  - `Dango` — contestant: `progress` (total steps taken), `cell` (current board position), `advance()` / `advance_backward()` for normal/boss movement. Boss uses `advance_backward` where progress increments but cell = `(-progress) % length` (reverse direction). `move_to_cell()` sets cell and adjusts progress to keep lap count.
  - `Board` — track with device cell sets (`boost_cells`, `trap_cells`, `rift_cells`).
  - `GameState` — all mutable state for one game: dangos dict, round counter, dice results, siglica marks, winner, logs, `stack_manager` reference, RNG instance, `is_second_half`, `dango_group`, `boss_met_dangos` set.

- **`core/`** — Engine and orchestration:
  - `GameEngine` — owns the board and config. `create_game_state()` initializes dangos (filtered by `dango_group`), stack, skills, and boss. `create_game_state_from_snapshot()` handles second-half initialization: auto-detects same-group (restore positions/stacks/skills from snapshot) vs cross-group (fresh start at cell 0). Boss always resets (`boss_spawned=False`, `boss_start_round = snapshot_round + 3`). `run_round()` is the main turn loop: determine action order → roll dice → execute moves → check devices → check winner. Round 1 order is reverse of initial stack order; round 2+ is random shuffle (same for second-half round 1). Boss spawns at relative round 3.
  - `StackManager` — manages stack state per cell (dict of `cell → list[dango_id]` bottom-to-top). Handles group movement (bottom dango carries upper stack), cell shuffling (rift device), and boss-at-bottom enforcement.
  - `Simulator` — thin wrapper: creates engine, runs single/multi (上半场) or second-half (下半场) simulations, delegates logging. `run_prediction()` and `run_prediction_multi()` accept `dango_group` and pass it to `create_game_state_from_snapshot()`.

- **`skills/`** — Each dango has a skill class inheriting from `BaseSkill`. The base class provides hook methods that the engine calls at specific phases. Skills store per-dango state in `dango.state` dict (e.g., `lastDice`, `pending_extra_steps`, `skill_activated`, `metBoss`). `SKILL_MAPPING` in `__init__.py` maps all 13 dango IDs to skill classes.

  **Hook execution order within a round:**
  1. `on_round_start` — clear per-round state
  2. `on_after_roll` — react to dice result (may modify `game_state.dice_results`)
  3. `modify_move_steps` — adjust steps before siglica penalty
  4. *(siglica penalty applied: `max(1, steps - 1)`)*
  5. `modify_final_steps` — final step adjustment after penalty (e.g., Linnai's skip→0)
  6. `on_after_move` — react after movement (e.g., Aimisi teleport, Katixiya last-place activation)
  7. `on_meet_boss` — triggered when dango meets boss (feixue uses `>=` check, others use `==`)
  8. `on_device_trigger` — triggered when landing on a device cell, returns extra steps or shuffle info
  9. `on_round_end` — per-round cleanup (boss teleport check happens here)
  10. `on_game_end` — called when winner found

  **A-group skills (6):**
  | Skill | Dango | Behavior |
  |-------|-------|----------|
  | 连掷激励 | 达妮娅 | Same dice as last round → +2 steps |
  | 幸运掷骰 | 菲比 | 50% chance +1 step |
  | 标记指令 | 西格莉卡 | Mark up to 2 adjacent higher-ranked dangos, they get -1 step (min 1). Round 1 skip. |
  | 追击之魂 | 绯雪 | After meeting boss, permanently +1 step per move |
  | 装置精通 | 陆·赫斯 | Boost: +4 total (1+3); Trap: -2 total (1+1) |
  | 绝境逆袭 | 卡提希娅 | Once per game: if last place after move, 60% chance +2 steps thereafter |

  **B-group skills (6):**
  | Skill | Dango | Behavior |
  |-------|-------|----------|
  | 最小激励 | 千咲 | If dice is among round minimum → +2 steps |
  | 循环骰子 | 莫宁 | Dice fixed to 3→2→1 cycle (overrides roll) |
  | 波动步伐 | 琳奈 | 60% double steps, 20% skip (0 steps), 20% normal. Skip uses `modify_final_steps` to bypass siglica `max(1,…)`. |
  | 中点传送 | 爱弥斯 | Once per game: after crossing progress 16, teleport to top of nearest non-boss dango ahead (if any) |
  | 稳定投掷 | 守岸人 | Dice only 2 or 3 (via `dice_range: (2,3)`) |
  | 双倍冲刺 | 珂莱塔 | 28% chance double steps |

- **`utils/`** — `GameLogger` prints round-by-round output for single mode; `StatsLogger` prints aggregate statistics for multi mode.

### Key design details

- **Two-mode system:** 上半场 (`single`/`multi`) starts a fresh race. 下半场 (`single -s` / `multi -s`) continues from a first-half snapshot JSON. Any group can be used in either mode. Same-group second half restores dango positions/stacks/skill-states from snapshot; cross-group second half starts current group fresh at cell 0. Boss is shared across halves; in second half it always resets and re-enters at relative round 3. Goal: `board_length` (上半场), `board_length * 2` (下半场).
- **Boss movement is reverse:** Boss moves from finish toward start. `advance_backward(steps)` sets `progress += steps` but `cell = (-progress) % length`. When the boss carries normal dangos backward, they use `advance(-steps)` (negative progress delta).
- **Boss stack position:** Boss is always at the bottom of its cell's stack (`add_to_stack_bottom`). Rift shuffling preserves this.
- **Boss teleport:** After all 6 normal dangos have met the boss (tracked in `boss_met_dangos`), the boss teleports to cell 0 and the set clears.
- **Device triggers happen after move:** `_check_device_trigger` runs after the dango lands, may apply additional displacement (boost/trap) or stack shuffle (rift). The `final_cell` in the move log reflects post-device position.
- **Winner detection:** A normal dango wins when `progress >= goal` AND it is at the top of its stack (not buried under another normal dango). Goal is `board_length` for first half, `board_length * 2` for second half.
- **Siglica marking:** Happens during `_roll_all_dice`, specifically after siglica's own roll. Marked dangos get -1 step (min 1) during `_execute_single_move`. Marks clear each round at `_on_round_start`. Does NOT fire in round 1.
- **Feixue meet-boss check:** Uses `dango_cell >= boss_cell` (not just equality), so meeting is triggered once feixue's cell catches up to or passes the boss.
- **Group system:** `config/default_config.py` defines groups via `DANGO_GROUPS` dict (currently "A" and "B"). Each dango in `DANGOS_CONFIG` has a `group` field. Adding a new group requires: (1) define `DANGO_IDS_X` list, (2) add to `DANGO_GROUPS`, (3) add dango entries to `DANGOS_CONFIG` with `group="X"`, (4) add skill configs to `SKILL_CONFIG`, (5) create skill files and register in `skills/__init__.py`. `GameEngine._initialize_dangos(game_state, group)` filters by `group` field; boss (`group="boss"`) is always included.
