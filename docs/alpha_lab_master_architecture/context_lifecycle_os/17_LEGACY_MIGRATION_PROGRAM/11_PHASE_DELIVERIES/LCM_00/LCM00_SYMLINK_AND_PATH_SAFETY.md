---
title: "LCM-00 Symlink and Path Safety"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-00, baseline-freeze]
phase_id: LCM-00
claim_ceiling: BASELINE_AND_GOVERNANCE_REFERENCE_ONLY
---
# LCM-00 Symlink and Path Safety

Absolute paths, traversal segments, duplicate normalized paths, and symlink following are forbidden. A symlink is recorded as a distinct object with its target string and cannot silently substitute content outside the repository root.


## Related

- [[LCM_00_BASELINE_FREEZE_AND_GOVERNANCE]]
- [[00_LCM_HOME]]
