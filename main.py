"""Main entry point for Dango Racing Simulator."""

import argparse
import json
import sys
from config import DANGOS_CONFIG, SKILL_CONFIG, SIMULATION_CONFIG, DANGO_IDS_A, DANGO_IDS_B, DANGO_IDS_C
from core.simulator import Simulator


def create_config(args) -> dict:
    group = getattr(args, "group", None)
    if group is None:
        group = "B" if getattr(args, "state", None) else "A"
    config = {
        "board_length": 32,
        "boost_cells": {3, 11, 16, 23},
        "trap_cells": {10, 28},
        "rift_cells": {6, 20},
        "dangos": DANGOS_CONFIG,
        "skill_config": SKILL_CONFIG,
        "verbose": True,
        "random_seed": args.seed,
        "boss_carries_upper_stack": SIMULATION_CONFIG.get("boss_carries_upper_stack", False),
        "boss_start_round": 3,
        "dango_group": group,
    }
    return config


def _get_group(args) -> str:
    group = getattr(args, "group", None)
    if group is not None:
        return group
    return "B" if getattr(args, "state", None) else "A"


def run_single_mode(args, config: dict) -> None:
    group = config.get("dango_group", "A")

    if args.state:
        with open(args.state, "r", encoding="utf-8") as f:
            snapshot = json.load(f)
        if args.seed is not None:
            snapshot["seed"] = args.seed

        print(f"运行下半场单次模拟... (使用{group}组团子)")
        print(f"随机种子: {snapshot.get('seed', '无 (随机)')}")

        simulator = Simulator(config)
        result = simulator.run_prediction(snapshot, verbose=True, dango_group=group)

        print("\n" + "=" * 60)
        print(f"下半场单次模拟完成 ({group}组)")
        print(f"获胜者: {result['winner_name']}")
        print(f"获胜回合: 第 {result['winner_found_round']} 回合")
    else:
        print(f"运行上半场单次模拟... (使用{group}组团子)")
        print(f"随机种子: {args.seed if args.seed else '无'}")

        simulator = Simulator(config)

        initial_order = None
        if args.fixed_order:
            if group == "B":
                initial_order = list(DANGO_IDS_B)
            elif group == "C":
                initial_order = list(DANGO_IDS_C)
            else:
                initial_order = list(DANGO_IDS_A)
            print(f"使用固定初始顺序: {initial_order}")

        result = simulator.run_single_simulation(initial_order=initial_order, verbose=True)

        print("\n" + "=" * 60)
        print("上半场单次模拟完成")
        print(f"获胜者: {result['winner_name']}")
        print(f"总回合数: {result['total_rounds']}")


def run_multi_mode(args, config: dict) -> None:
    group = config.get("dango_group", "A")

    if args.state:
        with open(args.state, "r", encoding="utf-8") as f:
            snapshot = json.load(f)
        if args.seed is not None:
            snapshot["seed"] = args.seed

        num = args.num_simulations if args.num_simulations > 1 else 100
        print(f"运行下半场多次模拟... (使用{group}组团子)")
        print(f"模拟次数: {num}")
        print(f"随机种子: {snapshot.get('seed', '无 (随机)')}")
        print(f"起始回合: 第 {snapshot.get('round', 0)} 回合\n")

        config["verbose"] = False
        simulator = Simulator(config)
        results = simulator.run_prediction_multi(snapshot, num, dango_group=group)

        print("\n" + "=" * 60)
        print(f"下半场多次模拟统计结果 ({group}组)")
        print("=" * 60)
        simulator.stats_logger.log_stats(results)
    else:
        print(f"运行上半场多次模拟... (使用{group}组团子)")
        print(f"模拟次数: {args.num_simulations}")
        print(f"随机种子: {args.seed if args.seed else '无 (随机)'}")

        config["verbose"] = False
        simulator = Simulator(config)
        results = simulator.run_multi_simulation(args.num_simulations)

        simulator.stats_logger.log_stats(results)


def main():
    parser = argparse.ArgumentParser(description="团子竞速模拟器 — 上半场/下半场竞速模拟")
    subparsers = parser.add_subparsers(dest="mode", help="运行模式")

    single_parser = subparsers.add_parser("single", help="单次模拟（-s 指定快照则运行下半场）")
    single_parser.add_argument("-s", "--state", type=str, default=None, help="上半场结束状态的JSON文件路径（可选，指定后运行下半场）")
    single_parser.add_argument("--seed", type=int, default=None, help="随机种子")
    single_parser.add_argument("--fixed-order", action="store_true", help="使用固定初始堆叠顺序")
    single_parser.add_argument("--group", type=str, choices=["A", "B", "C"], default=None, help="选择团子组别 (A组/B组/C组)，上半场默认A，下半场默认B")

    multi_parser = subparsers.add_parser("multi", help="多次模拟（-s 指定快照则运行下半场）")
    multi_parser.add_argument("-n", "--num-simulations", type=int, default=1000, help="模拟次数")
    multi_parser.add_argument("-s", "--state", type=str, default=None, help="上半场结束状态的JSON文件路径（可选，指定后运行下半场）")
    multi_parser.add_argument("--seed", type=int, default=None, help="随机种子")
    multi_parser.add_argument("--group", type=str, choices=["A", "B", "C"], default=None, help="选择团子组别 (A组/B组/C组)，上半场默认A，下半场默认B")

    args = parser.parse_args()

    if args.mode is None:
        parser.print_help()
        return

    config = create_config(args)

    if args.mode == "single":
        run_single_mode(args, config)
    elif args.mode == "multi":
        run_multi_mode(args, config)


if __name__ == "__main__":
    main()
