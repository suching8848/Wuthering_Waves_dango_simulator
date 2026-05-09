"""Lu Hesi skill: Boost/Trap device enhancements."""

from models.board import DEVICE_BOOST, DEVICE_TRAP
from skills.base_skill import BaseSkill


class LuHesiSkill(BaseSkill):
    """陆·赫斯技能：推进装置时总共+4格(1+3)，阻遏装置时总共-2格(1+1)。"""

    def get_name(self) -> str:
        return "装置精通"

    def on_device_trigger(self, game_state, device_type: str) -> dict:
        if device_type == DEVICE_BOOST:
            default_boost = 1
            extra = self.config.get("boost_extra_steps", 3)
            game_state.logs.append({
                "type": "skill_trigger",
                "dango_id": self.dango_id,
                "skill_name": self.get_name(),
                "desc": f"装置精通触发：推进 +{default_boost + extra} 格",
                "extra_steps": default_boost + extra,
                "round": game_state.round_no
            })
            return {"skill_triggered": True, "extra_steps": default_boost + extra, "device": "boost"}
        elif device_type == DEVICE_TRAP:
            default_trap = 1
            extra = self.config.get("trap_extra_steps", 1)
            game_state.logs.append({
                "type": "skill_trigger",
                "dango_id": self.dango_id,
                "skill_name": self.get_name(),
                "desc": f"装置精通触发：阻遏 -{default_trap + extra} 格",
                "extra_steps": default_trap + extra,
                "round": game_state.round_no
            })
            return {"skill_triggered": True, "extra_steps": default_trap + extra, "device": "trap"}
        return {}

    def modify_move_steps(self, game_state, base_steps: int) -> int:
        return base_steps