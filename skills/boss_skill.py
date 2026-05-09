"""Boss (布大王) skill implementation."""

from skills.base_skill import BaseSkill


class BossSkill(BaseSkill):
    """布大王技能：第3回合开始从终点向起点移动，骰子1-6，不参与排名，始终在堆叠底部。"""

    def get_name(self) -> str:
        return "噩梦之主"

    def on_after_roll(self, game_state, dice: int) -> dict:
        return {"dice": dice}

    def modify_move_steps(self, game_state, base_steps: int) -> int:
        return base_steps

    def on_round_end(self, game_state) -> None:
        return

    def on_game_end(self, game_state, winner) -> None:
        pass
