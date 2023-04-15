#!/usr/bin/env python3

import logging
import argparse
import os
import requests
import tarfile

REPOSITORY_OWNER = "GloriousEggroll"
REPOSITORY_NAME = "proton-ge-custom"

PROTON_PATH = os.path.expanduser("~/.steam/root/compatibilitytools.d")


def download_release(release: dict):
    assets = release["assets"]
    tgz_asset = next(filter(lambda x: x["name"].endswith(".tar.gz"), assets))
    response = requests.get(tgz_asset["browser_download_url"], stream=True)
    file = tarfile.open(fileobj=response.raw, mode="r|gz")
    file.extractall(PROTON_PATH)


def list_releases() -> list[dict]:
    url = f"https://api.github.com/repos/{REPOSITORY_OWNER}/{REPOSITORY_NAME}/releases"
    response = requests.get(url)
    return response.json()


class LatestCommand:
    def setup_parser(self, subparser):
        subparser.add_argument("--count", type=int, default=1)

    def run(self, args):
        releases = list_releases()
        for release in releases[: args.count]:
            if os.path.exists(f"{PROTON_PATH}/{release['tag_name']}"):
                logging.info(f"Skipping {release['tag_name']}, already exists")
                continue

            logging.info(f"Downloading {release['tag_name']}")
            download_release(release)


def main():
    logging.basicConfig(level=logging.INFO)

    argparser = argparse.ArgumentParser()
    subparsers = argparser.add_subparsers(dest="command", required=True)

    latest_command = LatestCommand()
    latest_command.setup_parser(subparsers.add_parser("latest"))

    args = argparser.parse_args()

    if args.command == "latest":
        latest_command.run(args)


if __name__ == "__main__":
    main()
