---
type: contract
system: NDS
phase: 53
status: implemented
---

# NDS Backtest Performance Profiles

## FAST

- 1,200 closed bars
- scales 2, 3, 5, 8
- 2,500 event/Hook caps
- default rapid-test profile

## PARITY

- 5,000 closed bars
- scales 2, 3, 5, 8, 13, 21, 34, 55
- 6,000 event/Hook caps
- production-context comparison profile

## CUSTOM

Uses explicit operator inputs.

The algorithms remain shared. FAST may differ only when a required parent lies outside its bounded context.

## Related

- [[NDS Lightweight Backtest Runtime]]
- [[NDS Backtest Parity Contract]]
