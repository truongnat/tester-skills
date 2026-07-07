#!/usr/bin/env python3
"""Convert a simple Markdown table to CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from common import ensure_dir, exit_if_missing, file_summary, print_report, resolve_mode, utc_timestamp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert a Markdown table to CSV.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--out", type=Path, help="Output CSV path.")
    return parser.parse_args()


def parse_markdown_table(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if cells and all(set(cell) <= {"-", ":"} for cell in cells):
            continue
        rows.append(cells)
    return rows


def main() -> int:
    args = parse_args()
    mode = resolve_mode(args)
    exit_if_missing(args.input)
    text = args.input.read_text(encoding="utf-8")
    rows = parse_markdown_table(text)
    target = args.out or args.input.with_suffix(".csv")
    report = {
        "mode": mode,
        "session_timestamp": utc_timestamp(),
        "input": file_summary(args.input),
        "row_count": len(rows),
        "column_count": len(rows[0]) if rows else 0,
        "preview": rows[:5],
        "suggested_output": str(target),
        "will_write": [str(target)] if mode == "execute" else [],
    }
    print_report(report)

    if mode == "execute":
        ensure_dir(target.parent)
        with target.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
