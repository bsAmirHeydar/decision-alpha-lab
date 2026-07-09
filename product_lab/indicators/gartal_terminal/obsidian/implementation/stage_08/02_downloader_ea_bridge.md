# 02 — Downloader EA Bridge

`GartalNewsDownloaderEA.mq5` is the live network owner.

## Responsibilities

- call `WebRequest()` from EA context
- download the weekly XML feed
- write raw XML to `MQL5/Files/GartalTerminal/ff_calendar_thisweek.xml`
- refresh on timer
- print byte/status diagnostics

## Customer Workflow

1. Compile the EA.
2. Add the source URL to MT5 WebRequest allowed list.
3. Attach the EA to any chart.
4. Attach the indicator to trading charts.
5. Set `InpUseSampleData=false` in the indicator.
6. Set `InpSourceFetchMode=0` in the indicator.

## Separation Rationale

Network IO belongs in EA/runtime service layer. Rendering belongs in the indicator layer.
