"""Simulator for running single and multi simulations."""

import random
import time
from core.game_engine import GameEngine
from utils.logger import GameLogger, StatsLogger


class Simulator:
    """Handles running single or multiple game simulations."""

    def __init__(self, config: dict = None):
        self.config = config or {}
        self.engine = GameEngine(self.config)
        self.verbose = self.config.get("verbose", True)
        self.random_seed = self.config.get("random_seed", None)
        self.game_logger = GameLogger(self.verbose)
        self.stats_logger = StatsLogger()

    def run_single_simulation(self, initial_order: list[str] | None = None, verbose: bool | None = None) -> dict:
        if verbose is None:
            verbose = self.verbose

        rng = random.Random(self.random_seed)

        game_state = self.engine.create_game_state(rng, initial_order)

        if verbose:
            self.game_logger.log_game_start(game_state)

        while game_state.winner is None and game_state.round_no < 1000:
            round_log = self.engine.run_round(game_state)

            if verbose:
                self.game_logger.log_round(game_state, round_log)

            if game_state.winner:
                break

        winner = self.engine.get_winner(game_state)
        if winner:
            winner_name = game_state.get_dango(winner).name if game_state.get_dango(winner) else winner
        else:
            winner_name = None

        result = {
            "winner": winner,
            "winner_name": winner_name,
            "total_rounds": game_state.round_no,
            "winner_found_round": game_state.winner_found_round,
            "final_rankings": self.engine._calculate_rankings(game_state),
            "final_stacks": game_state.stack_manager.get_all_stacks_snapshot(),
            "logs": game_state.logs,
        }

        if verbose:
            self.game_logger.log_game_end(game_state, result)

        return result

    def run_multi_simulation(self, num_simulations: int, verbose: bool = False) -> dict:
        start_time = time.time()

        wins = {}
        total_rounds_list = []

        base_seed = self.random_seed
        if base_seed is None:
            import os
            base_seed = int.from_bytes(os.urandom(4), 'big')

        for i in range(num_simulations):
            self.stats_logger.log_progress(i + 1, num_simulations)

            sim_rng = random.Random(base_seed + i)

            game_state = self.engine.create_game_state(sim_rng)

            while game_state.winner is None and game_state.round_no < 1000:
                self.engine.run_round(game_state)
                if game_state.winner:
                    break

            winner = self.engine.get_winner(game_state)
            if winner:
                wins[winner] = wins.get(winner, 0) + 1

            total_rounds_list.append(game_state.round_no)

        end_time = time.time()
        elapsed = end_time - start_time

        results = {
            "num_simulations": num_simulations,
            "wins": wins,
            "win_rates": {},
            "avg_rounds": sum(total_rounds_list) / len(total_rounds_list) if total_rounds_list else 0,
            "min_rounds": min(total_rounds_list) if total_rounds_list else 0,
            "max_rounds": max(total_rounds_list) if total_rounds_list else 0,
            "elapsed_time": elapsed,
            "rounds_list": total_rounds_list,
        }

        for dango_id, win_count in wins.items():
            results["win_rates"][dango_id] = win_count / num_simulations

        return results

    def run_prediction(self, snapshot: dict, verbose: bool = True, dango_group: str = "B") -> dict:
        seed = snapshot.get("seed", self.random_seed)
        rng = random.Random(seed)

        game_state = self.engine.create_game_state_from_snapshot(snapshot, rng, dango_group)

        if verbose:
            self.game_logger.log_game_start(game_state)
            print(f"下半场预测模式 (测试版)")
            print(f"上半场结束于第 {game_state.round_no} 回合，下半场将从第 {game_state.round_no + 1} 回合开始\n")

        while game_state.winner is None and game_state.round_no < 1000:
            round_log = self.engine.run_round(game_state)

            if verbose:
                self.game_logger.log_round(game_state, round_log)

            if game_state.winner:
                break

        winner = self.engine.get_winner(game_state)
        if winner:
            winner_name = game_state.get_dango(winner).name if game_state.get_dango(winner) else winner
        else:
            winner_name = None

        result = {
            "winner": winner,
            "winner_name": winner_name,
            "total_rounds": game_state.round_no,
            "winner_found_round": game_state.winner_found_round,
            "final_rankings": self.engine._calculate_rankings(game_state),
            "final_stacks": game_state.stack_manager.get_all_stacks_snapshot(),
            "logs": game_state.logs,
            "prediction_mode": True,
        }

        if verbose:
            self.game_logger.log_game_end(game_state, result)

        return result

    def run_prediction_multi(self, snapshot: dict, num_simulations: int, dango_group: str = "B") -> dict:
        start_time = time.time()

        wins = {}
        total_rounds_list = []

        base_seed = snapshot.get("seed", self.random_seed)
        if base_seed is None:
            import os
            base_seed = int.from_bytes(os.urandom(4), 'big')

        for i in range(num_simulations):
            self.stats_logger.log_progress(i + 1, num_simulations)

            sim_rng = random.Random(base_seed + i)

            game_state = self.engine.create_game_state_from_snapshot(snapshot, sim_rng, dango_group)

            while game_state.winner is None and game_state.round_no < 1000:
                self.engine.run_round(game_state)
                if game_state.winner:
                    break

            winner = self.engine.get_winner(game_state)
            if winner:
                wins[winner] = wins.get(winner, 0) + 1

            total_rounds_list.append(game_state.round_no)

        end_time = time.time()
        elapsed = end_time - start_time

        results = {
            "num_simulations": num_simulations,
            "wins": wins,
            "win_rates": {},
            "avg_rounds": sum(total_rounds_list) / len(total_rounds_list) if total_rounds_list else 0,
            "min_rounds": min(total_rounds_list) if total_rounds_list else 0,
            "max_rounds": max(total_rounds_list) if total_rounds_list else 0,
            "elapsed_time": elapsed,
            "rounds_list": total_rounds_list,
            "prediction_mode": True,
        }

        for dango_id, win_count in wins.items():
            results["win_rates"][dango_id] = win_count / num_simulations

        return results
