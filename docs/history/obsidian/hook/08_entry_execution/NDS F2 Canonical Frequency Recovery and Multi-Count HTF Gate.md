# NDS F2 Canonical Frequency Recovery and Multi-Count HTF Gate

## Core correction

```text
F2 body becomes observable
→ remains eligible by structural lifecycle
→ not limited to Age = 0
→ no late order after Entry or Target was already touched
```

Default:

```text
InpF2BTMaxSetupAgeBars = -1
InpF2BTConsumeAttemptOnlyOnFill = true
```

A cancelled unfilled pending releases its active attempt. The F2 hash becomes permanently consumed only after an entry deal fills.

## HTF authority

```text
Evaluate every canonical HTF count independently
→ own F phase, not own Hook/ND
→ own F1 confirmed
→ own exact child F2 not confirmed
```

```text
HTF bullish qualifying counts only → Buy
HTF bearish qualifying counts only → Sell
both directions qualify → block
```

An unrelated Hook or a newer immature count cannot hide another valid count.

## Exact confirmation boundary

```text
F1 confirmed = lifecycle confirmed + confirmation node
F2 confirmed = F2 lifecycle confirmed + confirmation node
```

Spawn permissions are not stabilization definitions. Local exact-F3 exit nevertheless exposes its necessary source-F2 spawn dependency through `InpF2BTRequireCanonicalF3SpawnForLocalExit = true`; fixed and HTF-F3 exits do not use that local dependency.

## Coverage and diagnostics

```text
FAST = 800 bars, L 2/3/5/8
```

Optional funnel CSV is default-off and writes one row only on deinit. No runtime prints are introduced.

## Authority

- [[../../nds_entry_architecture/f2_waist_break_point2_limit/17_canonical_frequency_recovery_and_lifecycle|Full correction contract]]
- [[NDS F2 Higher-Timeframe F-Phase Filter]]
- [[NDS F2 Higher-Timeframe F1-to-F2 Confirmation Window]]
- [[NDS F2 Waist-Break Point2 Limit Setup]]
