  ---
  id: EXP0018-SOURCE-MODULE-TRACE-V2
  title: "EXP0018 Source to Module Traceability v2"
  type: traceability
  status: active
  project: EXP0018
  version: 2.0.0
  created: 2026-07-10
  updated: 2026-07-10
  tags:
    - exp0018
- daye-trader
- implementation-design
  ---

# Traceability منبع تا ماژول

| مفهوم | Authority | Track/Phase | ماژول |
|---|---|---|---|
| A/L/N/P و a1..p4 | Word | P01/P03 | Time/Period |
| 22 relationships | Word | P04 | SignalRegistry |
| touch-only hunt | Word | P05 | HuntDetector |
| Hunter/Protected | Word + Bucko clarification | P05/P07 | Hunt/Lifecycle |
| close confirmation | Word | P06 | ConfirmationSM |
| first sweep | Word؛ نیازمند ADR | P07 | FirstSweepPolicy |
| hunter-only line | Word | P08 | Drawing |
| session boxes | Word | P09 | SessionBoxRenderer |
| TWO/TDO | Word + PDFs؛ conflict | P10 | AnchorResolver |
| True Open hierarchy | PDFs | P14 optional | ExtendedOpenRegistry |
| DFR | QT/Trader Daye | P15 optional | DfrEngine |
| SSMT variants | PDFs | P16 optional | SsmtEngine |
| news context | QT/Trader Daye | P18 optional | EventAdapter |
| triad observer | QT | P19 optional | TriadObserver |
