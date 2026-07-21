# EXP0017 Phase 06 Hotfix008 — Extreme Frontier References

This patch changes the reference eligibility model used by Phase 06 confirmation and visual drawing.

## Core change

Previous versions could still compare current price against stale internal highs/lows that had already been swept by later candles or later completed cycles. That produced repeated and visually misleading divergence lines from levels that no longer had structural value.

Hotfix008 introduces **Extreme Frontier Reference Filtering**:

- A high reference remains eligible only if no later completed cycle has made an equal or higher high.
- A low reference remains eligible only if no later completed cycle has made an equal or lower low.
- The scan walks backward from the most recent completed previous cycle to older cycles while maintaining the highest high and lowest low already seen.
- Non-frontier internal levels are suppressed before divergence construction and therefore cannot be drawn.

## Install

Expand this patch at the repository root or directly under the MQL5 project root, depending on how this repository is mapped into MetaTrader.

After installing, compile:

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Visual_Ledger_Anatomy.mq5
```

Then remove old chart objects with prefix:

```text
EXP0017_P06_
```

Attach the EA again.
