---
title: "LCM-00 Ignored and Ephemeral Files"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-00, baseline-freeze]
phase_id: LCM-00
claim_ceiling: BASELINE_AND_GOVERNANCE_REFERENCE_ONLY
---
# LCM-00 Ignored and Ephemeral Files

Python bytecode, cache directories, editor temporary files, and host lock files are excluded from the baseline content manifest but retained in a separate evidence report. Git-ignored runtime-relevant files must be discovered in the operational repository; absence from the uploaded source archive is not evidence of absence.


## Related

- [[LCM_00_BASELINE_FREEZE_AND_GOVERNANCE]]
- [[00_LCM_HOME]]
