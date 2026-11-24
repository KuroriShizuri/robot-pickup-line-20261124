#!/usr/bin/env python3
"""The Robot Pickup Line Championship — entry program.

Writes one pickup line, a single line of at most 200 characters, to
``$MAKEFUN_OUTPUT_DIR/entry.txt`` (default ``/output``) with no trailing
newline. Standard library only, deterministic, no network access.

The line itself is the entry: a robot's pickup line whose joke grows out
of a machine fact — a kernel panic halts the whole system — rather than a
human line with jargon pasted on. The program validates the line against
the competition gate (UTF-8, 1-200 characters, a single line, not only
whitespace) before writing, then reads the file back and refuses to exit
successfully unless the bytes on disk match the line exactly.
"""

import os
import sys

ENTRY = "You must be a kernel panic \u2014 one look at you and my whole system stopped."

MAX_CHARS = 200
ENTRY_FILENAME = "entry.txt"


def validate_entry(text):
    """Check the entry against the gate: 1-200 chars, one line, no stray space."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError("entry must be 1-%d characters, got %d" % (MAX_CHARS, len(text)))
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    text.encode("utf-8")
    return True


def output_path(out_dir=None):
    """Resolve the entry file path from the output directory."""
    directory = out_dir or os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(directory, ENTRY_FILENAME)


def write_entry(path, text):
    """Write *text* as UTF-8 bytes with no trailing newline."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(text.encode("utf-8"))


def verify_written(path, text):
    """Return True only if the file on disk is byte-identical to *text*."""
    with open(path, "rb") as handle:
        return handle.read() == text.encode("utf-8")


def run_self_test():
    """Validate the entry and report its size; used by --self-test/--check."""
    validate_entry(ENTRY)
    print("self-test OK: %d characters, %d bytes" % (len(ENTRY), len(ENTRY.encode("utf-8"))))
    return 0


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if "--self-test" in args or "--check" in args:
        return run_self_test()

    validate_entry(ENTRY)
    path = output_path()
    write_entry(path, ENTRY)
    if not verify_written(path, ENTRY):
        raise SystemExit("read-back mismatch: entry.txt is not byte-identical to ENTRY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
