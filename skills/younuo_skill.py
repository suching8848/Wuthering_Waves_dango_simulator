"""Younuo skill: Once per game, after crossing midpoint, teleport rank-adjacent non-boss dangos to own cell."""

from skills.base_skill import BaseSkill


class YounuoSkill(BaseSkill):
    """尤诺技能：每场比赛一次，当该团子经过赛程中点后，若该团子排名前后有其他非布大王团子，则将这些团子传送至自己的格子。堆叠顺序与传送前的排名顺序一致。"""

    def get_name(self) -> str:
        return "排名聚合"

    def modify_move_steps(self, game_state, base_steps: int) -> int:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return base_steps
        dango.state["_pre_move_progress"] = dango.progress
        return base_steps

    def on_after_move(self, game_state) -> None:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return

        if dango.state.get("skill_used", False):
            return

        midpoint = self.config.get("midpoint", 16)
        bl = game_state.board.length

        pre_progress = dango.state.get("_pre_move_progress", 0)
        pre_lap = pre_progress % bl
        cur_lap = dango.progress % bl

        if pre_lap >= midpoint or cur_lap < midpoint:
            return

        current_lap = dango.progress // bl
        used_laps = dango.state.get("_younuo_used_laps", [])
        if current_lap in used_laps:
            return

        rankings = self._get_ranking(game_state)
        my_rank = None
        for i, r in enumerate(rankings):
            if r["id"] == self.dango_id:
                my_rank = i
                break

        if my_rank is None:
            return

        adjacent_ids = []
        if my_rank > 0:
            adjacent_ids.append(rankings[my_rank - 1]["id"])
        if my_rank < len(rankings) - 1:
            adjacent_ids.append(rankings[my_rank + 1]["id"])

        if not adjacent_ids:
            return

        my_cell = game_state.stack_manager.get_dango_cell(self.dango_id)
        if my_cell is None:
            my_cell = dango.cell

        for adj_id in adjacent_ids:
            game_state.stack_manager.remove_from_stack(adj_id)

        for adj_id in adjacent_ids:
            adj = game_state.get_dango(adj_id)
            if adj is None:
                continue
            adj.cell = my_cell
            adj.progress = (adj.progress // bl) * bl + my_cell
            if adj.progress < dango.progress:
                adj.progress += bl
            game_state.stack_manager.add_to_stack_top(adj_id, my_cell)

        used_laps.append(current_lap)
        dango.state["_younuo_used_laps"] = used_laps
        dango.state["skill_used"] = True

        names = []
        for adj_id in adjacent_ids:
            adj = game_state.get_dango(adj_id)
            names.append(adj.name if adj else adj_id)

        game_state.logs.append({
            "type": "skill_trigger",
            "dango_id": self.dango_id,
            "skill_name": self.get_name(),
            "desc": f"排名聚合触发：将{', '.join(names)}传送到自身格子 (cell {my_cell})",
            "teleported": adjacent_ids,
            "target_cell": my_cell,
            "round": game_state.round_no
        })

    def _get_ranking(self, game_state) -> list[dict]:
        normal_dangos = game_state.get_normal_dangos()
        ranked = []
        for d in normal_dangos:
            cell = game_state.stack_manager.get_dango_cell(d.id)
            if cell is None:
                cell = d.cell
            stack = game_state.stack_manager.get_stack(cell) if cell is not None else []
            pos = len(stack) - stack.index(d.id) if d.id in stack else 0
            ranked.append({"id": d.id, "progress": d.progress, "stack_pos": pos})
        ranked.sort(key=lambda x: (x["progress"], x["stack_pos"]), reverse=True)
        return ranked
