# F2 Waist Limit — State Machine

```text
IDLE
├── no fresh confirmed F2 → stay IDLE
├── F2 missing canonical parent F1 waist → BLOCKED
├── exact geometry invalid → BLOCKED
├── broker distance invalid → BLOCKED
├── already-used F2 → BLOCKED
└── valid setup → acquire global entry lock

ENTRY LOCK
├── exposure changed → release lock, BLOCKED
├── paper mode → persist F2 attempt, PAPER_LIMIT
└── tester-send mode → place pending order with exact SL/TP

PENDING
└── hold; skip the full detector on later bars

POSITION
└── hold; broker manages exact F1-waist SL and F2-Leg2 TP; skip detector

CLOSED
└── next bar returns to IDLE and scans for a new fresh F2
```

## Recovery

- More than one managed position: fail closed; manual reconciliation.
- More than one managed pending order: preserve one deterministically and delete duplicates using the reused Phase 52 helper.
- Position plus pending order: the position owns the strategy and managed pending orders are deleted.
- Foreign position on the symbol: setup blocked to prevent netting-account merges.
