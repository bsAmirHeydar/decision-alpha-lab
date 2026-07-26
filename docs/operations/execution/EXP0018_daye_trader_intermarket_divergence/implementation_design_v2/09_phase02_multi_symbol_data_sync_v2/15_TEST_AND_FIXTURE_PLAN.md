---
id: EXP0018-P02-TEST-PLAN
title: "P02 Test and Fixture Plan"
type: test-plan
status: active
project: EXP0018
---
# برنامه تست

## Embedded MQL5

- exact 3-bar alignment
- missing B middle bar
- shifted timestamps with equal indices
- deterministic pair identity

## Python

- contract schema
- no-forward-fill
- exact/missing/shifted fixtures
- forbidden execution token scan

## Runtime MetaTrader

- suffix broker symbols
- late history load
- reconnect
- weekend gap
- reattach idempotency
- partial market data
