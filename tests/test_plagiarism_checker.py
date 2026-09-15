"""White-box and boundary tests for the core calculation module."""

from __future__ import annotations

import tempfile
import unittest
from collections import Counter
from pathlib import Path

from github_html_reader import read_for_inspection
from main import run
from main_clean import run as clean_run
from plagiarism_checker import (
    ArgumentError,
    EmptyDocumentError,
    FileOperationError,
    build_ngram_frequency,
    calculate_similarity,
    calculate_similarity_from_files,
    cosine_similarity,
    normalize_text,
)


class SimilarityTests(unittest.TestCase):
    """Exercise normal cases, boundaries, and expected failures."""

    def test_normalize_removes_spaces_and_newlines(self) -> None:
        self.assertEqual(normalize_text("甲 乙\n丙\t丁"), "甲乙丙丁")

    def test_normalize_preserves_punctuation(self) -> None:
        self.assertEqual(normalize_text("你好，世界。"), "你好，世界。")

    def test_ngram_frequency_counts_overlaps(self) -> None:
        self.assertEqual(build_ngram_frequency("aaaa"), Counter({"aaa": 2}))

    def test_ngram_shorter_than_window_is_empty(self) -> None:
        self.assertEqual(build_ngram_frequency("ab"), Counter())

    def test_identical_short_documents_are_one(self) -> None:
        self.assertAlmostEqual(calculate_similarity("甲", "甲"), 1.0)

    def test_identical_documents_are_one(self) -> None:
        self.assertAlmostEqual(calculate_similarity("abcdef", "abcdef"), 1.0)

    def test_whitespace_only_changes_do_not_affect_result(self) -> None:
        self.assertAlmostEqual(calculate_similarity("abc def ghi", "abcdefghi"), 1.0)

    def test_unrelated_documents_are_zero(self) -> None:
        self.assertAlmostEqual(calculate_similarity("甲甲甲", "乙乙乙"), 0.0)

    def test_partial_overlap_is_between_zero_and_one(self) -> None:
        result = calculate_similarity("abcdefghi", "abcdefxyz")
        self.assertGreater(result, 0.0)
        self.assertLess(result, 1.0)

    def test_empty_original_is_rejected(self) -> None:
        with self.assertRaises(EmptyDocumentError):
            calculate_similarity(" \n", "abcdef")

    def test_empty_plagiarized_is_rejected(self) -> None:
        with self.assertRaises(EmptyDocumentError):
            calculate_similarity("abcdef", "\t")

    def test_invalid_ngram_size_is_rejected(self) -> None:
        with self.assertRaises(ArgumentError):
            build_ngram_frequency("abcdef", 0)

    def test_cosine_zero_vectors_return_zero(self) -> None:
        self.assertEqual(cosine_similarity(Counter(), Counter("abc")), 0.0)

    def test_file_api_reads_utf8_bom_and_returns_value(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = root / "original.txt"
            plagiarized = root / "plagiarized.txt"
            original.write_text("\ufeffabcdef", encoding="utf-8")
            plagiarized.write_text("abcdef", encoding="utf-8")
            self.assertEqual(
                calculate_similarity_from_files(original, plagiarized), 1.0
            )

    def test_missing_file_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.txt"
            present = Path(directory) / "present.txt"
            present.write_text("abcdef", encoding="utf-8")
            with self.assertRaises(FileOperationError):
                calculate_similarity_from_files(missing, present)

    def test_command_line_run_writes_two_decimal_answer(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = root / "original.txt"
            plagiarized = root / "plagiarized.txt"
            answer = root / "answer.txt"
            original.write_text("abcdef", encoding="utf-8")
            plagiarized.write_text("abcdef", encoding="utf-8")
            self.assertEqual(run([str(original), str(plagiarized), str(answer)]), 0)
            self.assertEqual(answer.read_text(encoding="utf-8"), "1.00\n")

    def test_command_line_rejects_wrong_argument_count(self) -> None:
        self.assertEqual(run(["only-one-argument"]), 2)

    def test_optional_reader_extracts_github_code_cells(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "page.html"
            path.write_text(
                '<td class="blob-code-inner">甲&amp;乙</td>', encoding="utf-8"
            )
            self.assertEqual(read_for_inspection(path), "甲&乙")

    def test_optional_reader_keeps_plain_text_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plain.txt"
            path.write_text("甲乙丙", encoding="utf-8")
            self.assertEqual(read_for_inspection(path), "甲乙丙")

    def test_optional_command_line_writes_extracted_answer(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = root / "original.txt"
            plagiarized = root / "page.html"
            answer = root / "answer.txt"
            original.write_text("abcdef", encoding="utf-8")
            plagiarized.write_text(
                '<td class="blob-code-inner">abcdef</td>', encoding="utf-8"
            )
            self.assertEqual(
                clean_run([str(original), str(plagiarized), str(answer)]), 0
            )
            self.assertEqual(answer.read_text(encoding="utf-8"), "1.00\n")


if __name__ == "__main__":
    unittest.main()
