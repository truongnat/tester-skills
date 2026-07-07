#!/usr/bin/env python3
"""Redact sensitive values inside a Postman environment export."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import ensure_dir, exit_if_missing, file_summary, print_report, redact_text, resolve_mode, utc_timestamp, write_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Redact sensitive values in a Postman environment JSON file.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--out", type=Path, help="Output file for redacted environment JSON.")
    return parser.parse_args()


def load_env(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "values" not in data:
        raise SystemExit("Invalid Postman environment: missing 'values' key.")
    return data


def redact_env(data: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    redacted = json.loads(json.dumps(data))
    changes = []
    for item in redacted.get("values", []):
        if not isinstance(item, dict):
            continue
        key = str(item.get("key", ""))
        value = item.get("value", "")
        raw_value = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
        new_value = redact_text(raw_value)
        lowered = key.lower()
        forced = any(token in lowered for token in ("token", "secret", "password", "key", "auth"))
        if new_value != raw_value or forced:
            item["value"] = "[REDACTED]"
            changes.append({"key": key, "enabled": item.get("enabled"), "type": item.get("type")})
    return redacted, changes


def main() -> int:
    args = parse_args()
    mode = resolve_mode(args)
    exit_if_missing(args.input)
    data = load_env(args.input)
    redacted, changes = redact_env(data)
    target = args.out or args.input.with_name(f"{args.input.stem}.redacted{args.input.suffix}")
    report = {
        "mode": mode,
        "session_timestamp": utc_timestamp(),
        "input": file_summary(args.input),
        "variable_count": len(data.get("values", [])),
        "redacted_count": len(changes),
        "redacted_keys": changes[:20],
        "suggested_output": str(target),
        "will_write": [str(target)] if mode == "execute" else [],
    }
    print_report(report)

    if mode == "execute":
        ensure_dir(target.parent)
        write_text(target, json.dumps(redacted, indent=2, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
