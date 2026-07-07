#!/usr/bin/env python3
"""Create a normalized manifest for evidence files."""

from __future__ import annotations

import argparse
import json
import mimetypes
from pathlib import Path
from typing import Any

from common import ensure_dir, file_summary, print_report, resolve_mode, sensitive_matches, utc_timestamp, write_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create an evidence manifest from files.")
    parser.add_argument("inputs", nargs="+", type=Path, help="Evidence files to include.")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--out", type=Path, help="Output directory or manifest path.")
    parser.add_argument("--title", default="evidence", help="Short evidence set title.")
    return parser.parse_args()


def summarize_file(path: Path) -> dict[str, Any]:
    info = file_summary(path)
    info["mime_guess"] = mimetypes.guess_type(path.name)[0]
    if path.suffix.lower() in {".txt", ".log", ".json", ".md", ".har"}:
        text = path.read_text(encoding="utf-8", errors="replace")
        info["sensitive_match_counts"] = sensitive_matches(text)
    return info


def main() -> int:
    args = parse_args()
    mode = resolve_mode(args)
    files = [summarize_file(path) for path in args.inputs]
    report = {
        "mode": mode,
        "session_timestamp": utc_timestamp(),
        "title": args.title,
        "file_count": len(files),
        "files": files,
        "will_write": ["evidence-manifest.json"] if mode == "execute" else [],
    }
    print_report(report)

    if mode == "execute":
        target = args.out or Path.cwd() / "evidence-output"
        if target.suffix.lower() == ".json":
            ensure_dir(target.parent)
            manifest_path = target
        else:
            ensure_dir(target)
            manifest_path = target / "evidence-manifest.json"
        write_text(
            manifest_path,
            json.dumps(
                {
                    "session_timestamp": utc_timestamp(),
                    "title": args.title,
                    "file_count": len(files),
                    "files": files,
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
