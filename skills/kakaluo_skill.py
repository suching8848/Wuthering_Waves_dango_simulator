"""Kakaluo skill: If in last place at start of move, +3 extra steps."""

from skills.base_skill import BaseSkill


class KakaluoSkill(BaseSkill):
    """卡卡罗技能：开始移动时，如果在最后一名，额外前进3格。"""

    def get_name(self) -> str:
        return "末位追击"

    def modify_move_steps(self, game_state, base_steps: int) -> int:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return base_steps

        normal_dangos = game_state.get_normal_dangos()
        if len(normal_dangos) <= 1:
            return base_steps

        min_progress = min(d.progress for d in normal_dangos)
        max_progress = max(d.progress for d in normal_dangos)
        if dango.progress == min_progress and min_progress < max_progress:
            extra = self.config.get("extra_steps", 3)
            game_state.logs.append({
                "type": "skill_trigger",
                "dango_id": self.dango_id,
                "skill_name": self.get_name(),
                "desc": f"末位追击触发：+{extra} 格",
                "extra_steps": extra,
                "round": game_state.round_no
            })
            return base_steps + extra
        return base_steps
