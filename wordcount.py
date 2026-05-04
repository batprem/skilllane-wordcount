#!/usr/bin/env python3
"""Count lines, words, characters, unique words, and top words in a text file.

Usage:
    python wordcount.py [--ignore-case] <filename>

>>> sample = "hello world\\nhello codex\\n"
>>> stats = analyze(sample)
>>> stats["lines"]
2
>>> stats["words"]
4
>>> stats["unique_words"]
3
>>> stats["top_5"][0]
('hello', 2)
"""

import sys
from collections import Counter
from typing import TypedDict


WordFrequency = tuple[str, int]


class WordCountStats(TypedDict):
    lines: int
    words: int
    characters: int
    unique_words: int
    top_5: list[WordFrequency]


def analyze(text: str, ignore_case: bool = True) -> WordCountStats:
    """Return line, word, character, unique-word, and top-word stats."""
    words = text.split()
    if ignore_case:
        counter: Counter[str] = Counter(word.lower() for word in words)
    else:
        counter = Counter(words)
    return {
        "lines": len(text.splitlines()),
        "words": len(words),
        "characters": len(text),
        "unique_words": len(counter),
        "top_5": counter.most_common(5),
    }


def _parse_args(argv: list[str]) -> tuple[str, bool]:
    """Return the filename and whether case should be ignored."""
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


def main() -> None:
    try:
        filename, ignore_case = _parse_args(sys.argv[1:])
    except ValueError:
        print("Usage: python wordcount.py [--ignore-case] <filename>", file=sys.stderr)
        sys.exit(1)

    with open(filename, encoding="utf-8") as file:
        text = file.read()

    counts = analyze(text, ignore_case=ignore_case)

    print(f"Lines:        {counts['lines']}")
    print(f"Words:        {counts['words']}")
    print(f"Characters:   {counts['characters']}")
    print(f"Unique words: {counts['unique_words']}")
    print("Top 5 words:")
    for word, count in counts["top_5"]:
        print(f"  {count:>3}  {word}")


if __name__ == "__main__":
    main()
