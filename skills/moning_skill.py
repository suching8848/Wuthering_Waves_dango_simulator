"""Moning skill: Dice cycles through 3/2/1."""

from skills.base_skill import BaseSkill


class MoningSkill(BaseSkill):
    """莫宁技能：投骰子时，点数将固定在3/2/1循环出现。"""

    def get_name(self) -> str:
        return "循环骰子"

    def on_round_start(self, game_state) -> None:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return
        if "cycle_index" not in dango.state:
            cycle = self.config.get("dice_cycle", [3, 2, 1])
            dango.state["cycle_index"] = 0
            dango.state["dice_cycle"] = cycle

    def on_after_roll(self, game_state, dice: int) -> dict:
        dango = game_state.get_dango(self.dango_id)
        if dango is None:
            return {}

        cycle = dango.state.get("dice_cycle", [3, 2, 1])
        index = dango.state.get("cycle_index", 0)
        fixed_dice = cycle[index % len(cycle)]
        dango.state["cycle_index"] = index + 1

        game_state.dice_results[self.dango_id] = fixed_dice
        return {"dice": fixed_dice, "original_roll": dice}
