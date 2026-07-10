---
id: AIEOS2-09AAE78A207F
title: "Alpha Lab Exception and Waiver Standard"
type: standard
status: active
domain: engineering
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - engineering
---
# Alpha Lab Exception and Waiver Standard

## Rule

A MUST-level policy may be bypassed only through an explicit, temporary, reviewable waiver. Convenience and schedule pressure are not automatic justification.

## Waiver Fields

```text
waiver_id
rule being waived
scope/files/stages
reason and alternatives considered
risk and blast radius
compensating controls
owner and approver
start and expiry
evidence required for closure
rollback/remediation plan
```

## Non-Waivable Controls

Without an explicit architect decision, the following do not receive routine waivers:

- future leakage into live/model features;
- hidden execution authority;
- unbounded capital risk;
- secrets committed to source;
- fabricated test/compile evidence;
- orphan/duplicate research identity;
- silent domain ontology changes.

Expired waivers fail closed and become debt/incident items.
