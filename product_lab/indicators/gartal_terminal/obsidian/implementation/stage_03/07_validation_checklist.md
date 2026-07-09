# 07 — Stage 03 Validation Checklist

## Compile checks

- [ ] `GartalTerminal.mq5` compiles in MetaEditor.
- [ ] No duplicate function definitions.
- [ ] `GartalNewsTime.mqh` loads after utils/types and before store/sample usage.
- [ ] `GT_OffsetPartsToSeconds()` is available before `GT_LoadConfig()`.

## Runtime checks

- [ ] Auto GMT displays a sensible broker offset.
- [ ] Manual GMT overrides detected offset.
- [ ] Hybrid mode uses auto when confidence is acceptable.
- [ ] `InpTimeShiftMinutes` visibly shifts event line times.
- [ ] Today-only window shows only D0 events by default.
- [ ] `InpDaysForward=1` admits D+1 sample events.
- [ ] `InpDaysBack=1` admits D-1 sample events.
- [ ] Dashboard shows effective broker GMT and source mode.
- [ ] Vertical line tooltip includes broker and UTC time.

## Failure checks

- [ ] Empty currency filter still fails config validation.
- [ ] Extreme GMT values are clamped/blocked.
- [ ] Dashboard remains stable if there are no visible events.
