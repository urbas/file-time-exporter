import re
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict

TimestampExtractor = Callable[[Path, Dict[str, Any]], float]
ConfiguredTimestampExtractor = Callable[[Path], float]


def get_strategy(config: Dict[str, Any]) -> ConfiguredTimestampExtractor:
    """
    Get a timestamp extractor by name.
    """
    timestamp_extraction_config = config.get("timestamp_extraction", None)
    if timestamp_extraction_config is None:
        extractor = KNOWN_TIMESTAMP_EXTRACTORS["from-file-stat"]
        return lambda path: extractor(path, {})

    strategy_name = timestamp_extraction_config.get("strategy", "from-file-stat")

    strategy = KNOWN_TIMESTAMP_EXTRACTORS.get(strategy_name)
    if strategy is None:
        raise NotImplementedError(
            f"Unknown timestamp extraction strategy '{strategy_name}'."
        )
    return lambda path: strategy(path, timestamp_extraction_config.get("config", {}))


def timestamp_from_filename(path: Path, config: Dict[str, Any]) -> float:
    """
    Extract a timestamp from a filename.
    """
    regex_pattern = config.get("regex_pattern")
    if regex_pattern is None:
        name = path.name
    else:
        name = re.sub(regex_pattern, r"\1", path.name)
    return datetime.strptime(name, config["pattern"]).timestamp()


def stat_timestamp(path: Path, config: Dict[str, Any]) -> float:
    """
    Extract a timestamp from a file's stat.
    """
    if config.get("use_symlink_timestamp", False):
        return path.lstat().st_mtime
    return path.stat().st_mtime


KNOWN_TIMESTAMP_EXTRACTORS: Dict[str, TimestampExtractor] = {
    "from-file-name": timestamp_from_filename,
    "from-file-stat": stat_timestamp,
}
