# M0001 — Relative Territory Volatility (RTV)

## Version

Final Specification

## Status

Frozen Design Document

---

# 1. Purpose

M0001 (Relative Territory Volatility) is a structural metric designed to quantify how price behaves when revisiting the territory of a structural node.

The core question is:

> Does price exhibit a different volatility regime when it returns to the vicinity of an important structural node?

Instead of relying on classical volatility measures such as ATR or standard deviation, M0001 evaluates volatility through logarithmic candle movements within the context of structural node territories.

---

# 2. Inputs

## 2.1 Market Data

OHLC data:

* time
* open
* high
* low
* close

---

## 2.2 Structural Nodes

Nodes are supplied by:

LRuleNodeDetector

Only nodes satisfying:

```text
confirmed = True
```

are considered.

---

# 3. Design Philosophy

The entire metric is designed to behave exactly like a live market.

At no point is future information allowed.

Every decision must be made using only information available up to the current candle.

Therefore:

> Backtests and live execution follow identical logic.

---

# 4. Live Market Simulation

The algorithm operates candle-by-candle.

For each incoming candle:

* Market advances by one step.
* Every active node is evaluated.
* Decisions rely exclusively on historical information.

---

# 5. Node States

Each node exists in one of three states.

---

## TRACKING

The node is active.

No event is currently open.

Extreme values continue to evolve.

---

## ACTIVE EVENT

An event is currently being recorded.

Volatility measurements are accumulated.

---

## CONSUMED

The node is permanently inactive.

No further processing occurs.

---

# 6. Node State Variables

Each node maintains an independent state.

Stored fields include:

Identity:

* node_id
* node_time
* node_index
* node_price
* node_type

Tracking:

* extreme
* consumed
* hunted

Event:

* in_event

* revisit_id

* entry_index

* entry_time

* exit_index

* exit_time

Zone:

* territory_lower
* territory_upper

Metric Storage:

* before_logs
* inside_logs

Frozen Event Data:

* frozen_extreme

---

# 7. Initial Extreme

For LOW nodes:

```text
extreme = node_price
```

For HIGH nodes:

```text
extreme = node_price
```

---

# 8. Extreme Updating

Extreme updates only while the node is in TRACKING mode.

No updates occur during an active event.

---

## LOW Nodes

If:

```text
high > extreme
```

Then:

```text
extreme = high
```

---

## HIGH Nodes

If:

```text
low < extreme
```

Then:

```text
extreme = low
```

---

# 9. Extreme Distance

Distance is defined as:

```text
distance = |extreme − node_price|
```

---

# 10. Territory Construction

A parameter called:

```text
zone_ratio
```

defines the territory width.

Example:

```text
node_price = 100
extreme   = 150

distance = 50

zone_ratio = 0.9
```

Territory width becomes:

```text
distance × (1 − zone_ratio)

50 × 0.1 = 5
```

---

# 11. Territory Boundaries

Territory is symmetric around the node.

Definitions:

```text
half_width = distance × (1 − zone_ratio)

lower = node_price − half_width

upper = node_price + half_width
```

Example:

```text
Zone = [95, 105]
```

---

# 12. Territory Entry Detection

Entry is wick-based.

Price is considered inside the territory if:

NOT:

```text
high < lower
```

AND NOT:

```text
low > upper
```

Equivalently:

```text
Wick intersects territory.
```

---

# 13. Baseline Collection

Before an event begins:

Logarithmic movements are accumulated into:

```text
before_logs
```

These observations define the baseline market regime.

---

# 14. Logarithmic Movement

For each candle:

First compute:

```text
move = |high − low|
```

If:

```text
move ≤ 0
```

Then:

```text
log_move = 0
```

Otherwise:

```text
log_move = log(move)
```

---

# 15. Event Initiation

When price enters the territory:

The following occurs:

```text
in_event = True

revisit_id += 1

outside_count = 0

entry_time recorded

inside_logs cleared

frozen_extreme recorded
```

---

# 16. Frozen Extreme

Frozen extreme is defined as:

> The extreme value observed immediately before event initiation.

Once the event begins:

```text
frozen_extreme never changes.
```

It is stored in the final output.

---

# 17. Event Volatility Collection

During an active event:

Each candle contributes:

```text
inside_logs.append(log_move)
```

---

# 18. Temporary Territory Exit

If a candle closes outside the territory:

```text
outside_count += 1
```

