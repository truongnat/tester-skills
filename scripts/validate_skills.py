#!/usr/bin/env python3
"""Lightweight repository-local validator for SKILL.md files."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def skill_dirs() -> list[Path]:
    ignored = {".git", ".claude", ".claude-plugin", "artifacts", "dist", "docs", "scripts"}
    return sorted(
        path
        for path in ROOT.iterdir()
        if path.is_dir()
        and path.name not in ignored
        and (path / "SKILL.md").is_file()
    )


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("unterminated YAML frontmatter")

    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

    try:
        frontmatter = parse_frontmatter(text)
    except ValueError as exc:
        return [f"{skill_dir.name}: {exc}"]

    name = frontmatter.get("name")
    description = frontmatter.get("description")

    if not name:
        errors.append(f"{skill_dir.name}: missing frontmatter name")
    elif name != skill_dir.name:
        errors.append(f"{skill_dir.name}: name '{name}' must match folder name")
    elif not NAME_RE.match(name):
        errors.append(f"{skill_dir.name}: name must be kebab-case")

    if not description:
        errors.append(f"{skill_dir.name}: missing frontmatter description")
    elif len(description) < 40:
        errors.append(f"{skill_dir.name}: description is too short")

    if "[TODO" in text or "TODO:" in text:
        errors.append(f"{skill_dir.name}: contains TODO placeholder")

    return errors


def main() -> int:
    errors: list[str] = []
    skills = skill_dirs()

    for skill_dir in skills:
        errors.extend(validate_skill(skill_dir))

    if errors:
        for error in errors:
            print(error)
        return 1

    print(f"Validated {len(skills)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
