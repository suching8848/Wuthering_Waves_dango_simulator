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
        boss = game_state.get_boss()
        if boss is None:
            return

        stack_manager = getattr(game_state, 'stack_manager', None)
        if stack_manager is None:
            return

        last_place_dango = self._get_last_place_dango(game_state)
        if last_place_dango is None:
            return

        boss_cell = stack_manager.get_dango_cell(self.dango_id)
        last_cell = stack_manager.get_dango_cell(last_place_dango.id)

        if boss_cell is not None and last_cell is not None and boss_cell != last_cell:
            self._teleport_boss_to_start(game_state)

    def _get_last_place_dango(self, game_state):
        normal_dangos = game_state.get_normal_dangos()
        if not normal_dangos:
            return None
        return min(normal_dangos, key=lambda d: d.progress)

    def _teleport_boss_to_start(self, game_state) -> None:
        stack_manager = getattr(game_state, 'stack_manager', None)
        if stack_manager is None:
            return

        boss = game_state.get_boss()
        if boss is None:
            return

        old_cell = stack_manager.get_dango_cell(self.dango_id)
        if old_cell is not None:
            stack_manager.remove_from_stack(self.dango_id)

        stack_manager.add_to_stack_bottom(self.dango_id, 0)
        boss.move_to_cell(0, game_state.board.length)

    def on_game_end(self, game_state, winner) -> None:
        pass
