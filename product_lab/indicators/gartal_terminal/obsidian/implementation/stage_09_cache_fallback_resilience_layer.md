# Stage 09 — Cache / Fallback / Resilience Layer

## Objective

Stage 09 turns `gartal terminal` from a visually rich news indicator into a resilient product surface. The terminal must not collapse when the live source is missing, malformed, delayed, blocked, or structurally changed. It must classify the data source, explain the fallback state, and keep rendering the best available macro tape.

## Product Doctrine

The user should always know which data layer is driving the chart:

```text
LIVE → verified source payload parsed successfully
CACHE → verified cache used while live source is unavailable
STALE_CACHE → old but accepted cache used because fallback rules allow it
SAMPLE_FALLBACK → deterministic sample tape used as last-resort visual continuity
FAILED → no usable data source
```

Silent failure is forbidden. Every fallback path must write a readable diagnostic into the dashboard and runtime log.

## Engineering Scope

Stage 09 implements:

- source sanity checks before parsing
- raw byte guardrails
- event-block threshold guardrails
- lightweight raw hash tracking
- verified cache bundle save
- cache metadata sidecar
- cache freshness classification
- stale/expired cache policy
- failover accounting
- source quality propagation into `GT_NewsStore`
- dashboard source-health messaging
- downloader EA metadata output

## Main Module

```text
mql5/include/GartalNewsResilience.mqh
```

This module owns all resilience policy. It does not parse events and does not render chart objects. It only decides whether a raw payload is usable and how trustworthy it is.

## Refresh Chain

```text
GT_RefreshCalendar()
  → throttle guard
  → live/local raw source fetch
  → raw sanity check
  → parser
  → verified cache save
  → cache bundle load if live failed
  → parser again
  → sample fallback if cache failed
  → source quality applied to store
  → dashboard/timeline repaint
```

## Source Sanity Contract

A raw payload is allowed into the parser only if it passes:

- non-empty payload
- minimum raw bytes
- maximum raw bytes
- minimum `<event>` block count when required
- XML calendar structural hints such as `<country>`, `<title>`, `<impact>`

This catches most drift cases before they corrupt the event store.

## Cache Bundle Contract

The cache bundle has two layers:

```text
GartalTerminal/calendar_cache.txt   → raw verified calendar payload
GartalTerminal/calendar_cache.meta  → saved_at, bytes, source URL, hash, event blocks, parser summary
```

The raw cache is only written after live source passes sanity and parser acceptance.

## Freshness States

```text
FRESH       → age <= InpCacheFreshMinutes
STALE       → age > fresh threshold but <= stale/max policy
EXPIRED     → age > InpCacheMaxAgeHours
UNKNOWN_AGE → metadata missing or unreadable
MISS        → cache raw file unavailable
```

The input policy decides whether stale, expired, or unknown-age cache may be used.

## Dashboard Contract

The dashboard health badge must not simply say `LIVE` when fallback is active. It now displays:

- `LIVE`
- `CACHE`
- `STALE CACHE`
- `SAMPLE`
- `ERROR`

The health bar also shows source quality, cache status, sanity result, bytes, attempts, and parser status.

## Handoff to Stage 10

Stage 10 should now focus on product hardening, packaging, licensing hooks, release build discipline, customer install flow, and Beta/Stable release gates. The source pipeline is now resilient enough to be packaged.
