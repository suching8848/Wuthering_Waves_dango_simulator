"""Linnai skill: 60% double steps, 20% skip move."""

from skills.base_skill import BaseSkill


class LinnaiSkill(BaseSkill):
    """琳奈技能：每回合中，有60%概率按照双倍点数移动，但有20%概率当回合无法移动。"""

    def get_name(self) -> str:
        return "波动步伐"

    def on_after_roll(self, game_state, dice: int) -> dict:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return {}

        r = game_state.rng.random()
        double_prob = self.config.get("double_probability", 0.6)
        skip_prob = self.config.get("skip_probability", 0.2)

        if r < skip_prob:
            dango.state["skip_move"] = True
            dango.state["double_move"] = False
            game_state.logs.append({
                "type": "skill_trigger",
                "dango_id": self.dango_id,
                "skill_name": self.get_name(),
                "desc": f"波动步伐触发（{int(skip_prob * 100)}%概率）：本回合无法移动",
                "round": game_state.round_no
            })
        elif r < skip_prob + double_prob:
            dango.state["double_move"] = True
            dango.state["skip_move"] = False
            game_state.logs.append({
                "type": "skill_trigger",
                "dango_id": self.dango_id,
                "skill_name": self.get_name(),
                "desc": f"波动步伐触发（{int(double_prob * 100)}%概率）：双倍点数移动",
                "round": game_state.round_no
            })
        else:
            dango.state["skip_move"] = False
            dango.state["double_move"] = False

        return {}

    def modify_move_steps(self, game_state, base_steps: int) -> int:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return base_steps

        if dango.state.get("double_move", False):
            return base_steps * 2
        return base_steps

    def modify_final_steps(self, game_state, base_steps: int) -> int:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return base_steps

        if dango.state.pop("skip_move", False):
            return 0
        dango.state.pop("double_move", False)
        return base_steps
