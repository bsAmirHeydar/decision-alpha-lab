# 03 — Fallback Chain

## Chain

```text
LIVE SOURCE
  ↓ if fetch/sanity/parser fails
VERIFIED CACHE
  ↓ if missing/rejected
STALE CACHE
  ↓ if policy allows
SAMPLE FALLBACK
  ↓ if enabled
FAILED
```

## Policy

Fallback is not a hidden technical behavior. It is a product-state transition.

## Runtime Fields

```text
runtime.source_quality
runtime.source_quality_text
runtime.source_using_cache
runtime.source_using_stale_cache
runtime.source_using_sample_fallback
runtime.resilience_failover_count
runtime.resilience_last_summary
```
