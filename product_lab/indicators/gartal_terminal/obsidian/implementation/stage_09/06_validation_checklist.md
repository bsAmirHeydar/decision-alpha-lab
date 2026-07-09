# 06 — Validation Checklist

## MetaEditor

- [ ] Compile `GartalTerminal.mq5`
- [ ] Compile `GartalNewsDownloaderEA.mq5`

## Source Failure Tests

- [ ] Delete `GartalTerminal/ff_calendar_thisweek.xml`
- [ ] Confirm cache fallback activates
- [ ] Delete `GartalTerminal/calendar_cache.txt`
- [ ] Confirm sample fallback activates
- [ ] Put invalid text into raw source file
- [ ] Confirm sanity failure blocks parser
- [ ] Set `InpSourceMinEventBlocks` very high
- [ ] Confirm stale/sample fallback is reported

## Dashboard Tests

- [ ] LIVE badge appears when source is valid
- [ ] CACHE badge appears after live failure + fresh cache
- [ ] STALE CACHE appears when cache age policy marks stale
- [ ] SAMPLE appears after all real data sources fail
- [ ] ERROR appears when all fallbacks are disabled
