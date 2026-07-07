#!/usr/bin/env python3
"""Build a timeline from artifact files in a single run directory."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

from common import ensure_dir, exit_if_missing, file_summary, print_report, resolve_mode, utc_timestamp, write_text


TIMESTAMP_RE = re.compile(r"Session timestamp:\s*(.+)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a timeline from an artifact run directory.")
    parser.add_argument("input", type=Path, help="Artifact run directory.")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--out", type=Path, help="Output directory for timeline files.")
    return parser.parse_args()


def read_session_timestamp(path: Path) -> str | None:
    if path.suffix.lower() not in {".md", ".txt", ".log"}:
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    match = TIMESTAMP_RE.search(text)
    return match.group(1).strip() if match else None


def build_timeline(root: Path) -> list[dict[str, str | None]]:
    entries = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if "_timeline" in path.relative_to(root).parts:
            continue
        entries.append(
            {
                "file": str(path.relative_to(root)),
                "session_timestamp": read_session_timestamp(path),
                "modified_time": datetime.fromtimestamp(path.stat().st_mtime).astimezone().strftime("%Y-%m-%d %H:%M:%S %z"),
            }
        )
    return entries


def to_markdown(entries: list[dict[str, str | None]]) -> str:
    lines = [
        f"Session timestamp: {utc_timestamp()}",
        "",
        "| File | Session timestamp | Modified time |",
        "|---|---|---|",
    ]
    for item in entries:
        lines.append(f"| {item['file']} | {item['session_timestamp']} | {item['modified_time']} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    mode = resolve_mode(args)
    exit_if_missing(args.input)
    if not args.input.is_dir():
        raise SystemExit("Input must be an artifact run directory.")
    entries = build_timeline(args.input)
    report = {
        "mode": mode,
        "session_timestamp": utc_timestamp(),
        "input": file_summary(args.input),
        "file_count": len(entries),
        "timeline_preview": entries[:20],
        "will_write": ["timeline.json", "timeline.md"] if mode == "execute" else [],
    }
    print_report(report)

    if mode == "execute":
        out_dir = args.out or args.input / "_timeline"
        ensure_dir(out_dir)
        write_text(out_dir / "timeline.json", json.dumps(entries, indent=2, ensure_ascii=False) + "\n")
        write_text(out_dir / "timeline.md", to_markdown(entries))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
