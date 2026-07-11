# Strategy Factory Phase 20

This patch integrates EXP0017 Temporal Intermarket Divergence as the first real Strategy Factory anatomy adapter. It preserves the legacy detector, maps ready one-sided divergence candidates into canonical events, records stable lineage, suppresses duplicates, retires absent identities, creates differential evidence, routes through context and candidate boundaries, gates unsupported downstream stages, and emits monitoring telemetry. Live order authority is absent.

Local MetaEditor compile and controlled terminal replay remain required before the pilot can be considered operationally accepted.
