"""Fuluoluo skill: At round start, if at bottom of stack, +3 extra steps on move."""

from skills.base_skill import BaseSkill


class FuluoluoSkill(BaseSkill):
    """弗洛洛技能：回合开始时，若该团子处于堆叠最底层，则在移动时额外前进3格。"""

    def get_name(self) -> str:
        return "底层突破"

    def on_round_start(self, game_state) -> None:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return

        cell = game_state.stack_manager.get_dango_cell(self.dango_id)
        if cell is None:
            dango.state["_bottom_bonus"] = False
            return

        stack = game_state.stack_manager.get_stack(cell)
        is_bottom = stack and stack[0] == self.dango_id and not dango.is_boss
        if is_bottom:
            boss = game_state.get_boss()
            if boss is not None and game_state.boss_spawned:
                boss_cell = game_state.stack_manager.get_dango_cell(boss.id)
                if cell == boss_cell and stack[0] == boss.id:
                    is_bottom = len(stack) >= 2 and stack[1] == self.dango_id
        dango.state["_bottom_bonus"] = is_bottom

    def modify_move_steps(self, game_state, base_steps: int) -> int:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return base_steps

        if dango.state.get("_bottom_bonus", False):
            extra = self.config.get("extra_steps", 3)
            game_state.logs.append({
                "type": "skill_trigger",
                "dango_id": self.dango_id,
                "skill_name": self.get_name(),
                "desc": f"底层突破触发：+{extra} 格",
                "extra_steps": extra,
                "round": game_state.round_no
            })
            return base_steps + extra
        return base_steps
