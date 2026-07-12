# 11 — Overlap Arbitration and RR Entry Repricing

## 1. Canonical decision

Two same-direction trades should not both be taken when their executable stop spaces are almost the same. In that case the wider setup is selected. A setup whose structural entry does not provide the configured minimum Reward/Risk is not discarded automatically; its limit is moved to the nearest tick that provides at least the required ratio.

## 2. Stop corridor

For each final executable setup:

```text
Stop Corridor = interval between Entry and Stop
Corridor Width = abs(Entry - Stop)
```

For two setups A and B:

```text
Overlap % = length(intersection(A, B)) / min(width(A), width(B)) × 100
```

Using the narrower corridor as denominator answers the intended question: how much of one setup's stop space is already contained in the other?

## 3. Default arbitration

```text
InpF2BTUseStopSpaceOverlapDeduplication = true
InpF2BTStopSpaceOverlapThresholdPercent = 80.0
```

- overlap below threshold: contexts remain independent;
- overlap at or above threshold: one opportunity;
- winner: greater final `Risk Distance`;
- equal widths: keep earlier deterministic candidate / existing pending;
- opposite directions: no deduplication; hedge policy remains authoritative.

The threshold is operator-controlled. `70.0` merges more setups; `80.0` is the default.

## 4. Same-bar candidates

All executable candidates are built before any order is sent. Pairwise overlap arbitration suppresses narrower candidates first, so loop order cannot accidentally submit both.

## 5. Existing pending orders

If a wider overlapping same-direction setup appears while a narrower pending remains:

```text
remove narrower pending
→ submit wider pending
```

If the existing pending is equal or wider, the new candidate is blocked.

## 6. Existing positions

An already-filled position is not closed, resized, or replaced. Any new overlapping same-direction candidate is blocked until that position is gone.

## 7. Minimum-RR repricing

The structural levels are:

```text
Stop = behind direct parent F1 Waist
Target = F2 Leg2 endpoint
Initial Entry = behind F2 Waist
```

When initial RR is too low, solve:

```text
Entry* = (Target + Rmin × Stop) / (1 + Rmin)
```

Then normalize toward Stop:

```text
Bullish → round down
Bearish → round up
```

The adjusted limit is never moved toward Target. Stop and Target remain unchanged. The final order is accepted only when:

- direction geometry is valid;
- the order is still a true Buy Limit or Sell Limit;
- broker minimum distances are satisfied;
- final tick-normalized RR is at least the configured minimum.

## 8. Ordering of calculations

```text
Build structural F2 setup
→ normalize Stop and Target
→ build structural Entry
→ reprice Entry if RR is insufficient
→ recompute final Risk/Reward
→ deduplicate by final stop corridors
→ apply hedge/concurrency policy
→ OrderCheck
→ OrderSend
```

Using final executable prices prevents overlap arbitration from comparing stale pre-adjustment geometry.
