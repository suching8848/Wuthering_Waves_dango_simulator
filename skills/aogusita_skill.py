"""Aogusita skill: If at top of stack at round start, skip this round and act last next round."""

from skills.base_skill import BaseSkill


class AogusitaSkill(BaseSkill):
    """奥古斯塔技能：回合开始时，若该团子处于堆叠最顶端，则在本回合不行动，且在下回合中最后一个行动。"""

    def get_name(self) -> str:
        return "顶端蛰伏"

    def on_round_start(self, game_state) -> None:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return

        cell = game_state.stack_manager.get_dango_cell(self.dango_id)
        if cell is None:
            return

        stack = game_state.stack_manager.get_stack(cell)
        if stack and stack[-1] == self.dango_id:
            dango.state["skip_round"] = True
            dango.state["_act_last"] = True
            game_state.logs.append({
                "type": "skill_trigger",
                "dango_id": self.dango_id,
                "skill_name": self.get_name(),
                "desc": "顶端蛰伏触发：本回合不行动，下回合最后行动",
                "round": game_state.round_no
            })

    def modify_final_steps(self, game_state, base_steps: int) -> int:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return base_steps

        if dango.state.pop("skip_round", False):
            return 0
        return base_steps
