"""Test version."""

from __future__ import annotations

from importlib.metadata import version

from ustcwlt import __version__


def test_version() -> None:
    """Test version."""
    assert version("ustcwlt") == __version__
