# RTHP MT5 M1 Automatic Activation v1

This context-owned adapter connects read-only to a logged-in MetaTrader 5 terminal, acquires closed M1 bars for two selected symbols, validates and freezes the common source, delegates M1 materialization to the existing RTHP Train Activation, and verifies the final run. It never requests tick history, never synthesizes ticks, and never invokes trading functions.
