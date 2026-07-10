# Hunter Chart Targeting

Default policy is `ALL_OPEN_HUNTER_CHARTS`. P08 enumerates charts with `ChartFirst/ChartNext` and matches the broker symbol exactly. It never draws Hunter geometry on the Protected symbol chart.

Policies:
- current chart only if it is the Hunter;
- first open Hunter chart;
- all open Hunter charts.

Timeframe matching can be required, but defaults off so a confirmed line can appear consistently across all open timeframes of the Hunter symbol. Missing charts produce `WAITING_FOR_HUNTER_CHART`, not a false drawing success.
