# Validation Matrix

| ID | Test | Expected |
|---|---|---|
| BT-01 | Load in Strategy Tester | `INIT_SUCCEEDED` |
| BT-02 | Load on normal chart with default inputs | `INIT_FAILED` |
| BT-03 | Multiple ticks in one bar | one structural run |
| BT-04 | Valid F3H appears | limit request at Hook terminal |
| BT-05 | Valid HH appears | limit request at Hook terminal |
| BT-06 | Pending order exists | no second setup |
| BT-07 | Position exists | no Hook rebuild; F detector still runs |
| BT-08 | Same-direction F1/F2/F3 after entry | position closes |
| BT-09 | F3 existed before entry | position remains open |
| BT-10 | Opposite-direction F3 | position remains open |
| BT-11 | Hook death before fill | pending is cancelled |
| BT-12 | Restart same test with reset enabled | deterministic clean setup registry |
| BT-13 | FAST versus PARITY on short local structures | matching decisions |
| BT-14 | Parent outside FAST context | documented profile divergence allowed |
| BT-15 | Production expert | visuals and CSV wrapper behavior unchanged |
