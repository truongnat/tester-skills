#!/usr/bin/env python3
"""Compare actual and expected JSON structures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import ensure_dir, exit_if_missing, file_summary, print_report, resolve_mode, utc_timestamp, write_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two JSON files.")
    parser.add_argument("actual", type=Path)
    parser.add_argument("expected", type=Path)
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--out", type=Path, help="Output directory for diff files.")
    return parser.parse_args()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def diff(actual: Any, expected: Any, path: str = "$") -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if type(actual) is not type(expected):
        issues.append({"path": path, "issue": "type_mismatch", "actual": type(actual).__name__, "expected": type(expected).__name__})
        return issues

    if isinstance(actual, dict):
        actual_keys = set(actual)
        expected_keys = set(expected)
        for key in sorted(expected_keys - actual_keys):
            issues.append({"path": f"{path}.{key}", "issue": "missing_field", "actual": "-", "expected": "present"})
        for key in sorted(actual_keys - expected_keys):
            issues.append({"path": f"{path}.{key}", "issue": "extra_field", "actual": "present", "expected": "-"})
        for key in sorted(actual_keys & expected_keys):
            issues.extend(diff(actual[key], expected[key], f"{path}.{key}"))
        return issues

    if isinstance(actual, list):
        if len(actual) != len(expected):
            issues.append({"path": path, "issue": "length_mismatch", "actual": str(len(actual)), "expected": str(len(expected))})
        for index, (actual_item, expected_item) in enumerate(zip(actual, expected)):
            issues.extend(diff(actual_item, expected_item, f"{path}[{index}]"))
        return issues

    if actual != expected:
        issues.append({"path": path, "issue": "value_mismatch", "actual": repr(actual), "expected": repr(expected)})
    return issues


def to_markdown(issues: list[dict[str, str]]) -> str:
    lines = [
        f"Session timestamp: {utc_timestamp()}",
        "",
        "| Path | Issue | Actual | Expected |",
        "|---|---|---|---|",
    ]
    for issue in issues:
        lines.append(f"| {issue['path']} | {issue['issue']} | {issue['actual']} | {issue['expected']} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    mode = resolve_mode(args)
    exit_if_missing(args.actual)
    exit_if_missing(args.expected)
    actual = load_json(args.actual)
    expected = load_json(args.expected)
    issues = diff(actual, expected)
    report = {
        "mode": mode,
        "session_timestamp": utc_timestamp(),
        "actual": file_summary(args.actual),
        "expected": file_summary(args.expected),
        "issue_count": len(issues),
        "issues_preview": issues[:20],
        "will_write": ["diff.md", "diff.json"] if mode == "execute" else [],
    }
    print_report(report)

    if mode == "execute":
        out_dir = args.out or args.actual.parent / f"{args.actual.stem}-json-diff"
        ensure_dir(out_dir)
        write_text(out_dir / "diff.md", to_markdown(issues))
        (out_dir / "diff.json").write_text(json.dumps(issues, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
