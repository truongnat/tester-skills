#!/usr/bin/env python3
"""Shared helpers for support scripts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_ROOT = ROOT / "artifacts"
SENSITIVE_PATTERNS = {
    "bearer_token": re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._-]+\b"),
    "api_key": re.compile(r"(?i)\b(api[-_ ]?key|token|secret)\b\s*[:=]\s*[^\s,;]+"),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "phone": re.compile(r"(?<!\d)(?:\+?84|0)(?:\d[ .-]?){8,10}(?!\d)"),
}


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-") or "run"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sensitive_matches(text: str) -> dict[str, int]:
    return {name: len(pattern.findall(text)) for name, pattern in SENSITIVE_PATTERNS.items()}


def redact_text(text: str) -> str:
    redacted = text
    for name, pattern in SENSITIVE_PATTERNS.items():
        redacted = pattern.sub(f"[REDACTED_{name.upper()}]", redacted)
    return redacted


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def artifact_dir(skill: str, topic: str, timestamp: str | None = None) -> Path:
    local = datetime.now().astimezone() if timestamp is None else datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S %z")
    date_part = local.strftime("%Y-%m-%d")
    time_part = local.strftime("%H%M%S")
    return ARTIFACTS_ROOT / date_part / skill / f"{time_part}-{slugify(topic)}"


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def print_report(data: dict[str, Any]) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def base_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--report", action="store_true", help="Print a pre-execution report and exit.")
    mode.add_argument("--execute", action="store_true", help="Perform the write action after reporting.")
    parser.add_argument("--out", type=Path, help="Output file or artifact directory.")
    parser.add_argument("--topic", default="run", help="Topic slug for artifact folder naming.")
    return parser


def resolve_mode(args: argparse.Namespace) -> str:
    return "execute" if args.execute else "report"


def file_summary(path: Path) -> dict[str, Any]:
    info = {
        "path": str(path),
        "exists": path.exists(),
    }
    if path.exists():
        stat = path.stat()
        info.update(
            {
                "size_bytes": stat.st_size,
                "extension": path.suffix.lower(),
                "kind": "directory" if path.is_dir() else "file",
            }
        )
        if path.is_file():
            info["sha256"] = sha256_file(path)
    return info


def detect_dependency(module_name: str) -> bool:
    try:
        __import__(module_name)
        return True
    except Exception:
        return False


def exit_if_missing(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Input not found: {path}")


def env_size_limit(default_mb: int = 25) -> int:
    raw = os.getenv("TESTER_SKILLS_MAX_MB", str(default_mb))
    try:
        return max(1, int(raw)) * 1024 * 1024
    except ValueError:
        return default_mb * 1024 * 1024
