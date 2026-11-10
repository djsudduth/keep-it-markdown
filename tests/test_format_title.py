"""Note titles must not keep '/' (it breaks markdown file creation)."""

from kim import ILLEGAL_FILE_CHARS, Markdown


def test_slash_is_illegal_filename_char():
    assert "/" in ILLEGAL_FILE_CHARS


def test_format_title_replaces_slash():
    assert "/" not in Markdown.format_title("meeting/notes")


def test_format_title_still_replaces_other_illegal_chars():
    assert Markdown.format_title("a:b") == "a b"
