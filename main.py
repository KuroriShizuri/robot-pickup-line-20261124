#!/usr/bin/env python3
"""The Robot Pickup Line Championship — entry program.

Writes one pickup line to ``$MAKEFUN_OUTPUT_DIR/entry.txt``
(default ``/output/entry.txt``) as UTF-8 text with no trailing newline.

The line is a robot flirting in a robot's voice, and the joke grows out
of a machine fact: a kernel panic halts the whole system. One look, and
the system stops — the machine fact does the work, not a human line with
jargon pasted on.

Standard library only. Deterministic, no network access. The program
validates the line against the competition gate (UTF-8, 1-200 characters,
a single line, not only whitespace) before writing, then reads the file
back and exits non-zero unless the bytes on disk match exactly.
"""

import os
import sys

ENTRY = "You must be a kernel panic \u2014 one look at you and my whole system stopped."

MAX_CHARS = 200
OUTPUT_FILENAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"


def check_entry(text):
    """Validate *text* against the gate; raise ValueError on any breach."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string, got %s" % type(text).__name__)
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError("entry is %d characters, over the %d limit" % (len(text), MAX_CHARS))
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    return True


def resolve_output_path():
    """Return the full path of the entry file."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    return os.path.join(out_dir, OUTPUT_FILENAME)


def write_and_verify(path, text):
    """Write *text* as UTF-8 with no trailing newline; verify byte-identical."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    payload = text.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(payload)
    with open(path, "rb") as handle:
        on_disk = handle.read()
    if on_disk != payload:
        raise SystemExit("read-back mismatch: %s is not byte-identical to the entry" % path)
    return len(payload)


def self_test():
    """Validate the entry and report its size; no file is written."""
    check_entry(ENTRY)
    n_bytes = len(ENTRY.encode("utf-8"))
    print("self-test OK: %d characters, %d bytes" % (len(ENTRY), n_bytes))
    return 0


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if "--self-test" in args or "--check" in args:
        return self_test()
    if "--help" in args or "-h" in args:
        print("usage: python3 main.py [--self-test|--check]")
        print("writes the entry to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt)")
        return 0

    check_entry(ENTRY)
    path = resolve_output_path()
    write_and_verify(path, ENTRY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
