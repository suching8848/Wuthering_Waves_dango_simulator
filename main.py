"""Main entry point for Dango Racing Simulator."""

import argparse
import json
import sys
from config import DANGOS_CONFIG, SKILL_CONFIG, SIMULATION_CONFIG, DANGO_IDS_A, DANGO_IDS_B
from core.simulator import Simulator


def create_config(args) -> dict:
    group = getattr(args, "group", "A")
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


def run_single_mode(args, config: dict) -> None:
    group = config.get("dango_group", "A")
    print(f"运行上半场单次模拟... (使用{group}组团子)")
    print(f"随机种子: {args.seed if args.seed else '无'}")

    simulator = Simulator(config)

    initial_order = None
    if args.fixed_order:
        if group == "B":
            initial_order = list(DANGO_IDS_B)
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
    print(f"运行上半场多次模拟... (使用{group}组团子)")
    print(f"模拟次数: {args.num_simulations}")
    print(f"随机种子: {args.seed if args.seed else '无 (随机)'}")

    config["verbose"] = False
    simulator = Simulator(config)

    results = simulator.run_multi_simulation(args.num_simulations)

    simulator.stats_logger.log_stats(results)


def run_second_mode(args, config: dict) -> None:
    group = config.get("dango_group", "B")

    with open(args.state, "r", encoding="utf-8") as f:
        snapshot = json.load(f)

    if args.seed is not None:
        snapshot["seed"] = args.seed

    config["verbose"] = args.verbose
    simulator = Simulator(config)

    if args.multi and args.multi > 1:
        print(f"运行下半场多次模拟... (使用{group}组团子)")
        print(f"模拟次数: {args.multi}")
        print(f"随机种子: {snapshot.get('seed', '无 (随机)')}")
        print(f"起始回合: 第 {snapshot.get('round', 0)} 回合\n")

        results = simulator.run_prediction_multi(snapshot, args.multi, dango_group=group)

        print("\n" + "=" * 60)
        print(f"下半场多次模拟统计结果 ({group}组)")
        print("=" * 60)
        simulator.stats_logger.log_stats(results)
    else:
        print(f"运行下半场单次模拟... (使用{group}组团子)")
        print(f"随机种子: {snapshot.get('seed', '无 (随机)')}")

        result = simulator.run_prediction(snapshot, verbose=args.verbose, dango_group=group)

        print("\n" + "=" * 60)
        print(f"下半场单次模拟完成 ({group}组)")
        print(f"获胜者: {result['winner_name']}")
        print(f"获胜回合: 第 {result['winner_found_round']} 回合")


def add_second_subparser(subparsers, name: str, **kwargs) -> None:
    p = subparsers.add_parser(name, **kwargs)
    p.add_argument("-s", "--state", type=str, required=True, help="上半场结束状态的JSON文件路径")
    p.add_argument("--seed", type=int, default=None, help="随机种子（覆盖JSON中的种子）")
    p.add_argument("-n", "--multi", type=int, default=0, help="多次模拟次数（默认1次）")
    p.add_argument("-v", "--verbose", action="store_true", default=True, help="显示详细回合日志")
    p.add_argument("--group", type=str, choices=["A", "B"], default="B", help="选择团子组别 (A组续跑/B组新跑)，默认B组")


def main():
    parser = argparse.ArgumentParser(description="团子竞速模拟器 — 上半场/下半场竞速模拟")

    subparsers = parser.add_subparsers(dest="mode", help="运行模式")

    single_parser = subparsers.add_parser("single", help="上半场单次模拟")
    single_parser.add_argument("--seed", type=int, default=None, help="随机种子")
    single_parser.add_argument("--fixed-order", action="store_true", help="使用固定初始堆叠顺序")
    single_parser.add_argument("--group", type=str, choices=["A", "B"], default="A", help="选择团子组别 (A组/B组)，默认A组")

    multi_parser = subparsers.add_parser("multi", help="上半场多次模拟")
    multi_parser.add_argument("-n", "--num-simulations", type=int, default=1000, help="模拟次数")
    multi_parser.add_argument("--seed", type=int, default=None, help="随机种子")
    multi_parser.add_argument("--group", type=str, choices=["A", "B"], default="A", help="选择团子组别 (A组/B组)，默认A组")

    add_second_subparser(subparsers, "second", help="下半场模拟（从上半场快照继续）")
    add_second_subparser(subparsers, "predict", help="下半场模拟（second 的别名，向后兼容）")

    args = parser.parse_args()

    if args.mode is None:
        parser.print_help()
        return

    config = create_config(args)

    if args.mode == "single":
        run_single_mode(args, config)
    elif args.mode == "multi":
        run_multi_mode(args, config)
    elif args.mode in ("second", "predict"):
        run_second_mode(args, config)


if __name__ == "__main__":
    main()
