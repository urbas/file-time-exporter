import logging
import time
from typing import Any, Callable, Dict, Optional

import click
import yaml
from prometheus_client import Gauge, Summary, start_http_server

from file_time_exporter.lookup_strategies import glob_latest, single_file

FileLookupStrategy = Callable[[Dict[str, Any]], Optional[float]]

KNOWN_STRATEGIES: Dict[str, FileLookupStrategy] = {
    "single-file": single_file.lookup_timestamp,
    "glob-latest": glob_latest.lookup_timestamp,
}
LOG = logging.getLogger(__name__)


@click.command()
@click.argument("config_file", type=click.Path(exists=True, file_okay=True))
@click.option(
    "--refresh-interval",
    default=10,
    type=click.INT,
    help="Refresh interval in seconds",
    show_default=True,
)
@click.option(
    "--port", default=9426, type=click.INT, help="Port to listen on", show_default=True
)
@click.option(
    "--listen-address",
    default="localhost",
    type=click.STRING,
    help="Address to listen on",
    show_default=True,
)
@click.option(
    "--verbose",
    "-v",
    count=True,
    help="Increase verbosity. Can be used multiple times.",
)
@click.option(
    "--quiet",
    "-q",
    count=True,
    help="Decrease verbosity. Can be used multiple times.",
)
def main(
    config_file: str,
    refresh_interval: int,
    port: int,
    listen_address: str,
    verbose: int,
    quiet: int,
):
    """
    A Prometheus exporter that tracks modification timestamps of files as
    specified in the CONFIG_FILE yaml configuration.
    """

    # Set up logging verbosity
    verbosity = verbose - quiet
    if verbosity >= 2:
        level = logging.DEBUG
    elif verbosity == 1:
        level = logging.INFO
    elif verbosity == 0:
        level = logging.WARNING
    elif verbosity == -1:
        level = logging.ERROR
    else:
        level = logging.CRITICAL
    logging.basicConfig(level=level)

    request_time = Summary("file_time_seconds", "Time spent processing request", ["id"])

    file_time = Gauge(
        "file_time",
        "The timestamp of a tracked file.",
        ["id"],
    )

    with open(config_file) as config_file_handle:
        config = yaml.safe_load(config_file_handle)
    LOG.debug("Loaded config with %d entries", len(config))

    start_http_server(port, addr=listen_address)
    LOG.info("Started HTTP server on %s:%d", listen_address, port)

    while True:
        for config_entry in config:
            LOG.debug("Processing config entry: %s", config_entry["id"])
            start_time = time.time()
            strategy = KNOWN_STRATEGIES.get(config_entry["strategy"])
            if strategy is None:
                raise NotImplementedError(
                    f"Unknown file lookup strategy '{config_entry['strategy']}'."
                )
            file_timestamp = strategy(config_entry["config"])
            if file_timestamp is not None:
                file_time.labels(config_entry["id"]).set(file_timestamp)
                LOG.debug(
                    "Set timestamp for %s to %f", config_entry["id"], file_timestamp
                )
            else:
                LOG.debug("No timestamp found for %s", config_entry["id"])

            end_time = time.time()
            request_time.labels(config_entry["id"]).observe(end_time - start_time)

        time.sleep(refresh_interval)
