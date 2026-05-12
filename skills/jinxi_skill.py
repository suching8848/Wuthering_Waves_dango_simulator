"""Jinxi skill: If dangos stacked above, 40% chance to rise to top of all dangos."""

from skills.base_skill import BaseSkill


class JinxiSkill(BaseSkill):
    """今汐技能：如果头顶堆叠其他团子，有40%的概率移动到所有团子的最上方。"""

    def get_name(self) -> str:
        return "凌越巅峰"

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

        if self.dango_id not in stack:
            return

        idx = stack.index(self.dango_id)
        has_above = any(
            idx < len(stack) - 1
            and not (game_state.get_dango(stack[i]) is not None and game_state.get_dango(stack[i]).is_boss)
            for i in range(idx + 1, len(stack))
        )
        if not has_above:
            return

        prob = self.config.get("rise_probability", 0.4)
        if game_state.rng.random() < prob:
            game_state.stack_manager.remove_from_stack(self.dango_id)
            game_state.stack_manager.add_to_stack_top(self.dango_id, cell)
            game_state.logs.append({
                "type": "skill_trigger",
                "dango_id": self.dango_id,
                "skill_name": self.get_name(),
                "desc": f"凌越巅峰触发（{int(prob * 100)}%概率）：移动到堆叠最上方",
                "round": game_state.round_no
            })
