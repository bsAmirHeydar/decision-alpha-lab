---
id: EXP0018-P02-HANDOFF
title: "P02 Handoff to P03, P05 and P11"
type: handoff
status: active
project: EXP0018
---
# Handoff

## P03 Period Aggregation

فقط pairهای `is_ready=true` را مصرف می‌کند و OHLC هر symbol را جدا aggregate می‌کند.

## P05 Hunt Detection

فقط period snapshotهای ساخته‌شده از pairهای valid را می‌بیند. unmatched timestamp نباید به no-hunt تبدیل شود.

## P11 Replay

همین synchronizer باید با manual broker offset و chronological input استفاده شود. detector جدا برای replay ممنوع است.
