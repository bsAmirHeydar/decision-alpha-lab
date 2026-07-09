# 06 — Stage 08 Validation Checklist

## Compile

- [ ] `GartalTerminal.mq5` compiles
- [ ] `GartalNewsDownloaderEA.mq5` compiles

## Local Fixture

- [ ] Copy `test_fixtures/ff_calendar_stage08_sample.xml` to `MQL5/Files/GartalTerminal/ff_calendar_thisweek.xml`
- [ ] Set `InpUseSampleData=false`
- [ ] Set `InpSourceFetchMode=0`
- [ ] Confirm parser adds events
- [ ] Confirm Trump event is marked breaking

## Live Bridge

- [ ] Add source URL to MT5 allowed WebRequest list
- [ ] Run downloader EA
- [ ] Confirm raw file is created
- [ ] Attach indicator and read local bridge
- [ ] Verify broker-time alignment

## Failure

- [ ] Missing local file shows warning
- [ ] Cache fallback works
- [ ] Sample fallback works when enabled
- [ ] Dashboard stays responsive
