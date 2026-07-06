---
type: training_contract
id: ZONE-DATASET-CONTRACT
status: draft
language: english
---

# Zone Dataset Contract

The dataset should contain at least three layers:

1. Zone table.
2. Touch event table.
3. Trade table.

The first model should learn from zone and touch outcome, not only realized trade PnL.

## Required Core Fields

```yaml
zone_id: string
source_type: string
timeframe: string
entry_edge_price: float | null
stop_edge_price: float | null
has_stable_stop: bool
requires_ltf_refinement: bool
width_atr: float
parent_zone_id: string | null
mfe_after_touch: float
mae_after_touch: float
mfe_mae_ratio: float
path_smoothness: float
outcome_label: string
```

