---
id: UCPS-F609ED9EE52B
title: "Stage Charter and Exit Report Template"
type: template
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Stage Charter and Exit Report Template

## Stage charter fields

```yaml
stage_id: <UC-XX>
purpose: <bounded objective>
baseline_commit: <git commit>
inputs: []
write_scope: []
non_goals: []
mandatory_gates: []
rollback_plan: <path>
owners: []
approvers: []
```

## Exit report fields

```yaml
stage_id: <UC-XX>
result: <PASS|FAILED|BLOCKED>
changed_paths_manifest: <path>
output_digests: []
test_receipts: []
recovery_receipt: <path>
defects: []
residual_risks: []
waivers: []
approvals: []
next_stage_handoff: <digest>
```

The report must distinguish implementation completion from program authorization.
