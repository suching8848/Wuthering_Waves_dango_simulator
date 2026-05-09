"""Siglica skill: Mark opponents to reduce their movement."""

from skills.base_skill import BaseSkill


class SiglicaSkill(BaseSkill):
    """西格莉卡技能：标记排名紧邻自身且更高的至多两个团子，被标记者移动时-1格。"""

    def get_name(self) -> str:
        return "标记指令"

    def on_round_start(self, game_state) -> None:
        game_state.marked_by_siglica = set()

    def mark_targets(self, game_state) -> list[str]:
        dango = game_state.get_dango(self.dango_id)
        if dango is None or dango.is_boss:
            return []

        ranking = self._calculate_ranking(game_state)
        my_index = -1
        for i, d in enumerate(ranking):
            if d.id == self.dango_id:
                my_index = i
                break

        if my_index <= 0:
            return []

        mark_count = self.config.get("mark_count", 2)
        targets = []
        for i in range(my_index - 1, -1, -1):
            if len(targets) >= mark_count:
                break
            targets.append(ranking[i].id)

        game_state.marked_by_siglica.update(targets)
        return targets

    def _calculate_ranking(self, game_state) -> list:
        normal_dangos = game_state.get_normal_dangos()
        sorted_dangos = sorted(
            normal_dangos,
            key=lambda d: (d.progress, self._get_stack_position(game_state, d.id)),
            reverse=True
        )
        return sorted_dangos

    def _get_stack_position(self, game_state, dango_id: str) -> int:
        stack_manager = getattr(game_state, 'stack_manager', None)
        if stack_manager is None:
            return 0
        cell = stack_manager.get_dango_cell(dango_id)
        if cell is None:
            return 0
        stack = stack_manager.get_stack(cell)
        try:
            return len(stack) - stack.index(dango_id)
        except ValueError:
            return 0