#!/usr/bin/env python3
"""Parse OpenAPI/Swagger specs and summarize endpoints."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import detect_dependency, ensure_dir, exit_if_missing, file_summary, print_report, resolve_mode, utc_timestamp, write_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse an OpenAPI spec from JSON or YAML.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--out", type=Path, help="Output directory for summaries.")
    return parser.parse_args()


def load_spec(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    if path.suffix.lower() in {".yaml", ".yml"}:
        if not detect_dependency("yaml"):
            raise SystemExit("YAML input requires PyYAML.")
        import yaml

        return yaml.safe_load(text)
    raise SystemExit("Unsupported spec format. Use .json, .yaml, or .yml")


def summarize(spec: dict[str, Any]) -> dict[str, Any]:
    info = spec.get("info", {})
    paths = spec.get("paths", {})
    endpoints = []
    for path, operations in paths.items():
        for method, payload in operations.items():
            if method.lower() not in {"get", "post", "put", "patch", "delete", "options", "head"}:
                continue
            endpoints.append(
                {
                    "method": method.upper(),
                    "path": path,
                    "summary": payload.get("summary") or payload.get("operationId") or "",
                    "responses": sorted((payload.get("responses") or {}).keys()),
                    "security": payload.get("security"),
                }
            )
    return {
        "title": info.get("title"),
        "version": info.get("version"),
        "openapi": spec.get("openapi") or spec.get("swagger"),
        "servers": [item.get("url") for item in spec.get("servers", []) if isinstance(item, dict)],
        "security_schemes": sorted((spec.get("components", {}).get("securitySchemes") or {}).keys()),
        "endpoint_count": len(endpoints),
        "endpoints": endpoints,
    }


def to_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"Session timestamp: {utc_timestamp()}",
        f"Title: {summary.get('title')}",
        f"Version: {summary.get('version')}",
        f"OpenAPI: {summary.get('openapi')}",
        f"Servers: {summary.get('servers')}",
        f"Security schemes: {summary.get('security_schemes')}",
        "",
        "| Method | Path | Summary | Responses |",
        "|---|---|---|---|",
    ]
    for endpoint in summary["endpoints"]:
        lines.append(
            f"| {endpoint['method']} | {endpoint['path']} | {endpoint['summary']} | {', '.join(endpoint['responses'])} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    mode = resolve_mode(args)
    exit_if_missing(args.input)
    spec = load_spec(args.input)
    summary = summarize(spec)
    report = {
        "mode": mode,
        "session_timestamp": utc_timestamp(),
        "input": file_summary(args.input),
        "summary": {
            key: value for key, value in summary.items() if key != "endpoints"
        },
        "first_endpoints": summary["endpoints"][:10],
        "will_write": ["summary.md", "endpoints.json"] if mode == "execute" else [],
    }
    print_report(report)

    if mode == "execute":
        out_dir = args.out or args.input.parent / f"{args.input.stem}-openapi"
        ensure_dir(out_dir)
        write_text(out_dir / "summary.md", to_markdown(summary))
        (out_dir / "endpoints.json").write_text(json.dumps(summary["endpoints"], indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
