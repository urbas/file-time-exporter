from pathlib import Path
from typing import Iterable, Optional


def by_glob(base_dir: Path, glob_pattern: str) -> Iterable[Path]:
    """Find files matching glob_pattern in base_dir and return them as a list."""
    return base_dir.glob(glob_pattern)


def newest_file(paths: Iterable[Path]) -> Optional[Path]:
    """Return the newest file from a list of paths."""
    return max(paths, key=lambda path: path.stat().st_mtime)


def get_file_timestamp(path: Path) -> float:
    """Return the UTC timestamp of a file."""
    return path.stat().st_mtime
