---
title: RTHP Known-Time Guard IR
status: compiled
version: 1.0.2
---
# Known-Time Guard IR

- Known-Time IR digest: `sha256:1a80fa97f50f0e92ab9f2e3f03b6b435ccd17d5451a64d7568754cb87398c09f`
- Timezone: `America/New_York`
- Calendar: `RTHP_AMERICA_NEW_YORK_CALENDAR_V1`
- Late-data policy: `APPEND_CORRECTION`
- Future revisions allowed in-place: `false`

## Causal order

- `event_time <= observation_time`; failure action: `REJECT_EVENT`
- `observation_time <= known_time`; failure action: `REJECT_EVENT`
- `known_time <= decision_time`; failure action: `REJECT_EVENT`
- `decision_time <= maturity_time`; failure action: `REJECT_EVENT`
- `maturity_time <= correction_time`; failure action: `REJECT_EVENT`

## RTHP-specific safety

A stale or imputed observation may be retained as evidence but may not confirm divergence. Synchronized real evidence is required at the common M15 cut. A late correction is append-only and cannot rewrite the historical known-time path.
