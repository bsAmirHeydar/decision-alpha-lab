---
title: "LCM-00 Large File and Binary Policy"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-00, baseline-freeze]
phase_id: LCM-00
claim_ceiling: BASELINE_AND_GOVERNANCE_REFERENCE_ONLY
---
# LCM-00 Large File and Binary Policy

Large and binary files remain hash-bound. They are not deleted or externalized during LCM-00. Files above the threshold are surfaced for later Git LFS or artifact-store decisions. Externalization requires a successor locator and verified recovery test.


## Related

- [[LCM_00_BASELINE_FREEZE_AND_GOVERNANCE]]
- [[00_LCM_HOME]]
