---
title: "FP-I03 Operator Acceptance Checklist"
tags: [exp0019, faerie-protocol, fp-i03, time-calendar, obsidian]
status: normative
phase: FP-I03
phase_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# FP-I03 Operator Acceptance Checklist

## Before testing

- [ ] FP-I00, FP-I01, and FP-I02 patches are present.
- [ ] Working tree changes unrelated to FP-I03 are not staged.
- [ ] Python path contains FP-I02 and FP-I03 packages.
- [ ] Time configuration and session registry hashes match artifacts.

## Semantic checks

- [ ] DST start/end instants match golden table.
- [ ] Spring nonexistent local time returns zero candidates.
- [ ] Fall ambiguous local time returns two candidates.
- [ ] A/L/N/gap boundaries are half-open.
- [ ] Sunday 18:00 opens week; Friday 17:00 closes week.
- [ ] Trading-day labels use ending civil date.
- [ ] Two explicit broker offsets for the same UTC instant produce identical IDs.

## QA checks

- [ ] 83 FP-I03 tests pass.
- [ ] Cumulative FP-I00–I03 tests pass.
- [ ] Previous-context regressions pass.
- [ ] 20/20 conformance checks pass.
- [ ] 12 schemas parse and remain closed.
- [ ] MQL5 static scan passes.
- [ ] MetaEditor compile logs are retained or status remains pending.

## Handoff

- [ ] Phase status, acceptance evidence, hashes, inventory, and handoff validate.
- [ ] FP-I04 receives exact accepted hashes.
- [ ] No price, drawing, or execution authority was introduced.
