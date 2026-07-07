#!/usr/bin/env python3
"""Initialize an artifact directory with metadata."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import artifact_dir, ensure_dir, print_report, resolve_mode, utc_timestamp, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize an artifact folder for a skill run.")
    parser.add_argument("skill", help="Skill name, e.g. bug-report-writer")
    parser.add_argument("topic", help="Short topic, e.g. login-error")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--out", type=Path, help="Override artifact directory path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mode = resolve_mode(args)
    session_timestamp = utc_timestamp()
    target = args.out or artifact_dir(args.skill, args.topic, session_timestamp)
    report = {
        "mode": mode,
        "session_timestamp": session_timestamp,
        "skill": args.skill,
        "topic": args.topic,
        "artifact_dir": str(target),
        "will_write": ["metadata.json"] if mode == "execute" else [],
    }
    print_report(report)

    if mode == "execute":
        ensure_dir(target)
        write_json(
            target / "metadata.json",
            {
                "session_timestamp": session_timestamp,
                "skill": args.skill,
                "topic": args.topic,
                "artifact_dir": str(target),
            },
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
