"""Katixiya skill: Once per game, if last place, 60% chance to gain +2 steps."""

from skills.base_skill import BaseSkill


class KatixiyaSkill(BaseSkill):
    """卡提希娅技能：每场比赛最多触发1次。自身移动结束后若处于最后一名，本场比赛剩余回合60%概率额外前进2格。"""

    def get_name(self) -> str:
        return "绝境逆袭"

    def on_after_move(self, game_state) -> None:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return

        if dango.state.get("skill_activated", False):
            return

        if self._is_last_place(game_state, self.dango_id):
            dango.state["skill_activated"] = True
            game_state.logs.append({
                "type": "skill_activate",
                "dango_id": self.dango_id,
                "skill_name": self.get_name(),
                "desc": "绝境逆袭已激活（处于最后一名），剩余回合60%概率额外+2格",
                "round": game_state.round_no
            })

    def modify_move_steps(self, game_state, base_steps: int) -> int:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return base_steps

        if dango.state.get("skill_activated", False):
            prob = self.config.get("activation_probability", 0.6)
            extra = self.config.get("extra_steps", 2)
            if game_state.rng.random() < prob:
                game_state.logs.append({
                    "type": "skill_trigger",
                    "dango_id": self.dango_id,
                    "skill_name": self.get_name(),
                    "desc": f"绝境逆袭触发（{int(prob * 100)}%概率）：+{extra} 格",
                    "extra_steps": extra,
                    "round": game_state.round_no
                })
                return base_steps + extra
        return base_steps

    def _is_last_place(self, game_state, dango_id: str) -> bool:
        normal_dangos = game_state.get_normal_dangos()
        if len(normal_dangos) <= 1:
            return True

        target = game_state.get_dango(dango_id)
        if target is None:
            return True

        min_progress = min(d.progress for d in normal_dangos)
        max_progress = max(d.progress for d in normal_dangos)
        return target.progress == min_progress and min_progress < max_progress