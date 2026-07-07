#!/usr/bin/env python3
"""Install this repository's SKILL.md folders into a Claude skills directory."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_USER_TARGET = Path.home() / ".claude" / "skills"
DEFAULT_PROJECT_TARGET = ROOT / ".claude" / "skills"


def find_skill_dirs() -> list[Path]:
    ignored = {".git", ".claude", ".claude-plugin", "artifacts", "dist", "docs", "scripts"}
    return sorted(
        path
        for path in ROOT.iterdir()
        if path.is_dir()
        and path.name not in ignored
        and (path / "SKILL.md").is_file()
    )


def install_skill(skill_dir: Path, target_root: Path, force: bool, dry_run: bool) -> str:
    destination = target_root / skill_dir.name

    if destination.exists():
        if not force:
            return f"skip existing {destination} (use --force to replace)"
        if not dry_run:
            shutil.rmtree(destination)

    if not dry_run:
        shutil.copytree(skill_dir, destination)

    return f"install {skill_dir.name} -> {destination}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install tester skills for Claude.")
    parser.add_argument(
        "--scope",
        choices=("user", "project"),
        default="user",
        help="Install to ~/.claude/skills or this repo's .claude/skills.",
    )
    parser.add_argument(
        "--target",
        type=Path,
        help="Custom target skills directory. Overrides --scope.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing skill folders with the same names.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without copying files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target = args.target or (
        DEFAULT_USER_TARGET if args.scope == "user" else DEFAULT_PROJECT_TARGET
    )
    target = target.expanduser().resolve()

    skills = find_skill_dirs()
    if not skills:
        print("No skill folders found.")
        return 1

    if not args.dry_run:
        target.mkdir(parents=True, exist_ok=True)

    print(f"Target: {target}")
    for skill_dir in skills:
        print(install_skill(skill_dir, target, args.force, args.dry_run))

    print(f"Installed {len(skills)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
