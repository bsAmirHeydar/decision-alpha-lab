# ADR 0101 — MQL5 Is Runtime Contract Authority

**Status:** Accepted

MQL5 is the primary implementation for runtime contracts because anatomy detection, context freshness, risk, and execution ultimately operate in MetaTrader. Python mirrors these contracts for research. This prevents a Python-centric design from becoming impossible or slow in the terminal.
