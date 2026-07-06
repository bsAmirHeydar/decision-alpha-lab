---
type: canonical_architecture
id: ZONE-AF-0002
status: draft
language: english
project: Decision Alpha Lab
concepts:
  - Zone Object
  - Zone Lifecycle
  - Risk Contract
  - Stop Expiration
  - Touch Event
---

# ZONE-AF-0002 — Zone Object, Lifecycle, and Risk Contract

## 1. Zone Object Definition

A zone is a bounded price object with an explicit risk contract.

Minimum definition:

```yaml
zone_id: string
symbol: string
timeframe: string
source_type: enum
parent_zone_id: string | null
direction_mode: bullish | bearish | dual | neutral
entry_edge_price: float
stop_edge_price: float
upper_price: float
lower_price: float
zone_width_points: float
zone_width_atr: float
created_at: timestamp
valid_from: timestamp
valid_until: timestamp | null
status: candidate | watch | tradable | active | expired | failed | consumed
```

The entry edge and stop edge depend on directional interpretation.

For a bullish limit zone:

```text
Entry edge = upper or first-touch side of the demand/reversal area
Stop edge  = lower expiration side of the zone
```

For a bearish limit zone:

```text
Entry edge = lower or first-touch side of the supply/reversal area
Stop edge  = upper expiration side of the zone
```

The exact side convention must be standardized in implementation. The philosophical rule is stable:

> The first tradable boundary is the entry area. The far side is the expiration area.

---

## 2. Zone Categories by Execution Stability

Not every potential area is executable. The system must classify zones by execution stability.

### 2.1 Execution Zone

An execution zone has:

- defined entry edge;
- defined stop edge;
- acceptable width;
- mechanical source;
- valid context;
- stable expiration rule.

This zone can receive a limit order or a lower-timeframe limit plan.

### 2.2 Watch Zone

A watch zone has directional or reversal relevance but does not yet have a stable stop or a sufficiently narrow risk contract.

Typical examples:

- broad F2 reversal areas without a stop;
- F3 broad reversal environment;
- symmetry extension areas without lower-timeframe confirmation;
- context conflict zones.

A watch zone requires lower-timeframe refinement.

### 2.3 Context Zone

A context zone is useful for interpretation but not direct execution.

It can influence:

- directional bias;
- no-trade filtering;
- failure interpretation;
- parent zone mapping;
- child-zone search.

### 2.4 Dead Zone

A dead zone is an area where price interaction tends to produce chop, delay, or unclean path behavior. It should be labeled and used for filtering.

---

## 3. Zone Lifecycle

```text
Candidate -> Watch -> Tradable -> Active -> Resolved
```

Detailed lifecycle:

1. **Candidate**: a mechanical source proposes a potential price range.
2. **Watch**: the area has relevance but entry/stop may not yet be stable.
3. **Tradable**: entry edge and stop edge are stable enough.
4. **Active**: price touches or enters the zone.
5. **Resolved**: the zone held, failed, faked out, chopped, expired, or produced expansion.

Resolution states:

```text
held
failed
fake_break_success
failure_continuation
chop
dead
missed
consumed
expired
```

---

## 4. Touch Event

A zone itself is not enough. The research sample should usually be the **touch event**.

A single zone can have multiple touch events.

Touch event fields:

```yaml
touch_id: string
zone_id: string
touch_time: timestamp
touch_type: wick_touch | body_touch | close_inside | full_fill | midpoint_touch
touch_depth_pct: float
entry_triggered: bool
entry_price: float | null
stop_price: float | null
mae_after_touch: float
mfe_after_touch: float
time_to_mfe: int
path_smoothness_score: float
outcome_label: enum
```

The touch event is critical because the same zone may behave differently depending on approach speed, session, context state, and whether it is a first or later touch.

---

## 5. Stop as Zone Expiration

In this architecture, the stop is not just a loss-control device. It is the expiration of the zone thesis.

A zone expires when:

- price reaches the far side of the zone according to the stop policy;
- the context invalidates the zone before touch;
- time invalidation occurs;
- the parent zone fails;
- repeated touches consume the zone;
- lower-timeframe structure proves the zone cannot defend its risk contract.

The stop must be conceptually attached to the zone. If no stop can be defined, there is no execution zone.

---

## 6. Width and Cost

Zone width is the direct cost of the risk contract.

Important fields:

```text
raw_width
atr_normalized_width
spread_adjusted_width
buffered_stop_width
potential_to_width_ratio
```

A wide zone is not automatically invalid, but it is expensive. The correct policy is usually:

```text
Wide parent zone -> search for child zone -> trade child zone if stable
```

If no child zone appears, the parent may remain a watch zone rather than an execution zone.

---

## 7. Potential Map

The zone must estimate open reward potential.

Potential references:

- opposite zone;
- structural high/low;
- liquidity pool;
- measured expansion objective;
- previous displacement range;
- ATR multiple;
- path-open area;
- trend continuation area;
- failure continuation path.

The system should not require a fixed target, but it must estimate whether reward side is sufficiently open.

---

## 8. Zone Quality Requirements

A high-quality execution zone should have:

- narrow enough risk;
- clear stop edge;
- clear potential path;
- mechanical source;
- context support or meaningful context conflict;
- lower-timeframe refinement when needed;
- acceptable session/time conditions;
- not too many prior touches;
- no obvious dead-zone behavior;
- measurable MFE/MAE advantage in historical testing.

---

## 9. Core Data Principle

Every zone must become a structured research object. Every touch must become an event. Every event must be labeled.

Without this, training will collapse into impressionistic pattern recognition.

