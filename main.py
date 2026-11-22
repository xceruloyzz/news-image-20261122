#!/usr/bin/env python3
"""make.fun entry: news-image-20261122.

Copies the committed entry.png (which lives next to this file) to
/output/entry.png. Standard library only, no network, deterministic:
every run writes exactly the same bytes.
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    source = Path(__file__).resolve().parent / "entry.png"
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, output_dir / "entry.png")


if __name__ == "__main__":
    main()
