# 17 — Canonical Frequency Recovery and Lifecycle Corrections

## 1. Purpose

Version 2.00 removes accidental frequency suppression while preserving every user-requested structural filter. It does not loosen Entry, Stop, RR, overlap, direction, or exit definitions. It corrects when a valid F2 remains eligible and which HTF count owns authorization.

## 2. F2 validity is lifecycle-owned

Old behavior:

```text
MaxSetupAgeBars = 0
→ F2 could be ordered only on its first observable bar
```

Canonical behavior:

```text
InpF2BTMaxSetupAgeBars = -1
→ no arbitrary bar expiry
```

A complete unconfirmed F2 body remains eligible while all of the following remain true:

- the exact F2 event is not invalidated;
- its direct parent F1 remains valid and confirmed;
- F2 confirmation/target consumption has not occurred;
- the final executable entry has not already been touched since the body became observable;
- the original F2 Leg2 target has not been retested since observability;
- the context has not already filled under one-attempt policy.

This allows an F2 born while the H1 gate is closed to be ordered later when the correct H1 window opens, without creating a retrospective order after the market already passed the entry or target.

## 3. Attempt ownership

Default:

```text
InpF2BTConsumeAttemptOnlyOnFill = true
```

States:

```text
pending accepted
→ active attempt; duplicate pending prohibited

pending cancelled before fill
→ active attempt released

entry deal fills
→ setup hash permanently consumed
```

Internal HTF cancellation, target cancellation, external cancellation, rejection, or expiry all release the active pending identity when no fill occurred. Filled positions remain one-attempt-only.

## 4. Multi-count HTF gate

All canonical HTF F1 roots are evaluated. At least one count must be:

```text
in count-local F phase
and, when enabled,
F1 confirmed / exact child F2 not confirmed
```

Unrelated Hooks cannot veto it. A newer immature count cannot hide it. Opposite qualifying directions remain fail-closed.

## 5. Exact confirmation boundaries

```text
F1 stabilization = confirmed F1 lifecycle + confirmation node
F2 stabilization = confirmed exact direct-child F2 lifecycle + confirmation node
```

The window no longer depends on F1 ability to spawn F2 or F2 ability to spawn F3.

## 6. Local F3 exit eligibility

The old mode-dependent F2 size dependency is no longer hidden. Local exact-F3 exit requires a source F2 that canonical Phoenix can promote into F3, so the dependency has its own explicit input:

```text
InpF2BTRequireCanonicalF3SpawnForLocalExit = true
```

This input applies only to `FP_NDS_F2_EXIT_F3_FLAG_RETEST`. The general research input `InpF2BTRequireF2SizeGate` remains independent. Fixed-F2 and independent HTF-F3 exits do not require local source-F2 spawn authority.

## 7. Detection coverage

FAST profile now uses:

```text
800 closed bars
L = 2, 3, 5, 8
max events = 1800
```

PARITY remains:

```text
2500 closed bars
L = 2, 3, 5, 8, 13, 21
```

This restores common medium-scale contexts without reintroducing Hook, renderer, global canonical post-processing, or per-tick detection into the lower-timeframe fast path.

## 8. Parallel-account boundary

Default parallel-context inputs require an MT5 hedging account. Version 2.00 can fail initialization explicitly instead of silently running a materially different netting policy:

```text
InpF2BTRequireHedgingAccountForParallelContexts = true
```

## 9. Optional funnel diagnostics

Default:

```text
InpF2BTEnableFunnelDiagnostics = false
```

When enabled, the EA writes one CSV row at deinitialization to the MT5 Common Files area. It does not print per tick or per bar. Counters cover cycles, candidates, HTF reasons, direction blocks, setup-build blocks, overlap suppression, send/exposure blocks, orders, fills, and pending cancellations.

## 10. Invariants preserved

The correction preserves:

- closed-bar structural detection;
- no market chasing after a missed limit;
- RR repricing toward the fixed F1-waist stop;
- wider-wins overlap arbitration;
- exact per-position local-F3 lineage;
- independent HTF-F3 exit contexts;
- fixed F2 Leg2 RR reference in every exit mode.
