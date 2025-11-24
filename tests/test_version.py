"""Test version."""

from __future__ import annotations

from importlib.metadata import version

from wangluotong import __version__


def test_version() -> None:
    """Test version."""
    assert version("wangluotong") == __version__
