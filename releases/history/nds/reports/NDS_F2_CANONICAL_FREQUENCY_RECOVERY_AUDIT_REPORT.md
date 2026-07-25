# NDS F2 Canonical Frequency Recovery — Audit Report

## Release

```text
Expert version: 2.00
Trade contract: NDS-F2-WAIST-BREAK-11
Schema: nds_f2_waist_break_point2_v11
HTF phase module: NDS-F2-HTF-F-PHASE-03
```

## Audit objective

The cumulative F2 Waist-Break Point-2 strategy was reviewed because the tester produced materially fewer trades than the structural setup implied. The review covered:

- F2 candidate lifetime;
- exact Entry/Stop/Target causality;
- minimum RR repricing;
- same-direction overlap arbitration;
- attempt consumption and pending cancellation;
- parallel and hedge execution;
- higher-timeframe F/Hook ownership;
- the HTF F1-confirmed to F2-confirmed window;
- local and higher-timeframe F3 exits;
- fast-profile detection coverage;
- runtime diagnostics and performance.

## Final canonical setup retained

```text
Complete unconfirmed F2 body
Origin → Leg1 → Waist → Leg2

Point 1 = F2 Waist
Point 2 = strict penetration behind F2 Waist
Entry   = pending limit behind F2 Waist
Stop    = behind exact direct-parent F1 Waist
RR reference / fixed target = original F2 Leg2 endpoint
```

The patch does not change this geometry.

# Findings and corrections

## 1. One-bar-only F2 eligibility — corrected

### Previous behavior

```text
InpF2BTMaxSetupAgeBars = 0
```

A complete F2 could be ordered only on the first bar on which its Leg2 became causally observable. If H1 authorization was closed on that bar, the setup was permanently lost even if the correct H1 window opened later.

### Correct behavior

```text
InpF2BTMaxSetupAgeBars = -1
```

The F2 remains eligible by structural lifecycle rather than arbitrary age. It is rejected when its exact event or parent becomes invalid, it confirms, its target is consumed, its executable entry has already been crossed, or the setup has already filled.

### Causality protection

The patch does not create retrospective orders. Before staging a delayed order it checks all closed bars from the body-observability index:

```text
original F2 Leg2 target already retested → reject
final RR-adjusted entry already touched → reject
```

Thus a setup may wait for HTF permission, but it cannot chase a missed Point 2.

## 2. Global Hook veto — corrected

### Previous behavior

The newest visible Hook on any scale or sequence could close the entire HTF gate.

### Correct behavior

Hook/ND ownership is resolved per canonical F1 root. Exact Hook resolve/F1-origin identity has first authority; a same-direction/same-scale preceding-root fallback supports legacy branches. Only the Hook owned by a count may veto that count.

```text
valid Count A + unrelated Hook B
→ Count A remains eligible
```

## 3. Single HTF winner — corrected

### Previous behavior

A single newest/highest-priority F event was selected. A newer immature count could hide another count whose F1→F2 window was open.

### Correct behavior

Every visible canonical HTF F1 root is evaluated independently. The aggregate direction is:

```text
one or more bullish qualifiers and zero bearish qualifiers → Buy
one or more bearish qualifiers and zero bullish qualifiers → Sell
both directions qualify → ambiguous / no entry
no qualifier → no entry
```

This implements the requested “one of the higher-timeframe counts” authorization.

## 4. F1/F2 stabilization boundaries — corrected

The requested lifecycle window is:

```text
[ F1 confirmation, exact direct-child F2 confirmation )
```

The previous implementation included later spawn permissions in the confirmation definition. Those are separate authorities and have been removed from the HTF window boundary.

### F1 opens the window when

```text
level = F1
chain_index = 1
status = CONFIRMED
lifecycle_status = FP_F1_LC_CONFIRMED
has_confirm = true
```

### Exact child F2 closes the window when

```text
level = F2
chain_index = 2
status = CONFIRMED
f2_lifecycle_status = FP_F2_LC_CONFIRMED
has_confirm = true
parent_sequence_id = F1.sequence_id
parent_event_id = F1.event_id
```

`lifecycle_can_spawn_f2` and `f2_can_spawn_f3` are not used as stabilization boundaries.

## 5. Pending acceptance consumed the setup — corrected

### Previous behavior

A setup hash was permanently consumed as soon as a pending order was accepted. If HTF policy cancelled that unfilled order, the same still-valid F2 could never re-arm.

### Correct behavior

Default:

