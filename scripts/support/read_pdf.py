#!/usr/bin/env python3
"""Inspect PDF files and optionally extract text."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import detect_dependency, ensure_dir, exit_if_missing, file_summary, print_report, resolve_mode, utc_timestamp, write_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect a PDF and optionally extract text.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--out", type=Path, help="Output directory for extracted text.")
    parser.add_argument("--max-pages", type=int, default=10)
    return parser.parse_args()


def inspect_pdf(path: Path, max_pages: int) -> dict[str, object]:
    if not detect_dependency("pypdf"):
        return {
            "dependency_missing": "pypdf",
            "page_count": None,
            "extractable_pages": 0,
            "sample_text": [],
        }

    from pypdf import PdfReader

    reader = PdfReader(str(path))
    sample_text = []
    for index, page in enumerate(reader.pages[:max_pages], start=1):
        text = (page.extract_text() or "").strip()
        sample_text.append(
            {
                "page": index,
                "chars": len(text),
                "preview": text[:300],
            }
        )
    return {
        "page_count": len(reader.pages),
        "extractable_pages": len(sample_text),
        "sample_text": sample_text,
    }


def main() -> int:
    args = parse_args()
    mode = resolve_mode(args)
    exit_if_missing(args.input)
    if args.input.suffix.lower() != ".pdf":
        raise SystemExit("Unsupported file type. Use a .pdf input.")
    info = inspect_pdf(args.input, args.max_pages)
    report = {
        "mode": mode,
        "session_timestamp": utc_timestamp(),
        "input": file_summary(args.input),
        "inspection": info,
        "will_write": ["extracted.txt"] if mode == "execute" and "dependency_missing" not in info else [],
    }
    print_report(report)

    if mode != "execute":
        return 0
    if info.get("dependency_missing"):
        raise SystemExit("Cannot execute PDF extraction: missing optional dependency pypdf.")

    from pypdf import PdfReader

    out_dir = args.out or args.input.parent / f"{args.input.stem}-pdf"
    ensure_dir(out_dir)
    reader = PdfReader(str(args.input))
    text = []
    for index, page in enumerate(reader.pages, start=1):
        text.append(f"\n--- Page {index} ---\n")
        text.append((page.extract_text() or "").strip())
    write_text(out_dir / "extracted.txt", "\n".join(text).strip() + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
