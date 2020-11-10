"""Clean up Python projects."""

import argparse
from ctypes import WinError
from enum import Enum
from itertools import chain
from pathlib import Path
from shutil import rmtree

from alive_progress import alive_bar


class ItemType(Enum):
    """Item types which are cleaned and associated defaults."""

    DIRECTORY = {
        "logger_string": "directories",
        "patterns": [
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            ".ipynb_checkpoints",
            "docs/_build",
        ],
    }
    FILE = {"logger_string": "files", "patterns": ["Thumbs.db", "DS_Store", ".dccache", "*.log"]}


def search(location: Path, patterns: list[str]) -> list[Path]:
    """Return the paths which match the given set of patterns from any location."""

    def match_pattern(pattern: str) -> list[Path]:
        matches = []
        for match in location.rglob(pattern):
            matches.append(match)
            progress_bar()
        return matches

    with alive_bar(title="Searching...") as progress_bar:
        match_lists = [match_pattern(pattern) for pattern in patterns]
    return list(set(chain.from_iterable(match_lists)))


def delete(path: Path, item_type: ItemType) -> None:
    """Deletes the item at the given path."""
    try:
        if item_type == ItemType.DIRECTORY:
            rmtree(str(path))
        elif item_type == ItemType.FILE:
            path.unlink(missing_ok=True)
    except PermissionError as e:
        print(f"{e} @ {path}, skipping...")
    except WinError as e:
        print(f"{e} @ {path}, skipping...")


def clean(location: Path, item_type: ItemType) -> None:
    """Searches for and then deletes all matches of the given item type at the given location."""
    matches = search(location, item_type.value)
    with alive_bar(len(matches), title="Deleting...") as progress_bar:
        for match in matches:
            delete(match, item_type)
            progress_bar()


def main(location: str) -> None:
    """Runs the clean function for directories and files."""
    location = Path.cwd() if not location else Path(location).resolve()
    print("\nCLEANING DIRECTORIES")
    print("--------------------")
    clean(location, ItemType.DIRECTORY)
    print("\nCLEANING FILES")
    print("---------------")
    clean(location, ItemType.FILE)


def parse_root_arg():
    """Returns the location root command line argument."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=str, required=False, default=None)
    args = parser.parse_args()
    return args.root


if __name__ == "__main__":
    root = parse_root_arg()
    main(root)
