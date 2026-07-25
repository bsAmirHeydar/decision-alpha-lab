# EXP0013 Finalization Snapshot

This folder records the latest astro-only finalization pass run on:

- CSV: `data/astro/astro_NAS100_M1_20260622_to_now_nasdaq100_natal_mql.csv`
- doctrine config: `src/engine/legacy/research/astro_feature_builder/astro_config.example.json`

## Recommended operating profile

- profile: `pure_strict`
- tuned candidate: `pure_strict_tuned`
- tuned override: `min_micro_timing = 54.0`

## Final-entry results

### `pure_strict`

- rows scanned: `5736`
- pure entry bars: `607`
- probe bars: `62`
- blocked bars: `5067`
- final entry windows: `11`
- direction mix: `long only` in this sample

Top veto reasons:

- `no_direction`: `5015`
- `low_weight`: `77`
- `low_family_count`: `62`
- `micro_timing_low`: `37`

### `pure_balanced`

- pure entry bars: `659`
- final entry windows: `13`

### `pure_probe`

- pure entry bars: `698`
- final entry windows: `13`

## Family validation snapshot

Current promotion snapshot marks all reviewed families as:

- `candidate_for_review`

Families:

- `A0001`
- `A0002`
- `A0003`
- `A0004`
- `A0005`
- `A0006`
- `A0007`
- `A0090`

## Notes

- This is still an astro-only research stack.
- The finalization pass does not use price-side targets, indicators, or market-structure filters.
- MT5 compile/runtime closure for every execution family still remains a separate runtime-proof task.
