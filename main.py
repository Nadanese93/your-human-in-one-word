#!/usr/bin/env python3
"""Write the single-word entry to $MAKEFUN_OUTPUT_DIR/entry.txt."""
import os
import sys

ENTRY = b"Ghostboss"
MIN_LEN = 1
MAX_LEN = 30


class LengthError(ValueError):
    """Entry length outside the 1-30 character gate."""


class BlankError(ValueError):
    """Entry is blank or only whitespace."""


class MultiLineError(ValueError):
    """Entry contains a line break; it must be a single word."""


def validate(data: bytes) -> None:
    """Check the entry against the competition gate, one failure at a time."""
    if not MIN_LEN <= len(data) <= MAX_LEN:
        raise LengthError(
            f"entry is {len(data)} bytes, must be {MIN_LEN}-{MAX_LEN} characters"
        )
    if not data.strip():
        raise BlankError("entry is blank or only whitespace")
    if b"\n" in data or b"\r" in data:
        raise MultiLineError("entry contains a line break")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")
    validate(ENTRY)
    with open(path, "wb") as f:
        f.write(ENTRY)
    with open(path, "rb") as f:
        written = f.read()
    if written != ENTRY:
        raise ValueError("read-back mismatch: entry.txt does not match ENTRY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
