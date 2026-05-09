"""Game Engine - Core game logic for Dango Racing Simulator."""

import random
from typing import Any, Optional
from models.dango import Dango
from models.board import Board, DEVICE_BOOST, DEVICE_TRAP, DEVICE_RIFT
from models.game_state import GameState
from core.stack_manager import StackManager
from skills import SKILL_MAPPING


class GameEngine:
    """Main game engine handling game flow and rules."""

    def __init__(self, config: dict = None):
        self.config = config or {}
        self.board = Board(
            length=self.config.get("board_length", 32),
            boost_cells=self.config.get("boost_cells", {3, 11, 16, 23}),
            trap_cells=self.config.get("trap_cells", {10, 28}),
            rift_cells=self.config.get("rift_cells", {6, 20}),
        )
        self.skill_config = self.config.get("skill_config", {})
        self.boss_carries_upper_stack = self.config.get("boss_carries_upper_stack", False)
        self.boss_start_round = self.config.get("boss_start_round", 3)
        self.dango_configs = self.config.get("dangos", {})

    def create_game_state(self, rng: random.Random, initial_order: list[str] = None) -> GameState:
        game_state = GameState()
        game_state.board = self.board
        game_state.round_no = 0
        game_state.boss_start_round = self.boss_start_round
        game_state.stack_manager = StackManager(self.board.length)
        game_state.rng = rng
        game_state.marked_by_siglica = set()
        game_state.winner = None
        game_state.logs = []

        self._initialize_dangos(game_state)
        self._initialize_stack(game_state, rng, initial_order)
        self._initialize_skills(game_state)

        return game_state

    def _initialize_dangos(self, game_state: GameState) -> None:
        for dango_id, dango_config in self.dango_configs.items():
            dango = Dango(
                id=dango_id,
                name=dango_config.get("name", dango_id),
                is_boss=dango_config.get("is_boss", False),
                dice_range=dango_config.get("dice_range", (1, 3)),
            )
            game_state.dangos[dango_id] = dango

    def _initialize_stack(self, game_state: GameState, rng: random.Random, initial_order: list[str] = None) -> None:
        normal_dango_ids = [d.id for d in game_state.get_normal_dangos()]

        if initial_order is None:
            rng.shuffle(normal_dango_ids)

        game_state.stack_manager.initialize_stack(normal_dango_ids, cell=0)

    def _initialize_skills(self, game_state: GameState) -> None:
        for dango_id, dango in game_state.dangos.items():
            skill_class = SKILL_MAPPING.get(dango_id)
            if skill_class:
                skill_config = self.skill_config.get(dango_id, {})
                dango.skill = skill_class(dango_id, skill_config)
                dango.state = {}
            else:
                dango.skill = None

    def run_round(self, game_state: GameState) -> dict:
        game_state.round_no += 1
        round_log = {"round": game_state.round_no, "actions": []}

        self._on_round_start(game_state)
        self._determine_action_order(game_state)
        self._roll_all_dice(game_state)
        self._siglica_mark_targets(game_state)
        self._execute_all_moves(game_state, round_log)
        self._on_round_end(game_state)

        round_log["stacks"] = game_state.stack_manager.get_all_stacks_snapshot()
        round_log["rankings"] = self._calculate_rankings(game_state)

        return round_log

    def _on_round_start(self, game_state: GameState) -> None:
        game_state.marked_by_siglica = set()
        for dango in game_state.dangos.values():
            if dango.skill:
                dango.skill.on_round_start(game_state)

    def _determine_action_order(self, game_state: GameState) -> None:
        active_ids = game_state.get_active_dango_ids()
        game_state.rng.shuffle(active_ids)
        game_state.current_order = active_ids

    def _roll_all_dice(self, game_state: GameState) -> None:
        game_state.dice_results = {}
        for dango_id in game_state.current_order:
            dango = game_state.get_dango(dango_id)
            if dango:
                dice = game_state.rng.randint(dango.dice_range[0], dango.dice_range[1])
                game_state.dice_results[dango_id] = dice

                if dango.skill:
                    dango.skill.on_after_roll(game_state, dice)

    def _siglica_mark_targets(self, game_state: GameState) -> None:
        siglica = game_state.get_dango("siglica")
        if siglica and siglica.skill:
            marked = siglica.skill.mark_targets(game_state)
            if marked:
                game_state.logs.append({
                    "type": "siglica_mark",
                    "marked": marked,
                    "round": game_state.round_no
                })

    def _execute_all_moves(self, game_state: GameState, round_log: dict) -> None:
        for dango_id in game_state.current_order:
            dango = game_state.get_dango(dango_id)
            if dango is None:
                continue

            dice = game_state.dice_results.get(dango_id, 0)
            move_log = self._execute_single_move(game_state, dango, dice)
            round_log["actions"].append(move_log)

            if self._check_winner(game_state):
                return

    def _execute_single_move(self, game_state: GameState, dango: Dango, dice: int) -> dict:
        move_log = {
            "dango_id": dango.id,
            "dango_name": dango.name,
            "dice": dice,
            "is_boss": dango.is_boss,
        }

        original_cell = game_state.stack_manager.get_dango_cell(dango.id)
        move_log["original_cell"] = original_cell

        base_steps = dice
        if dango.skill:
            base_steps = dango.skill.modify_move_steps(game_state, base_steps)

        if dango.id in game_state.marked_by_siglica and not dango.is_boss:
            penalty = 1
            base_steps = max(1, base_steps - penalty)
            move_log["marked_penalty"] = True

        move_log["final_steps"] = base_steps

        if dango.is_boss:
            self._move_boss(game_state, dango, base_steps, move_log)
        else:
            self._move_normal_dango(game_state, dango, base_steps, move_log)

        if dango.skill:
            dango.skill.on_after_move(game_state)

        self._check_meet_boss(game_state, dango)
        self._check_device_trigger(game_state, dango, move_log)

        return move_log

    def _move_normal_dango(self, game_state: GameState, dango: Dango, steps: int, move_log: dict) -> None:
        stack_manager = game_state.stack_manager

        if dango.is_boss:
            new_cell = (dango.cell - steps) % game_state.board.length
        else:
            new_cell = (dango.cell + steps) % game_state.board.length

        move_log["target_cell_before_device"] = new_cell

        moved_group = stack_manager.move_group(dango.id, new_cell)
        move_log["moved_group"] = moved_group

        dango.advance(steps, game_state.board.length)

        move_log["final_cell"] = dango.cell
        move_log["final_progress"] = dango.progress

    def _move_boss(self, game_state: GameState, boss: Dango, steps: int, move_log: dict) -> None:
        stack_manager = game_state.stack_manager
        old_cell = boss.cell

        new_cell = (boss.cell - steps) % game_state.board.length
        move_log["target_cell_before_device"] = new_cell

        stack_manager.remove_from_stack(boss.id)
        stack_manager.add_to_stack_bottom(boss.id, new_cell)

        boss.advance_backward(steps, game_state.board.length)

        move_log["final_cell"] = boss.cell
        move_log["final_progress"] = boss.progress

    def _check_meet_boss(self, game_state: GameState, dango: Dango) -> None:
        if dango.is_boss:
            return

        boss = game_state.get_boss()
        if boss is None:
            return

        if dango.cell == boss.cell and dango.skill:
            dango.skill.on_meet_boss(game_state)
            game_state.logs.append({
                "type": "meet_boss",
                "dango_id": dango.id,
                "cell": dango.cell,
                "round": game_state.round_no
            })

    def _check_device_trigger(self, game_state: GameState, dango: Dango, move_log: dict) -> None:
        device = game_state.board.get_device_at_cell(dango.cell)
        if device is None:
            return

        device_log = {"device": device, "cell": dango.cell, "triggered": True}

        if dango.skill:
            skill_result = dango.skill.on_device_trigger(game_state, device)
            if skill_result:
                device_log["skill_effect"] = skill_result

        if device == DEVICE_BOOST:
            if "skill_effect" in device_log:
                extra = device_log["skill_effect"].get("extra_steps", 3)
            else:
                extra = 1
            dango.advance(extra, game_state.board.length)
            device_log["boost_steps"] = extra
            game_state.stack_manager.add_to_stack_top(dango.id, dango.cell)

        elif device == DEVICE_TRAP:
            if "skill_effect" in device_log:
                extra = device_log["skill_effect"].get("extra_steps", 1)
            else:
                extra = 1
            dango.advance_backward(extra, game_state.board.length)
            device_log["trap_steps"] = -extra
            game_state.stack_manager.remove_from_stack(dango.id)
            game_state.stack_manager.add_to_stack_top(dango.id, dango.cell)

        elif device == DEVICE_RIFT:
            boss = game_state.get_boss()
            boss_id = boss.id if boss else "budaiwang"
            game_state.stack_manager.shuffle_cell(dango.cell, game_state.rng, boss_id)
            device_log["shuffled"] = True

        move_log["device_trigger"] = device_log

    def _on_round_end(self, game_state: GameState) -> None:
        for dango in game_state.dangos.values():
            if dango.skill:
                dango.skill.on_round_end(game_state)

        boss = game_state.get_boss()
        if boss and game_state.is_boss_active():
            if boss.skill:
                boss.skill.on_round_end(game_state)

    def _check_winner(self, game_state: GameState) -> bool:
        for dango in game_state.get_normal_dangos():
            if dango.has_reached_goal(self.board.length):
                stack = game_state.stack_manager.get_stack(dango.cell)
                if stack:
                    top_dango_id = stack[-1]
                    top_dango = game_state.get_dango(top_dango_id)
                    if top_dango and not top_dango.is_boss:
                        game_state.winner = top_dango_id
                        game_state.winner_found_round = game_state.round_no
                        return True
        return False

    def _calculate_rankings(self, game_state: GameState) -> list[dict]:
        normal_dangos = game_state.get_normal_dangos()
        rankings = []

        for dango in normal_dangos:
            cell = game_state.stack_manager.get_dango_cell(dango.id)
            stack = game_state.stack_manager.get_stack(cell) if cell is not None else []
            stack_position = len(stack) - stack.index(dango.id) if dango.id in stack else 0

            rankings.append({
                "id": dango.id,
                "name": dango.name,
                "progress": dango.progress,
                "cell": dango.cell,
                "stack_position": stack_position,
            })

        rankings.sort(key=lambda x: (x["progress"], x["stack_position"]), reverse=True)

        for i, rank in enumerate(rankings):
            rank["rank"] = i + 1

        return rankings

    def get_winner(self, game_state: GameState) -> Optional[str]:
        return game_state.winner