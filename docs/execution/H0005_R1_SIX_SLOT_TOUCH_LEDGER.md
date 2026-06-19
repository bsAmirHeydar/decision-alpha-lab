# H0005 Reversal R1 — Six-Slot Touch Ledger Execution

This document locks the live execution contract for `E0001_ReversalOneToOne.mq5` build `1.10`.

## Research contract

The executor implements only the H0005 reversal branch, reward `R = 1.0`:

- Regime source: latest completed M0002 branch sample only.
- Active regime required: `REVERSAL_AFTER_EXIT`.
- Entry universe: active, confirmed, not-yet-touched structural zones from M0001.
- Buy candidate: low-node reversal zone, entry at the upper zone edge, stop at the lower zone edge.
- Sell candidate: high-node reversal zone, entry at the lower zone edge, stop at the upper zone edge.
- Take profit: true fixed reward, `TP = entry + direction * abs(entry - stop) * rewardR`.
- Default reward: `InpRewardR = 1.0`.

## Live order contract

When the latest branch regime is reversal, the engine keeps a live pending grid:

- up to `InpBuyLimitSlots = 3` buy limits,
- up to `InpSellLimitSlots = 3` sell limits,
- simultaneous opposite-side exposure allowed by default,
- no global cap by default with `InpMaxSimultaneousTrades = -1`.

The six slots are not a martingale grid. They are the nearest eligible H0005 structural-touch candidates, selected separately for buy and sell direction.

## Touch ledger

Each structural touch is identified by a stable compact comment:

```text
<prefix><reward><side>N<node_id>
```

Example:

```text
DALR1R10BN245
DALR1R10SN252
```

The comment intentionally does **not** include the latest branch-sample id. A branch-sample id can change while the same structural zone is still active; including it would make the live engine delete/recreate orders instead of managing the same touch.

Rules:

1. One setup comment can have only one live pending order or one open position.
2. When a pending order fills, the setup comment is locked.
3. While locked, the engine does not open another pending order for the same touch.
4. The lock is released only after price moves away from the entry edge by `InpTouchRevisitResetBufferPoints`.
5. After unlock, a new pending order is allowed only if the same structural zone is still eligible, representing a true revisit.

## Pending update policy

The engine updates existing managed pending orders instead of blindly deleting them:

- price/SL/TP drift: `OrderModify`;
- volume drift: delete/recreate, but only when the order is not protected near market;
- near-fill protection: pending orders close to market are not deleted just because the setup refreshed.

This prevents the bad behavior where an order is removed exactly as price approaches the planned H0005 touch.

## Regime invalidation

When the latest branch regime is not reversal, or no active H0005 reversal zones remain, all managed pending limits are deleted. Open positions are not force-closed by this executor; their SL/TP remains the execution contract.

## Default inputs for exact H5 R1 live behavior

```text
InpRewardR = 1.0
InpMaxSimultaneousTrades = -1
InpAllowOppositeTrades = true
InpBuyLimitSlots = 3
InpSellLimitSlots = 3
InpSyncManagedPendings = true
InpCancelStaleManagedPendings = true
InpCancelManagedPendingsAfterEntry = false
InpUpdateExistingManagedPendings = true
InpProtectPendingWhenPriceApproaches = true
InpAllowMarketCatchWhenAlreadyTouching = false
InpTouchRevisitResetBufferPoints = 10
```

## Safety expectation

This is an execution adapter for a research hypothesis. It does not claim profitability by itself. The intended validation path is: compile cleanly, run visual Strategy Tester, inspect `DAL_E0001_BUILD_SANITY`, then verify that at most three buy and three sell limits are alive during reversal regimes and that all managed pending orders are removed during continuation regimes.
