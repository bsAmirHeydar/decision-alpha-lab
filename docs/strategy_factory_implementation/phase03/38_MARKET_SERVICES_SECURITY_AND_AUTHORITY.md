---
title: "Market Services Security and Authority"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Authority ceiling

Market services may read market and account-independent symbol metadata. They may not:

- construct trade requests;
- calculate final account risk;
- modify orders;
- open positions;
- alter model thresholds;
- suppress audit failures.

# Input safety

Broker symbols are external input and use bounded ASCII validation with forbidden wire delimiters. Internal service IDs remain strict identifiers.

# Resource safety

Symbol and series registration should eventually be limited by compiled plugin capabilities. Arbitrary runtime symbol expansion is not permitted in live mode.

# Fail closed

Malformed market data cannot be coerced into valid records. Source errors must not cause default zero prices to enter caches.

# Future permissions

Live execution authority will be isolated behind a separate adapter and explicit runtime mode. Importing market services will never confer trading authority.
