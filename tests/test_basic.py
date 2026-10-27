"""Sanity tests. Run with: pytest -q"""
from utils.url_safety import is_safe_url
from utils.text import truncate


def test_truncate():
    assert truncate("abc", 10) == "abc"
    assert len(truncate("x" * 5000, 4000)) <= 4020


def test_url_safety_rejects_localhost():
    assert not is_safe_url("http://localhost/x")
    assert not is_safe_url("http://127.0.0.1/x")
    assert not is_safe_url("ftp://example.com/x")


def test_url_safety_accepts_https():
    assert is_safe_url("https://www.google.com")