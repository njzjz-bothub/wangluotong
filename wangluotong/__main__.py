"""Main entry point for the command line interface."""

from __future__ import annotations

import argparse
import logging
import os
import sys

import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Log in to USTC WLT."""
    parser = argparse.ArgumentParser(
        description="Log in to USTC WLT (wlt.ustc.edu.cn)",
    )

    # Get environment variables
    env_username = os.environ.get("WANGLUOTONG_USERNAME")
    env_password = os.environ.get("WANGLUOTONG_PASSWORD")

    parser.add_argument(
        "--username",
        default=env_username,
        required=env_username is None,
        help="Username for USTC WLT (or set WANGLUOTONG_USERNAME)",
    )
    parser.add_argument(
        "--password",
        default=env_password,
        required=env_password is None,
        help="Password for USTC WLT (or set WANGLUOTONG_PASSWORD)",
    )
    parser.add_argument(
        "--type",
        type=int,
        default=int(os.environ.get("WANGLUOTONG_TYPE", "0")),
        help="Type of network exit (0-7, default: 0, or set WANGLUOTONG_TYPE)",
    )
    parser.add_argument(
        "--exp",
        type=int,
        default=int(os.environ.get("WANGLUOTONG_EXP", "0")),
        help="Expired time (0 means no expiration, default: 0, or set WANGLUOTONG_EXP)",
    )

    args = parser.parse_args()

    # Prepare the request data
    data = {
        "cmd": "set",
        "name": args.username,
        "password": args.password,
        "type": str(args.type),
        "exp": str(args.exp),
    }

    # Make the request
    url = "http://wlt.ustc.edu.cn/cgi-bin/ip"
    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error("Login failed: %s", e)  # noqa: TRY400
        sys.exit(1)
    else:
        # Note: Using HTTP as specified by the USTC WLT service
        logger.info("Login successful!")


if __name__ == "__main__":
    main()
