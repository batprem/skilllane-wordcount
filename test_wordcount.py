import io
from pathlib import Path

import pytest

import wordcount


def test_analyze_counts_basic_sample() -> None:
    text = "hello world\nhello codex\n"

    stats = wordcount.analyze(text)

    assert stats["lines"] == 2
    assert stats["words"] == 4
    assert stats["characters"] == len(text)
    assert stats["unique_words"] == 3
    assert stats["top_5"][0] == ("hello", 2)


def test_analyze_case_insensitive_limits_top_five() -> None:
    text = "One one TWO two THREE three FOUR four FIVE five SIX six"

    stats = wordcount.analyze(text)

    assert stats["lines"] == 1
    assert stats["words"] == 12
    assert stats["unique_words"] == 6
    assert len(stats["top_5"]) == 5
    assert stats["top_5"][0] == ("one", 2)


def test_analyze_case_sensitive_when_ignore_case_false() -> None:
    text = "One one ONE"

    stats = wordcount.analyze(text, ignore_case=False)

    assert stats["words"] == 3
    assert stats["unique_words"] == 3
    assert stats["top_5"][0] == ("One", 1)


def test_analyze_handles_empty_text() -> None:
    stats = wordcount.analyze("")

    assert stats["lines"] == 0
    assert stats["words"] == 0
    assert stats["characters"] == 0
    assert stats["unique_words"] == 0
    assert stats["top_5"] == []


@pytest.mark.parametrize(
    "argv,expected",
    [
        (["sample.txt"], ("sample.txt", True)),
        (["--ignore-case", "sample.txt"], ("sample.txt", True)),
    ],
)
def test_parse_args_valid(argv: list[str], expected: tuple[str, bool]) -> None:
    assert wordcount._parse_args(argv) == expected


@pytest.mark.parametrize(
    "argv",
    [
        [],
        ["-x", "sample.txt"],
        ["sample1.txt", "sample2.txt"],
    ],
)
def test_parse_args_invalid(argv: list[str]) -> None:
    with pytest.raises(ValueError):
        wordcount._parse_args(argv)


def test_main_prints_expected_output_for_file(tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("hello world\nhello codex\n", encoding="utf-8")

    monkeypatch.setattr("sys.argv", ["wordcount.py", "--ignore-case", str(path)])

    wordcount.main()

    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == (
        "Lines:        2\n"
        "Words:        4\n"
        "Characters:   24\n"
        "Unique words: 3\n"
        "Top 5 words:\n"
        "    2  hello\n"
        "    1  world\n"
        "    1  codex\n"
    )


def test_main_exits_with_usage_when_filename_missing(capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["wordcount.py"])

    with pytest.raises(SystemExit) as exc:
        wordcount.main()

    captured = capsys.readouterr()
    assert exc.value.code == 1
    assert captured.out == ""
    assert captured.err == "Usage: python wordcount.py [--ignore-case] <filename>\n"


def test_main_errors_for_unknown_flag(capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["wordcount.py", "--bad-flag"])

    with pytest.raises(SystemExit) as exc:
        wordcount.main()

    captured = capsys.readouterr()
    assert exc.value.code == 1
    assert captured.err == "Usage: python wordcount.py [--ignore-case] <filename>\n"
