---
title: "LCM-00 Decision Log"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-00, baseline-freeze]
phase_id: LCM-00
claim_ceiling: BASELINE_AND_GOVERNANCE_REFERENCE_ONLY
---
# LCM-00 Decision Log

- Use a separate LCM program rather than extending ACL with ACL-16.
- Freeze byte content before classification or folder movement.
- Treat Git metadata absent from the source archive as UNKNOWN.
- Preserve unresolved human ownership rather than inventing identities.
- Permit LCM-01 survey despite operational blockers, while forbidding semantic and destructive actions.
- Use an annotated post-commit tag as the operational repository anchor.


## Related

- [[LCM_00_BASELINE_FREEZE_AND_GOVERNANCE]]
- [[00_LCM_HOME]]
