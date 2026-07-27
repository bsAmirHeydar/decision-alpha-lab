---
id: UCPS-7F7AE70802AC
title: "UC-04 Implementation Charter"
type: charter
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-27
updated: 2026-07-27
tags:
  - consolidation
  - uc04
  - charter
---
# UC-04 Implementation Charter

## Mission

UC-04 converts the physically reorganized Alpha Lab repository into one semantically governed platform without inventing domain truth, silently changing historical behavior, or deleting logic before equivalence and zero-consumer evidence exist.

UC-03 established canonical physical boundaries. UC-04 owns semantic identity, shared primitives, logic-preservation proof, consumer cutover and bounded retirement candidacy. It does not own model promotion, order placement, capital allocation or platform sealing.

## Execution waves

| Wave | Purpose | Authority |
|---|---|---|
| UC04-W0 | Path authority, test recovery, RTHP binding recovery, evidence foundation | Recovery only |
| UC04-W1 | First low-risk shared primitive characterization and implementation | Candidate-bounded |
| UC04-W2+ | Additional capability families after prior-wave acceptance | Explicitly gated |

Each wave is independently installable, verifiable and reversible. A later wave may not convert a W0 recovery receipt into semantic merge authority.

## Mandatory sequence for every candidate

1. inventory all implementations and consumers;
2. freeze source digests and observable behavior;
3. define known-time, state, side-effect and failure semantics;
4. create characterization fixtures;
5. implement the smallest canonical primitive;
6. prove differential and metamorphic equivalence;
7. issue a logic-preservation certificate;
8. cut consumers over in bounded groups;
9. prove rollback and zero legacy references;
10. request retirement authority separately.

## Permanent prohibitions

- No unproven logic retirement.
- No broad search-and-replace over trading semantics.
- No future-derived information.
- No hidden order or capital authority.
- No claim of equivalence from compilation alone.
- No deletion based only on duplicate names or similar source text.

## Machine authority

UC-04 machine records live under `registry/consolidation/uc04/`. Their schemas live under `schemas/consolidation/uc04/`. The executable W0 verifier is `tools/consolidation/uc04w0/verify.py`.
