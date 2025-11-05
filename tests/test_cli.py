"""Test CLI functionality."""

from __future__ import annotations

import logging
import sys
from unittest.mock import MagicMock, patch

import pytest
import requests

from ustcwlt.__main__ import main


def test_cli_help(capsys: pytest.CaptureFixture[str]) -> None:
    """Test CLI help message."""
    with (
        pytest.raises(SystemExit) as exc_info,
        patch.object(sys, "argv", ["ustcwlt", "--help"]),
    ):
        main()
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "Log in to USTC WLT" in captured.out
    assert "--username" in captured.out
    assert "--password" in captured.out


def test_cli_missing_username(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test CLI with missing username."""
    # Clear any environment variables
    monkeypatch.delenv("USTCWLT_USERNAME", raising=False)
    monkeypatch.delenv("USTCWLT_PASSWORD", raising=False)

    with (
        pytest.raises(SystemExit) as exc_info,
        patch.object(sys, "argv", ["ustcwlt"]),
    ):
        main()
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "required: --username" in captured.err


def test_cli_missing_password(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test CLI with missing password."""
    # Clear any environment variables
    monkeypatch.delenv("USTCWLT_USERNAME", raising=False)
    monkeypatch.delenv("USTCWLT_PASSWORD", raising=False)

    with (
        pytest.raises(SystemExit) as exc_info,
        patch.object(sys, "argv", ["ustcwlt", "--username", "testuser"]),
    ):
        main()
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "required: --password" in captured.err


@patch("ustcwlt.__main__.requests.post")
def test_cli_success(
    mock_post: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test successful CLI login."""
    mock_response = MagicMock()
    mock_response.text = "Success"
    mock_post.return_value = mock_response

    with (
        caplog.at_level(logging.INFO),
        patch.object(
            sys,
            "argv",
            ["ustcwlt", "--username", "testuser", "--password", "testpass"],
        ),
    ):
        main()

    assert "Login successful!" in caplog.text

    # Verify the request was made correctly
    mock_post.assert_called_once()
    call_args = mock_post.call_args
    assert call_args[0][0] == "http://wlt.ustc.edu.cn/cgi-bin/ip"
    assert call_args[1]["data"]["cmd"] == "set"
    assert call_args[1]["data"]["name"] == "testuser"
    assert call_args[1]["data"]["password"] == "testpass"  # noqa: S105
    assert call_args[1]["data"]["type"] == "0"
    assert call_args[1]["data"]["exp"] == "0"


@patch("ustcwlt.__main__.requests.post")
def test_cli_with_custom_type_and_exp(
    mock_post: MagicMock,
) -> None:
    """Test CLI with custom type and exp values."""
    mock_response = MagicMock()
    mock_response.text = "Success"
    mock_post.return_value = mock_response

    with patch.object(
        sys,
        "argv",
        [
            "ustcwlt",
            "--username",
            "testuser",
            "--password",
            "testpass",
            "--type",
            "3",
            "--exp",
            "60",
        ],
    ):
        main()

    # Verify the request was made with custom values
    call_args = mock_post.call_args
    assert call_args[1]["data"]["type"] == "3"
    assert call_args[1]["data"]["exp"] == "60"


@patch("ustcwlt.__main__.requests.post")
def test_cli_with_env_vars(
    mock_post: MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test CLI with environment variables."""
    monkeypatch.setenv("USTCWLT_USERNAME", "envuser")
    monkeypatch.setenv("USTCWLT_PASSWORD", "envpass")
    monkeypatch.setenv("USTCWLT_TYPE", "2")
    monkeypatch.setenv("USTCWLT_EXP", "30")

    mock_response = MagicMock()
    mock_response.text = "Success"
    mock_post.return_value = mock_response

    with patch.object(sys, "argv", ["ustcwlt"]):
        main()

    # Verify the request used environment variables
    call_args = mock_post.call_args
    assert call_args[1]["data"]["name"] == "envuser"
    assert call_args[1]["data"]["password"] == "envpass"  # noqa: S105
    assert call_args[1]["data"]["type"] == "2"
    assert call_args[1]["data"]["exp"] == "30"


@patch("ustcwlt.__main__.requests.post")
def test_cli_request_failure(
    mock_post: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test CLI with request failure."""
    mock_post.side_effect = requests.exceptions.RequestException("Network error")

    with (
        caplog.at_level(logging.ERROR),
        pytest.raises(SystemExit) as exc_info,
        patch.object(
            sys,
            "argv",
            ["ustcwlt", "--username", "testuser", "--password", "testpass"],
        ),
    ):
        main()

    assert exc_info.value.code == 1
    assert "Login failed:" in caplog.text
    assert "Network error" in caplog.text
