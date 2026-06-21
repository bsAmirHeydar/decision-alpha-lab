# E0006 — Input Reference

This file groups the current E0006 inputs by purpose.

## Symbol and bar source

```text
InpSymbol = ""
InpTimeframe = PERIOD_CURRENT
InpBars = 2500
```

`InpSymbol=""` means current chart symbol. `InpTimeframe=PERIOD_CURRENT` means current chart timeframe.

## Structural scales

```text
InpOriginNodeL = 5
InpInternalNodeL = 2
InpZoneRatio = 0.90
```

`InpOriginNodeL` controls the main nodes whose zones can receive limit orders.

`InpInternalNodeL` controls the smaller nodes used for internal hunt qualification and internal opposite-node exits.

`InpZoneRatio` is passed to the M0001 live territory logic.

## Entry qualification

```text
InpUseInternalHuntFilter = true
InpMinInternalHuntsForZone = 3
InpInternalHuntSameSideOnly = true
```

When enabled, LOW origins require hunted internal LOW nodes and HIGH origins require hunted internal HIGH nodes.

## Revisit-only mode

```text
InpOnlyTradeRevisitZones = false
InpRevisitFirstCycleMustQualify = true
InpRevisitMinInternalHunts = 0
```

When enabled, E0006 skips first-touch entries and only trades zones with a prior non-hunted M0001 touch cycle. Both first cycle and current revisit cycle can be required to pass the internal hunt threshold.

`InpRevisitMinInternalHunts=0` reuses `InpMinInternalHuntsForZone`.

## Order sizing and identity

```text
InpMagicNumber = 6006006
InpRiskCash = 100.0
InpOrderCommentPrefix = "DALE6"
InpPendingExpirationMinutes = 0
InpAllowMinLotIfRiskTooSmall = false
InpCommissionPerLotRoundTurn = 0.0
```

The magic number and managed comment prefix protect the EA from modifying unrelated orders.

## Reward and exit

```text
InpRewardR = 0.0
InpUseInternalOppositeNodeTP = true
InpExitOppositeInternalNodeCount = 3
InpModifyPositionTPOnEveryNewBar = true
```

`InpRewardR=0.0` means no initial fixed-R TP. The internal opposite-node TP manager owns the exit.

When `InpRewardR>0`, an initial fixed-R TP is placed on the pending order.

## Stop and spread handling

```text
InpUseNodePriceStop = false
InpBuyEntrySpreadMultiplier = 1.0
InpSellStopSpreadMultiplier = 1.0
InpSellTpSpreadMultiplier = 1.0
```

BUY entry always uses the buy spread shift:

```text
entry = zone_upper + spread * InpBuyEntrySpreadMultiplier
```

SELL stop always uses spread when needed:

```text
zone stop: SL = zone_upper + spread * InpSellStopSpreadMultiplier
node stop: SL = node.price + spread * InpSellStopSpreadMultiplier
```

`InpSellTpSpreadMultiplier` is only relevant when fixed-R TP is enabled.

## Pending and position caps

```text
InpMaxNodesScan = 0
InpMaxBuyPendingOrders = 0
InpMaxSellPendingOrders = 0
InpMaxBuyOpenPositionsBeforeBlock = 0
InpMaxSellOpenPositionsBeforeBlock = 0
InpDeleteSidePendingWhenOpenCapHit = true
```

`0` means unlimited/off for cap-style inputs.

Pending caps limit desired pending orders by side.

Open-position blockers delete and block same-side pending orders when the number of open positions in that side reaches the configured threshold.

## Sync and session

```text
InpModifyExistingPendingOrders = true
InpDeleteStalePendingOrders = true
InpTradingEnabled = true
InpRunOnInit = true
InpUpdateEveryNBars = 1
InpPrintOrderLogs = false
InpUseTradingSessionFilter = false
InpTradingStartHour = 0
InpTradingStartMinute = 0
InpTradingEndHour = 23
InpTradingEndMinute = 59
```

E0006 is new-bar only. `InpUpdateEveryNBars=1` means every new candle.

The session filter is broker-time based.

## Useful presets

Strict revisit-only internal game:

```text
InpOnlyTradeRevisitZones = true
InpRevisitFirstCycleMustQualify = true
InpMinInternalHuntsForZone = 3
InpRevisitMinInternalHunts = 0
InpRewardR = 0.0
InpUseInternalOppositeNodeTP = true
InpExitOppositeInternalNodeCount = 3
```

All eligible first-touch zones, no fixed-R TP:

```text
InpOnlyTradeRevisitZones = false
InpUseInternalHuntFilter = true
InpMinInternalHuntsForZone = 3
InpRewardR = 0.0
InpUseInternalOppositeNodeTP = true
```

Fixed-R benchmark:

```text
InpRewardR = 20.0
InpUseInternalOppositeNodeTP = false
```

Debug / fast smoke test:

```text
InpMinInternalHuntsForZone = 1
InpExitOppositeInternalNodeCount = 1
InpPrintOrderLogs = true
```
