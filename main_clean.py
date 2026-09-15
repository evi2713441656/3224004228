"""Optional entry point that extracts text from GitHub-rendered HTML files."""

from __future__ import annotations

import sys
from pathlib import Path

from github_html_reader import read_for_inspection
from plagiarism_checker import CheckerError, calculate_similarity


def run(arguments: list[str]) -> int:
    """Run the optional HTML-aware variant and return an exit code."""
    if len(arguments) != 3 or any(not argument.strip() for argument in arguments):
        print(
            "用法: python main_clean.py <原文绝对路径> <抄袭版绝对路径> <答案绝对路径>",
            file=sys.stderr,
        )
        return 2

    original_path, plagiarized_path, answer_path = map(Path, arguments)
    try:
        similarity = calculate_similarity(
            read_for_inspection(original_path), read_for_inspection(plagiarized_path)
        )
        answer_path.write_text(f"{similarity:.2f}\n", encoding="utf-8")
    except (CheckerError, OSError) as error:
        print(f"查重失败: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))
