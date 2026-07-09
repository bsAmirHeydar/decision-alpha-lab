# Stage 10 — Product Hardening + Packaging + Release Build

Status: implementation patch  
Product: [[gartal terminal]]  
Previous: [[stage_09_cache_fallback_resilience_layer]]  
Next: MetaEditor compile gate + beta QA

## Core idea

The first nine stages built the terminal's technical organs:

1. core lifecycle
2. event model
3. time normalization
4. chart timeline
5. luxury dashboard
6. runtime filters
7. alert state machine
8. Forex Factory/Fair Economy source adapter
9. resilience and cache failover

Stage 10 makes that system shippable. The main principle is simple: customer builds must have explicit release identity, controlled presets, clear installation docs, and no silent debug/demo behavior.

## Implemented modules

- `GartalNewsProduct.mqh`
- release profile inputs
- license mode hook
- strict release mode
- dashboard release badge
- brand watermark
- release presets
- customer docs
- package scripts
- beta QA checklist

## Release profile flow

```text
Inputs
  -> GT_LoadConfig
  -> GT_ApplyReleaseProfile
  -> GT_ValidateConfig
  -> GT_ProductValidateLicense
  -> GT_NormalizeConfigTime
  -> GT_RefreshCalendar
```

The profile is applied before validation so stable/strict release rules can block invalid customer builds.

## License hook doctrine

Current licensing is intentionally a hook, not a final protection system. It gives the product a clean place to enforce license policy later without coupling licensing to dashboard, parser, alerts, or source fetch.

Current modes:

| Mode | Meaning |
|---|---|
| OFF | no license check |
| OPTIONAL | missing key becomes demo/audit state |
| REQUIRED | missing/short key blocks init |

## Strict release mode

Strict release mode does the following:

- hides time/timeline/resilience debug strips
- clamps dashboard rows
- forces product-grade dashboard defaults
- blocks stable builds from sample-data mode
- disables log-only alert mode

## Packaging doctrine

The packaging script does not compile MQL5. Compilation remains a MetaEditor gate. The script only packages compiled artifacts if present, plus presets and customer docs.

## Stage 10 acceptance

- product identity visible in dashboard
- release channel visible in dashboard
- license status visible in health row
- beta/live/stable presets present
- customer install docs present
- package script produces a release zip
- QA checklist exists before paid distribution
