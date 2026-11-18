#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261118 (Python 3.13, stdlib only).

Copies the front-page image held in this repository to the output
directory, exactly as the kit's starter does. The image itself was drawn
by draw_image.py (Pillow) from the verified world news of Wednesday
18 November 2026; this program needs no network and no third-party
library, so its two grading runs write identical bytes.

Run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXPECT_W, EXPECT_H = 1024, 1024


def png_size(path):
    """Read width/height from a PNG's IHDR chunk (stdlib only)."""
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        raise ValueError("not a PNG file")
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    w, h = png_size(dst)
    if (w, h) != (EXPECT_W, EXPECT_H):
        raise ValueError(f"entry.png is {w}x{h}, expected "
                         f"{EXPECT_W}x{EXPECT_H}")
    print("wrote", dst, f"({w}x{h}, {os.path.getsize(dst)} bytes)")


if __name__ == "__main__":
    main()
    sys.exit(0)
