---
title: "LCM-00 Scope Policy"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-00, baseline-freeze]
phase_id: LCM-00
claim_ceiling: BASELINE_AND_GOVERNANCE_REFERENCE_ONLY
---
# LCM-00 Scope Policy

All regular files in the repository tree are in scope except explicitly enumerated ephemeral artifacts. Paths are normalized to root-relative POSIX form. Regular files receive SHA-256 digests. Symlinks are records and are never followed.

Exclusion is not erasure: every excluded path is written to the ignored-and-ephemeral report with its reason.


## Related

- [[LCM_00_BASELINE_FREEZE_AND_GOVERNANCE]]
- [[00_LCM_HOME]]
