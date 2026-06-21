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


Release 105 internal opposite-node TP manager:

Initial fixed-R take-profit is disabled by default:
- `InpRewardR = 0.0`

Open-position exit is now managed on every new candle:
- `InpUseInternalOppositeNodeTP = true`
- `InpExitOppositeInternalNodeCount = 3`
- `InpModifyPositionTPOnEveryNewBar = true`

BUY position rule:
- After a BUY position is opened from a LOW origin zone, E0006 counts valid internal HIGH nodes created after the position entry time.
- When the N-th internal HIGH node becomes valid, E0006 places/modifies the position TP at that HIGH node price.

SELL position rule:
- After a SELL position is opened from a HIGH origin zone, E0006 counts valid internal LOW nodes created after the position entry time.
- When the N-th internal LOW node becomes valid, E0006 places/modifies the position TP at that LOW node price.

The internal nodes use `InpInternalNodeL`.
The TP manager runs once per new candle, not on every tick.
If `InpRewardR > 0`, pending orders still receive an initial fixed-R TP. With the default zero value, pending orders are placed with TP=0 and the internal opposite-node TP manager owns the exit.


Release 106 optional revisit-only entry filter:

New inputs:
- `InpOnlyTradeRevisitZones = false`
- `InpRevisitFirstCycleMustQualify = true`
- `InpRevisitMinInternalHunts = 0` where zero reuses `InpMinInternalHuntsForZone`.

When revisit-only mode is OFF, E0006 keeps the Release 105 behavior: a valid origin zone can receive a limit once the same-side internal hunt count passes the configured threshold.

When revisit-only mode is ON:
1. E0006 computes M0001 events for origin zones.
2. A zone is not tradeable on its first touch.
3. The origin node must have a prior M0001 touch event that was confirmed and not hunted.
4. The first cycle before that prior touch must satisfy the internal same-side hunt threshold, when `InpRevisitFirstCycleMustQualify` is true.
5. The post-touch/revisit cycle must also satisfy the same internal hunt threshold.
6. Only then does E0006 place the pending limit for the next revisit.

LOW origin example:
- First cycle: internal LOW hunts before the first non-hunted LOW-zone touch must be >= N.
- Revisit cycle: internal LOW hunts after that first touch closes must also be >= N.
- Only then can the LOW origin receive a BUY LIMIT on revisit.

HIGH origin example:
- First cycle: internal HIGH hunts before the first non-hunted HIGH-zone touch must be >= N.
- Revisit cycle: internal HIGH hunts after that first touch closes must also be >= N.
- Only then can the HIGH origin receive a SELL LIMIT on revisit.

The revisit filter still runs on new candles only, and uses the same M0001 hunt predicate and the configured internal-node L.


Release 107 node-price stop anchor:

A new stop anchor option was added:
- `InpUseNodePriceStop = false` keeps the old zone-back stop.
- `InpUseNodePriceStop = true` moves the stop behind the origin node price.

BUY/LOW zone:
- Entry remains `zone_upper + spread * InpBuyEntrySpreadMultiplier`.
- Zone-back stop mode: `SL = zone_lower`.
- Node-price stop mode: `SL = origin node price`.

SELL/HIGH zone:
- Entry remains `zone_lower`.
- Zone-back stop mode: `SL = zone_upper + spread * InpSellStopSpreadMultiplier`.
- Node-price stop mode: `SL = origin node price + spread * InpSellStopSpreadMultiplier`.

Fixed-R TP, when enabled, is recalculated from the selected stop distance.
With the default `InpRewardR = 0.0`, the order starts without a fixed TP and the internal opposite-node TP manager owns the exit.


## Documentation added in Release 108

For detailed reasoning behind the execution logic, see:

```text
docs/debug/E0006/README.md
docs/debug/E0006/ENTRY_QUALIFICATION_README.md
docs/debug/E0006/REVISIT_ONLY_README.md
docs/debug/E0006/EXIT_AND_RISK_README.md
docs/debug/E0006/INPUT_REFERENCE_README.md
```

These files document the current E0006 lifecycle: all-zone execution, internal same-side hunt qualification, revisit-only filtering, position caps, node-price/zone-back stop anchors, and internal opposite-node TP management.
