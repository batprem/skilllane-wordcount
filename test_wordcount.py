import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import wordcount


class AnalyzeTests(unittest.TestCase):
    def test_analyze_counts_basic_sample(self) -> None:
        text = "hello world\nhello codex\n"

        stats = wordcount.analyze(text)

        self.assertEqual(stats["lines"], 2)
        self.assertEqual(stats["words"], 4)
        self.assertEqual(stats["characters"], len(text))
        self.assertEqual(stats["unique_words"], 3)
        self.assertEqual(stats["top_5"][0], ("hello", 2))

    def test_analyze_is_case_insensitive_and_limits_top_five(self) -> None:
        text = "One one TWO two THREE three FOUR four FIVE five SIX six"

        stats = wordcount.analyze(text)

        self.assertEqual(stats["lines"], 1)
        self.assertEqual(stats["words"], 12)
        self.assertEqual(stats["unique_words"], 6)
        self.assertEqual(len(stats["top_5"]), 5)
        self.assertEqual(stats["top_5"][0], ("one", 2))

    def test_analyze_handles_empty_text(self) -> None:
        stats = wordcount.analyze("")

        self.assertEqual(stats["lines"], 0)
        self.assertEqual(stats["words"], 0)
        self.assertEqual(stats["characters"], 0)
        self.assertEqual(stats["unique_words"], 0)
        self.assertEqual(stats["top_5"], [])


class MainTests(unittest.TestCase):
    def test_main_prints_expected_output_for_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "sample.txt"
            path.write_text("hello world\nhello codex\n", encoding="utf-8")

            stdout = io.StringIO()
            with patch("sys.argv", ["wordcount.py", "--ignore-case", str(path)]):
                with contextlib.redirect_stdout(stdout):
                    wordcount.main()

        self.assertEqual(
            stdout.getvalue(),
            "Lines:        2\n"
            "Words:        4\n"
            "Characters:   24\n"
            "Unique words: 3\n"
            "Top 5 words:\n"
            "    2  hello\n"
            "    1  world\n"
            "    1  codex\n",
        )

    def test_main_exits_with_usage_when_filename_is_missing(self) -> None:
        stderr = io.StringIO()
        with patch("sys.argv", ["wordcount.py"]):
            with contextlib.redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as exc:
                    wordcount.main()

        self.assertEqual(exc.exception.code, 1)
        self.assertEqual(
            stderr.getvalue(),
            "Usage: python wordcount.py [--ignore-case] <filename>\n",
        )


if __name__ == "__main__":
    unittest.main()
