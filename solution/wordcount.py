#!/usr/bin/env python3
"""Word counter — count lines, words, characters + unique words + top 5.

Usage:
    python wordcount.py [--ignore-case] <filename>

>>> from io import StringIO
>>> sample = "hello world\\nhello codex\\n"
>>> counts = analyze(sample)
>>> counts["lines"]
2
>>> counts["words"]
4
>>> counts["unique_words"]
3
>>> counts["top_5"][0]
('hello', 2)
"""
import sys
from collections import Counter


def analyze(text: str, ignore_case: bool = True) -> dict:
    """Return line / word / char + unique + top-5 stats for `text`."""
    lines = text.splitlines()
    words = text.split()
    if ignore_case:
        counter = Counter(w.lower() for w in words)
    else:
        counter = Counter(words)
    return {
        "lines": len(lines),
        "words": len(words),
        "characters": len(text),
        "unique_words": len(counter),
        "top_5": counter.most_common(5),
    }


def _parse_args(argv: list[str]) -> tuple[str, bool]:
    filename = None
    ignore_case = True

    for arg in argv:
        if arg == "--ignore-case":
            ignore_case = True
        elif arg.startswith("-"):
            raise ValueError(arg)
        elif filename is None:
            filename = arg
        else:
            raise ValueError(arg)

    if filename is None:
        raise ValueError("filename")

    return filename, ignore_case


def main(path: str, ignore_case: bool = True) -> None:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    stats = analyze(text, ignore_case=ignore_case)
    print(f"Lines:        {stats['lines']}")
    print(f"Words:        {stats['words']}")
    print(f"Characters:   {stats['characters']}")
    print(f"Unique words: {stats['unique_words']}")
    print("Top 5 words:")
    for word, count in stats["top_5"]:
        print(f"  {count:>3}  {word}")


if __name__ == "__main__":
    try:
        filename, ignore_case = _parse_args(sys.argv[1:])
    except ValueError:
        print("Usage: python wordcount.py [--ignore-case] <filename>", file=sys.stderr)
        sys.exit(1)
    main(filename, ignore_case=ignore_case)
