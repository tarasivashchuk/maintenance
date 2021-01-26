"""Clean up Python projects."""

import argparse
from ctypes import WinError
from enum import Enum
from itertools import chain
from pathlib import Path
from shutil import rmtree

import click
from alive_progress import alive_bar


def search(location: Path, patterns: list[str]) -> list[Path]:
    """Return the paths which match the given set of patterns from any location."""

    def match_pattern(pattern: str) -> list[Path]:
        matches = []
        for match in location.rglob(pattern):
            matches.append(match)
            progress_bar()
        return matches

    with alive_bar() as progress_bar:
        match_lists = [match_pattern(pattern) for pattern in patterns]
    return list(set(chain.from_iterable(match_lists)))


def empty_directory(directory_path: Path) -> None:
    for item in directory_path.glob("*"):
        if not item.is_file():
            empty_directory(item)
        item.unlink()

def delete(path: Path) -> None:
    """Deletes the item at the given path."""
    try:
        if path.is_dir():
            empty_directory(path)
        path.unlink()
    except PermissionError:
        click.echo(f"You do not have permissions to delete {path}, skipping...")

def clean(location: Path) -> None:
    """Searches for and then deletes all matches of the given item type at the given location."""
    matches = search(location,)
    with alive_bar(len(matches), title="PyCleaning") as progress_bar:
        for match in matches:
            delete(match)
            progress_bar()


def main(location: str) -> None:
    """Runs the clean function for directories and files."""
    location = Path.cwd() if not location else Path(location).resolve()
    clean(location)


def parse_root_arg():
    """Returns the location root command line argument."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=str, required=False, default=None)
    parser.add_argument("--patterns", nargs="*", type=str, required=True, default=["__pycache__", ".pytest_cache", ".mypy_cache"], help="Glob patterns to recursively search for and delete - can match both files and directories")
    args = parser.parse_args()
    return args.root


def run():
    root = parse_root_arg()    
    main(root)

if __name__ == "__main__":
    run()
