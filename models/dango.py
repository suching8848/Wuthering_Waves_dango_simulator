"""Dango (团子) model."""

from typing import Any, Optional
from dataclasses import dataclass, field


@dataclass
class Dango:
    """Represents a Dango contestant in the racing game."""

    id: str
    name: str
    is_boss: bool = False
    progress: int = 0
    cell: int = 0
    skill_name: str = ""
    state: dict = field(default_factory=dict)
    dice_range: tuple[int, int] = (1, 3)

    def get_progress(self) -> int:
        return self.progress

    def get_cell(self) -> int:
        return self.cell

    def has_reached_goal(self, board_length: int = 32) -> bool:
        return self.progress >= board_length

    def advance(self, steps: int, board_length: int = 32) -> None:
        self.progress += steps
        self.cell = self.progress % board_length

    def advance_backward(self, steps: int, board_length: int = 32) -> None:
        self.progress += steps
        self.cell = (-self.progress) % board_length

    def move_to_cell(self, cell: int, board_length: int = 32) -> None:
        self.cell = cell
        self.progress = (self.progress // board_length) * board_length + cell
        if self.progress < 0:
            self.progress += ((-self.progress // board_length) + 1) * board_length

    def __repr__(self) -> str:
        return f"Dango({self.id}, progress={self.progress}, cell={self.cell})"