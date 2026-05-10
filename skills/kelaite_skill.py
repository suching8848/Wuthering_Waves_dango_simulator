"""Kelaite skill: 28% chance to move at double dice points."""

from skills.base_skill import BaseSkill


class KelaiteSkill(BaseSkill):
    """珂莱塔技能：28%概率以骰子的双倍点数前进。"""

    def get_name(self) -> str:
        return "双倍冲刺"

    def modify_move_steps(self, game_state, base_steps: int) -> int:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return base_steps

        prob = self.config.get("double_probability", 0.28)
        if game_state.rng.random() < prob:
            game_state.logs.append({
                "type": "skill_trigger",
                "dango_id": self.dango_id,
                "skill_name": self.get_name(),
                "desc": f"双倍冲刺触发（{int(prob * 100)}%概率）：{base_steps * 2} 格",
                "extra_steps": base_steps,
                "round": game_state.round_no
            })
            return base_steps * 2
        return base_steps
