"""Common common_code."""

from pathlib import Path
from typing import List
from typing import Optional

import logzero

from alive_progress import alive_bar


def clean(location: Path, patterns: List[str], logger: Optional[logzero.logger] = None):
    """Clean the target location of all patterns."""
    dirs_progress = alive_bar(title="Directories")
    files_progress = alive_bar(title="Files")
    for pattern in patterns:
        for match in location.rglob(pattern):
            try:
                match_type = clean_match(match)
                dirs_progress.send(1) if match_type == "dir" else files_progress.send(1)
                if logger is not None:
                    logger.info(f"Successfully cleaned: {match}")
            except Exception as e:
                if logger is not None:
                    logger.error(f"For {match}: {e}")
                raise e
    dirs_progress.close()
    files_progress.close()
    return True


def clean_match(match):
    if match.is_dir():
        match.rmdir(match)
        return "dir"
    else:
        match.rm()
        return "file"


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
        type=bool,
        required=False,
        default=False,
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
