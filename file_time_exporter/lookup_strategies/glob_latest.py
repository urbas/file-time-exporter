from pathlib import Path
from typing import Any, Dict, Optional

from file_time_exporter import timestamp_extractors


def lookup_timestamp(config: Dict[str, Any]) -> Optional[float]:
    """
    Returns the timestamp of the latest file matching the glob pattern.
    """
    paths = Path(config["directory"]).glob(config["glob"])
    timestamp_extractor = timestamp_extractors.get_strategy(config)
    all_timestamps = [timestamp_extractor(path) for path in paths]
    return max(all_timestamps, default=None)
