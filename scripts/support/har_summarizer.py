#!/usr/bin/env python3
"""Summarize requests inside a HAR file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import ensure_dir, exit_if_missing, file_summary, print_report, redact_text, resolve_mode, utc_timestamp, write_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize requests from a HAR file.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--out", type=Path, help="Output directory for HAR summaries.")
    parser.add_argument("--limit", type=int, default=30, help="Max entries to include in report preview.")
    return parser.parse_args()


def load_har(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "log" not in data:
        raise SystemExit("Invalid HAR file: missing 'log' object.")
    return data


def summarize_entry(entry: dict[str, Any]) -> dict[str, Any]:
    request = entry.get("request", {}) or {}
    response = entry.get("response", {}) or {}
    timings = entry.get("timings", {}) or {}
    content = response.get("content", {}) or {}
    return {
        "started": entry.get("startedDateTime"),
        "method": request.get("method"),
        "url": redact_text(request.get("url", "")),
        "status": response.get("status"),
        "mime_type": content.get("mimeType"),
        "time_ms": entry.get("time"),
        "wait_ms": timings.get("wait"),
        "receive_ms": timings.get("receive"),
    }


def summarize_har(data: dict[str, Any]) -> dict[str, Any]:
    entries = [summarize_entry(entry) for entry in data.get("log", {}).get("entries", [])]
    status_counts: dict[str, int] = {}
    host_counts: dict[str, int] = {}
    for item in entries:
        status_key = str(item.get("status"))
        status_counts[status_key] = status_counts.get(status_key, 0) + 1
        url = item.get("url") or ""
        host = url.split("/")[2] if "://" in url and len(url.split("/")) > 2 else ""
        if host:
            host_counts[host] = host_counts.get(host, 0) + 1
    slowest = sorted(entries, key=lambda item: item.get("time_ms") or 0, reverse=True)[:10]
    return {
        "entry_count": len(entries),
        "status_counts": status_counts,
        "host_counts": dict(sorted(host_counts.items(), key=lambda item: item[1], reverse=True)[:10]),
        "slowest_entries": slowest,
        "entries": entries,
    }


def to_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"Session timestamp: {utc_timestamp()}",
        f"Entry count: {summary['entry_count']}",
        f"Status counts: {summary['status_counts']}",
        f"Host counts: {summary['host_counts']}",
        "",
        "| Started | Method | URL | Status | Time ms | MIME |",
        "|---|---|---|---:|---:|---|",
    ]
    for item in summary["slowest_entries"]:
        lines.append(
            f"| {item.get('started')} | {item.get('method')} | {item.get('url')} | {item.get('status')} | {item.get('time_ms')} | {item.get('mime_type')} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    mode = resolve_mode(args)
    exit_if_missing(args.input)
    if args.input.suffix.lower() != ".har":
        raise SystemExit("Unsupported file type. Use a .har input.")
    data = load_har(args.input)
    summary = summarize_har(data)
    report = {
        "mode": mode,
        "session_timestamp": utc_timestamp(),
        "input": file_summary(args.input),
        "summary": {
            "entry_count": summary["entry_count"],
            "status_counts": summary["status_counts"],
            "host_counts": summary["host_counts"],
        },
        "preview_entries": summary["entries"][: args.limit],
        "will_write": ["summary.md", "entries.json"] if mode == "execute" else [],
    }
    print_report(report)

    if mode == "execute":
        out_dir = args.out or args.input.parent / f"{args.input.stem}-har"
        ensure_dir(out_dir)
        write_text(out_dir / "summary.md", to_markdown(summary))
        write_text(out_dir / "entries.json", json.dumps(summary["entries"], indent=2, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
