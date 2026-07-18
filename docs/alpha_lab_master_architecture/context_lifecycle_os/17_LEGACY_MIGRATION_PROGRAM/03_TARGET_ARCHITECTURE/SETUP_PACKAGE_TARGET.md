---
title: "Setup Package Target"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Setup Package Target

```text
<setup_id>/
  setup_manifest.yaml
  owners.yaml
  contracts/
    context_binding.yaml
    eligibility.yaml
    trigger.yaml
    confirmation.yaml
    invalidation.yaml
    expiry.yaml
    abstention.yaml
    treatment_bindings.yaml
  fixtures/
  tests/
  adapters/
  migration/
```

A Setup consumes Context observations and produces a bounded opportunity record with reason codes. It does not redraw Context, recalculate session clocks independently or call broker APIs.
