---
title: "LCM-00 Atomic Publication"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-00, baseline-freeze]
phase_id: LCM-00
claim_ceiling: BASELINE_AND_GOVERNANCE_REFERENCE_ONLY
---
# LCM-00 Atomic Publication

All generated baseline artifacts are written to a private staging directory. A non-empty destination is rejected. Only after every artifact and binding is complete is the staging directory atomically renamed into place. Failures remove staging and publish nothing partial.


## Related

- [[LCM_00_BASELINE_FREEZE_AND_GOVERNANCE]]
- [[00_LCM_HOME]]
