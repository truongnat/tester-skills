#!/usr/bin/env python3
"""Flatten JSON data into a Markdown table."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import ensure_dir, exit_if_missing, file_summary, print_report, resolve_mode, utc_timestamp, write_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert JSON object or list to a Markdown table.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--out", type=Path, help="Output Markdown path.")
    parser.add_argument("--limit", type=int, default=50, help="Max row count to write.")
    return parser.parse_args()


def flatten(value: Any, prefix: str = "") -> dict[str, str]:
    rows: dict[str, str] = {}
    if isinstance(value, dict):
        for key, item in value.items():
            next_prefix = f"{prefix}.{key}" if prefix else str(key)
            rows.update(flatten(item, next_prefix))
    elif isinstance(value, list):
        if not value:
            rows[prefix or "$"] = "[]"
        else:
            for index, item in enumerate(value):
                next_prefix = f"{prefix}[{index}]" if prefix else f"[{index}]"
                rows.update(flatten(item, next_prefix))
    else:
        rows[prefix or "$"] = json.dumps(value, ensure_ascii=False)
    return rows


def to_rows(data: Any) -> list[list[str]]:
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        keys = sorted({key for item in data for key in item.keys()})
        rows = [keys]
        for item in data:
            rows.append([json.dumps(item.get(key), ensure_ascii=False) if not isinstance(item.get(key), str) else item.get(key) for key in keys])
        return rows
    flattened = flatten(data)
    return [["Path", "Value"]] + [[key, value] for key, value in flattened.items()]


def to_markdown(rows: list[list[str]], limit: int) -> str:
    trimmed = rows[: limit + 1]
    header = trimmed[0]
    lines = [
        f"Session timestamp: {utc_timestamp()}",
        "",
        "| " + " | ".join(header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for row in trimmed[1:]:
        lines.append("| " + " | ".join(str(cell).replace("\n", "\\n") for cell in row) + " |")
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    mode = resolve_mode(args)
    exit_if_missing(args.input)
    data = json.loads(args.input.read_text(encoding="utf-8"))
    rows = to_rows(data)
    target = args.out or args.input.with_suffix(".md")
    report = {
        "mode": mode,
        "session_timestamp": utc_timestamp(),
        "input": file_summary(args.input),
        "row_count": max(0, len(rows) - 1),
        "column_count": len(rows[0]) if rows else 0,
        "preview": rows[:5],
        "suggested_output": str(target),
        "will_write": [str(target)] if mode == "execute" else [],
    }
    print_report(report)

    if mode == "execute":
        ensure_dir(target.parent)
        write_text(target, to_markdown(rows, args.limit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
