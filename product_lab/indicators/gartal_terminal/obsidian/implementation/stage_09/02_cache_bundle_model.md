# 02 — Cache Bundle Model

## Raw Cache

```text
GartalTerminal/calendar_cache.txt
```

Stores the last verified raw calendar payload.

## Metadata Sidecar

```text
GartalTerminal/calendar_cache.meta
```

Stores:

- product
- stage
- saved_at_epoch
- saved_at_text
- source_url
- source_format
- raw_bytes
- raw_hash
- event_blocks
- parser_summary

## Why Metadata Exists

MT5 file timestamp APIs are not ideal for a portable product workflow. A sidecar file makes cache age explicit, inspectable, and versionable.
