#!/usr/bin/env python3
"""Parse a Postman collection and summarize requests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import ensure_dir, exit_if_missing, file_summary, print_report, redact_text, resolve_mode, utc_timestamp, write_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse a Postman collection JSON file.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--out", type=Path, help="Output directory for summaries.")
    return parser.parse_args()


def load_collection(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "item" not in data:
        raise SystemExit("Invalid Postman collection: missing 'item' root key.")
    return data


def summarize_item(item: dict[str, Any], folder: str = "") -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    name = item.get("name", "")
    full_name = f"{folder} / {name}".strip(" /")

    if "item" in item:
        for child in item["item"]:
            results.extend(summarize_item(child, full_name))
        return results

    request = item.get("request", {})
    method = request.get("method", "")
    url = request.get("url", {})
    raw_url = url.get("raw") if isinstance(url, dict) else str(url)
    headers = request.get("header", []) or []
    auth = request.get("auth") or {}
    body = request.get("body") or {}
    results.append(
        {
            "name": full_name or name,
            "method": method,
            "url": redact_text(raw_url or ""),
            "header_count": len(headers),
            "auth_type": auth.get("type"),
            "body_mode": body.get("mode"),
        }
    )
    return results


def summarize_collection(data: dict[str, Any]) -> dict[str, Any]:
    info = data.get("info", {})
    requests: list[dict[str, Any]] = []
    for item in data.get("item", []):
        requests.extend(summarize_item(item))
    variables = data.get("variable", []) or []
    auth = data.get("auth") or {}
    return {
        "name": info.get("name"),
        "schema": info.get("schema"),
        "request_count": len(requests),
        "variable_names": sorted(v.get("key") for v in variables if isinstance(v, dict) and v.get("key")),
        "collection_auth_type": auth.get("type"),
        "requests": requests,
    }


def to_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"Session timestamp: {utc_timestamp()}",
        f"Collection: {summary.get('name')}",
        f"Schema: {summary.get('schema')}",
        f"Request count: {summary.get('request_count')}",
        f"Variables: {summary.get('variable_names')}",
        f"Collection auth: {summary.get('collection_auth_type')}",
        "",
        "| Name | Method | URL | Headers | Auth | Body mode |",
        "|---|---|---|---:|---|---|",
    ]
    for req in summary["requests"]:
        lines.append(
            f"| {req['name']} | {req['method']} | {req['url']} | {req['header_count']} | {req['auth_type']} | {req['body_mode']} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    mode = resolve_mode(args)
    exit_if_missing(args.input)
    data = load_collection(args.input)
    summary = summarize_collection(data)
    report = {
        "mode": mode,
        "session_timestamp": utc_timestamp(),
        "input": file_summary(args.input),
        "summary": {
            key: value for key, value in summary.items() if key != "requests"
        },
        "first_requests": summary["requests"][:10],
        "will_write": ["summary.md", "requests.json"] if mode == "execute" else [],
    }
    print_report(report)

    if mode == "execute":
        out_dir = args.out or args.input.parent / f"{args.input.stem}-postman"
        ensure_dir(out_dir)
        write_text(out_dir / "summary.md", to_markdown(summary))
        write_text(out_dir / "requests.json", json.dumps(summary["requests"], indent=2, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
