---
title: "Context Package Target"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Context Package Target

A migrated Context extends the ACL-02 template and adds migration evidence:

```text
<context_id>/
  context_manifest.yaml
  owners.yaml
  doctrine/
  contracts/
  fixtures/
  tests/
  adapters/
  security/
  governance/
  generated/
  migration/
    legacy_inventory.csv
    legacy_mapping.yaml
    behavioral_contract.yaml
    golden_cases.jsonl
    golden_traces.jsonl
    parity_report.json
    cutover_plan.yaml
    rollback.md
    deletion_eligibility.yaml
```

Context packages own market state and observable occurrence semantics. They do not own order submission, capital, chart rendering or treatment selection beyond an explicit treatment envelope.
