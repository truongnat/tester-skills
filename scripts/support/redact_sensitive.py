#!/usr/bin/env python3
"""Detect and redact common sensitive values from text files."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import ensure_dir, exit_if_missing, file_summary, print_report, redact_text, resolve_mode, sensitive_matches, utc_timestamp, write_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Redact common sensitive values from a text file.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--out", type=Path, help="Output file path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mode = resolve_mode(args)
    exit_if_missing(args.input)
    text = args.input.read_text(encoding="utf-8", errors="replace")
    matches = sensitive_matches(text)
    target = args.out or args.input.with_name(f"{args.input.stem}.redacted{args.input.suffix}")
    report = {
        "mode": mode,
        "session_timestamp": utc_timestamp(),
        "input": file_summary(args.input),
        "match_counts": matches,
        "suggested_output": str(target),
        "will_write": [str(target)] if mode == "execute" else [],
    }
    print_report(report)

    if mode == "execute":
        ensure_dir(target.parent)
        write_text(target, redact_text(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
