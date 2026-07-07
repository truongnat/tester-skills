#!/usr/bin/env python3
"""Package an artifact directory into a zip file."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

from common import ensure_dir, exit_if_missing, file_summary, print_report, resolve_mode, utc_timestamp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Package an artifact directory into a zip archive.")
    parser.add_argument("input", type=Path, help="Artifact directory to package.")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--out", type=Path, help="Output zip path.")
    return parser.parse_args()


def list_files(root: Path) -> list[str]:
    files = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if "_timeline" in relative.parts:
            continue
        files.append(str(relative))
    return sorted(files)


def write_zip(source_dir: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                relative = path.relative_to(source_dir)
                if "_timeline" in relative.parts:
                    continue
                archive.write(path, relative)


def main() -> int:
    args = parse_args()
    mode = resolve_mode(args)
    exit_if_missing(args.input)
    if not args.input.is_dir():
        raise SystemExit("Input must be an artifact directory.")
    files = list_files(args.input)
    target = args.out or args.input.with_suffix(".zip")
    report = {
        "mode": mode,
        "session_timestamp": utc_timestamp(),
        "input": file_summary(args.input),
        "file_count": len(files),
        "preview_files": files[:20],
        "suggested_output": str(target),
        "will_write": [str(target)] if mode == "execute" else [],
    }
    print_report(report)

    if mode == "execute":
        ensure_dir(target.parent)
        write_zip(args.input, target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
