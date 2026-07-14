#!/usr/bin/env python3
"""从 skill 内置模板安全地初始化中文研究工作区。"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="初始化研究构想工作区；保留所有已有文件。")
    parser.add_argument("--path", required=True, help="目标工作区目录")
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parent.parent
    template_dir = skill_dir / "assets" / "工作区模板"
    target_dir = Path(args.path).expanduser().resolve()

    if not template_dir.is_dir():
        raise SystemExit(f"找不到工作区模板：{template_dir}")

    target_dir.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    preserved: list[str] = []

    for source in sorted(template_dir.iterdir(), key=lambda item: item.name):
        if not source.is_file():
            continue
        target = target_dir / source.name
        if target.exists():
            preserved.append(source.name)
            continue
        shutil.copy2(source, target)
        created.append(source.name)

    print(f"工作区：{target_dir}")
    print("新建：" + ("、".join(created) if created else "无"))
    print("保留：" + ("、".join(preserved) if preserved else "无"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
