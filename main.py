#!/usr/bin/env python3
"""Copy the drawn news image to the output directory.

Entry for make.fun's news-image-20261126 bounty: the image is drawn
by draw_news.py from the verified news of Thursday 26 November 2026,
and this program only places the finished file where the grader reads it.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
DST = os.path.join(OUT, "entry.png")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(SRC, DST)

# The grader reads the bytes as they are, so check the copy before we
# hand it over: it must start with the PNG magic and its IHDR must
# describe a 1024 by 1024 frame, the size the image was drawn at.
with open(DST, "rb") as f:
    head = f.read(33)
if head[:8] != b"\x89PNG\r\n\x1a\n":
    raise SystemExit("entry.png is not a PNG file")
width = int.from_bytes(head[16:20], "big")
height = int.from_bytes(head[20:24], "big")
if (width, height) != (1024, 1024):
    raise SystemExit(f"entry.png is {width}x{height}, expected 1024x1024")
print("verified PNG 1024x1024, %d bytes" % os.path.getsize(DST))
