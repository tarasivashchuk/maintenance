"""Common common_code."""

import shutil

from pathlib import Path
from time import time
from typing import List

from tqdm.auto import tqdm

import common_code


def clean(location: Path, patterns: List[str]):
    """Clean the target location of all patterns."""

    dirs_progress = tqdm(desc="Directories")
    files_progress = tqdm(desc="Files")

    start = time()
    for pattern in patterns:
        for match in location.rglob(f"**/{pattern}"):
            if match.is_dir():
                shutil.rmtree(match.as_posix())
                dirs_progress.update()
            else:
                match.unlink()
                files_progress.update()
    end = time()
    print(f"Pattern matching successfully completed in {int(end-start)} seconds!")


def parse_args():
    """Parse arguments for modifying functionality."""
    import argparse

    parser = argparse.ArgumentParser(description="Common common_code")

    parser.add_argument(
        "--config",
        "-C",
        required=False,
        type=str,
        default=".clean",
        help="Name of the config file with patterns to use for matching and removing",
    )
    parser.add_argument(
        "--patterns",
        "-P",
        nargs="*",
        required=False,
        help="Any extra matching patterns not in the configuration file",
    )
    parser.add_argument(
        "--location",
        "-L",
        type=str,
        required=False,
        default="/Users/taras",
        help="Location from which to recursively search for patterns",
    )

    return parser.parse_args()


def main():
    """Run the module."""
    args = parse_args()
    clean_config = common_code.config_dir.joinpath(args.config)
    if not clean_config.exists():
        raise FileNotFoundError("No cleaning configuration file found!")
    with clean_config.open() as f:
        cleaning_patterns = [pattern.strip() for pattern in f.readlines()]
    if args.patterns:
        [cleaning_patterns.append(pattern) for pattern in args.patterns]
    location = Path(args.location)
    clean(location, cleaning_patterns)


if __name__ == "__main__":
    main()
