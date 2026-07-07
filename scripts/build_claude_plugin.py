#!/usr/bin/env python3
"""Build a clean Claude Code plugin package from the repository skills."""

from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST_ROOT = ROOT / "dist"
PLUGIN_NAME = "tester-skills-plugin"
PLUGIN_DIR = DIST_ROOT / PLUGIN_NAME


def find_skill_dirs() -> list[Path]:
    ignored = {".git", ".claude", ".claude-plugin", "artifacts", "dist", "docs", "scripts"}
    return sorted(
        path
        for path in ROOT.iterdir()
        if path.is_dir()
        and path.name not in ignored
        and (path / "SKILL.md").is_file()
    )


def write_manifest(plugin_dir: Path) -> None:
    manifest = {
        "name": "tester-skills",
        "displayName": "Tester Skills",
        "version": "1.0.0",
        "description": (
            "A Vietnamese skill pack for manual testers covering requirements, "
            "test cases, API testing, test strategy, exploratory testing, defect "
            "reporting, investigation, and QA reporting."
        ),
        "author": {"name": "truongnat"},
        "repository": "https://github.com/truongnat/tester-skills",
        "license": "MIT",
        "keywords": [
            "qa",
            "testing",
            "manual-testing",
            "api-testing",
            "test-cases",
            "bug-reporting",
        ],
    }
    manifest_dir = plugin_dir / ".claude-plugin"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    (manifest_dir / "plugin.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )


def zip_dir(source_dir: Path, zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(source_dir.parent))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Claude Code plugin bundle.")
    parser.add_argument(
        "--no-zip",
        action="store_true",
        help="Only build the plugin directory, do not create a zip archive.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skills = find_skill_dirs()
    if not skills:
        print("No skill folders found.")
        return 1

    if PLUGIN_DIR.exists():
        shutil.rmtree(PLUGIN_DIR)

    skills_dir = PLUGIN_DIR / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    write_manifest(PLUGIN_DIR)

    for skill_dir in skills:
        shutil.copytree(skill_dir, skills_dir / skill_dir.name)

    readme = PLUGIN_DIR / "README.md"
    readme.write_text(
        "# Tester Skills Plugin\n\n"
        "Load with:\n\n"
        "```bash\n"
        "claude --plugin-dir ./dist/tester-skills-plugin\n"
        "```\n\n"
        "Then invoke skills with `/tester-skills:<skill-name>`.\n",
        encoding="utf-8",
    )

    print(f"Built plugin directory: {PLUGIN_DIR}")
    print(f"Included {len(skills)} skills.")

    if not args.no_zip:
        zip_path = DIST_ROOT / f"{PLUGIN_NAME}.zip"
        zip_dir(PLUGIN_DIR, zip_path)
        print(f"Built plugin zip: {zip_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
