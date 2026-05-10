"""Game Engine - Core game logic for Dango Racing Simulator."""

import random
from typing import Optional
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
        self.dango_group = self.config.get("dango_group", "A")

    def create_game_state(self, rng: random.Random, initial_order: list[str] = None, dango_group: str = None) -> GameState:
        if dango_group is None:
            dango_group = self.dango_group

        game_state = GameState()
        game_state.board = self.board
        game_state.round_no = 0
        game_state.boss_start_round = self.boss_start_round
        game_state.stack_manager = StackManager(self.board.length)
        game_state.rng = rng
        game_state.marked_by_siglica = set()
        game_state.winner = None
        game_state.logs = []
        game_state.boss_spawned = False
        game_state.dango_group = dango_group

        self._initialize_dangos(game_state, dango_group)
        self._initialize_stack(game_state, rng, initial_order)
        self._initialize_skills(game_state)
        self._initialize_boss(game_state)

        return game_state

    def create_game_state_from_snapshot(self, snapshot: dict, rng: random.Random, dango_group: str = "B") -> GameState:
        game_state = GameState()
        game_state.board = self.board
        game_state.round_no = snapshot.get("round", 0)
        game_state.stack_manager = StackManager(self.board.length)
        game_state.rng = rng
        game_state.marked_by_siglica = set()
        game_state.winner = None
        game_state.logs = []
        game_state.first_half_winner = snapshot.get("first_half_winner")
        game_state.is_second_half = True
        game_state.dango_group = dango_group

        snapshot_round = snapshot.get("round", 0)
        game_state.boss_start_round = snapshot_round + 3
        game_state.boss_spawned = False

        self._initialize_dangos(game_state, dango_group)

        snapshot_dango_ids = set(snapshot.get("dangos", {}).keys())
        current_group_ids = set(d.id for d in game_state.get_normal_dangos())
        same_group = bool(snapshot_dango_ids & current_group_ids)

        if same_group:
            self._restore_from_snapshot(game_state, snapshot)
        else:
            group_ids = [d.id for d in game_state.get_normal_dangos()]
            rng.shuffle(group_ids)
            game_state.initial_stack_order = list(group_ids)
            game_state.stack_manager.initialize_stack(group_ids, cell=0)

        self._initialize_skills(game_state)

        if same_group:
            dangos_snapshot = snapshot.get("dangos", {})
            for dango_id, dango_data in dangos_snapshot.items():
                preserved_state = dango_data.get("state", {})
                if preserved_state:
                    dango = game_state.get_dango(dango_id)
                    if dango:
                        dango.state.update(preserved_state)

        return game_state

    def _restore_from_snapshot(self, game_state: GameState, snapshot: dict) -> None:
        dangos_snapshot = snapshot.get("dangos", {})
        for dango_id, dango_data in dangos_snapshot.items():
            dango = game_state.get_dango(dango_id)
            if dango is None:
                continue
            dango.progress = dango_data["progress"]
            dango.cell = dango_data["cell"]

        stacks_snapshot = snapshot.get("stacks", {})
        placed_ids = set()
        for cell_str, dango_ids in stacks_snapshot.items():
            cell = int(cell_str)
            for d_id in dango_ids:
                if d_id in game_state.dangos:
                    game_state.stack_manager.add_to_stack_top(d_id, cell)
                    placed_ids.add(d_id)

        for dango_id, dango_data in dangos_snapshot.items():
            if dango_id not in placed_ids and dango_id in game_state.dangos:
                game_state.stack_manager.add_to_stack_top(dango_id, dango_data["cell"])

        game_state.initial_stack_order = list(dangos_snapshot.keys())

    def _initialize_dangos(self, game_state: GameState, dango_group: str = None) -> None:
        if dango_group is None:
            dango_group = self.dango_group

        for dango_id, dango_config in self.dango_configs.items():
            group = dango_config.get("group")
            is_boss = dango_config.get("is_boss", False)
            if group != dango_group and not is_boss:
                continue
            dango = Dango(
                id=dango_id,
                name=dango_config.get("name", dango_id),
                is_boss=is_boss,
                dice_range=dango_config.get("dice_range", (1, 3)),
            )
            game_state.dangos[dango_id] = dango

    def _initialize_stack(self, game_state: GameState, rng: random.Random, initial_order: list[str] = None) -> None:
        normal_dango_ids = [d.id for d in game_state.get_normal_dangos()]

        if initial_order is None:
            rng.shuffle(normal_dango_ids)
            game_state.initial_stack_order = list(normal_dango_ids)
        else:
            normal_dango_ids = list(initial_order)
            game_state.initial_stack_order = list(normal_dango_ids)

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

    def _initialize_boss(self, game_state: GameState) -> None:
        boss = game_state.get_boss()
        if boss is None:
            return

        boss.progress = 0
        boss.cell = 0
        game_state.boss_spawned = False

    def run_round(self, game_state: GameState) -> dict:
        game_state.round_no += 1
        round_log = {"round": game_state.round_no, "actions": []}

        self._on_round_start(game_state)
        self._determine_action_order(game_state)
        self._roll_all_dice(game_state)
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
        if game_state.round_no == 1 and not game_state.is_second_half:
            game_state.current_order = list(reversed(game_state.initial_stack_order))
            return

        if game_state.is_second_half and game_state.round_no == game_state.boss_start_round - 2:
            game_state.current_order = list(reversed(game_state.initial_stack_order))
            return

        if game_state.round_no >= game_state.boss_start_round and not game_state.boss_spawned:
            boss = game_state.get_boss()
            if boss is not None:
                boss.progress = 0
                boss.cell = 0
                game_state.stack_manager.add_to_stack_bottom(boss.id, 0)
                game_state.boss_spawned = True

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

                if dango.id == "siglica" and dango.skill:
                    marked = dango.skill.mark_targets(game_state)
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

        if dango.skill:
            base_steps = dango.skill.modify_final_steps(game_state, base_steps)

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

    def _update_group_progress(self, game_state: GameState, moved_group: list[str], steps: int) -> None:
        for dango_id in moved_group:
            moved_dango = game_state.get_dango(dango_id)
            if moved_dango is None:
                continue
            moved_dango.advance(steps, game_state.board.length)

    def _relocate_stack_group(self, game_state: GameState, moving_group: list[str], new_cell: int, boss_at_bottom: bool = False) -> None:
        stack_manager = game_state.stack_manager
        for dango_id in moving_group:
            stack_manager.remove_from_stack(dango_id)

        if boss_at_bottom and moving_group:
            boss_id = moving_group[0]
            for dango_id in moving_group[1:]:
                stack_manager.add_to_stack_top(dango_id, new_cell)
            stack_manager.add_to_stack_bottom(boss_id, new_cell)
        else:
            for dango_id in moving_group:
                stack_manager.add_to_stack_top(dango_id, new_cell)

    def _apply_group_displacement(self, game_state: GameState, moved_group: list[str], steps: int, reverse: bool = False) -> None:
        for dango_id in moved_group:
            moved_dango = game_state.get_dango(dango_id)
            if moved_dango is None:
                continue
            if moved_dango.is_boss:
                if reverse:
                    moved_dango.advance_backward(steps, game_state.board.length)
                else:
                    moved_dango.advance_backward(-steps, game_state.board.length)
            elif reverse:
                moved_dango.advance(-steps, game_state.board.length)
            else:
                moved_dango.advance(steps, game_state.board.length)

    def _move_normal_dango(self, game_state: GameState, dango: Dango, steps: int, move_log: dict) -> None:
        stack_manager = game_state.stack_manager
        current_cell = stack_manager.get_dango_cell(dango.id)
        if current_cell is None:
            current_cell = dango.cell

        new_cell = (current_cell + steps) % game_state.board.length
        move_log["target_cell_before_device"] = new_cell

        if game_state.round_no == 1 and not game_state.is_second_half:
            stack_manager.remove_from_stack(dango.id)
            stack_manager.add_to_stack_top(dango.id, new_cell)
            moved_group = [dango.id]
        else:
            moved_group = stack_manager.move_group(dango.id, new_cell)
        move_log["moved_group"] = moved_group

        self._apply_group_displacement(game_state, moved_group, steps)

        move_log["final_cell"] = dango.cell
        move_log["final_progress"] = dango.progress

    def _move_boss(self, game_state: GameState, boss: Dango, steps: int, move_log: dict) -> None:
        stack_manager = game_state.stack_manager
        current_cell = stack_manager.get_dango_cell(boss.id)
        if current_cell is None:
            current_cell = boss.cell

        moving_group = [boss.id]
        if self.boss_carries_upper_stack:
            moving_group += stack_manager.get_upper_stack(boss.id)

        new_cell = (current_cell - steps) % game_state.board.length
        move_log["target_cell_before_device"] = new_cell
        move_log["moved_group"] = moving_group

        for dango_id in moving_group:
            stack_manager.remove_from_stack(dango_id)

        for dango_id in moving_group[1:]:
            stack_manager.add_to_stack_top(dango_id, new_cell)
        stack_manager.add_to_stack_bottom(boss.id, new_cell)

        boss.advance_backward(steps, game_state.board.length)
        for dango_id in moving_group[1:]:
            carried_dango = game_state.get_dango(dango_id)
            if carried_dango is None:
                continue
            carried_dango.advance(-steps, game_state.board.length)

        move_log["final_cell"] = boss.cell
        move_log["final_progress"] = boss.progress

    def _check_meet_boss(self, game_state: GameState, dango: Dango) -> None:
        if dango.is_boss:
            return

        boss = game_state.get_boss()
        if boss is None or not game_state.boss_spawned:
            return

        boss_cell = game_state.stack_manager.get_dango_cell(boss.id)
        dango_cell = game_state.stack_manager.get_dango_cell(dango.id)
        if dango_cell is None:
            dango_cell = dango.cell

        met_boss = dango_cell == boss_cell
        if not met_boss and dango.id == "feixue" and boss_cell is not None and dango_cell is not None:
            met_boss = dango_cell >= boss_cell

        if met_boss:
            game_state.boss_met_dangos.add(dango.id)
            if dango.skill:
                dango.skill.on_meet_boss(game_state)
                game_state.logs.append({
                    "type": "meet_boss",
                    "dango_id": dango.id,
                    "cell": dango_cell,
                    "round": game_state.round_no
                })

    def _move_device_group(self, game_state: GameState, bottom_dango_id: str, steps: int, reverse: bool = False, boss_at_bottom: bool = False) -> list[str]:
        if steps == 0:
            return []

        stack_manager = game_state.stack_manager
        current_cell = stack_manager.get_dango_cell(bottom_dango_id)
        if current_cell is None:
            return []

        stack = stack_manager.get_stack(current_cell)
        if bottom_dango_id not in stack:
            return []

        index = stack.index(bottom_dango_id)
        moving_group = stack[index:]
        if not moving_group:
            return []

        delta = -steps if reverse else steps
        new_cell = (current_cell + delta) % game_state.board.length
        self._relocate_stack_group(game_state, moving_group, new_cell, boss_at_bottom=boss_at_bottom)
        self._apply_group_displacement(game_state, moving_group, steps, reverse=reverse)
        return moving_group

    def _check_device_trigger(self, game_state: GameState, dango: Dango, move_log: dict) -> None:
        cell = game_state.stack_manager.get_dango_cell(dango.id)
        if cell is None:
            cell = dango.cell

        device = game_state.board.get_device_at_cell(cell)
        if device is None:
            return

        device_log = {"device": device, "cell": cell, "triggered": True}

        if dango.skill:
            skill_result = dango.skill.on_device_trigger(game_state, device)
            if skill_result:
                device_log["skill_effect"] = skill_result

        if device == DEVICE_BOOST:
            if "skill_effect" in device_log:
                extra = device_log["skill_effect"].get("extra_steps", 3)
            else:
                extra = 1
            moved_group = self._move_device_group(
                game_state,
                dango.id,
                extra,
                reverse=dango.is_boss,
                boss_at_bottom=dango.is_boss,
            )
            device_log["boost_steps"] = extra
            if moved_group:
                device_log["moved_group"] = moved_group

        elif device == DEVICE_TRAP:
            if "skill_effect" in device_log:
                extra = device_log["skill_effect"].get("extra_steps", 1)
            else:
                extra = 1
            moved_group = self._move_device_group(
                game_state,
                dango.id,
                extra,
                reverse=not dango.is_boss,
                boss_at_bottom=dango.is_boss,
            )
            device_log["trap_steps"] = -extra if not dango.is_boss else extra
            if moved_group:
                device_log["moved_group"] = moved_group

        elif device == DEVICE_RIFT:
            boss = game_state.get_boss()
            boss_id = boss.id if boss else "budaiwang"
            game_state.stack_manager.shuffle_cell(cell, game_state.rng, boss_id)
            device_log["shuffled"] = True

        move_log["final_cell"] = game_state.stack_manager.get_dango_cell(dango.id)
        move_log["final_progress"] = dango.progress
        move_log["device_trigger"] = device_log

    def _on_round_end(self, game_state: GameState) -> None:
        for dango in game_state.dangos.values():
            if dango.skill:
                dango.skill.on_round_end(game_state)

        self._check_boss_teleport(game_state)

    def _check_boss_teleport(self, game_state: GameState) -> None:
        boss = game_state.get_boss()
        if boss is None or not game_state.boss_spawned:
            return

        normal_count = len(game_state.get_normal_dangos())
        if len(game_state.boss_met_dangos) < normal_count:
            return

        boss_cell = game_state.stack_manager.get_dango_cell(boss.id)
        if boss_cell is None:
            boss_cell = boss.cell

        stack_manager = game_state.stack_manager
        moving_group = [boss.id] + stack_manager.get_upper_stack(boss.id)

        for dango_id in moving_group:
            stack_manager.remove_from_stack(dango_id)

        for dango_id in moving_group[1:]:
            stack_manager.add_to_stack_top(dango_id, 0)
        stack_manager.add_to_stack_bottom(boss.id, 0)

        boss.cell = 0
        game_state.boss_met_dangos.clear()

        game_state.logs.append({
            "type": "boss_teleport",
            "from_cell": boss_cell,
            "to_cell": 0,
            "round": game_state.round_no,
        })

    def _check_winner(self, game_state: GameState) -> bool:
        goal = self.board.length * 2 if game_state.is_second_half else self.board.length
        for dango in game_state.get_normal_dangos():
            if dango.has_reached_goal(goal):
                cell = game_state.stack_manager.get_dango_cell(dango.id)
                if cell is None:
                    cell = dango.cell
                stack = game_state.stack_manager.get_stack(cell)
                if stack:
                    top_dango_id = stack[-1]
                    top_dango = game_state.get_dango(top_dango_id)
                    if top_dango and not top_dango.is_boss and top_dango_id == dango.id:
                        game_state.winner = top_dango_id
                        game_state.winner_found_round = game_state.round_no
                        return True
        return False

    def _calculate_rankings(self, game_state: GameState) -> list[dict]:
        normal_dangos = game_state.get_normal_dangos()
        rankings = []

        for dango in normal_dangos:
            cell = game_state.stack_manager.get_dango_cell(dango.id)
            if cell is None:
                cell = dango.cell
            stack = game_state.stack_manager.get_stack(cell) if cell is not None else []
            stack_position = len(stack) - stack.index(dango.id) if dango.id in stack else 0

            rankings.append({
                "id": dango.id,
                "name": dango.name,
                "progress": dango.progress,
                "cell": cell,
                "stack_position": stack_position,
            })

        rankings.sort(key=lambda x: (x["progress"], x["stack_position"]), reverse=True)

        for i, rank in enumerate(rankings):
            rank["rank"] = i + 1

        return rankings

    def get_winner(self, game_state: GameState) -> Optional[str]:
        return game_state.winner
