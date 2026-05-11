"""Interactive menu for Dango Racing Simulator."""

import subprocess
import sys
from pathlib import Path

PRESETS_DIR = Path(__file__).parent / "presets"

PRESETS = [
    ("a_early.json", "A组上半场早期（第2回合）"),
    ("a_late.json", "A组上半场后期（达妮娅已胜）"),
    ("b_finish.json", "B组终点局势（珂莱塔终点，布大王下方）"),
]


def ask(msg: str, default: str = "", choices: list[str] | None = None) -> str:
    while True:
        val = input(msg).strip()
        val = val if val else default
        if choices is None or val in choices:
            return val
        print(f"  无效输入，请重新选择")


def show_banner():
    print()
    print("=" * 48)
    print("  团子竞速模拟器 v2.61")
    print("=" * 48)
    print()


def menu() -> bool:
    """Show main menu. Returns False if user wants to exit."""
    show_banner()
    print("  1. 上半场 — 单次模拟（过程回放）")
    print("  2. 上半场 — 多次统计（自定次数）")
    print("  3. 下半场 — 单次模拟（-s 快照）")
    print("  4. 下半场 — 多次预测（-s 快照，自定次数）")
    print("  0. 退出")
    print()

    choice = ask("请选择 [1]: ", "1", choices=["0", "1", "2", "3", "4"])
    if choice == "0":
        print("再见！")
        return False

    group = ask_group()
    seed = ask("随机种子（留空=随机）: ")

    cmd = ["python", "main.py"]

    if choice == "1":
        cmd.extend(["single", "--group", group])
        if seed:
            cmd.extend(["--seed", seed])
        fixed = ask("固定初始堆叠? (y/n) [n]: ", "n", choices=["y", "n", "Y", "N"])
        if fixed.lower() == "y":
            cmd.append("--fixed-order")

    elif choice == "2":
        cmd.extend(["multi", "--group", group])
        if seed:
            cmd.extend(["--seed", seed])
        n = ask("模拟次数 [1000]: ", "1000")
        cmd.extend(["-n", n])

    elif choice in ("3", "4"):
        preset_file = pick_preset()
        if choice == "3":
            cmd.extend(["single", "-s", preset_file, "--group", group])
        else:
            cmd.extend(["multi", "-s", preset_file, "--group", group])
            n = ask("模拟次数 [100]: ", "100")
            cmd.extend(["-n", n])
        if seed:
            cmd.extend(["--seed", seed])

    print()
    print(f"  -> {' '.join(cmd)}")
    confirm = ask("确认运行? (y/n) [y]: ", "y", choices=["y", "n", "Y", "N"])
    if confirm.lower() != "y":
        print("已取消。")
        return True

    print()
    print("-" * 48)
    subprocess.run(cmd)
    print("-" * 48)
    return True


def ask_group() -> str:
    print()
    print("  1. A组")
    print("  2. B组")
    print()
    g = ask("请选择组别 [1]: ", "1", choices=["1", "2"])
    return "B" if g == "2" else "A"


def pick_preset() -> str:
    print()
    print("  预设快照:")
    for i, (_, desc) in enumerate(PRESETS, 1):
        print(f"  {i}. {desc}")
    print("  0. 自定义路径")
    print()

    choices = [str(i) for i in range(len(PRESETS) + 1)]
    p = ask("请选择 [1]: ", "1", choices=choices)

    if p == "0":
        path = ask("请输入 JSON 文件路径: ")
        return path

    return str(PRESETS_DIR / PRESETS[int(p) - 1][0])


if __name__ == "__main__":
    try:
        while menu():
            pass
    except KeyboardInterrupt:
        print("\n\n已取消。")
        sys.exit(0)
