from pathlib import Path

from file_time_exporter.timestamp_extractors import from_json_content


def test_from_json_content() -> None:
    path = Path(__file__).parent / "../files/from-json-content.json"

    config = {
        "jsonpath": "foo.date",
        "timestamp_pattern": "%Y-%m-%dT%H:%M:%S%z",
    }

    assert from_json_content(path, config) == 1769975004.0
