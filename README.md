# File Time Exporter

A Prometheus exporter that exports file timestamps.

Example use-cases:

- track that your backups are up-to-date
- track that your regular processes that touch or create files don't skip a beat

## Usage

```bash
file-time-exporter --port 12345 --refresh-interval 120 example_config.yaml
```

See [example configuration](example_config.yaml).
