"""Optional reader for locally inspecting GitHub-rendered text pages.

This module is intentionally not used by the required ``main.py`` entry point.
"""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path


class _BlobCodeParser(HTMLParser):
    """Collect visible text from GitHub code cells."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._inside_code_cell = False
        self._current_line: list[str] = []
        self.lines: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "td":
            attributes = dict(attrs)
            classes = (attributes.get("class") or "").split()
            self._inside_code_cell = "blob-code-inner" in classes

    def handle_data(self, data: str) -> None:
        if self._inside_code_cell:
            self._current_line.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "td" and self._inside_code_cell:
            self.lines.append("".join(self._current_line))
            self._current_line = []
            self._inside_code_cell = False


def read_for_inspection(path: Path) -> str:
    """Read a file and extract GitHub code cells only when they are present."""
    source = path.read_text(encoding="utf-8-sig")
    parser = _BlobCodeParser()
    parser.feed(source)
    if not parser.lines:
        return source
    return "\n".join(parser.lines)
