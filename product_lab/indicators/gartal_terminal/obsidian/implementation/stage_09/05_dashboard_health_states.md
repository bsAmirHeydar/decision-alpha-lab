# 05 — Dashboard Health States

## Health Badge

```text
LIVE
CACHE
STALE CACHE
SAMPLE
ERROR
```

## Health Bar

The health bar shows:

```text
source=<store.source_status>
quality=<runtime.source_quality_text>
fetch=<fetch mode>
bytes=<raw bytes>
attempts=<refresh attempts>
cache=<cache status>
sanity=<sanity summary>
parser=<parser summary>
```

## Resilience Debug

When `InpShowResilienceDebug=true`, the dashboard renders an extra diagnostic strip with cache age, cache state, save/load counters, sanity failures, and failover count.
