"""Phoebe skill: 50% chance to gain extra 1 step."""

from skills.base_skill import BaseSkill


class PhoebeSkill(BaseSkill):
    """菲比技能：50%概率额外前进1格。"""

    def get_name(self) -> str:
        return "幸运掷骰"

    def on_after_roll(self, game_state, dice: int) -> dict:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return {}

        prob = self.config.get("extra_step_probability", 0.5)
        triggered = game_state.rng.random() < prob
        extra_steps = 1 if triggered else 0

        if triggered:
            current_extra = dango.state.get("pending_extra_steps", 0)
            dango.state["pending_extra_steps"] = current_extra + extra_steps

        return {
            "skill_triggered": triggered,
            "extra_steps": extra_steps,
            "probability": prob,
        }

    def modify_move_steps(self, game_state, base_steps: int) -> int:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return base_steps

        extra_steps = dango.state.pop("pending_extra_steps", 0)
        return base_steps + extra_steps