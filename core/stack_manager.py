"""Stack Manager for handling stack/ordering logic."""

import random
from typing import Optional
from models.dango import Dango


class StackManager:
    """Manages stacking of dangos on board cells."""

    def __init__(self, board_length: int = 32):
        self.board_length = board_length
        self.stacks: dict[int, list[str]] = {}
        self.dango_positions: dict[str, int] = {}

    def initialize_stack(self, dango_ids: list[str], cell: int = 0) -> None:
        self.stacks[cell] = list(dango_ids)
        for dango_id in dango_ids:
            self.dango_positions[dango_id] = cell

    def get_stack(self, cell: int) -> list[str]:
        return self.stacks.get(cell, [])

    def get_dango_cell(self, dango_id: str) -> Optional[int]:
        return self.dango_positions.get(dango_id)

    def remove_from_stack(self, dango_id: str) -> None:
        cell = self.dango_positions.get(dango_id)
        if cell is not None and cell in self.stacks:
            if dango_id in self.stacks[cell]:
                self.stacks[cell].remove(dango_id)
                if not self.stacks[cell]:
                    del self.stacks[cell]
        self.dango_positions.pop(dango_id, None)

    def add_to_stack_top(self, dango_id: str, cell: int) -> None:
        if cell not in self.stacks:
            self.stacks[cell] = []
        if dango_id not in self.stacks[cell]:
            self.stacks[cell].append(dango_id)
        self.dango_positions[dango_id] = cell

    def add_to_stack_bottom(self, dango_id: str, cell: int) -> None:
        if cell not in self.stacks:
            self.stacks[cell] = []
        if dango_id not in self.stacks[cell]:
            self.stacks[cell].insert(0, dango_id)
        self.dango_positions[dango_id] = cell

    def get_stack_order_index(self, dango_id: str) -> int:
        cell = self.dango_positions.get(dango_id)
        if cell is None or cell not in self.stacks:
            return -1
        try:
            return self.stacks[cell].index(dango_id)
        except ValueError:
            return -1

    def get_upper_stack(self, dango_id: str) -> list[str]:
        cell = self.dango_positions.get(dango_id)
        if cell is None or cell not in self.stacks:
            return []
        index = self.stacks[cell].index(dango_id)
        return self.stacks[cell][index + 1:]

    def get_lower_stack(self, dango_id: str) -> list[str]:
        cell = self.dango_positions.get(dango_id)
        if cell is None or cell not in self.stacks:
            return []
        index = self.stacks[cell].index(dango_id)
        return self.stacks[cell][:index]

    def move_group(self, bottom_dango_id: str, new_cell: int) -> list[str]:
        moved_group = []
        cell = self.dango_positions.get(bottom_dango_id)
        if cell is None:
            return moved_group

        stack = self.stacks.get(cell, [])
        if bottom_dango_id not in stack:
            return moved_group

        index = stack.index(bottom_dango_id)
        moving_dangos = stack[index:]
        remaining_stack = stack[:index]
        if remaining_stack:
            self.stacks[cell] = remaining_stack
        else:
            del self.stacks[cell]

        for d_id in moving_dangos:
            self.dango_positions.pop(d_id, None)

        for d_id in reversed(moving_dangos):
            self.add_to_stack_top(d_id, new_cell)
            moved_group.append(d_id)

        return list(reversed(moved_group))

    def shuffle_cell(self, cell: int, rng: random.Random, boss_id: str = "budaiwang") -> None:
        if cell not in self.stacks or not self.stacks[cell]:
            return

        stack = self.stacks[cell]
        boss_in_cell = boss_id in stack

        non_boss_stack = [d for d in stack if d != boss_id]
        rng.shuffle(non_boss_stack)

        if boss_in_cell:
            self.stacks[cell] = [boss_id] + non_boss_stack
        else:
            self.stacks[cell] = non_boss_stack

    def ensure_boss_at_bottom(self, boss_id: str = "budaiwang") -> None:
        for cell, stack in self.stacks.items():
            if boss_id in stack:
                stack.remove(boss_id)
                self.stacks[cell] = [boss_id] + stack
                break

    def get_all_stacks_snapshot(self) -> dict[int, list[str]]:
        return {cell: list(stack) for cell, stack in self.stacks.items()}

    def __repr__(self) -> str:
        return f"StackManager(stacks={self.stacks})"