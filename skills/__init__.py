"""Skill implementations for all Dango types."""

from .base_skill import BaseSkill
from .daniya_skill import DaniyaSkill
from .phoebe_skill import PhoebeSkill
from .siglica_skill import SiglicaSkill
from .feixue_skill import FeixueSkill
from .lu_hesi_skill import LuHesiSkill
from .katixiya_skill import KatixiyaSkill
from .boss_skill import BossSkill
from .qianxiao_skill import QianxiaoSkill
from .moning_skill import MoningSkill
from .linnai_skill import LinnaiSkill
from .aimisi_skill import AimisiSkill
from .shouanren_skill import ShouanrenSkill
from .kelaite_skill import KelaiteSkill

SKILL_MAPPING = {
    "daniya": DaniyaSkill,
    "phoebe": PhoebeSkill,
    "siglica": SiglicaSkill,
    "feixue": FeixueSkill,
    "luhesi": LuHesiSkill,
    "katixiya": KatixiyaSkill,
    "budaiwang": BossSkill,
    "qianxiao": QianxiaoSkill,
    "moning": MoningSkill,
    "linnai": LinnaiSkill,
    "aimisi": AimisiSkill,
    "shouanren": ShouanrenSkill,
    "kelaite": KelaiteSkill,
}

__all__ = [
    "BaseSkill",
    "DaniyaSkill",
    "PhoebeSkill",
    "SiglicaSkill",
    "FeixueSkill",
    "LuHesiSkill",
    "KatixiyaSkill",
    "BossSkill",
    "QianxiaoSkill",
    "MoningSkill",
    "LinnaiSkill",
    "AimisiSkill",
    "ShouanrenSkill",
    "KelaiteSkill",
    "SKILL_MAPPING",
]
