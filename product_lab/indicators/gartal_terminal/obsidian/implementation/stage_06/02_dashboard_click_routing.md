# Dashboard Click Routing

`OnChartEvent()` receives object names from MT5. Stage 06 routes only objects under:

```text
<InpObjectPrefix>DASH_
```

Click handling path:

```text
OnChartEvent
  -> GT_HandleDashboardClick
  -> GT_HandleRuntimeFilterClick
  -> specific filter handler
  -> update runtime diagnostics
  -> GT_UpdateStoreMetrics
  -> GT_RedrawAll
```

## Object Naming Convention

- `GT_DASH_FLT_HIGH_BG`
- `GT_DASH_FLT_HIGH_TXT`
- `GT_DASH_FLT_CCY_USD_BG`
- `GT_DASH_FLT_RESET_TXT`

The click handler uses tokens, so both background and text clicks are accepted.
