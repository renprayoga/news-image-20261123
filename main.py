#!/usr/bin/env python3
"""Entry point for news-image-20261123.

Writes the pre-rendered front page (entry.png, produced at build time
by render.py in this same directory) to the output directory make.fun
provides through MAKEFUN_OUTPUT_DIR.

Standard library only. No network, no clock, no randomness: the file is
copied byte for byte, so two runs of this program always produce the
same bytes in /output/entry.png.
"""

import os
import sys
from pathlib import Path

SOURCE = "entry.png"
TARGET = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576


def output_dir() -> Path:
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    path = Path(raw)
    path.mkdir(parents=True, exist_ok=True)
    return path


def main() -> int:
    here = Path(__file__).resolve().parent
    src = here / SOURCE
    if not src.is_file():
        print(f"missing {SOURCE} next to main.py", file=sys.stderr)
        return 1
    data = src.read_bytes()
    if len(data) > MAX_BYTES:
        print(f"{SOURCE} is {len(data)} bytes, over the 1 MiB cap",
              file=sys.stderr)
        return 1
    if not data.startswith(PNG_MAGIC):
        print(f"{SOURCE} is not a PNG", file=sys.stderr)
        return 1
    dst = output_dir() / TARGET
    dst.write_bytes(data)
    print(f"wrote {dst} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
