# NDS F2 Canonical Point-2 Projection Root Fix — Audit Report

## Release

```text
Expert version: 2.10
Trade contract: NDS-F2-WAIST-BREAK-12
Schema: nds_f2_waist_break_point2_v12
Patch boundary: execution setup only
```

## Audit objective

The F1/F2/F3 definitions and lifecycle engines were previously completed and accepted. The defect was in the F2 Waist-Break Point-2 trading adapter: its comments and ownership model blurred the boundary between the two-leg F2 flag body and the complete F2 lifecycle, and pending orders were not fully tied to the exact source body version.

This patch corrects the setup at the execution boundary and deliberately leaves the Phoenix F architecture unchanged.

## Locked canonical sequence

```text
1. F2 builds its two-leg flag body:
   Origin → Leg1 → Waist → Leg2 / original flag end

2. The market enters the post-flag correction:
   minimum internal 1/2, or the special F2 Waist-break branch

3. In the preferred Waist-break branch:
   Point 1 = F2 flag Waist
   Point 2 = the node / strict price passage that breaks that Waist

4. The market later returns in the F2 direction and strictly re-passes the
   original F2 flag end. That later event confirms F2.
```

The execution setup must capture Point 2. It must not redefine the two-leg body as the entire F2 and must not wait for complete F2 confirmation before entering.

## Final trading contract

### Bullish F2

```text
Pending entry = Buy Limit strictly below the existing F2 flag Waist
Stop          = strictly below the direct parent F1 Waist
Fixed TP / RR = original F2 flag end / Leg2
```

### Bearish F2

```text
Pending entry = Sell Limit strictly above the existing F2 flag Waist
Stop          = strictly above the direct parent F1 Waist
Fixed TP / RR = original F2 flag end / Leg2
```

The pending order is staged after the current two-leg F2 body is causally observable and before the future Waist-breaking Point 2 occurs. The fill is the executable capture of Point 2. Phoenix remains responsible for the later internal-count and confirmation lifecycle.

# Root findings and corrections

## 1. Execution semantics were mixed with F2 definition — corrected

### Defect

The setup layer described the F2 body as though it were the entire F2 lifecycle. That wording made it possible to confuse:

```text
F2 two-leg body
with
complete F2 confirmation
```

### Correction

A dedicated execution-only adapter was introduced:

```text
FP_NDSF2CanonicalPoint2SetupAdapter.mqh
```

It consumes existing `FP_FlagEvent` state and owns only:

- projected Point 1 = existing F2 Waist;
- executable Point 2 = strict future passage beyond that Waist;
- pending-order geometry;
- source-body ownership.

It does not detect, rebuild, mutate, or reinterpret F1/F2/F3.

## 2. One nominal tick did not always mean a canonical Waist break — corrected

Phoenix structural comparisons use `boundary_epsilon_points`. If epsilon is wider than one trade tick, a limit one tick behind the Waist can fill while still inside the equality band.

The minimum executable Point-2 offset is now:

```text
max(
  requested entry ticks × trade tick size,
  Phoenix boundary epsilon + one trade tick
)
```

Buy entries are normalized down and Sell entries are normalized up. A fill therefore lies strictly beyond the same boundary used by the Phoenix break comparator.

## 3. Pending orders were not owned by the exact F2 body version — corrected

Each pending order now stores the exact source body identity:

```text
body_id
direction
scale
sequence_id
parent_sequence_id
origin node/time
waist node/time
Leg2 node/time
original F2 flag-end price
```

On each closed entry-timeframe bar, the pending order is reconciled against the current canonical F2 event stream.

Only the affected pending order is cancelled when its source:

- extends Leg2 before entry;
- confirms;
- invalidates;
- disappears;
- is superseded by a new canonical body version.

No Phoenix event is edited. A new body version may independently generate a new setup hash.

## 4. Dynamic exits had no broker TP before fill — target-consumption gap corrected

The local-F3 and HTF-F3 exit modes intentionally submit pending orders with:

```text
ORDER_TP = 0
```

Previously, pre-fill target-consumption logic could not recover the original F2 flag end from the order itself. A stale pending order could therefore survive after the economic target had already been reached.

The active source-body reservation now stores `f2_flag_end_price`. When broker TP is zero, pending reconciliation uses this immutable original F2 endpoint.