```text
InpF2BTConsumeAttemptOnlyOnFill = true
```

Lifecycle:

```text
pending accepted → active reservation; duplicate prohibited
pending cancelled/rejected/expired before fill → reservation released
entry deal added → setup hash permanently consumed
```

Internal HTF cancellation, target cancellation, wider-order replacement, and terminal external order states release the active reservation. The entry deal is linked through the exact pending order ticket.

## 6. Pending-ticket resolution — corrected

The active-attempt and dynamic-exit registries now require a real order ticket in every exit mode. When a broker/tester accepts a pending request but returns zero in `result.order`, the code resolves the actual order by the unique setup comment. It no longer substitutes a deal id or placeholder ticket.

## 7. Local F3 size dependency — made explicit

A local exact-child F3 exit cannot be resolved from a source F2 that canonical Phoenix does not authorize to spawn F3. The dependency previously appeared as an implicit mode-specific filter.

It now has a dedicated input:

```text
InpF2BTRequireCanonicalF3SpawnForLocalExit = true
```

It applies only to `FP_NDS_F2_EXIT_F3_FLAG_RETEST`. Fixed-F2 and independent HTF-F3 exits are unaffected. The general research input `InpF2BTRequireF2SizeGate` remains separate.

## 8. FAST coverage — corrected

Previous FAST coverage:

```text
420 bars
L = 2, 3, 5
```

New FAST coverage:

```text
800 bars
L = 2, 3, 5, 8
max events = 1800
```

This restores common medium-scale F1/F2 chains while preserving the dedicated lower-timeframe fast path: no Hook construction, renderer, Zone, CG, AI, or global visual canonicalization.

PARITY remains 2500 bars with `L = 2,3,5,8,13,21`.

## 9. Parallel-account ambiguity — corrected

Default hedge and same-direction parallel inputs imply independent same-symbol positions. Version 2.00 adds:

```text
InpF2BTRequireHedgingAccountForParallelContexts = true
```

When parallel capabilities are enabled on a non-hedging account, initialization returns `INIT_PARAMETERS_INCORRECT` instead of silently producing a netting-only result.

## 10. Funnel diagnostics — added without runtime prints

Default:

```text
InpF2BTEnableFunnelDiagnostics = false
```

When enabled, one CSV row is written at deinitialization. There are no per-tick or per-bar custom prints. Counters include:

- cycles;
- pair candidates;
- HTF block reasons;
- direction blocks;
- build blocks;
- overlap suppression;
- exposure/send blocks;
- orders sent and filled;
- HTF and target pending cancellations.

## 11. RR and wider-overlap logic — retained

Minimum RR still uses:

```text
RR = abs(F2 Leg2 - Entry) / abs(Entry - F1-waist Stop)
```

Sub-threshold Entry is moved toward Stop while Stop and F2 Leg2 remain fixed. Same-direction overlapping setups still use executable stop corridors and retain the wider corridor at the configured threshold.

## 12. Exit ownership — retained

- Fixed mode exits at the source F2 Leg2.
- Local-F3 mode remains bound to `Position → exact source F2 → exact direct-child F3`.
- HTF-F3 mode remains isolated per position ticket and locked HTF F3 identity.
- Every mode continues to use original F2 Leg2 for setup-time RR.

# Default behavior after patch

```text
Profile = FAST (800 bars, L 2/3/5/8)
F2 arbitrary age expiry = disabled
Attempt consumption = first fill
HTF = H1
HTF F-phase filter = enabled
HTF F1→F2 window = enabled
HTF pending cancellation = enabled
Minimum RR = 1.0 with Entry repricing
Overlap threshold = 80%, wider wins
Opposite hedge = enabled
Same-direction contexts = enabled
Independent contexts require hedging account
Runtime prints = none
Funnel CSV = disabled
```

# Validation performed

The following passed in the build environment:

- MQL5 compatibility scan: `0 errors, 0 warnings`;
- Alpha Lab policy validation: `0 errors, 0 warnings`;
- repository layout audit;
- static QA: no blocking findings;
- all F2 contract regression scripts;
- new canonical-frequency-recovery contract QA;
- project include-closure resolution from the expert;
- changed-MQL delimiter balance;
- changed Markdown-link resolution;
- Python syntax compilation for all F2 QA scripts;
- patch ZIP integrity and SHA-256 manifest verification.

## Validation limitation

MetaEditor is not installed in the build environment. A real MQL5 compile and Strategy Tester execution must be performed on the target terminal. No claim of successful MetaEditor compilation is made.
