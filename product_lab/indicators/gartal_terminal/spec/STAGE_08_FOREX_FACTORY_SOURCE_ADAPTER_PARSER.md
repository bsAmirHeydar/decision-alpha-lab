# STAGE 08 — Forex Factory Source Adapter + Parser

## Status

Implemented as source adapter + XML parser + EA bridge.

## Product Decision

`gartal terminal` remains an indicator for chart rendering. Live network acquisition is delegated to a helper EA because MT5 custom indicators are not the correct owner for blocking WebRequest calls.

## New Runtime Modules

- `GartalNewsCalendarClient.mqh`
- `GartalNewsParser.mqh`
- `experts/GartalNewsDownloaderEA.mq5`

## Primary Source

```text
https://nfs.faireconomy.media/ff_calendar_thisweek.xml
```

## Indicator Runtime Path

```text
InpUseSampleData=false
InpSourceFetchMode=0
InpLocalRawFile=GartalTerminal\\ff_calendar_thisweek.xml
```

## Helper EA Path

```text
GartalNewsDownloaderEA.mq5
  -> WebRequest(source URL)
  -> MQL5/Files/GartalTerminal/ff_calendar_thisweek.xml
  -> indicator reads file
```

## Parser Coverage

- XML event blocks
- title
- country/currency mapping
- date/time
- impact
- actual/forecast/previous
- URL notes
- all-day events
- tentative events
- breaking-title proxy

## Non-Goals

- production website HTML scraping
- true unscheduled headline stream
- perfect source timezone inference
- historical date-range download

## Validation Gate

Stage 08 is accepted when:

- the indicator can parse a local FF XML fixture
- the helper EA can write a raw source file
- the dashboard shows source/parser diagnostics
- parser-added event count is visible
- source failure does not freeze chart rendering
