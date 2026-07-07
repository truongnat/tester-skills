#!/usr/bin/env python3
"""Install tester skills from GitHub without cloning the repository."""

from __future__ import annotations

import argparse
import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path


DEFAULT_REPO_ZIP = "https://github.com/truongnat/tester-skills/archive/refs/heads/main.zip"
DEFAULT_TARGET = Path.home() / ".claude" / "skills"


def download(url: str, destination: Path) -> None:
    with urllib.request.urlopen(url) as response:
        destination.write_bytes(response.read())


def find_repo_root(extract_dir: Path) -> Path:
    candidates = [path for path in extract_dir.iterdir() if path.is_dir()]
    if len(candidates) == 1:
        return candidates[0]
    return extract_dir


def find_skill_dirs(repo_root: Path) -> list[Path]:
    ignored = {".git", ".claude", ".claude-plugin", "artifacts", "dist", "docs", "scripts"}
    roots = [repo_root]
    if (repo_root / "skills").is_dir():
        roots.insert(0, repo_root / "skills")

    skills: list[Path] = []
    for root in roots:
        skills.extend(
            path
            for path in root.iterdir()
            if path.is_dir()
            and path.name not in ignored
            and (path / "SKILL.md").is_file()
        )

    deduped = {path.name: path for path in skills}
    return sorted(
        deduped.values(),
        key=lambda path: path.name,
    )


def install_skill(skill_dir: Path, target_root: Path, force: bool) -> str:
    destination = target_root / skill_dir.name
    if destination.exists():
        if not force:
            return f"skip existing {destination} (use --force to replace)"
        shutil.rmtree(destination)
    shutil.copytree(skill_dir, destination)
    return f"install {skill_dir.name} -> {destination}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install tester skills from GitHub.")
    parser.add_argument("--url", default=DEFAULT_REPO_ZIP, help="Repository zip URL to install from.")
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET, help="Claude skills target directory.")
    parser.add_argument("--force", action="store_true", help="Replace existing skill folders.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target = args.target.expanduser().resolve()

    with tempfile.TemporaryDirectory(prefix="tester-skills-") as temp_name:
        temp_dir = Path(temp_name)
        archive_path = temp_dir / "repo.zip"
        extract_dir = temp_dir / "repo"

        print(f"Downloading {args.url}")
        download(args.url, archive_path)

        extract_dir.mkdir()
        with zipfile.ZipFile(archive_path) as archive:
            archive.extractall(extract_dir)

        repo_root = find_repo_root(extract_dir)
        skills = find_skill_dirs(repo_root)
        if not skills:
            print("No skill folders found in downloaded archive.")
            return 1

        target.mkdir(parents=True, exist_ok=True)
        print(f"Target: {target}")
        for skill_dir in skills:
            print(install_skill(skill_dir, target, args.force))

    print("Restart Claude or run /reload-plugins if your client supports it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
