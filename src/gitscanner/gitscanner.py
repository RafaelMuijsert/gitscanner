#!/usr/bin/env python3
"""Scans each project group for open Git repositories.

Copyright (C) 2025
"""

import argparse
import json
import logging
import sys
from pathlib import Path

import requests

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 5


def git_exposed(url: str, timeout: float = DEFAULT_TIMEOUT) -> bool:
    """Check whether the site located at URL contains an exposed Git repository.

    Arguments:
        url (str): The URL which should be checked. Must end with a /.
        timeout (float): Timeout when checking URLs.

    Returns:
        bool: True if the URL contains an exposed repository, otherwise False.

    """
    try:
        response = requests.get(
            url + ".git" if url.endswith("/") else url + "/.git",
            timeout=timeout,
        )
    except requests.RequestException as err:
        logger.debug(err)
        return False
    else:
        logger.info("%s: %s", url, response.ok)
        return response.ok


def load_urls(file_path: str) -> list[str]:
    """Load URLs from a JSON file.

    Arguments:
        file_path (str): The path to the JSON file containing each group.

    Returns:
        list: A list containing all URLs.

    """
    with Path(file_path).open(encoding="utf-8") as file:
        contents: list[str] = json.load(file)
        return contents


def main() -> None:
    """Evaluate each URL combination."""
    parser = argparse.ArgumentParser(description="Scan for exposed Git repos")
    _ = parser.add_argument("filename")
    _ = parser.add_argument("-v", "--verbose", action="store_true")
    _ = parser.add_argument(
        "-t",
        "--timeout",
        nargs="?",
        const=DEFAULT_TIMEOUT,
        type=float,
    )
    args = parser.parse_args()

    verbose: bool = args.verbose  # pyright: ignore[reportAny]
    logging.basicConfig(level=logging.INFO if verbose else logging.WARNING)

    file_name: str = args.filename  # pyright: ignore[reportAny]
    urls = load_urls(file_name)

    timeout: float = args.timeout  # pyright: ignore[reportAny]

    exposed_repositories: list[str] = [
        url for url in urls if git_exposed(url, timeout=timeout)
    ]
    for url in exposed_repositories:
        _ = sys.stdout.write(url + "\n")


if __name__ == "__main__":
    main()
