"""Core implementation of character 3-gram cosine similarity.

The implementation uses only the Python standard library so that it can run in
the restricted grading environment without network access or third-party
packages.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from pathlib import Path


class CheckerError(Exception):
    """Base class for expected checker errors."""


class ArgumentError(CheckerError):
    """Raised when a public function receives invalid arguments."""


class FileOperationError(CheckerError):
    """Raised when an input file cannot be read."""


class EmptyDocumentError(CheckerError):
    """Raised when an input document has no usable content."""


_WHITESPACE = re.compile(r"\s+")
NGRAM_SIZE = 3


def normalize_text(text: str) -> str:
    """Remove whitespace while preserving all non-whitespace characters."""
    if not isinstance(text, str):
        raise ArgumentError("文本必须是字符串")
    return _WHITESPACE.sub("", text)


def build_ngram_frequency(text: str, ngram_size: int = NGRAM_SIZE) -> Counter[str]:
    """Build a frequency vector from overlapping character n-grams."""
    if not isinstance(text, str):
        raise ArgumentError("文本必须是字符串")
    if not isinstance(ngram_size, int) or isinstance(ngram_size, bool):
        raise ArgumentError("ngram_size 必须是正整数")
    if ngram_size <= 0:
        raise ArgumentError("ngram_size 必须是正整数")
    normalized = normalize_text(text)
    return Counter(
        normalized[index : index + ngram_size]
        for index in range(len(normalized) - ngram_size + 1)
    )


def cosine_similarity(first: Counter[str], second: Counter[str]) -> float:
    """Return cosine similarity of two sparse frequency vectors in [0, 1]."""
    if not isinstance(first, Counter) or not isinstance(second, Counter):
        raise ArgumentError("输入必须是 Counter 词频向量")
    if not first or not second:
        return 0.0

    dot_product = sum(value * second.get(key, 0) for key, value in first.items())
    first_norm = math.sqrt(sum(value * value for value in first.values()))
    second_norm = math.sqrt(sum(value * value for value in second.values()))
    if first_norm == 0.0 or second_norm == 0.0:
        return 0.0
    return max(0.0, min(1.0, dot_product / (first_norm * second_norm)))


def calculate_similarity(original: str, plagiarized: str) -> float:
    """Calculate the similarity of two document strings."""
    original_text = normalize_text(original)
    plagiarized_text = normalize_text(plagiarized)
    if not original_text or not plagiarized_text:
        raise EmptyDocumentError("原文和抄袭版论文都必须包含非空白内容")
    if original_text == plagiarized_text:
        return 1.0
    return cosine_similarity(
        build_ngram_frequency(original_text),
        build_ngram_frequency(plagiarized_text),
    )


def _read_utf8(path: Path) -> str:
    """Read one UTF-8 document and translate OS errors to checker errors."""
    try:
        return path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as error:
        raise FileOperationError(f"无法读取文件: {path}") from error


def calculate_similarity_from_files(
    original_path: Path, plagiarized_path: Path
) -> float:
    """Read two files and calculate their similarity."""
    if not isinstance(original_path, Path) or not isinstance(plagiarized_path, Path):
        raise ArgumentError("文件路径必须是 pathlib.Path")
    return calculate_similarity(_read_utf8(original_path), _read_utf8(plagiarized_path))
