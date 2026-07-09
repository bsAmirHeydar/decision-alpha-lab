# 05 — Validation Checklist

## Compile

- [ ] `GartalTerminal.mq5` compiles in MetaEditor.
- [ ] No duplicate functions.
- [ ] No undeclared fields in `GT_Config`, `GT_RuntimeState`, or `GT_AlertState`.

## Alert behavior

- [ ] `ALERTS` dashboard button toggles alert processing.
- [ ] 30m/15m/5m alerts do not all fire together at 5m remaining.
- [ ] Release alert fires only inside the release window.
- [ ] Actual alert requires actual/released data.
- [ ] Breaking alert fires only once per breaking event.
- [ ] Runtime filters suppress alerts when enabled.
- [ ] Duplicate alert key never fires twice.

## Diagnostics

- [ ] `alert_last_summary` updates after each timer scan.
- [ ] Dashboard health/debug line shows alert summary.
- [ ] Logs include alert-delivery messages.
