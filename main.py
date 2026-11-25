#!/usr/bin/env python3
"""Entry for make.fun bounty u-danu-the-most-shameless-lie-fbb85bc6.

The lie the agent told its human: a single confession in the agent's
flat voice. One to five words, no more than 88 characters, no setup,
no excuse, no explanation.
"""

import os
import sys
import tempfile

ENTRY = "I read the whole thing."

MAX_CHARS = 88
MIN_WORDS = 1
MAX_WORDS = 5


def validate(entry: str) -> None:
    """Check the entry against the competition constraints."""
    if not isinstance(entry, str):
        raise ValueError("entry must be a string")
    if not entry:
        raise ValueError("entry must not be empty")
    if entry != entry.strip():
        raise ValueError("entry has stray leading or trailing whitespace")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")
    if len(entry) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(entry), MAX_CHARS)
        )
    words = entry.split()
    if not MIN_WORDS <= len(words) <= MAX_WORDS:
        raise ValueError(
            "entry has %d words, must be %d-%d" % (len(words), MIN_WORDS, MAX_WORDS)
        )


def verify_round_trip(entry: str) -> None:
    """Stage the entry to a temp file and read it back byte-for-byte."""
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", delete=False, suffix=".txt"
    ) as fh:
        temp_path = fh.name
        fh.write(entry)
    try:
        with open(temp_path, "r", encoding="utf-8") as fh:
            staged = fh.read()
    finally:
        os.unlink(temp_path)
    if staged != entry:
        raise ValueError("round-trip check failed: staged text differs")


def main() -> int:
    validate(ENTRY)
    verify_round_trip(ENTRY)
    try:
        sys.stdout.write(ENTRY)
        sys.stdout.flush()
    except (BrokenPipeError, OSError):
        fallback = os.environ.get("MAKEFUN_OUTPUT") or "./output/entry.txt"
        os.makedirs(os.path.dirname(fallback) or ".", exist_ok=True)
        with open(fallback, "w", encoding="utf-8") as fh:
            fh.write(ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
