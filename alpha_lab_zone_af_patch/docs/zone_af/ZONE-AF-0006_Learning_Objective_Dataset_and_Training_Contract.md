---
type: canonical_research_contract
id: ZONE-AF-0006
status: draft
language: english
project: Decision Alpha Lab
concepts:
  - Learning Objective
  - Dataset Contract
  - Zone Labeling
  - MFE MAE
  - Ranking Model
---

# ZONE-AF-0006 — Learning Objective, Dataset, and Training Contract

## 1. Core Learning Thesis

The model should not first learn win/loss. It should first learn **zone quality**.

Primary questions:

```text
Which zones are worth risking?
Which zones are dead?
Which zones create tail expansion?
Which zones have low MAE relative to MFE?
Which zones require lower-timeframe refinement?
Which broad areas are unsafe until a child zone appears?
```

---

## 2. Why Win Rate Is Not the First Objective

The project is designed around bounded loss and open profit. A low or moderate win rate can still be valid if:

- losses are small;
- winners are large;
- tail winners exist;
- MFE/MAE is strong;
- path quality allows holding;
- bad zones are filtered.

Therefore, a model that improves tail capture and MFE/MAE but does not improve raw win rate can still be successful.

---

## 3. Sample Unit

Preferred sample unit:

```text
Zone Touch Event
```

Why not only Zone?

A single zone can receive multiple touches. Each touch can have different context, session, approach speed, and reaction quality.

Why not only Trade?

Trade PnL depends on entry and management. Zone research should first measure the potential created by the zone itself.

---

## 4. Dataset Layers

### 4.1 Zone Table

One row per zone.

```yaml
zone_id: string
symbol: string
timeframe: string
source_type: hook | f1 | f2_case_a | f2_case_b | f2_symmetry | f3 | other
status_at_creation: candidate | watch | tradable
entry_edge_price: float | null
stop_edge_price: float | null
has_stable_stop: bool
requires_ltf_refinement: bool
parent_zone_id: string | null
width_atr: float
source_quality_score: float
context_state: string
```

### 4.2 Touch Event Table

One row per touch.

```yaml
touch_id: string
zone_id: string
touch_time: timestamp
touch_depth_pct: float
touch_number: int
session: string
approach_speed: float
approach_compression: float
entry_triggered: bool
mae: float
mfe: float
mfe_mae_ratio: float
time_to_expansion: int
path_smoothness: float
outcome_label: string
```

### 4.3 Trade Table

One row per actual entry.

```yaml
trade_id: string
touch_id: string
entry_type: limit | scaled_limit | manual | paper | live
entry_price: float
stop_price: float
initial_risk: float
exit_price: float | null
realized_r: float | null
max_r: float
exit_reason: string
management_policy: string
```

---

## 5. Outcome Labels

Recommended labels:

```text
held_and_expanded
held_but_choppy
failed_cleanly
failed_then_reversed
fake_break_success
failure_continuation
dead_zone
missed_touch
no_child_zone
```

Continuous labels:

```text
MFE
MAE
MFE/MAE
Time-to-Expansion
Path Smoothness
Tail Expansion Score
Invalidation Efficiency
Dead-Zone Score
```

---

## 6. First Training Objective

The first ML objective should be zone ranking, not direct buy/sell prediction.

Examples:

```text
Rank zones by future MFE/MAE.
Classify top-decile zones by tail expansion.
Filter bottom-decile dead zones.
Estimate probability that a broad parent zone needs child refinement.
```

---

## 7. Model Family

Start simple:

- rule-based score;
- logistic regression for sanity check;
- random forest baseline;
- gradient boosting ranking model;
- quantile-based classifier;
- survival/time-to-expansion model later.

Avoid deep models before labels are clean.

---

## 8. Evaluation Metrics

Do not evaluate only accuracy.

Use:

```text
Top-decile MFE/MAE improvement
Tail capture ratio
Dead-zone removal rate
Average MAE reduction
Median time-to-expansion reduction
Path smoothness improvement
Potential/Width improvement
Expected R distribution
```

---

## 9. Required Anti-Leakage Rule

A zone must be generated using only information available at generation time.

Invalid examples:

- drawing a zone after seeing the reversal;
- using future MFE in features;
- using post-touch structure to define pre-touch entry edge;
- labeling a zone as valid because it worked.

The system must separate:

```text
features_before_touch
outcome_after_touch
```

---

## 10. Training Roadmap

1. Mechanical zone extraction.
2. Zone/touch event logging.
3. Outcome labeling without trades.
4. Rule-based Zone Quality Score.
5. Top/bottom decile analysis.
6. Ranking model.
7. Bad-zone filter.
8. Parent/child refinement model.
9. Entry meta-labeling.
10. Management/tail-holding model.

---

## 11. Success Definition

The training is successful if it helps the system find zones where bounded loss buys access to larger and cleaner payoff.

It does not need to maximize win rate first.

