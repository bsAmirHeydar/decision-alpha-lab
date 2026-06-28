# Flag Counting Validation Case Registry

Status: active validation registry for Phoenix.
Source of truth: `docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md`.

## Purpose

This registry turns validation from visual opinion into deterministic baselines.

Broker-specific symbol names and exact historical availability differ. Therefore a case has two states:

```text
baseline_required
baselined
```

Do not invent expected counts. The first accepted run for a pinned broker/range creates the baseline; later patches compare against it.

---

## Baseline file naming

Recommended output location:

```text
lab/03_experiments/EXP_flag_counting/validation_cases/
```

Recommended files per case:

```text
FC-GC-001_node_plateau.json
FC-GC-001_node_plateau.png
FC-GC-001_node_plateau_report.md
```

---

## Required fields per baseline

```yaml
case_id:
title:
status: baseline_required | baselined
broker_symbol:
timeframe:
from_time:
to_time:
timezone_or_broker_time:
inputs_hash:
source_commit:
expected_node_count_by_L:
expected_hook_count_by_L:
expected_raw_event_count:
expected_visible_event_count:
expected_visible_f1_count:
expected_visible_f2_count:
expected_visible_f3_count:
expected_locked_f3_count:
expected_hidden_count:
known_screenshot:
audit_export_file:
notes:
```

---

## Mandatory baseline cases

### FC-GC-001 — Node plateau and equality

Purpose:

```text
Prove plateau highs/lows emit one node and equality is not a break.
```

Required status before Level 02 freeze: `baselined`.

### FC-GC-002 — Hook/ND branch size

Purpose:

```text
Prove 2-node branch is not ND, 3/4-node branch can be ND, and >4 branch rejects current L or requires higher L.
```

Required status before Level 04 freeze: `baselined`.

### FC-GC-003 — Bullish and bearish flag body

Purpose:

```text
Prove Origin -> Leg1 -> Waist -> Leg2 construction for both directions and strict Leg2 break.
```

Required status before Level 05 freeze: `baselined`.

### FC-GC-004 — F1 internal confirmation

Purpose:

```text
Prove F1 confirms only after internal 1/2 and Leg2 re-break before Waist invalidation.
```

Required status before Level 07 freeze: `baselined`.

### FC-GC-005 — F2 backfill and size qualification

Purpose:

```text
Prove F2 origin is strict-window backfilled from post-F1 correction, and undersized F2 cannot authorize F3.
```

Required status before Level 08 freeze: `baselined`.

### FC-GC-006 — F3 OR completion and lock

Purpose:

```text
Prove F3 OR condition and locked persistence after first confirmed opposite F1.
```

Required status before Level 09 freeze: `baselined`.

### FC-GC-007 — Sequence ownership and duplicate hiding

Purpose:

```text
Prove repeated same-direction F1s in one phase are hidden from main chart with reasons, while audit preserves them.
```

Required status before Level 10/11 freeze: `baselined`.

### FC-GC-008 — Renderer independence

Purpose:

```text
Prove renderer settings do not change raw_events, visible_events, IDs, or canonical winners.
```

Required status before Level 12 freeze: `baselined`.

### FC-GC-009 — Time gap/index curve stability

Purpose:

```text
Prove index-based curves and labels survive weekend/time gaps without geometry corruption.
```

Required status before Level 12 freeze: `baselined`.

### FC-GC-010 — Full Phoenix smoke range

Purpose:

```text
Run multi-L Phoenix on a dense real market range and store raw/visible event summary for regression.
```

Required status before release candidate: `baselined`.

---

## Recommended real-market seed ranges

Use these as starting candidates, then pin exact broker-valid ranges in the baseline files:

```text
GOLD M1 trend continuation range
GOLD M1 reversal range
GOLD H1 long historical range
Weekend/time-gap range
Dense equal-high/equal-low range
Known F1 -> F2 -> F3 chain range
Hook branch >4 requiring higher L range
```

The exact `from_time`, `to_time`, and expected counts must come from the user's MT5 data, not from documentation guesses.
