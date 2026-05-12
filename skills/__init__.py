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
from .aogusita_skill import AogusitaSkill
from .younuo_skill import YounuoSkill
from .fuluoluo_skill import FuluoluoSkill
from .changli_skill import ChangliSkill
from .jinxi_skill import JinxiSkill
from .kakaluo_skill import KakaluoSkill

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
    "aogusita": AogusitaSkill,
    "younuo": YounuoSkill,
    "fuluoluo": FuluoluoSkill,
    "changli": ChangliSkill,
    "jinxi": JinxiSkill,
    "kakaluo": KakaluoSkill,
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
    "AogusitaSkill",
    "YounuoSkill",
    "FuluoluoSkill",
    "ChangliSkill",
    "JinxiSkill",
    "KakaluoSkill",
    "SKILL_MAPPING",
]
