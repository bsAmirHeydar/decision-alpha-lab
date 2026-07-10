---
id: EXP0018-P05-HOSTILE
title: "P05 Hostile Review and Known Limitations"
project: EXP0018
phase: P05
status: implemented-awaiting-metaeditor-validation
---

# Hostile Review

Threats reviewed:

- missing second symbol interpreted as protected;
- cross-symbol price comparison;
- equality omitted;
- stale P04 fingerprint suppressing open-period updates;
- current partial period treated as valid without policy;
- exact first-touch timestamp fabricated from aggregate OHLC;
- side silently converted into direction;
- duplicate observation identities.

Known limitation: the phase observes touch state from period aggregates and does not claim first-touch chronology. This is acceptable for the P06 close snapshot but must be addressed by chronological replay evidence before lifecycle analytics rely on first-touch time.
