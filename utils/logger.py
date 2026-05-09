"""Logger utilities for game output."""

from typing import Any


class GameLogger:
    """Logger for detailed single simulation output."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def log_game_start(self, game_state) -> None:
        if not self.verbose:
            return
        print("=" * 60)
        print("团子竞速模拟器 - 单次模拟模式")
        print("=" * 60)
        print(f"地图长度: {game_state.board.length}")
        print(f"推进装置: {sorted(game_state.board.boost_cells)}")
        print(f"阻遏装置: {sorted(game_state.board.trap_cells)}")
        print(f"时空裂隙: {sorted(game_state.board.rift_cells)}")
        print()

    def log_round(self, game_state, round_log: dict) -> None:
        if not self.verbose:
            return

        print(f"\n第 {round_log['round']} 回合")
        print("-" * 40)

        print("行动顺序: " + " -> ".join(game_state.current_order))
        print()

        print("投骰结果:")
        for dango_id, dice in game_state.dice_results.items():
            dango = game_state.get_dango(dango_id)
            name = dango.name if dango else dango_id
            print(f"  {name} = {dice}")
        print()

        siglica_marks = [log for log in game_state.logs if log.get("type") == "siglica_mark" and log.get("round") == game_state.round_no]
        if siglica_marks:
            for mark_log in siglica_marks:
                marked_names = []
                for d_id in mark_log.get("marked", []):
                    d = game_state.get_dango(d_id)
                    marked_names.append(d.name if d else d_id)
                print(f"西格莉卡标记: {', '.join(marked_names)}")
            print()

        for action in round_log.get("actions", []):
            self._log_action(action, game_state)

        print("\n当前排名:")
        for rank in round_log.get("rankings", []):
            dango = game_state.get_dango(rank["id"])
            name = dango.name if dango else rank["id"]
            print(f"  {rank['rank']}. {name} (进度: {rank['progress']}, 格子: {rank['cell']})")

        print()

    def _log_action(self, action: dict, game_state) -> None:
        print(f"[{action['dango_name']} 行动]")
        print(f"  原位置: cell {action.get('original_cell', '?')}")
        print(f"  骰子: {action['dice']}")

        if action.get("marked_penalty"):
            print(f"  西格莉卡标记: -1")

        print(f"  最终移动: {action['final_steps']}")

        moved_group = action.get("moved_group", [])
        if moved_group:
            group_names = []
            for d_id in moved_group:
                d = game_state.get_dango(d_id)
                group_names.append(d.name if d else d_id)
            print(f"  移动组: {', '.join(group_names)}")

        target = action.get("target_cell_before_device", action.get("final_cell", "?"))
        print(f"  目标位置: cell {target}")

        device_trigger = action.get("device_trigger")
        if device_trigger:
            device = device_trigger.get("device")
            cell = device_trigger.get("cell")
            print(f"  触发装置: {device} (cell {cell})")

            if device == "boost":
                print(f"    推进: +{device_trigger.get('boost_steps', 1)} 格")
            elif device == "trap":
                print(f"    阻遏: {device_trigger.get('trap_steps', -1)} 格")
            elif device == "rift":
                print(f"    时空裂隙: 堆叠重排")

        print(f"  最终位置: cell {action.get('final_cell', '?')}")

        meet_boss_logs = [log for log in game_state.logs if log.get("type") == "meet_boss" and log.get("round") == game_state.round_no and log.get("dango_id") == action["dango_id"]]
        if meet_boss_logs:
            print(f"  与布大王相遇!")

        print()

    def log_game_end(self, game_state, result: dict) -> None:
        if not self.verbose:
            return

        print("=" * 60)
        print("比赛结束")
        print("=" * 60)

        if result["winner"]:
            winner_name = result.get("winner_name", result["winner"])
            print(f"获胜者: {winner_name}")
            print(f"获胜回合: 第 {result['winner_found_round']} 回合")
        else:
            print("无获胜者")

        print(f"\n最终排名:")
        for rank in result.get("final_rankings", []):
            marker = " (获胜者)" if rank["id"] == result["winner"] else ""
            print(f"  {rank['rank']}. {rank['name']} (进度: {rank['progress']}, 格子: {rank['cell']}){marker}")

        print(f"\n最终堆叠:")
        final_stacks = result.get("final_stacks", {})
        for cell in sorted(final_stacks):
            stack = final_stacks[cell]
            if not stack:
                continue
            stack_names = []
            for d_id in stack:
                d = game_state.get_dango(d_id)
                stack_names.append(d.name if d else d_id)
            print(f"  cell {cell}: {' -> '.join(stack_names)}")


class StatsLogger:
    """Logger for multi-simulation statistics output."""

    def log_stats(self, results: dict) -> None:
        print("\n" + "=" * 60)
        print("多次模拟模式统计结果")
        print("=" * 60)

        print(f"\n模拟次数: {results['num_simulations']}")
        print(f"总耗时: {results['elapsed_time']:.2f} 秒")
        print(f"平均回合数: {results['avg_rounds']:.2f}")
        print(f"最小回合数: {results['min_rounds']}")
        print(f"最大回合数: {results['max_rounds']}")

        print(f"\n获胜统计:")
        for dango_id, win_count in sorted(results["wins"].items(), key=lambda x: x[1], reverse=True):
            win_rate = results["win_rates"][dango_id]
            print(f"  {dango_id}: {win_count} 次 ({win_rate * 100:.2f}%)")

        print()

    def log_progress(self, current: int, total: int) -> None:
        if current % 100 == 0:
            print(f"进度: {current}/{total} ({current / total * 100:.1f}%)")