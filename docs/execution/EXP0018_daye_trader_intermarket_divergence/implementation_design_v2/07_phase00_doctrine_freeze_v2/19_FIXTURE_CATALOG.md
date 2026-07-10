---
id: EXP0018-P00-FIXTURES
title: "EXP0018 Phase 00 — Doctrine Fixture Catalog"
type: test-spec
status: draft
project: EXP0018
version: 2.1.0
created: 2026-07-10
updated: 2026-07-10
owner: Strategy Architect
tags:
  - exp0018
  - daye-trader
  - phase00
  - doctrine-freeze
---

# کاتالوگ Fixture دکترین

## ساختار هر Fixture

```text
fixture_id
rule/decision_id
symbols
NY timestamps
period identities
reference highs/lows per symbol
current highs/lows per symbol
host close
expected hunt facts
expected final status
expected hunter/protected
expected visual event
expected lifecycle transition
```

## Fixtureهای اجباری

- equality high؛
- equality low؛
- A-only high hunt؛
- B-only high hunt؛
- A-only low hunt؛
- B-only low hunt؛
- double hunt before close؛
- second symbol missing؛
- duplicate callback؛
- restart/replay same ID؛
- first sweep duplicate؛
- protected later breach؛
- p4 16:30–16:59:59؛
- 17:00 gap؛
- DST spring boundary؛
- DST fall boundary؛
- expiry short history؛
- NP chosen interpretation؛
- TWO chosen anchor؛
- Weekly chosen boundary؛
- major label؛
- minor no-label؛
- line persistence after retirement.