If price returns inside:

```text
outside_count = 0
```

---

# 19. Event Termination

An event ends when:

```text
outside_count ≥ exit_gap
```

Meaning:

> Price remained completely outside the territory for a specified number of consecutive candles.

---

# 20. Event Length

Defined as:

```text
event_length = len(inside_logs)
```

---

# 21. Event Baseline

Suppose:

```text
N = event_length
```

Then:

The last N observations from:

```text
before_logs
```

are extracted.

These constitute the baseline comparison sample.

---

If insufficient baseline exists:

The event is discarded.

---

# 22. Statistical Measures

For inside_logs:

Compute:

```text
mean_inside

median_inside
```

---

For baseline:

Compute:

```text
mean_before

median_before
```

---

# 23. RTV Definition

If:

```text
mean_before ≠ 0
```

Then:

```text
RTV = mean_inside / mean_before
```

Otherwise:

RTV is undefined.

---

# 24. Consumption Modes

Two consumption models exist.

---

## TOUCH Mode

After completion of the first event:

```text
consumed = True
```

The node becomes permanently inactive.

No revisits are possible.

---

## HUNT Mode

Completion of an event does NOT automatically consume the node.

The node remains active unless hunted.

---

# 25. Hunt Definition

---

## LOW Nodes

If:

```text
low < node_price
```

Then:

```text
hunted = True
```

---

## HIGH Nodes

If:

```text
high > node_price
```

Then:

```text
hunted = True
```

---

# 26. Consumption Under Hunt Mode

If:

```text
hunted = True
```

Then:

```text
consumed = True
```

The node becomes inactive.

---

If:

```text
hunted = False
```

The node survives.

---

# 27. Revisit Definition

Revisits are only possible under Hunt Mode.

Requirements:

* Previous event completed.
* Node not consumed.
* Price re-enters the territory.

---

# 28. Revisit Behaviour

Each revisit forms an entirely independent event.

Previous events remain preserved.

Example:

```text
Node 25

Event 1

Event 2

Event 3
```

All are stored independently.

---

# 29. Baseline During Revisits

For every revisit:

```text
before_logs cleared
```

A completely new baseline is constructed.

---

# 30. Event Logs During Revisits

For every revisit:

```text
inside_logs cleared
```

Only candles belonging to that revisit contribute.

---

# 31. Territory Persistence

Territory boundaries are preserved after event completion.

They are NOT removed.

The previous territory is reused to detect future revisits.

---

# 32. Extreme Handling During Revisits

After event completion:

```text
extreme = None
```

However:

```text
territory remains unchanged.
```

---

When price re-enters the preserved territory:

A new extreme is seeded.

---

## LOW Nodes

The new extreme becomes:

```text
extreme = current candle high
```

---

## HIGH Nodes

The new extreme becomes:

```text
extreme = current candle low
```

---

# 33. Extreme Evolution After Revisit Seeding

Once seeded:

Extreme evolves normally.

LOW:

```text
if high > extreme:

    extreme = high
```

HIGH:

```text
if low < extreme:

    extreme = low
```

---

# 34. System Characteristics

The metric is:

* Fully live-compatible.
* Free of future leakage.
* Structural-node based.
* Revisit-aware.
* Wick-sensitive.
* Log-volatility driven.
* Baseline-normalized.
* Event-history preserving.
* Configurable via multiple consumption models.

---

# 35. Final Output

Each output row represents one completed event.

Fields include:

Identity:

* node_id
* node_time
* node_type
* node_price

Event:

* revisit_id
* entry_time
* exit_time
* event_length

Territory:

* territory_lower
* territory_upper
* expansion_extreme

Statistics:

* mean_inside

* mean_before

* median_inside

* median_before

Metric:

* RTV

Consumption:

* hunted

---

# 36. RTV Interpretation

## RTV > 1

Volatility inside the territory exceeded normal market behaviour.

The revisit exhibited elevated activity.

---

## RTV ≈ 1

Volatility inside the territory resembled the baseline regime.

No meaningful behavioural change was detected.

---

## RTV < 1

Volatility inside the territory was lower than the surrounding market regime.

The revisit exhibited relative calmness.

---

# Conclusion

M0001 is a structural behavioural engine that models price revisits to important market nodes through a fully live-simulated process, eliminating future leakage while supporting dynamic territory formation, configurable node consumption, independent revisits, and normalized volatility comparisons.
