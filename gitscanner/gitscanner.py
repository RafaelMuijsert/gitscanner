#!/usr/bin/env python3
"""
Scans each project group for open Git repositories.
"""
import argparse
import json
import logging

import requests

SCHEME = "http://"
POSTFIX = ".webtech-uva.nl/"


def git_exposed(url):
    """
    Checks whether the site located at URL contains an exposed Git repository.

    Parameters:
        url (str): The URL which should be checked. Must end with a /.

    Returns:
        bool: True if the URL contains an exposed repository, otherwise False.
    """
    try:
        response = requests.get(url + ".git", timeout=1)
        return response.status_code == 200
    except requests.RequestException as err:
        logging.debug(err)
        return False


def load_groups(file_path):
    """
    Loads each project group from a JSON file.

    Parameters:
        file_path (str): The path to the JSON file containing each group.

    Returns:
        dict: A dictionary in the form group->members.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_exposed_repositories(groups):
    """
    Gets each exposed repository from a dictionary of groups.

    Parameters:
        groups (dict): A dictionary in the form group->members

    Returns:
        list: A list containing the URLs of exposed repositories from groups.
    """
    exposed = []
    for group in groups:
        # Check whether the root URL contains a Git repo
        base = SCHEME + group + POSTFIX
        if git_exposed(base):
            exposed.append(base)

        for person in groups[group]:
            url = f"{base}~{person}/"
            if git_exposed(url):
                exposed.append(url)

    return exposed


def main():
    """
    Evaluates each URL combination
    """
    parser = argparse.ArgumentParser(description="Scan for exposed Git repo's")
    parser.add_argument("filename")
    args = parser.parse_args()

    groups = load_groups(args.filename)
    exposed_repositories = get_exposed_repositories(groups)
    for url in exposed_repositories:
        print(url)


if __name__ == "__main__":
    main()
