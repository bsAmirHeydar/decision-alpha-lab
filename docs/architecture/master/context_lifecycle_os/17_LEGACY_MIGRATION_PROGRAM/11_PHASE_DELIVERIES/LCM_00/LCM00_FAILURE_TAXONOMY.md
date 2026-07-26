---
title: "LCM-00 Failure Taxonomy"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-00, baseline-freeze]
phase_id: LCM-00
claim_ceiling: BASELINE_AND_GOVERNANCE_REFERENCE_ONLY
---
# LCM-00 Failure Taxonomy

Hard failures include unsafe paths, duplicate manifest paths, missing source bytes, hash mismatch, non-empty publication destination, permit escalation, role conflict where approval is required, failed restore rehearsal, manifest tampering, and undeclared baseline mutation.

UNKNOWN evidence is not a hard integrity failure when explicitly bounded, but it blocks stronger claims.


## Related

- [[LCM_00_BASELINE_FREEZE_AND_GOVERNANCE]]
- [[00_LCM_HOME]]
