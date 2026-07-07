#!/usr/bin/env python3
"""Download a URL with report-first behavior and size/type checks."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import urllib.parse
import urllib.request
from pathlib import Path

from common import ensure_dir, env_size_limit, print_report, redact_text, resolve_mode, utc_timestamp, write_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Safely download a remote file.")
    parser.add_argument("url", help="Remote URL to inspect or download.")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--out", type=Path, help="Output file path.")
    parser.add_argument("--max-bytes", type=int, default=env_size_limit(), help="Maximum allowed download size.")
    return parser.parse_args()


def inspect(url: str) -> dict[str, str | int | None]:
    request = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(request) as response:
            return {
                "content_type": response.headers.get("Content-Type"),
                "content_length": int(response.headers.get("Content-Length", "0") or "0"),
                "final_url": response.geturl(),
            }
    except Exception:
        return {
            "content_type": None,
            "content_length": 0,
            "final_url": url,
        }


def default_out(url: str) -> Path:
    parsed = urllib.parse.urlparse(url)
    name = Path(parsed.path).name or "download.bin"
    return Path(name)


def main() -> int:
    args = parse_args()
    mode = resolve_mode(args)
    summary = inspect(args.url)
    target = args.out or default_out(args.url)
    report = {
        "mode": mode,
        "session_timestamp": utc_timestamp(),
        "url": redact_text(args.url),
        "final_url": redact_text(str(summary["final_url"])),
        "content_type": summary["content_type"],
        "content_length": summary["content_length"],
        "max_bytes": args.max_bytes,
        "suggested_output": str(target),
        "warnings": [],
    }
    if summary["content_length"] and int(summary["content_length"]) > args.max_bytes:
        report["warnings"].append("content length exceeds max-bytes limit")
    if not summary["content_type"]:
        report["warnings"].append("content type could not be determined from HEAD request")
    print_report(report)

    if mode != "execute":
        return 0

    ensure_dir(target.parent)
    with urllib.request.urlopen(args.url) as response:
        payload = response.read(args.max_bytes + 1)
    if len(payload) > args.max_bytes:
        raise SystemExit("Download aborted: payload exceeds max-bytes limit.")
    target.write_bytes(payload)
    meta = {
        "session_timestamp": utc_timestamp(),
        "url": args.url,
        "saved_to": str(target),
        "size_bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "mime_guess": mimetypes.guess_type(target.name)[0],
    }
    write_text(target.with_suffix(target.suffix + ".meta.json"), json.dumps(meta, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
