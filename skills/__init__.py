"""Skill implementations for all Dango types."""

from .base_skill import BaseSkill
from .daniya_skill import DaniyaSkill
from .phoebe_skill import PhoebeSkill
from .siglica_skill import SiglicaSkill
from .feixue_skill import FeixueSkill
from .lu_hesi_skill import LuHesiSkill
from .katixiya_skill import KatixiyaSkill
from .boss_skill import BossSkill

SKILL_MAPPING = {
    "daniya": DaniyaSkill,
    "phoebe": PhoebeSkill,
    "siglica": SiglicaSkill,
    "feixue": FeixueSkill,
    "luhesi": LuHesiSkill,
    "katixiya": KatixiyaSkill,
    "budaiwang": BossSkill,
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
    "SKILL_MAPPING",
]