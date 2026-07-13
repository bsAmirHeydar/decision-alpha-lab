---
tags: [exp0019, faerie-protocol, fp-i06, relation-compiler, hunt-engine]
status: normative
phase: FP-I06
version: 1.0.0
last_updated: 2026-07-13
language: en
---
# FP-I06 Relation Diagnostic Checklist

## Compilation
- [ ] Exact FP-I05 store hash recorded.
- [ ] Exact relation registry hash recorded.
- [ ] Anchor trading date recorded.
- [ ] Calendar-day selection matches store snapshot.
- [ ] AL/AN/LN each compile once.
- [ ] NA/NL/NN compile once per selected exact offset.
- [ ] WW does not compile.

## Scan
- [ ] M1 rows are unique and ordered.
- [ ] Both symbol cells match plan symbols.
- [ ] HIGH uses own highs and own high references.
- [ ] LOW uses own lows and own low references.
- [ ] Same-M1 dual contact emits no roles.
- [ ] Missing/conflict data blocks classification.

## Candidate
- [ ] LOW → BULLISH.
- [ ] HIGH → BEARISH.
- [ ] Hunter and Protected differ.
- [ ] Candidate ID repeats under identical replay.
- [ ] Protected second touch cancels.
- [ ] No CONFIRMED state is emitted in I06.

## QA
- [ ] Phase tests pass.
- [ ] FP-I00–I05 regressions pass.
- [ ] Daye regressions pass.
- [ ] Boundary/MQL5/vector checks pass.
- [ ] MetaEditor evidence recorded honestly.
