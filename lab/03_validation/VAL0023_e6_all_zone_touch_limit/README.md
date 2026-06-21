# E0006 — All-Zone Touch Limit Fixed-R Executor

E0006 is a lightweight execution module that uses existing M0001 / execution modules instead of rebuilding structure logic.

## Contract

- Source of truth for zones: M0001 live territory logic.
- Scan all confirmed structural nodes by default.
- No maximum trade-count cap by default.
- One managed pending limit order per live, non-hunted M0001 zone.
- New-bar only execution. No tick-by-tick recalculation.
- Stop loss is the far end of the zone.
- Take profit is fixed-R, default `20R`.

## Direction

LOW node / support zone:

```text
BUY LIMIT
entry = zone_upper + spread
sl    = zone_lower
tp    = entry + abs(entry - sl) * RewardR
```

HIGH node / resistance zone:

```text
SELL LIMIT
entry = zone_lower
sl    = zone_upper + spread
tp    = entry - abs(entry - sl) * RewardR + spread
```

The sell-side SL and TP spread shift follows the requested execution rule.

## Important inputs

```text
InpRewardR = 20.0
InpMaxNodesScan = 0
InpBuyEntrySpreadMultiplier = 1.0
InpSellStopSpreadMultiplier = 1.0
InpSellTpSpreadMultiplier = 1.0
InpUpdateEveryNBars = 1
InpPrintOrderLogs = false
```

`InpMaxNodesScan=0` means all confirmed nodes are scanned. This is not a trade limit.

## Order lifecycle

The EA upserts each managed pending order:

```text
if pending exists for the zone:
    modify entry/sl/tp if zone moved
else:
    place new limit if geometry is orderable
```

A stale pending order is deleted only if its managed node no longer appears as a valid live zone.

## Compile target

```text
mql5/Experts/DecisionAlphaLab/Execution/E0006_AllZoneTouchLimitFixedR.mq5
```


## Release 101 — per-side pending-order caps

New inputs:

```text
InpMaxBuyPendingOrders = 0
InpMaxSellPendingOrders = 0
```

`0` means unlimited. Any positive value caps how many BUY LIMIT or SELL LIMIT orders E0006 keeps desired per side during each new-bar sync. The scan order remains newest confirmed zones first, so when a cap is active the newest valid zones are kept and older extra pending orders become stale and can be deleted when `InpDeleteStalePendingOrders=true`.


## Release 102 — open-position side blocking

New inputs:

```text
InpMaxBuyOpenPositionsBeforeBlock = 0
InpMaxSellOpenPositionsBeforeBlock = 0
InpDeleteSidePendingWhenOpenCapHit = true
```

`0` disables the open-position blocker for that side.

On every new closed candle, E0006 counts currently open BUY and SELL positions by symbol and magic number. If the count in a side reaches its configured threshold, the module immediately deletes all managed pending orders of that same side and does not place any new pending orders of that side in that candle.

Example:

```text
InpMaxBuyOpenPositionsBeforeBlock = 2
```

If there are already 2 open BUY positions, E0006 deletes managed BUY LIMIT orders and blocks new BUY LIMIT creation while SELL logic remains independent.


Release 103 internal hunt qualification filter:

E0006 now separates the L used for origin zones from the L used for internal game nodes.

Inputs:
- `InpOriginNodeL`: L for the structural node whose zone receives the limit order.
- `InpInternalNodeL`: L for smaller internal nodes used only for qualification.
- `InpUseInternalHuntFilter`: enables/disables the filter.
- `InpMinInternalHuntsForZone`: minimum hunted internal nodes required before an origin zone becomes orderable.
- `InpInternalHuntSameSideOnly`: when true, LOW origins count only internal LOW hunts and HIGH origins count only internal HIGH hunts.

BUY/LOW origin rule:
- After the origin LOW node is formed, detect internal LOW nodes with `InpInternalNodeL`.
- Count how many of those internal LOW nodes are later hunted using the same M0001 hunt predicate.
- The LOW origin zone becomes eligible for a BUY LIMIT only if the count is at least `InpMinInternalHuntsForZone`.

SELL/HIGH origin rule:
- After the origin HIGH node is formed, detect internal HIGH nodes with `InpInternalNodeL`.
- Count how many of those internal HIGH nodes are later hunted.
- The HIGH origin zone becomes eligible for a SELL LIMIT only if the count is at least `InpMinInternalHuntsForZone`.

The check runs once per new candle, not on every tick.

Release 104 compile fix:
- Replace long variadic `Print(...)` audit calls with single-string audit/sanity messages.
- This avoids MQL5 `wrong parameters count` errors from too many Print arguments.
