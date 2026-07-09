# STAGE 09 — Cache / Fallback / Resilience Layer

## Status

Implemented as a product-hardening stage after the Forex Factory source adapter.

## Main Code Addition

```text
mql5/include/GartalNewsResilience.mqh
```

## Main Behaviors

1. Throttle refresh attempts.
2. Sanity-check raw source payloads before parsing.
3. Save only verified raw payloads to cache.
4. Write cache metadata sidecar.
5. Load cache with freshness classification.
6. Permit/reject stale, expired, and unknown-age cache based on inputs.
7. Fall back to sample data only after live/cache failure.
8. Propagate source quality to dashboard and event store.

## New Inputs

```text
InpCacheWriteMetadata
InpCacheAllowStale
InpCacheAllowExpired
InpCacheAcceptUnknownAge
InpCacheMetadataFile
InpCacheFreshMinutes
InpCacheStaleAfterMinutes
InpCacheMaxAgeHours
InpSourceMinRawBytes
InpSourceMaxRawBytes
InpSourceMinEventBlocks
InpSourceRequireEventBlocks
InpSourceMinRefreshSeconds
InpShowResilienceDebug
```

## Source Quality States

```text
NONE
LIVE
CACHE
STALE_CACHE
SAMPLE_FALLBACK
FAILED
```

## Cache States

```text
NONE
MISS
FRESH
STALE
EXPIRED
UNKNOWN_AGE
```

## Compile Targets

```text
product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5
product_lab/indicators/gartal_terminal/mql5/experts/GartalNewsDownloaderEA.mq5
```
