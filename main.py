#!/usr/bin/env python3
"""news-image-20261121 entrypoint: copy the committed entry.png to the
output directory. Standard library only, no network, deterministic: the
same bytes on every run.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
out = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
os.makedirs(out, exist_ok=True)
shutil.copyfile(os.path.join(here, "entry.png"),
                os.path.join(out, "entry.png"))
