"""Board (赛道) model."""

from typing import Set
from dataclasses import dataclass, field


DEVICE_BOOST = "boost"
DEVICE_TRAP = "trap"
DEVICE_RIFT = "rift"


@dataclass
class Board:
    """Represents the racing board/track."""

    length: int = 32
    boost_cells: Set[int] = field(default_factory=lambda: {3, 11, 16, 23})
    trap_cells: Set[int] = field(default_factory=lambda: {10, 28})
    rift_cells: Set[int] = field(default_factory=lambda: {6, 20})

    def is_boost_cell(self, cell: int) -> bool:
        return cell in self.boost_cells

    def is_trap_cell(self, cell: int) -> bool:
        return cell in self.trap_cells

    def is_rift_cell(self, cell: int) -> bool:
        return cell in self.rift_cells

    def get_device_at_cell(self, cell: int) -> str | None:
        if self.is_boost_cell(cell):
            return DEVICE_BOOST
        elif self.is_trap_cell(cell):
            return DEVICE_TRAP
        elif self.is_rift_cell(cell):
            return DEVICE_RIFT
        return None

    def normalize_cell(self, cell: int) -> int:
        return cell % self.length