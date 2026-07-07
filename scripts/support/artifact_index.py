#!/usr/bin/env python3
"""Build a daily artifact index from artifacts/YYYY-MM-DD/*."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import ARTIFACTS_ROOT, ensure_dir, print_report, resolve_mode, utc_timestamp, write_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Index artifact runs for a report date.")
    parser.add_argument("report_date", help="Date in YYYY-MM-DD format.")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--out", type=Path, help="Output directory or file location.")
    return parser.parse_args()


def build_index(root: Path) -> dict[str, Any]:
    entries = []
    for skill_dir in sorted(path for path in root.iterdir() if path.is_dir()):
        runs = []
        for run_dir in sorted(path for path in skill_dir.iterdir() if path.is_dir()):
            files = sorted(str(p.relative_to(root)) for p in run_dir.rglob("*") if p.is_file())
            runs.append(
                {
                    "run": run_dir.name,
                    "file_count": len(files),
                    "files": files[:20],
                }
            )
        entries.append(
            {
                "skill": skill_dir.name,
                "run_count": len(runs),
                "runs": runs,
            }
        )
    return {
        "skills": entries,
        "skill_count": len(entries),
        "run_count": sum(entry["run_count"] for entry in entries),
    }


def to_markdown(report_date: str, data: dict[str, Any]) -> str:
    lines = [
        f"Session timestamp: {utc_timestamp()}",
        f"Report date: {report_date}",
        "",
        "| Skill | Run count | Example files |",
        "|---|---:|---|",
    ]
    for skill in data["skills"]:
        example_files = ", ".join(skill["runs"][0]["files"][:3]) if skill["runs"] else ""
        lines.append(f"| {skill['skill']} | {skill['run_count']} | {example_files} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    mode = resolve_mode(args)
    day_root = ARTIFACTS_ROOT / args.report_date
    exists = day_root.exists()
    data = build_index(day_root) if exists else {"skills": [], "skill_count": 0, "run_count": 0}
    report = {
        "mode": mode,
        "session_timestamp": utc_timestamp(),
        "report_date": args.report_date,
        "artifact_root": str(day_root),
        "exists": exists,
        "summary": {
            "skill_count": data["skill_count"],
            "run_count": data["run_count"],
        },
        "skills": data["skills"][:10],
        "will_write": ["artifact-index.json", "artifact-index.md"] if mode == "execute" else [],
    }
    print_report(report)

    if mode == "execute":
        out_dir = args.out or day_root / "_index"
        ensure_dir(out_dir)
        write_text(out_dir / "artifact-index.json", json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        write_text(out_dir / "artifact-index.md", to_markdown(args.report_date, data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
