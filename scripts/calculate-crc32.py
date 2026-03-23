#!/usr/bin/env python3
"""
Compute CRC-32 checksums for a text file, one logical entry per line.

Summary
-------
- The program accepts exactly one command-line argument: the input file path.
- It reads the file as UTF-8 text (UTF-8 with BOM is also accepted).
- Each line is treated as one entry after removing only its line-ending
  characters ('\\n' or '\\r\\n').
- All other characters are preserved exactly, including spaces and tabs.
- Empty lines in the middle of the file are preserved and hashed.
- Empty lines at the very end of the file are ignored.
- The output file is written in the same directory, with '_out' inserted
  before the final file extension.

Examples
--------
Input file name:
    input.txt
Output file name:
    input_out.txt

Name transformation examples:
    input.txt      -> input_out.txt
    names.csv      -> names_out.csv
    archive.tar.gz -> archive.tar_out.gz
    README         -> README_out

Important distinction
---------------------
A normal trailing newline does NOT create an extra entry.

These two files contain the same two entries:
    apple
    banana

and:
    apple
    banana\\n

By contrast, this file has one extra empty line at the end:
    apple
    banana
    <empty line>

That trailing empty line is ignored by this script.

Output format
-------------
The output contains one CRC-32 checksum per retained input entry, formatted
as an 8-character uppercase hexadecimal string.

Important
---------
CRC-32 is a checksum, not encryption.

Usage
-----
    python crc32_lines.py input.txt
"""

from __future__ import annotations

import argparse
import sys
import zlib
from pathlib import Path


def crc32_hex(text: str) -> str:
    """
    Compute the CRC-32 checksum of a string.

    Parameters
    ----------
    text : str
        The exact text to hash.

    Returns
    -------
    str
        The checksum as an 8-character uppercase hexadecimal string.

    Notes
    -----
    The input text is encoded as UTF-8 before hashing. The result is masked
    with 0xFFFFFFFF so it is always represented as an unsigned 32-bit value.
    """
    checksum = zlib.crc32(text.encode("utf-8")) & 0xFFFFFFFF
    return f"{checksum:08X}"


def make_output_path(input_path: Path) -> Path:
    """
    Create the output path for a given input file.

    The output file is placed in the same directory as the input file, with
    '_out' inserted before the final suffix.

    Parameters
    ----------
    input_path : Path
        Path to the input file.

    Returns
    -------
    Path
        Path to the output file.
    """
    return input_path.with_name(f"{input_path.stem}_out{input_path.suffix}")


def process_file(input_path: Path) -> Path:
    """
    Read the input file and write one CRC-32 checksum per retained line.

    Processing rules
    ----------------
    1. Each physical line in the file is read independently.
    2. Only line-ending characters are removed before hashing.
    3. Empty lines in the middle of the file are preserved.
    4. Empty lines at the very end of the file are ignored.

    Parameters
    ----------
    input_path : Path
        Path to the input text file.

    Returns
    -------
    Path
        Path to the generated output file.
    """
    output_path = make_output_path(input_path)

    with input_path.open("r", encoding="utf-8-sig", newline="") as infile:
        entries = [line.rstrip("\r\n") for line in infile]

    # Remove only trailing empty entries. Empty entries that occur earlier
    # in the file must be preserved.
    while entries and entries[-1] == "":
        entries.pop()

    with output_path.open("w", encoding="utf-8", newline="\n") as outfile:
        for entry in entries:
            outfile.write(crc32_hex(entry) + "\n")

    return output_path


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed arguments containing:
        - input_file: the path to the input text file
    """
    parser = argparse.ArgumentParser(
        description="Generate one CRC-32 checksum per input line."
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Path to the input text file (one entry per line).",
    )
    return parser.parse_args()


def main() -> int:
    """
    Run the command-line program.

    Returns
    -------
    int
        Exit status code:
        - 0 on success
        - 1 on error
    """
    args = parse_args()
    input_path = args.input_file

    if not input_path.exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        return 1

    if not input_path.is_file():
        print(f"Error: input path is not a file: {input_path}", file=sys.stderr)
        return 1

    try:
        output_path = process_file(input_path)
    except UnicodeDecodeError:
        print(
            "Error: could not decode the input file as UTF-8 or UTF-8 with BOM.",
            file=sys.stderr,
        )
        return 1
    except OSError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Done: wrote CRC-32 checksums to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
