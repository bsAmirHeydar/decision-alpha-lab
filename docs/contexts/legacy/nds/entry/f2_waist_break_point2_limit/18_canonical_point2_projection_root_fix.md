# 18 — Canonical Point-2 Projection Root Fix

## Decision

The previously completed Phoenix F architecture is authoritative and remains untouched.

The execution profile is corrected as a consumer adapter rather than a second F2 definition.

## Correct semantic chain

```text
existing Phoenix F2 flag body
Origin → Leg1 → Waist → Leg2

existing Phoenix post-flag correction
minimum 1/2 or Waist-break branch

existing Phoenix confirmation
return and strict re-pass of original Leg2 / flag end
```

The trade setup captures the preferred Waist-break Point 2 by staging a pending order beyond the F2 flag Waist after the two-leg body is observable and before Point 2 occurs.

## Root defects removed

### 1. Body/lifecycle wording drift

The execution code and documentation no longer describe the two-leg body as the entire F2 lifecycle.

### 2. Weak one-tick penetration

The limit offset now respects the Phoenix boundary epsilon plus one trade tick. A fill therefore represents a strict Waist passage under the same comparator contract as the F engine.

### 3. Pending orders detached from their source body

Each pending order now stores exact body identity and is reconciled against the rebuilt event stream. Leg2 extension, F2 confirmation, invalidation, disappearance, or supersession cancels only the affected order.

### 4. Dynamic-mode target-consumption gap

Dynamic exit orders carry broker TP `0`, but their pre-fill economic target is still the original F2 flag end. Target-consumption cancellation now reads that target from the active source-body reservation.

### 5. Hold-path reconciliation gap

A pending order now forces one closed-bar F2 execution scan for source reconciliation even when overlap replacement is off or the HTF entry gate is closed. This does not add per-tick structural scanning.

## Files deliberately not modified

```text
mql5/Include/FlagCountingPhoenix/FP_FlagBodyEngine.mqh
mql5/Include/FlagCountingPhoenix/FP_FlagBodyRules.mqh
mql5/Include/FlagCountingPhoenix/FP_InternalCountEngine.mqh
mql5/Include/FlagCountingPhoenix/FP_InternalCountRules.mqh
mql5/Include/FlagCountingPhoenix/FP_F1LifecycleEngine.mqh
mql5/Include/FlagCountingPhoenix/FP_F2LifecycleEngine.mqh
mql5/Include/FlagCountingPhoenix/FP_F2LifecycleRules.mqh
mql5/Include/FlagCountingPhoenix/FP_F3LifecycleEngine.mqh
mql5/Include/FlagCountingPhoenix/FP_SequenceEngine.mqh
```

## Resulting execution contract

```text
source = exact existing Phoenix F2 body
projected Point 1 = source F2 Waist
executable Point 2 = strict pending fill beyond source F2 Waist
stop = behind direct parent F1 Waist
RR reference = source F2 original flag end
confirmation = still owned by Phoenix after post-flag count and favorable return
```
