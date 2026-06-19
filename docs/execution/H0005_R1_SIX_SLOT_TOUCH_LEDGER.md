# H0005 Reversal Fixed-R Touch Execution — Build 1.13

This document locks the live execution contract for `E0001_ReversalOneToOne.mq5` build `1.13`.

The executor is not a new strategy. It is a live adapter for the already-tested Hypothesis 5 reversal leg:

```text
H0005
regime = REVERSAL
entry = structural zone touch limit
stop = far side of the same zone
reward = fixed R, default 1.0
```

## Regime gate

The EA is allowed to maintain pending orders only when the latest M0002 branch outcome is:

```text
DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT
```

When the latest branch becomes continuation or no reversal regime is available, all managed pending orders for the EA magic/comment prefix are deleted. Open positions are not force-closed; they remain managed by their own SL/TP.

## Zone model

For a node price `N` and live expansion extreme `E`, the M0001 zone is built exactly from the project territory function:

```text
distance   = abs(E - N)
half_width = distance * (1 - zone_ratio)
zone_lower = N - half_width
zone_upper = N + half_width
```

With `zone_ratio = 0.90`, the zone is the 10% band above and below the node price relative to the current expansion distance.

## Spread-aware entry, stop, and TP

The executor uses pending limits only. Market catch is disabled by default.

### Buy from LOW node

```text
raw touch edge = zone_upper
entry          = zone_upper + spread
stop           = zone_lower
risk           = entry - stop
tp             = entry + risk * InpRewardR
```

The buy limit is moved up by the current spread because a buy opens on Ask. This makes the order fire when the Bid-side structural touch edge is reached, without needing a market order.

### Sell from HIGH node

```text
raw touch edge = zone_lower
entry          = zone_lower
stop           = zone_upper + spread
risk           = stop - entry
tp             = entry - risk * InpRewardR
```

The sell stop is moved up by the current spread because a short stop closes on Ask. TP is computed from that spread-aware risk so the realized reward multiple is not silently compressed by spread.

## Number of pending limits

Build 1.13 changes the meaning of directional slots:

```text
InpBuyLimitSlots  = 0  => keep every active buy-touch setup
InpSellLimitSlots = 0  => keep every active sell-touch setup
positive value    => safety cap for that side
```

The default is unlimited on both sides because the purpose is to execute Hypothesis 5 as purely as possible and not miss valid revisits just because a fixed 3+3 grid was already full.

## Touch and revisit ledger

Each structural node has a stable managed comment:

```text
<prefix>R<reward10><B|S>N<node_id>
```

Example:

```text
DALR1R10BN245
DALR1R10SN252
```

The ledger rule is:

```text
one fill per touch
re-arm only after price leaves the touch edge by InpTouchRevisitResetBufferPoints
then the next return to the same node is a valid revisit
```

This allows repeated trades on true revisits while preventing duplicate orders during the same touch.

## Node retirement

A historical touch does not retire a node. Revisits remain tradable while the node is structurally alive.

A node is retired when it is structurally hunted/consumed by the M0001 live territory logic. After that, the executor no longer places orders for that node.

## Diagnostics

The EA logs the full reason chain. Important journal tags:

```text
DAL_E0001_BUILD_SANITY
DAL_E0001_CACHE
DAL_E0001_LIMIT_ORDER
DAL_E0001_PENDING_UPDATE
DAL_E0001_PENDING_DELETE
DAL_E0001_TOUCH_LOCK
DAL_E0001_TOUCH_UNLOCK
DAL_E0001_CYCLE
```

The cache reason includes counts such as scanned nodes, hunted nodes, build rejects, and selected buy/sell setups. Order logs include raw zone edges, spread, executable entry, stop, TP, risk volume, and broker retcodes.

## Validation checklist

1. Compile `E0001_ReversalOneToOne.mq5` cleanly.
2. Run Strategy Tester in visual mode with `InpLogMode = DAL_EXEC_LOG_ORDERS` or `DAL_EXEC_LOG_VERBOSE`.
3. Confirm that in reversal regime the EA parks pending limits before touch.
4. Confirm buy limits sit at `zone_upper + spread` and buy stops at `zone_lower`.
5. Confirm sell limits sit at `zone_lower` and sell stops at `zone_upper + spread`.
6. Confirm TP distance equals `spread-aware risk * InpRewardR`.
7. Confirm continuation regime deletes all managed pending orders.
8. Confirm a filled touch does not duplicate until price leaves and revisits.


## Release 1.13 include installation note

MetaEditor resolves angle-bracket includes such as `<DecisionAlphaLab/Execution/DAL_ExecReversalOneToOne.mqh>` from the terminal-level `MQL5/Include` directory. If the EA source is updated inside `MQL5/Shared Projects/decision-alpha-lab` but the terminal include copy remains old, the compiler can report `wrong parameters count, 17 passed, but 15 requires` and missing setup fields such as `raw_entry_edge`.

For live compilation, keep these two copies synchronized:

- repository source: `decision-alpha-lab/mql5/Include/DecisionAlphaLab/...`
- terminal include source: `MQL5/Include/DecisionAlphaLab/...`

The release installer copies the updated include tree to the terminal-level include directory before compilation.
