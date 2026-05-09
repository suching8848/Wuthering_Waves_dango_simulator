"""Main entry point for Dango Racing Simulator."""

import argparse
import sys
from config import DANGOS_CONFIG, SKILL_CONFIG, SIMULATION_CONFIG
from core.simulator import Simulator


def create_config(args) -> dict:
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
    }
    return config


def run_single_mode(args, config: dict) -> None:
    print("运行单次拟合模式...")
    print(f"随机种子: {args.seed if args.seed else '无'}")

    simulator = Simulator(config)

    initial_order = None
    if args.fixed_order:
        initial_order = ["daniya", "phoebe", "siglica", "feixue", "luhesi", "katixiya"]
        print(f"使用固定初始顺序: {initial_order}")

    result = simulator.run_single_simulation(initial_order=initial_order, verbose=True)

    print("\n" + "=" * 60)
    print("单次模拟完成")
    print(f"获胜者: {result['winner_name']}")
    print(f"总回合数: {result['total_rounds']}")


def run_multi_mode(args, config: dict) -> None:
    print("运行多次模拟模式...")
    print(f"模拟次数: {args.num_simulations}")
    print(f"随机种子: {args.seed if args.seed else '无 (随机)'}")

    config["verbose"] = False
    simulator = Simulator(config)

    results = simulator.run_multi_simulation(args.num_simulations)

    simulator.stats_logger.log_stats(results)


def main():
    parser = argparse.ArgumentParser(description="团子竞速模拟器")

    subparsers = parser.add_subparsers(dest="mode", help="运行模式")

    single_parser = subparsers.add_parser("single", help="单次模拟模式")
    single_parser.add_argument("--seed", type=int, default=None, help="随机种子")
    single_parser.add_argument("--fixed-order", action="store_true", help="使用固定初始堆叠顺序")

    multi_parser = subparsers.add_parser("multi", help="多次模拟模式")
    multi_parser.add_argument("-n", "--num-simulations", type=int, default=1000, help="模拟次数")
    multi_parser.add_argument("--seed", type=int, default=None, help="随机种子")

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