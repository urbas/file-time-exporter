from pathlib import Path
from typing import Any, Dict, Optional

from file_time_exporter import timestamp_extractors


def lookup_timestamp(config: Dict[str, Any]) -> Optional[float]:
    """
    Lookup the timestamp of a single file.
    """
    try:
        timestamp_extractor = timestamp_extractors.get_strategy(config)
        return timestamp_extractor(Path(config["path"]))
    except FileNotFoundError:
        return None
