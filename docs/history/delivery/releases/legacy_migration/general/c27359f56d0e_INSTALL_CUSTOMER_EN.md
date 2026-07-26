# gartal terminal — Customer Installation Guide

## Files

A customer release package may contain:

```text
MQL5/Indicators/GartalTerminal/GartalTerminal.ex5
MQL5/Experts/GartalTerminal/GartalNewsDownloaderEA.ex5
MQL5/Presets/gartal_terminal_live_bridge.set
MQL5/Presets/gartal_terminal_stable_customer.set
docs/
fixtures/
```

## Installation

1. Open MetaTrader 5.
2. Go to `File > Open Data Folder`.
3. Copy `GartalTerminal.ex5` into `MQL5/Indicators/GartalTerminal/`.
4. Copy `GartalNewsDownloaderEA.ex5` into `MQL5/Experts/GartalTerminal/`.
5. Copy preset `.set` files into `MQL5/Presets/`.
6. Restart MT5 or refresh Navigator.

## WebRequest permission

The downloader EA needs WebRequest access. Add this URL in MT5:

```text
Tools > Options > Expert Advisors > Allow WebRequest for listed URL
https://nfs.faireconomy.media
```

The indicator reads the local bridge file created by the downloader EA:

```text
MQL5/Files/GartalTerminal/ff_calendar_thisweek.xml
```

## Recommended chart setup

1. Attach `GartalNewsDownloaderEA` to one clean chart.
2. Attach `GartalTerminal` indicator to the trading charts.
3. Load `gartal_terminal_live_bridge.set` for beta builds.
4. Use broker GMT auto/hybrid mode first.
5. If a broker has unusual server time, set the manual GMT override.

## Release warning

`gartal terminal` is a macro-news visualization and alert terminal. It does not predict news outcomes and does not guarantee execution safety during volatile releases.
