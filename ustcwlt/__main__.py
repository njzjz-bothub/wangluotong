"""Main entry point for the command line interface."""

from __future__ import annotations

import argparse
import os
import sys

import requests


def main() -> None:
    """Log in to USTC WLT."""
    parser = argparse.ArgumentParser(
        description="Log in to USTC WLT (wlt.ustc.edu.cn)",
    )
    parser.add_argument(
        "--username",
        default=os.environ.get("USTCWLT_USERNAME"),
        help="Username for USTC WLT (or set USTCWLT_USERNAME)",
    )
    parser.add_argument(
        "--password",
        default=os.environ.get("USTCWLT_PASSWORD"),
        help="Password for USTC WLT (or set USTCWLT_PASSWORD)",
    )
    parser.add_argument(
        "--type",
        type=int,
        default=int(os.environ.get("USTCWLT_TYPE", "0")),
        help="Type of network exit (0-7, default: 0, or set USTCWLT_TYPE)",
    )
    parser.add_argument(
        "--exp",
        type=int,
        default=int(os.environ.get("USTCWLT_EXP", "0")),
        help="Expired time (0 means no expiration, default: 0, or set USTCWLT_EXP)",
    )

    args = parser.parse_args()

    # Validate required arguments
    if not args.username:
        parser.error("--username is required (or set USTCWLT_USERNAME)")
    if not args.password:
        parser.error("--password is required (or set USTCWLT_PASSWORD)")

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
        print(f"Login successful! Response: {response.text}")  # noqa: T201
    except requests.exceptions.RequestException as e:
        print(f"Login failed: {e}", file=sys.stderr)  # noqa: T201
        sys.exit(1)


if __name__ == "__main__":
    main()
