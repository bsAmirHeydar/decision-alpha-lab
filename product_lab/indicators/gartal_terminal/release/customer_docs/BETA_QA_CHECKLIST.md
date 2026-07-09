# gartal terminal — Beta QA Checklist

## Compile gate

- [ ] `GartalTerminal.mq5` compiles with zero errors.
- [ ] `GartalNewsDownloaderEA.mq5` compiles with zero errors.
- [ ] No duplicate function declarations.
- [ ] No undeclared identifiers.
- [ ] No accidental source-only files are included in customer zip unless `-IncludeSource` is used.

## Source bridge gate

- [ ] WebRequest URL is whitelisted in MT5.
- [ ] Downloader EA writes `MQL5/Files/GartalTerminal/ff_calendar_thisweek.xml`.
- [ ] Indicator reads local bridge file with `InpUseSampleData=false`.
- [ ] Dashboard shows `LIVE` or `CACHE`, not silent failure.
- [ ] Cache fallback shows explicit status if source fails.

## Time gate

- [ ] Broker GMT auto/hybrid produces correct event line placement.
- [ ] Manual GMT override moves all events consistently.
- [ ] UTC/source/broker diagnostics are coherent.
- [ ] Today-only default is correct for broker-time day window.

## Visual gate

- [ ] Dashboard is readable on 1080p and 1440p screens.
- [ ] Bottom timeline labels do not overlap excessively.
- [ ] Red events are visually dominant.
- [ ] Breaking/speech/tentative flags are visible.
- [ ] Object cleanup removes old dashboard/timeline objects.

## Filter gate

- [ ] RED/ORANGE/YELLOW toggles repaint dashboard and timeline.
- [ ] Currency chips repaint dashboard and timeline.
- [ ] RESET restores default filter state.
- [ ] Alert eligibility respects runtime filters when enabled.

## Alert gate

- [ ] 30/15/5 minute alerts fire once per event.
- [ ] Release alert fires once.
- [ ] Duplicate ledger suppresses repeated alerts.
- [ ] Runtime ALERTS toggle pauses/resumes alert processing.

## Release gate

- [ ] `Package-GartalTerminal.ps1` creates release zip.
- [ ] Release manifest is generated.
- [ ] Customer docs are included.
- [ ] Presets are included.
- [ ] License mode behaves as expected for demo/beta/stable.
