# VAL0021 — H6 Node Survival Map

Run `M0006_NodeSurvivalMap.mq5` on the target symbol/timeframe.

Recommended daily settings:

```text
InpBars = 0
InpH6UseAllAvailableBars = false
InpH6FastDefaultClosedBars = 120000
InpH6NodeHorizonRed = 20
InpH6NodeHorizonGreen = 50
InpH6NodeHorizonPurple = 100
InpH6DrawNodeChart = true
InpH6NodeMaxChartObjects = 250
InpH6UpdateOnNewBar = false
```

Validation checks:

- build sanity says `officialReport=H0006_NODE_SURVIVAL_MAP`
- audit says `sampleCalls=0`, `branchSamplesBuilt=0`, `m0002Calls=0`
- horizons are `20/50/100`
- chart update reports object counts and prefix `DAL_H6_NODE_`
- MetaTrader chart shows red, green, and purple horizontal node levels when enabled
