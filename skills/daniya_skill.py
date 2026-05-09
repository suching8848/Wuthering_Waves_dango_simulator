"""Daniya skill: Extra steps when rolling same number as last time."""

from skills.base_skill import BaseSkill


class DaniyaSkill(BaseSkill):
    """达妮娅技能：投骰子时，若投出和上一次相同的点数，则额外前进2格。"""

    def get_name(self) -> str:
        return "连掷激励"

    def on_after_roll(self, game_state, dice: int) -> dict:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return {}

        last_dice = dango.state.get("lastDice", None)
        triggered = False

        if last_dice is not None and dice == last_dice:
            extra_steps = self.config.get("extra_steps_on_same_dice", 2)
            current_extra = dango.state.get("pending_extra_steps", 0)
            dango.state["pending_extra_steps"] = current_extra + extra_steps
            triggered = True

        dango.state["lastDice"] = dice

        return {
            "skill_triggered": triggered,
            "last_dice": last_dice,
            "current_dice": dice,
        }

    def modify_move_steps(self, game_state, base_steps: int) -> int:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return base_steps
        extra_steps = dango.state.pop("pending_extra_steps", 0)
        return base_steps + extra_steps