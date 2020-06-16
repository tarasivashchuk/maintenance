"""Common common_code."""
from logging import Logger
from pathlib import Path
from typing import List
from typing import Optional

import logzero

from alive_progress import alive_bar


def clean(location: Path, patterns: List[str], logger: Optional[Logger] = None):
    """Clean the target location of all patterns."""
    with alive_bar(title="Cleaning...") as progress:
        for pattern in patterns:
            for match in location.rglob(pattern):
                try:
                    clean_match(progress, match)
                    if logger is not None:
                        logger.info(f"Successfully cleaned: {match}")
                except Exception as e:
                    if logger is not None:
                        logger.error(f"For {match}: {e}")
                    raise e
    return True


def clean_match(progress, match):
    if match.is_dir():
        return clean_dir(progress, match)
    else:
        return clean_file(progress, match)


def clean_dir(progress, path):
    for match in path.glob("*"):
        if match.is_dir():
            clean_dir(progress, match)
        else:
            clean_file(progress, match)
    path.rmdir()
    return progress()


def clean_file(progress, file):
    file.unlink()
    return progress()


def parse_args():
    """Parse arguments for modifying functionality."""
    import argparse

    parser = argparse.ArgumentParser(description="Common common_code")

    parser.add_argument(
        "--config",
        required=False,
        type=str,
        default="/Users/taras/.config/clean.maintenance",
        help="Name of the config file with patterns to use for matching and removing",
    )
    parser.add_argument(
        "--location",
        "-l",
        type=str,
        required=False,
        default=str(Path().cwd().resolve()),
        help="Location from which to recursively search for patterns",
    )
    parser.add_argument(
        "--log",
        required=False,
        default=False,
        action="store_true",
        help="Whether to log the cleaned files and directories",
    )
    parser.add_argument(
        "--extra-patterns",
        "-e",
        nargs="*",
        required=False,
        help="Any extra matching patterns not in the configuration file",
    )
    return parser.parse_args()


def load_patterns_config(path: Path) -> List[str]:
    if not path.exists():
        raise FileNotFoundError("No cleaning configuration file found!")
    with path.open() as f:
        cleaning_patterns = [pattern.strip() for pattern in f.readlines()]
    return cleaning_patterns


def main():
    """Run the module."""
    args = parse_args()
    cleaning_patterns = load_patterns_config(Path(args.config))
    location = Path(args.location)
    logger = logzero.setup_logger(name="maintenance-clean") if args.log else None
    if args.extra_patterns:
        [cleaning_patterns.append(pattern) for pattern in args.extra_patterns]
    return clean(location, cleaning_patterns, logger)


if __name__ == "__main__":
    main()
