---
title: "Local Compile Acceptance Form"
---

# Local Compile Acceptance Form

Complete this after running MetaEditor locally.

## Environment

- MetaTrader build:
- MetaEditor path:
- Terminal instance ID:
- Broker/server:
- Windows version:
- Compile timestamp UTC:
- Git commit:

## Host Compile

- `SF02_StrategyHost.mq5` errors:
- warnings:
- `.ex5` produced: yes/no
- initialization result:

## Self-Test Compile and Run

- `SF02_RuntimeSelfTest.mq5` errors:
- warnings:
- passed assertions:
- failed assertions:
- OnInit return:

## Acceptance

- [ ] 0 compile errors
- [ ] No unexplained warnings
- [ ] Self-test `failed=0`
- [ ] No broker request emitted
- [ ] Runtime reaches RUNNING
- [ ] Runtime reaches STOPPED on removal
- [ ] Results attached to Phase 02 evidence

Do not begin Phase 03 coding until compile errors are resolved. Warnings must be either fixed or explicitly accepted in an ADR.
