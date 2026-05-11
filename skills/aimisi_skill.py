"""Aimisi skill: Once per game, after passing midpoint, teleport to nearest dango ahead."""

from skills.base_skill import BaseSkill


class AimisiSkill(BaseSkill):
    """爱弥斯技能：每场比赛一次，当该团子经过赛程中点后，若前方存在其他非布大王的团子，则会传送到最近团子顶端。"""

    def get_name(self) -> str:
        return "中点传送"

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

        midpoint = self.config.get("midpoint", 16)
        bl = game_state.board.length

        pre_progress = dango.state.get("_pre_move_progress", 0)
        pre_lap_progress = pre_progress % bl
        cur_lap_progress = dango.progress % bl

        if pre_lap_progress >= midpoint or cur_lap_progress < midpoint:
            return

        current_lap = dango.progress // bl
        used_laps = dango.state.get("teleport_used_laps", [])
        if dango.state.get("teleport_used") and 0 not in used_laps:
            used_laps.append(0)
        if current_lap in used_laps:
            return

        normal_dangos = game_state.get_normal_dangos()
        ahead = [d for d in normal_dangos if d.id != self.dango_id and d.progress > dango.progress]
        if not ahead:
            return

        nearest = min(ahead, key=lambda d: d.progress - dango.progress)
        target_cell = game_state.stack_manager.get_dango_cell(nearest.id)
        if target_cell is None:
            target_cell = nearest.cell

        game_state.stack_manager.remove_from_stack(self.dango_id)
        game_state.stack_manager.add_to_stack_top(self.dango_id, target_cell)

        new_progress = (dango.progress // bl) * bl + target_cell
        if new_progress < dango.progress:
            new_progress += bl
        dango.progress = new_progress
        dango.cell = target_cell
        used_laps.append(current_lap)
        dango.state["teleport_used_laps"] = used_laps

        game_state.logs.append({
            "type": "skill_trigger",
            "dango_id": self.dango_id,
            "skill_name": self.get_name(),
            "desc": f"中点传送触发：传送到{nearest.name}顶端 (cell {target_cell})",
            "target_dango": nearest.id,
            "target_cell": target_cell,
            "round": game_state.round_no
        })
