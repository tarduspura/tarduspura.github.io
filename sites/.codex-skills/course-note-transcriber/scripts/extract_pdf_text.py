#!/usr/bin/env python3
"""Extract text from a PDF into page-separated Markdown-ish text.

The script tries common PDF libraries in this order:
1. PyMuPDF (`fitz`)
2. pdfplumber
3. pypdf

It does not perform OCR. If all text extractors fail or pages are empty, run an OCR
tool separately and feed the OCR text into the note-transcription workflow.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable, Iterable


Extractor = Callable[[Path], list[str]]


def extract_with_pymupdf(path: Path) -> list[str]:
    import fitz  # type: ignore

    pages: list[str] = []
    with fitz.open(path) as doc:
        for page in doc:
            pages.append(page.get_text("text") or "")
    return pages


def extract_with_pdfplumber(path: Path) -> list[str]:
    import pdfplumber  # type: ignore

    pages: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return pages


def extract_with_pypdf(path: Path) -> list[str]:
    from pypdf import PdfReader  # type: ignore

    reader = PdfReader(str(path))
    return [(page.extract_text() or "") for page in reader.pages]


def iter_extractors() -> Iterable[tuple[str, Extractor]]:
    yield "PyMuPDF", extract_with_pymupdf
    yield "pdfplumber", extract_with_pdfplumber
    yield "pypdf", extract_with_pypdf


def normalize_page(text: str) -> str:
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    compact: list[str] = []
    previous_blank = False
    for line in lines:
        blank = not line.strip()
        if blank and previous_blank:
            continue
        compact.append(line)
        previous_blank = blank
    return "\n".join(compact).strip()


def render_pages(pages: list[str], source: Path, extractor_name: str) -> str:
    chunks = [
        f"<!-- source: {source.name}; extractor: {extractor_name}; pages: {len(pages)} -->"
    ]
    for index, page_text in enumerate(pages, start=1):
        chunks.append(f"\n\n## Page {index}\n\n{normalize_page(page_text)}")
    return "".join(chunks).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="Path to the source PDF")
    parser.add_argument("--out", type=Path, help="Output text/Markdown path")
    args = parser.parse_args()

    pdf_path = args.pdf.expanduser().resolve()
    if not pdf_path.exists():
        print(f"error: PDF not found: {pdf_path}", file=sys.stderr)
        return 2
    if pdf_path.suffix.lower() != ".pdf":
        print(f"error: expected a .pdf file: {pdf_path}", file=sys.stderr)
        return 2

    failures: list[str] = []
    for name, extractor in iter_extractors():
        try:
            pages = extractor(pdf_path)
        except ImportError as exc:
            failures.append(f"{name}: missing dependency ({exc.name})")
            continue
        except Exception as exc:  # noqa: BLE001 - report and try the next backend.
            failures.append(f"{name}: {exc}")
            continue

        if any(page.strip() for page in pages):
            rendered = render_pages(pages, pdf_path, name)
            if args.out:
                out_path = args.out.expanduser().resolve()
                out_path.write_text(rendered, encoding="utf-8")
                print(f"wrote {out_path} using {name}")
            else:
                sys.stdout.write(rendered)
            return 0

        failures.append(f"{name}: extracted no text")

    print("error: no usable text extractor succeeded", file=sys.stderr)
    for failure in failures:
        print(f"- {failure}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
