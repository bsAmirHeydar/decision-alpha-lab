---
id: UCPS-1AF9A03163C7
title: "UC-02 Exit Decision and UC-03 Handoff"
type: execution-record
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-24
updated: 2026-07-24
tags:
  - consolidation
  - uc02
  - authority-freeze
---
# UC-02 Exit Decision and UC-03 Handoff

## Acceptance conditions

UC-02 is accepted only when UC-01 remains accepted, artifact coverage is 100 percent, unresolved authority is zero, capability and package ledgers are populated, all ten named legacy systems have decisions, contracts validate, guards pass and qualification is reproducible.

## Handoff contents

The UC-03 handoff binds:

- authority-package identity and digest;
- canonical topology contract;
- capability ownership contract;
- system disposition contract;
- repository authority ledger;
- wave portfolio;
- safety constraints.

## UC-03 authorization

`uc03_authorized=true` authorizes only physical reorganization according to the ledger and wave plan. It does not authorize semantic merge, runtime activation or deletion.

## Withholding rule

If any gate is blocked or failed, the handoff remains `WITHHELD`; operators must not infer authorization from the presence of generated files.
