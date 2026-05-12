"""Changli skill: If dangos stacked below, 65% chance to act last next round."""

from skills.base_skill import BaseSkill


class ChangliSkill(BaseSkill):
    """长离技能：如果下方堆叠其他团子，下一个回合有65%的概率最后一个行动。"""

    def get_name(self) -> str:
        return "蓄势待发"

    def on_after_move(self, game_state) -> None:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return

        cell = game_state.stack_manager.get_dango_cell(self.dango_id)
        if cell is None:
            return

        stack = game_state.stack_manager.get_stack(cell)
        if not stack:
            return

        idx = stack.index(self.dango_id) if self.dango_id in stack else -1
        if idx <= 0:
            return

        has_below = any(
            not (game_state.get_dango(d_id) is not None and game_state.get_dango(d_id).is_boss)
            for d_id in stack[:idx]
        )
        if not has_below:
            return

        prob = self.config.get("delay_probability", 0.65)
        if game_state.rng.random() < prob:
            dango.state["_act_last"] = True
            game_state.logs.append({
                "type": "skill_trigger",
                "dango_id": self.dango_id,
                "skill_name": self.get_name(),
                "desc": f"蓄势待发触发（{int(prob * 100)}%概率）：下回合最后行动",
                "round": game_state.round_no
            })
