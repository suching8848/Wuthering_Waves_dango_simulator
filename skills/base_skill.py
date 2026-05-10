"""Base skill class for modular skill system."""

from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseSkill(ABC):
    """Abstract base class for all skills."""

    def __init__(self, dango_id: str, config: dict = None):
        self.dango_id = dango_id
        self.config = config or {}

    @abstractmethod
    def get_name(self) -> str:
        pass

    def on_round_start(self, game_state: Any) -> None:
        pass

    def on_after_roll(self, game_state: Any, dice: int) -> dict:
        return {}

    def on_before_move(self, game_state: Any, base_steps: int) -> int:
        return base_steps

    def modify_move_steps(self, game_state: Any, base_steps: int) -> int:
        return base_steps

    def on_after_move(self, game_state: Any) -> None:
        pass

    def on_device_trigger(self, game_state: Any, device_type: str) -> dict:
        return {}

    def on_meet_boss(self, game_state: Any) -> None:
        pass

    def on_round_end(self, game_state: Any) -> None:
        pass

    def modify_final_steps(self, game_state: Any, base_steps: int) -> int:
        return base_steps

    def on_game_end(self, game_state: Any, winner: Optional[str]) -> None:
        pass