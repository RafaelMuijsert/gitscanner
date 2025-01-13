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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def git_exposed(url: str) -> bool:
    """Check whether the site located at URL contains an exposed Git repository.

    Arguments:
        url (str): The URL which should be checked. Must end with a /.

    Returns:
    -------
        bool: True if the URL contains an exposed repository, otherwise False.

    """
    try:
        response = requests.get(url + ".git", timeout=1)
    except requests.RequestException as err:
        logger.debug(err)
        return False
    else:
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


def get_exposed_repositories(urls: list[str]) -> list[str]:
    """Get each exposed repository from a dictionary of groups.

    Arguments:
        urls (dict): A dictionary in the form group->members

    Returns:
        list: A list containing the URLs of exposed repositories from groups.

    """
    exposed: list[str] = [url for url in urls if git_exposed(url)]
    return exposed


def main() -> None:
    """Evaluate each URL combination."""
    parser = argparse.ArgumentParser(description="Scan for exposed Git repos")
    _ = parser.add_argument("filename")
    args = parser.parse_args()

    file_name: str = args.filename  # pyright: ignore[reportAny]
    urls = load_urls(file_name)
    exposed_repositories = get_exposed_repositories(urls)
    for url in exposed_repositories:
        _ = sys.stdout.write(url + "\n")


if __name__ == "__main__":
    main()
