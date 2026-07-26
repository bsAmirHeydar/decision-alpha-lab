# F2 Waist Limit — State Machine

```text
NEW BAR
├── managed position exists → HOLD, no detector
├── managed pending exists → HOLD, no detector
└── no exposure → load closed bars

DETECT
├── build canonical nodes
├── build F1
├── build F2
└── skip Hook/F3/global visual post-processing

SELECT
├── no newly observable confirmed F2 → IDLE
├── no parent F1 waist → BLOCK
├── setup already consumed → BLOCK
├── illegal price ordering → BLOCK
├── illegal pending side → BLOCK
└── valid geometry → BROKER PREFLIGHT

SEND
├── `OrderCheck` fails → ERROR
├── `OrderSend` fails/rejects → ERROR
└── accepted Buy/Sell Limit with attached SL/TP → mark F2 used
```

A filled position is managed by the Strategy Tester through the attached Stop Loss and Take Profit. No dynamic exit loop is loaded.
