"""Default configuration for Dango Racing Simulator."""

BOARD_LENGTH = 32

BOOST_CELLS = {3, 11, 16, 23}
TRAP_CELLS = {10, 28}
RIFT_CELLS = {6, 20}

# ============================================================
# 团子组定义 — 添加新组只需三步：
#   1. 定义 DANGO_IDS_C = ["xxx", "yyy", ...]  （6个团子ID）
#   2. 在 DANGO_GROUPS 添加 "C": DANGO_IDS_C
#   3. 在下方 DANGOS_CONFIG 添加每个团子的配置（group="C"）
#   4. 在 SKILL_CONFIG 添加对应技能参数
#   5. 在 skills/ 目录创建技能文件，并在 skills/__init__.py 注册
# ============================================================
DANGO_IDS_A = ["daniya", "phoebe", "siglica", "feixue", "luhesi", "katixiya"]
DANGO_IDS_B = ["qianxiao", "moning", "linnai", "aimisi", "shouanren", "kelaite"]
DANGO_IDS_C = ["aogusita", "younuo", "fuluoluo", "changli", "jinxi", "kakaluo"]
DANGO_IDS = DANGO_IDS_A + DANGO_IDS_B + DANGO_IDS_C
BOSS_ID = "budaiwang"

DANGO_GROUPS = {
    "A": DANGO_IDS_A,
    "B": DANGO_IDS_B,
    "C": DANGO_IDS_C,
}

DANGOS_CONFIG = {
    # A组
    "daniya": {
        "name": "达妮娅团子",
        "is_boss": False,
        "dice_range": (1, 3),
        "group": "A",
    },
    "phoebe": {
        "name": "菲比团子",
        "is_boss": False,
        "dice_range": (1, 3),
        "group": "A",
    },
    "siglica": {
        "name": "西格莉卡团子",
        "is_boss": False,
        "dice_range": (1, 3),
        "group": "A",
    },
    "feixue": {
        "name": "绯雪团子",
        "is_boss": False,
        "dice_range": (1, 3),
        "group": "A",
    },
    "luhesi": {
        "name": "陆·赫斯团子",
        "is_boss": False,
        "dice_range": (1, 3),
        "group": "A",
    },
    "katixiya": {
        "name": "卡提希娅团子",
        "is_boss": False,
        "dice_range": (1, 3),
        "group": "A",
    },
    # B组
    "qianxiao": {
        "name": "千咲团子",
        "is_boss": False,
        "dice_range": (1, 3),
        "group": "B",
    },
    "moning": {
        "name": "莫宁团子",
        "is_boss": False,
        "dice_range": (1, 3),
        "group": "B",
    },
    "linnai": {
        "name": "琳奈团子",
        "is_boss": False,
        "dice_range": (1, 3),
        "group": "B",
    },
    "aimisi": {
        "name": "爱弥斯团子",
        "is_boss": False,
        "dice_range": (1, 3),
        "group": "B",
    },
    "shouanren": {
        "name": "守岸人团子",
        "is_boss": False,
        "dice_range": (2, 3),
        "group": "B",
    },
    "kelaite": {
        "name": "珂莱塔团子",
        "is_boss": False,
        "dice_range": (1, 3),
        "group": "B",
    },
    # C组
    "aogusita": {
        "name": "奥古斯塔团子",
        "is_boss": False,
        "dice_range": (1, 3),
        "group": "C",
    },
    "younuo": {
        "name": "尤诺团子",
        "is_boss": False,
        "dice_range": (1, 3),
        "group": "C",
    },
    "fuluoluo": {
        "name": "弗洛洛团子",
        "is_boss": False,
        "dice_range": (1, 3),
        "group": "C",
    },
    "changli": {
        "name": "长离团子",
        "is_boss": False,
        "dice_range": (1, 3),
        "group": "C",
    },
    "jinxi": {
        "name": "今汐团子",
        "is_boss": False,
        "dice_range": (1, 3),
        "group": "C",
    },
    "kakaluo": {
        "name": "卡卡罗团子",
        "is_boss": False,
        "dice_range": (1, 3),
        "group": "C",
    },
    "budaiwang": {
        "name": "布大王团子",
        "is_boss": True,
        "dice_range": (1, 6),
        "start_round": 3,
        "group": "boss",
    },
}

INITIAL_STACK_ORDER = DANGO_IDS_A.copy()

SIMULATION_CONFIG = {
    "verbose": True,
    "log_stacks": True,
    "log_rankings": True,
    "random_seed": None,
    "boss_carries_upper_stack": True,
}

SKILL_CONFIG = {
    "daniya": {
        "extra_steps_on_same_dice": 2,
    },
    "phoebe": {
        "extra_step_probability": 0.5,
    },
    "siglica": {
        "mark_count": 2,
        "mark_penalty": 1,
        "min_steps": 1,
    },
    "feixue": {
        "extra_steps_after_meeting_boss": 1,
    },
    "luhesi": {
        "boost_extra_steps": 3,
        "trap_extra_steps": 1,
    },
    "katixiya": {
        "activation_probability": 0.6,
        "extra_steps": 2,
    },
    # B组技能配置
    "qianxiao": {
        "extra_steps_on_min_dice": 2,
    },
    "moning": {
        "dice_cycle": [3, 2, 1],
    },
    "linnai": {
        "double_probability": 0.6,
        "skip_probability": 0.2,
    },
    "aimisi": {
        "midpoint": 16,
    },
    "shouanren": {},
    "kelaite": {
        "double_probability": 0.28,
    },
    # C组技能配置
    "aogusita": {},
    "younuo": {
        "midpoint": 16,
    },
    "fuluoluo": {
        "extra_steps": 3,
    },
    "changli": {
        "delay_probability": 0.65,
    },
    "jinxi": {
        "rise_probability": 0.4,
    },
    "kakaluo": {
        "extra_steps": 3,
    },
}