## 5. Fast hold paths could skip source reconciliation — corrected

A pending order now forces one entry-timeframe canonical F1/F2 scan per newly closed entry bar, even when:

- overlap replacement is disabled;
- the HTF gate is closed;
- HTF pending cancellation is disabled.

This scan exists only to reconcile the exact source lifecycle. It does not add per-tick detection and does not alter Phoenix F logic.

## 6. Body-version identity strengthened

The setup hash and active reservation now include stable sequence/body identity in addition to structural node times. A pre-entry Leg2 extension is a different source body and target, not the same setup.

## 7. Entry causality retained

The setup remains lifecycle-owned rather than one-bar-owned, but it cannot be armed retrospectively.

From the closed bar where the current Leg2 becomes observable, the adapter rejects setup creation if:

- the final executable Point-2 entry has already been touched; or
- the original F2 flag end has already been consumed.

# Protected core verification

The following accepted Phoenix files were byte-for-byte identical to the v2.00 source boundary:

| Protected core file | SHA-256 | Result |
|---|---|---|
| `FP_FlagBodyEngine.mqh` | `9af5e394645335d158e6d9ca830ec37f5182363abcb38aa8297e76d13da65993` | unchanged |
| `FP_FlagBodyRules.mqh` | `7d840962afe23650716ee7a3719fc4d3abf63411dbd307f19fcf40ea34a32b07` | unchanged |
| `FP_InternalCountEngine.mqh` | `fd0f2b632dd9173bf70cf3fba5c022ceaf9fd9dfd95832f2c48231c25c84ba74` | unchanged |
| `FP_InternalCountRules.mqh` | `d01a28f5781c161ffb940bc114c33e3597e48781cbc3c15c5b06c8c852de30fb` | unchanged |
| `FP_F1LifecycleEngine.mqh` | `fabd94a0692c36ead5775889783d493435d819c17d762809fe9dc140d4cbe2bc` | unchanged |
| `FP_F2LifecycleEngine.mqh` | `d5007818ecff6605d83eb3d4b987ff38cabd288ee46c965395ff8e955e21df3c` | unchanged |
| `FP_F2LifecycleRules.mqh` | `5bbeff9f68d01230be354552926ba6404e79f521251dc1316279ee026bd5f581` | unchanged |
| `FP_F3LifecycleEngine.mqh` | `89539b1177c43e338295d3cd54559b6e7a6a99d5bfb31be37918e2af4e3b0f07` | unchanged |
| `FP_SequenceEngine.mqh` | `c6cce55dd5bbb8ac4fc0931e789d1a2f0698103453bd6c462eaaadb19d36a9db` | unchanged |

The new root-fix QA hard-codes these hashes and fails on any protected-core mutation.

# Existing strategy behavior preserved

The patch does not change:

- F1/F2/F3 construction;
- F2 origin selection;
- F2 Leg1, Waist, Leg2, extension, internal count, confirmation, or invalidation;
- HTF F-phase direction filter;
- HTF F1-confirmed to exact-child-F2-confirmed entry window;
- minimum RR and RR-based entry repricing;
- same-direction overlap and wider-context arbitration;
- hedge and parallel-context policies;
- fixed, exact local-F3, or HTF-F3 exit contracts;
- per-position F3 exit binding.

# Runtime performance

The new adapter contains no:

```text
Print / PrintFormat
Chart objects
Timer
CSV
Hook reconstruction
Zone / CG / AI path
per-tick F detection
```

The only additional structural work is the already-light F1/F2 execution scan once per new entry-timeframe bar while at least one pending order exists, so stale source bodies can be cancelled safely.

# Validation result

```text
All NDS F2 contract QA scripts: PASS
New canonical Point-2 root-fix QA: PASS
Protected-core SHA-256 invariants: PASS
MQL5 compatibility: 0 errors / 0 warnings
Engineering policy: 0 errors / 0 warnings
Repository layout: PASS
Static QA: no blocking findings
Python syntax: PASS
Changed-MQL delimiter balance: PASS
Include closure: PASS
Patch ZIP integrity: PASS
MetaEditor compile: unavailable in build environment
```

Static QA emitted only pre-existing warnings in unrelated audit/reporting files. None belongs to the modified execution path.

# Final invariant

```text
Phoenix defines F2.
The setup adapter only projects and executes the preferred Waist-break Point 2.
```
