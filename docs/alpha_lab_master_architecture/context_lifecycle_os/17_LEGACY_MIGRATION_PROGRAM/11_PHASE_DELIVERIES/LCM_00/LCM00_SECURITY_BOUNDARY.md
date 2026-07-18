---
title: "LCM-00 Security Boundary"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-00, baseline-freeze]
phase_id: LCM-00
claim_ceiling: BASELINE_AND_GOVERNANCE_REFERENCE_ONLY
---
# LCM-00 Security Boundary

LCM-00 performs local filesystem and Git inspection only. Network access, secret access, production-key access, runtime generation, order submission, and capital activation are prohibited. Binary content is hashed but not executed.


## Related

- [[LCM_00_BASELINE_FREEZE_AND_GOVERNANCE]]
- [[00_LCM_HOME]]
