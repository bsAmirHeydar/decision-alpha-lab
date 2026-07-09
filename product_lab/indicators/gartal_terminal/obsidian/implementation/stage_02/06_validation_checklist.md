---
title: Stage 02 — Validation Checklist
type: qa-checklist
stage: 02
---

# Validation Checklist

## Compile checks

- [ ] `GartalTerminal.mq5` compiles in MetaEditor.
- [ ] All include files resolve.
- [ ] No duplicate function definitions exist from Stage 01 parser/store split.
- [ ] `GartalNewsStore.mqh` is included before dashboard/timeline/alerts.

## Runtime checks

- [ ] With `InpUseSampleData=true`, dashboard shows `SAMPLE_STAGE02`.
- [ ] Event count is non-zero.
- [ ] Visible count respects impact/currency inputs.
- [ ] Same-minute CPI rows appear together.
- [ ] Speech rows are detected.
- [ ] Holiday row disappears when holiday filter is false.
- [ ] Breaking row disappears when breaking filter is false.
- [ ] XAUUSD marks USD events as relevant.
- [ ] Timeline shows upcoming tape.
- [ ] Vertical lines are drawn for visible events only.

## Edge checks

- [ ] Set `InpShowPastEvents=false` and confirm released/expired rows disappear.
- [ ] Set `InpDaysForward=1` and confirm tomorrow rows appear.
- [ ] Set `InpDaysBack=1` and confirm previous-day rows appear.
- [ ] Disable all impacts and confirm dashboard can show empty state without failing.
