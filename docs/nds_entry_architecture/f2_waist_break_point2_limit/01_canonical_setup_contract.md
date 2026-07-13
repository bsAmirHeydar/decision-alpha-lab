# 01 — Canonical Setup Contract

## 1. Authority boundary

This execution profile **does not define F1, F2, F3, their internal counts, or their confirmation lifecycle**.

The authoritative Phoenix sequence remains unchanged:

```text
F2 flag body:
Origin → Leg1 → Waist → Leg2 / flag end

Then F2 post-flag correction:
minimum internal 1/2, including the special Waist-break branch

Then F2 confirmation:
price returns in the F2 direction and strictly re-passes the original F2 flag end
```

The setup layer only projects and executes one preferred entry inside that already-defined F2 lifecycle.

Core files deliberately left untouched include:

```text
FP_FlagBodyEngine.mqh
FP_FlagBodyRules.mqh
FP_InternalCountEngine.mqh
FP_InternalCountRules.mqh
FP_F1LifecycleEngine.mqh
FP_F2LifecycleEngine.mqh
FP_F2LifecycleRules.mqh
FP_F3LifecycleEngine.mqh
FP_SequenceEngine.mqh
```

## 2. Exact setup being traded

The desired branch is the existing F2 Waist-break branch:

```text
Point 1 = the Waist of the already-complete two-leg F2 flag body
Point 2 = the post-flag adverse node / price passage that strictly breaks that Waist
```

The trade must enter at Point 2. Because Point 2 does not exist before the Waist is crossed, the executable representation is a pending limit staged in advance:

```text
Bullish F2 → Buy Limit strictly below the F2 flag Waist
Bearish F2 → Sell Limit strictly above the F2 flag Waist
```

The fill is the executable Point 2. The fill does **not** mean the complete F2 has confirmed. F2 confirmation remains a later Phoenix lifecycle event.

## 3. Full causal sequence

```text
1. Phoenix creates the F2 two-leg flag body
   Origin → Leg1 → Waist → Leg2 / flag end

2. The setup adapter binds to that exact body version

3. It stages a limit strictly beyond the F2 flag Waist

4. The market corrects after the flag body

5. Crossing the F2 Waist fills the order
   F2 Waist = branch Point 1
   strict crossing / breaking node = branch Point 2

6. The market later returns in the original F2 direction

7. Re-passing the original F2 flag end confirms F2
```

This is the only interpretation allowed by this profile.

## 4. Entry, stop, and economic target

```text
Entry = strict Point-2 projection beyond F2 flag Waist
Stop  = behind the direct parent F1 Waist
RR reference = original F2 flag end / Leg2
```

For the fixed exit mode:

```text
Broker TP = original F2 flag end / Leg2
```

For both dynamic F3 exit modes:

```text
Initial broker TP = 0
RR reference still = original F2 flag end / Leg2
Actual exit is managed later by the selected F3 exit contract
```

## 5. Strict structural break semantics

Phoenix defines equality as not being a break. Therefore the Point-2 order cannot be placed merely one nominal tick behind the Waist when the configured structural boundary epsilon is wider.

The minimum entry offset is now:

```text
max(
  requested entry ticks × trade tick size,
  Phoenix boundary epsilon + one trade tick
)
```

Consequently, an executable fill is guaranteed to be beyond the same strict boundary used by Phoenix.

## 6. Source-body ownership

Every pending order is bound to the exact F2 flag-body version that created it:

```text
body_id
sequence identity
scale
origin node and time
waist node and time
Leg2 node and time
```

The order is cancelled if that exact source body:

- extends Leg2 before Point 2;
- confirms;
- invalidates through its own Phoenix lifecycle;
- disappears or is superseded in the rebuilt canonical event stream.

A new valid body version may then create its own new setup hash and order. The setup adapter never edits the underlying F event.

## 7. Timing and no-lookahead

The order may be armed only after the current F2 flag body is observable from confirmed closed-bar nodes.

The adapter rejects retrospective entry when, after body observability and before order creation:

- the final executable Point-2 limit was already touched; or
- the original F2 flag end was already touched.

The setup is lifecycle-owned rather than one-bar-owned, but it cannot chase a missed level.

## 8. Post-flag internal counting

The existing Phoenix internal-count engine remains authoritative.

The execution adapter does not invent a replacement `internal_pack`, does not rewrite the displayed 1/2 labels, and does not call the two-leg flag body the whole F2 lifecycle.

It performs one execution projection only:

```text
existing F2 flag Waist → projected branch Point 1
strict future Waist passage → executable branch Point 2
```

This projection is necessary because waiting for a confirmed Point-2 node would make the limit entry retrospective.

## 9. Reward/Risk policy

```text
Risk   = abs(final Entry - Stop)
Reward = abs(original F2 flag end - final Entry)
RR     = Reward / Risk
```

Default minimum RR is `1.0`.

When enabled, RR repricing moves only the Entry farther toward the fixed Stop. It never moves the F1-waist Stop or the original F2 flag-end reference.

## 10. Pending lifecycle

A pending order is held only while all of the following remain true:

```text
exact source F2 body still exists
source F2 remains unconfirmed
source F2 remains non-invalidated
source body version has not extended or changed
original target has not been consumed
HTF gate still allows the order when cancel-on-gate-close is enabled
```

Dynamic exit modes also use the original F2 flag end for pre-fill target consumption even though their broker TP is initially zero.

## 11. Non-goals

This patch does not:

- change any canonical F detector or lifecycle engine;
- alter F2 origin, Leg1, Waist, Leg2, internal count, confirmation, size, or F3 authorization;
- turn the two-leg body into the entire F2 lifecycle;
- wait for a confirmed Point-2 node and then chase it;
- use Hook, Zone, CG, or AI as the lower-timeframe setup definition.
