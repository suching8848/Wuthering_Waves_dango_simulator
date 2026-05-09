"""GameState model."""

from typing import Any, Optional
from dataclasses import dataclass, field
from .dango import Dango
from .board import Board


@dataclass
class GameState:
    """Represents the current state of a game."""

    round_no: int = 0
    board: Board = field(default_factory=Board)
    dangos: dict[str, Dango] = field(default_factory=dict)
    current_order: list[str] = field(default_factory=list)
    dice_results: dict[str, int] = field(default_factory=dict)
    marked_by_siglica: set[str] = field(default_factory=set)
    winner: Optional[str] = None
    winner_found_round: Optional[int] = None
    logs: list = field(default_factory=list)
    boss_start_round: int = 3
    initial_stack_order: list[str] = field(default_factory=list)
    boss_spawned: bool = False

    def get_dango(self, dango_id: str) -> Optional[Dango]:
        return self.dangos.get(dango_id)

    def get_all_dangos(self) -> list[Dango]:
        return list(self.dangos.values())

    def get_normal_dangos(self) -> list[Dango]:
        return [d for d in self.dangos.values() if not d.is_boss]

    def get_boss(self) -> Optional[Dango]:
        for d in self.dangos.values():
            if d.is_boss:
                return d
        return None

    def is_boss_active(self) -> bool:
        return self.round_no >= self.boss_start_round

    def get_active_dangos(self) -> list[Dango]:
        if self.is_boss_active() and self.boss_spawned:
            return list(self.dangos.values())
        return self.get_normal_dangos()

    def get_active_dango_ids(self) -> list[str]:
        if self.is_boss_active() and self.boss_spawned:
            return list(self.dangos.keys())
        return [d.id for d in self.get_normal_dangos()]