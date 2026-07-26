---
title: "Security, Safety, and Capital Boundary"
tags:
  - strategy-factory
  - implementation-roadmap
  - alpha-lab
status: canonical
doc_version: 1.0.0
---

# Security, Safety, and Capital Boundary

## Authority Separation

- Research artifacts have no order authority.
- Model artifacts have no direct broker authority.
- Decision runtime may emit recommendations only.
- Risk engine may reject or reduce approved decisions.
- Broker adapter alone maps approved intents to broker-specific requests.

## Required Safety Controls

- paper/live mode separation;
- explicit environment profile;
- account allowlist;
- symbol allowlist;
- strategy allowlist;
- per-intent risk cap;
- per-event-cluster cap;
- per-symbol and per-strategy exposure;
- daily loss lock;
- max concurrent positions;
- duplicate prevention;
- kill switch;
- stale-context abstention;
- model-version allowlist;
- immutable execution trace.

## No-Send Development Rule

Until Phase 18 acceptance, MQL5 shared code must not contain `OrderSend`, `OrderCheck`, or `CTrade` order authority.
