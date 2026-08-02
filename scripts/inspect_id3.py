#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect ID3 tags in an MP3 file."
    )
    parser.add_argument("file", type=Path)

    args = parser.parse_args()

    try:
        audio = EasyID3(args.file)
    except ID3NoHeaderError:
        print("No ID3 tags found.")
        return

    print(f"File: {args.file}\n")

    for key in sorted(audio.keys()):
        print(f"{key}: {audio[key]}")


if __name__ == "__main__":
    main()