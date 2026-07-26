# Chart Targeting Policy

Default behavior targets all currently open charts whose exact broker symbol equals the snapshot broker symbol. Alternative policies allow current-chart-only or first-open-chart projection.

Timeframe is intentionally unrestricted because session boxes are structural overlays. Opening missing charts is disabled by default to avoid workspace mutation. A missing target chart produces `WAITING_FOR_SYMBOL_CHART`, not a false success.
