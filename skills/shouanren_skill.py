"""Shouanren skill: Dice only rolls 2 or 3 (handled by dice_range in config)."""

from skills.base_skill import BaseSkill


class ShouanrenSkill(BaseSkill):
    """守岸人技能：骰子只会掷出2或3。"""

    def get_name(self) -> str:
        return "稳定投掷"
