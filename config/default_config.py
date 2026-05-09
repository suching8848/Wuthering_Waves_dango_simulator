"""Default configuration for Dango Racing Simulator."""

BOARD_LENGTH = 32

BOOST_CELLS = {3, 11, 16, 23}
TRAP_CELLS = {10, 28}
RIFT_CELLS = {6, 20}

DANGO_IDS = ["daniya", "phoebe", "siglica", "feixue", "luhesi", "katixiya"]
BOSS_ID = "budaiwang"

DANGOS_CONFIG = {
    "daniya": {
        "name": "达妮娅团子",
        "is_boss": False,
        "dice_range": (1, 3),
    },
    "phoebe": {
        "name": "菲比团子",
        "is_boss": False,
        "dice_range": (1, 3),
    },
    "siglica": {
        "name": "西格莉卡团子",
        "is_boss": False,
        "dice_range": (1, 3),
    },
    "feixue": {
        "name": "绯雪团子",
        "is_boss": False,
        "dice_range": (1, 3),
    },
    "luhesi": {
        "name": "陆·赫斯团子",
        "is_boss": False,
        "dice_range": (1, 3),
    },
    "katixiya": {
        "name": "卡提希娅团子",
        "is_boss": False,
        "dice_range": (1, 3),
    },
    "budaiwang": {
        "name": "布大王团子",
        "is_boss": True,
        "dice_range": (1, 6),
        "start_round": 3,
    },
}

INITIAL_STACK_ORDER = DANGO_IDS.copy()

SIMULATION_CONFIG = {
    "verbose": True,
    "log_stacks": True,
    "log_rankings": True,
    "random_seed": None,
    "boss_carries_upper_stack": False,
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
}