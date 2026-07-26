---
title: V4-27 — Complete Search and Exposure Ledger
status: accepted-reference
version: 1.0.0
created: 2026-07-16
updated: 2026-07-16
tags:
  - saed-v4
  - v4-27
  - search-ledger
  - exposure-ledger
---

# Mission

Implement the complete, immutable and content-addressed scientific search universe for SAED V4. Every proposed configuration, compilation, seed, retry, duplicate, invalid run, pruned run, failure, timeout, cancellation, completion, selection and rejection is represented. Every human, agent, validator or service exposure to research evidence is represented with actor identity, data role, object hash, known time, query identity, hypothesis identity and experiment lineage.

# Entry boundary

V4-27 consumes only the accepted V4-26 mechanistic-interpretability certificate and its exact handoff. It cannot reopen V4-26 models, tune mechanisms against protected evidence, access hidden evaluation, compile runtime artifacts, allocate risk or submit orders.

# Workstreams

1. Freeze actors, evidence roles, search families and experiment manifests before search.
2. Implement the complete trial state machine and append-only SHA-256 hash chain.
3. Implement exposure accounting for dashboards, charts, metrics, examples, agent summaries, exports, narratives, hypothesis changes, manual interventions, notebooks and queries.
4. Construct the materially related multiplicity universe, including failures, prunes, retries, duplicates and post-result human or agent exposures.
5. Enforce known-time, protected-role firewalls, subtype budgets and zero hidden-evaluation budget.
6. Detect missing trials, orphan runs, nonterminal trials, broken lineage, hash-chain mutation and authority escape.
7. Produce deterministic replay, a complete-ledger research certificate and an exact V4-28 handoff.

# Acceptance

The phase is accepted only as a local deterministic reference when both chains verify, every manifest trial is terminally accounted for, all relevant exposures are included, protected and hidden evidence counts remain zero, budgets pass, no authority escapes and replay is exact. Online FDR is explicitly deferred to V4-28.

# Non-goals

No real-alpha claim, promotion, runtime compilation, parity claim, capital allocation, broker execution, online learning, hidden-evaluation air gap or production authorization.

# Related

- [[00_MOC_V4_27_Complete_Search_And_Exposure_Ledger]]
- [[V4_26_Mechanistic_Interpretability]]
- [[V4_28_Anytime_Valid_Online_FDR]]
