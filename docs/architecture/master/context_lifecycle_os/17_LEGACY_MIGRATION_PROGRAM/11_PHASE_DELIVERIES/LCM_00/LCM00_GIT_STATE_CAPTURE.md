---
title: "LCM-00 Git State Capture"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-00, baseline-freeze]
phase_id: LCM-00
claim_ceiling: BASELINE_AND_GOVERNANCE_REFERENCE_ONLY
---
# LCM-00 Git State Capture

When `.git` is available, the tool records HEAD, branch or detached state, tags at HEAD, porcelain-v2 working-tree status, submodule status, and Git LFS availability. When `.git` is absent, every field remains explicit UNKNOWN and no commit or branch is inferred.

The operational installation creates an annotated Git tag after the phase commit to establish the real repository anchor.


## Related

- [[LCM_00_BASELINE_FREEZE_AND_GOVERNANCE]]
- [[00_LCM_HOME]]
