from pathlib import Path
from typing import Any

from file_time_exporter import timestamp_extractors


def lookup_timestamp(config: dict[str, Any]) -> float | None:
    """Lookup the timestamp of a single file."""
    try:
        timestamp_extractor = timestamp_extractors.get_strategy(config)
        return timestamp_extractor(Path(config["path"]))
    except FileNotFoundError:
        return None
