import json
from datetime import datetime
from pathlib import Path
from typing import Any

from jsonpath_ng import parse


def from_json_content(path: Path, config: dict[str, Any]) -> float:
    """Extract a timestamp from a JSON file's content."""
    jsonpath = config["jsonpath"]
    timestamp_pattern = config["timestamp_pattern"]

    with path.open("r") as f:
        data = json.load(f)

    jsonpath_expr = parse(jsonpath)
    matches = jsonpath_expr.find(data)

    if not matches:
        raise ValueError(f"No matches found for JSONPath: {jsonpath}")

    timestamp_str = matches[0].value
    return datetime.strptime(timestamp_str, timestamp_pattern).timestamp()
