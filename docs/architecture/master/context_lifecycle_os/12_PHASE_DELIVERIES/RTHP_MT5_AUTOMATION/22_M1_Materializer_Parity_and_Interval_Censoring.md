---
title: RTHP MT5 Automation — M1 Materializer Parity and Interval Censoring
status: implemented
version: 1.0.0
updated: 2026-07-22
---

# M1 Materializer

The materializer consumes closed M1 OHLC bars. A touch is observable only at the bar close, the exact tick time is unknown, and no OHLC order is inferred. Simultaneous touches in the same M1 interval are treated as simultaneous. MFE and MAE use the known M1 High/Low envelope without claiming path order. Fixed-horizon return labels use closed prices.
