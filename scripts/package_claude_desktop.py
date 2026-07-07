#!/usr/bin/env python3
"""Package skills as zip files for manual upload in Claude Desktop/Web."""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "dist" / "claude-desktop-skills"


def find_skill_dirs() -> list[Path]:
    ignored = {".git", ".claude", ".claude-plugin", "artifacts", "dist", "docs", "scripts"}
    return sorted(
        path
        for path in ROOT.iterdir()
        if path.is_dir()
        and path.name not in ignored
        and (path / "SKILL.md").is_file()
    )


def add_dir_to_zip(archive: zipfile.ZipFile, source_dir: Path, base_dir: Path) -> None:
    for path in sorted(source_dir.rglob("*")):
        if path.is_file():
            archive.write(path, path.relative_to(base_dir))


def main() -> int:
    skills = find_skill_dirs()
    if not skills:
        print("No skill folders found.")
        return 1

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for skill_dir in skills:
        zip_path = OUTPUT_DIR / f"{skill_dir.name}.zip"
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            add_dir_to_zip(archive, skill_dir, ROOT)
        print(f"Created {zip_path}")

    all_zip = OUTPUT_DIR / "tester-skills-all.zip"
    with zipfile.ZipFile(all_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for skill_dir in skills:
            add_dir_to_zip(archive, skill_dir, ROOT)
    print(f"Created {all_zip}")
    print(f"Packaged {len(skills)} skills for Claude Desktop/Web upload.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
