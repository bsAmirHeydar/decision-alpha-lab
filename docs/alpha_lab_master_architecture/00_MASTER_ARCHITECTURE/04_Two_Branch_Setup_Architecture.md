---
id: ALMA-CDBD575217
title: "Two-Branch Setup Architecture"
type: architecture
status: canonical
domain: alpha-lab-master-architecture
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - alpha-lab
  - master-architecture
---
# Two-Branch Setup Architecture

## 1. The Split

After context validation, Alpha Lab opens two parallel but equal branches:

```text
Context
├── Human-authored setup branch
└── AI setup-discovery branch
```

Both branches must produce the same canonical complete-treatment artifact and face the same research firewall, outcome engine, statistical tests and promotion gates.

## 2. Human Setup Branch

A human setup follows:

```text
Setup thesis
→ detailed setup document
→ implementation design
→ complete treatment policy
→ scenario tests
→ central evidence pipeline
```

The setup document defines:

- target context versions;
- expected mechanism;
- eligibility and no-trade cases;
- direction;
- entry;
- stop;
- exit/target;
- trailing, partials and management;
- sizing constraints;
- economic assumptions;
- regime assumptions;
- falsification criteria.

Human conviction is valuable input but not evidence. A manual setup is not privileged over AI output.

## 3. AI Setup Branch

The AI branch receives context snapshots and a governed treatment universe. It may learn:

- trade versus skip;
- candidate ranking;
- treatment selection;
- expected utility;
- target/stop probabilities;
- survival or time-to-event;
- regime-specialist routing;
- uncertainty and novelty;
- post-entry management policy.

The AI must be able to return no trade.

## 4. Canonical Setup Artifact

A setup is not an entry trigger. It is:

```text
Eligibility
× Entry
× Stop
× Exit
× Management
× Sizing Constraints
× Cost Profile
× Execution Profile
× Abstention Policy
```

The Treatment Compiler rejects incomplete, incoherent or broker-infeasible combinations.

## 5. Objective Styles

Styles such as high win rate, high reward, runner, low drawdown or high frequency are expressed as constrained multi-objective preference profiles. For example, high win rate is optimized only subject to minimum expectancy, sample, cost robustness and tail-loss limits.

## 6. Hybrid Policies

Human and AI decisions may be combined explicitly:

- human eligibility + AI skip/trade;
- human stop + AI exit;
- AI ranking + deterministic risk gate;
- human regime selector + specialist models.

The hybrid is represented as a versioned policy graph, not informal discretion.

## 7. Shared Research Destination

The origin of a setup is recorded for attribution, but once compiled, every setup enters the same trial ledger and evidence system. The architecture tests policies, not reputations.
