"""Feixue skill: After meeting boss, gain +1 extra step per move."""

from skills.base_skill import BaseSkill


class FeixueSkill(BaseSkill):
    """绯雪技能：当绯雪团子与布大王相遇后，之后每次移动时额外前进1格。"""

    def get_name(self) -> str:
        return "追击之魂"

    def on_meet_boss(self, game_state) -> None:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return
        dango.state["metBoss"] = True

    def modify_move_steps(self, game_state, base_steps: int) -> int:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return base_steps

        if dango.state.get("metBoss", False):
            extra = self.config.get("extra_steps_after_meeting_boss", 1)
            return base_steps + extra
        return base_steps