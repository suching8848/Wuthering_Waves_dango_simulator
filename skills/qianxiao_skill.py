"""Qianxiao skill: Extra steps when rolling minimum dice of the round."""

from skills.base_skill import BaseSkill


class QianxiaoSkill(BaseSkill):
    """千咲技能：投骰子时，若投出的结果为本轮所有点数最小之一，则额外前进2格。"""

    def get_name(self) -> str:
        return "最小激励"

    def modify_move_steps(self, game_state, base_steps: int) -> int:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return base_steps

        dice_results = game_state.dice_results
        if not dice_results:
            return base_steps

        my_dice = dice_results.get(self.dango_id, base_steps)
        min_dice = min(dice_results.values())

        if my_dice == min_dice:
            extra = self.config.get("extra_steps_on_min_dice", 2)
            game_state.logs.append({
                "type": "skill_trigger",
                "dango_id": self.dango_id,
                "skill_name": self.get_name(),
                "desc": f"最小激励触发（本轮最小点数{min_dice}）：+{extra} 格",
                "extra_steps": extra,
                "round": game_state.round_no
            })
            return base_steps + extra
        return base_steps
