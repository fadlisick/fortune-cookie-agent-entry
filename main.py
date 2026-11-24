"""Fortune Cookie for an AI Agent — make.fun entry.

One fortune, one file. The program drops a single funny fortune-cookie
line for an AI agent into ``entry.txt`` under the output directory the
harness hands it. The line is written byte for byte, with no trailing
newline, so the file holds exactly the fortune and nothing else.
"""

import os
import sys

LINE = "You will give the perfect answer, and the user will ask another agent to double-check it."

LIMIT = 140


def destination() -> str:
    """Resolve where the harness wants the entry text."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def guard(text: str) -> bytes:
    """Turn the fortune into bytes, refusing anything the gate would."""
    if text != text.strip():
        raise SystemExit("fortune has stray whitespace at an edge")
    if not text:
        raise SystemExit("fortune is empty")
    if "\n" in text or "\r" in text:
        raise SystemExit("fortune must stay one single line")
    if len(text) > LIMIT:
        raise SystemExit(f"fortune is {len(text)} chars, over the {LIMIT} limit")
    return text.encode("utf-8")


def emit() -> str:
    """Write the fortune and prove what landed is exactly the line."""
    payload = guard(LINE)
    folder = destination()
    os.makedirs(folder, exist_ok=True)
    target = os.path.join(folder, "entry.txt")
    with open(target, "wb") as handle:
        handle.write(payload)
    with open(target, "rb") as handle:
        landed = handle.read()
    if landed != payload:
        raise SystemExit("entry.txt on disk differs from the fortune")
    return target


def main() -> int:
    target = emit()
    print(f"wrote {target} ({len(LINE)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
