---
id: H0005
status: active_rebuilt
family: directional_memory_execution
official_contract: atomic_no_sample_live_replay_with_explicit_risk
created: 2026-06-20
owner: Decision Alpha Lab
priority: critical
---

# H0005 — Directional Memory and Execution

## Research question

If the latest known structural regime is reversal or continuation, does it improve the next structural decision in a way that can become executable alpha?

---

## Old formulation

The old H5 report built paths from completed branch samples. It could show useful structural behavior, but it mixed several ideas:

- regime label sequence,
- reversal touch path,
- continuation break path,
- structural path R,
- regime-change exit.

This made continuation look strong, but code review showed that continuation R was not necessarily a real execution R because continuation had no real initial stop in the classic path report.

---

## Current formulation

The official H0005 formulation is atomic and no-sample:

1. replay candles using only the current prefix,
2. build raw M0001 events,
3. create known-time regime batches,
4. activate reversal or continuation candidates only after regime is knowable,
5. enter only after live-style touch or break,
6. measure only after entry,
7. use explicit risk for R.

---

## Family split

### Reversal

Reversal asks whether a zone creates a reaction.

Expected execution style:

- zone touch entry,
- zone-edge stop or structural invalidation,
- fixed R or first opposite zone target,
- strict same-bar policy.

### Continuation

Continuation asks whether a break state creates a path.

Expected execution style:

- close-break, intrabar-break, Donchian-break, or another explicit trigger,
- ATR/structural/trailing risk,
- fixed R or trailing/regime exit,
- explicit distinction between path R and tradable R.

---

## Null hypothesis

After enforcing live-known time, no-sample replay, and explicit risk, reversal and continuation decisions do not outperform matched random or baseline policies.

---

## Alternative hypothesis

After enforcing live-known time, no-sample replay, and explicit risk, at least one family produces positive expectancy or useful convex path behavior.

---

## Required report fields

- regime source contract,
- same-time batch policy,
- ambiguity policy,
- entry family,
- entry trigger,
- risk mode,
- exit mode,
- win rate,
- profit factor,
- expectancy,
- MFE/MAE in R,
- random baseline,
- family-level separation.

---

## Current interpretation

Reversal appears to be a reaction edge candidate, especially for shorter fixed R tests. Continuation appears to be a strong path candidate, but old continuation PF must not be treated as execution PF unless retested with real risk.
