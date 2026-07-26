# برنامه اعتبارسنجی آینده EXP0018

## Gate 1 — Time

- مرز 18:00 نیویورک
- تغییر DST
- PA across trading days
- p4→a1
- weekends

## Gate 2 — Period Extremes

برای هر W/D/A/L/N/P/a1..p4، high/low دستی با خروجی کد تطبیق داده شود.

## Gate 3 — Hunt

- equality
- one-symbol touch
- both-symbol touch
- no close requirement

## Gate 4 — Confirmation

- intrabar candidate که تا close می‌میرد
- first confirming candle
- چند signal در یک candle
- opposite-direction simultaneous signals

## Gate 5 — Reference Lifecycle

- first sweep
- protected survives
- protected later hunts
- retired reference cannot reappear

## Gate 6 — Drawing

- hunter chart only
- correct origin/destination
- labels only for six major signals
- immutable history

## Gate 7 — Auxiliary Drawings

- A/L/N/P boxes
- TWO
- TDO

## Gate 8 — Data Failure

- partial history
- symbol suffix
- missing minute bars
- expiry chart
- reattach/restart
