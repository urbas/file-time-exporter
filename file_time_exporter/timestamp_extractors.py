import re
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any

from .timestamp_strategies.from_json_content import from_json_content

TimestampExtractor = Callable[[Path, dict[str, Any]], float]
ConfiguredTimestampExtractor = Callable[[Path], float]


def get_strategy(config: dict[str, Any]) -> ConfiguredTimestampExtractor:
    """Get a timestamp extractor by name."""
    timestamp_extraction_config = config.get("timestamp_extraction")
    if timestamp_extraction_config is None:
        extractor = KNOWN_TIMESTAMP_EXTRACTORS["from-file-stat"]
        return lambda path: extractor(path, {})

    strategy_name = timestamp_extraction_config.get("strategy", "from-file-stat")

    strategy = KNOWN_TIMESTAMP_EXTRACTORS.get(strategy_name)
    if strategy is None:
        raise NotImplementedError(
            f"Unknown timestamp extraction strategy '{strategy_name}'.",
        )
    return lambda path: strategy(path, timestamp_extraction_config.get("config", {}))


def timestamp_from_filename(path: Path, config: dict[str, Any]) -> float:
    """Extract a timestamp from a filename."""
    regex_pattern = config.get("regex_pattern")
    if regex_pattern is None:
        name = path.name
    else:
        name = re.sub(regex_pattern, r"\1", path.name)
    return datetime.strptime(name, config["pattern"]).timestamp()


def stat_timestamp(path: Path, config: dict[str, Any]) -> float:
    """Extract a timestamp from a file's stat."""
    if config.get("use_symlink_timestamp", False):
        return path.lstat().st_mtime
    return path.stat().st_mtime


KNOWN_TIMESTAMP_EXTRACTORS: dict[str, TimestampExtractor] = {
    "from-file-name": timestamp_from_filename,
    "from-file-stat": stat_timestamp,
    "from-json-content": from_json_content,
}
