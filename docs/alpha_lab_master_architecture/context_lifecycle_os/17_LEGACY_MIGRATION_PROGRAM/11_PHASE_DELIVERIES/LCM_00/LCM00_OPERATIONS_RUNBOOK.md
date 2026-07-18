---
title: "LCM-00 Operations Runbook"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-00, baseline-freeze]
phase_id: LCM-00
claim_ceiling: BASELINE_AND_GOVERNANCE_REFERENCE_ONLY
---
# LCM-00 Operations Runbook

1. Apply the additive patch.
2. Verify all pre-freeze paths remain byte-identical and all additions are declared.
3. Run the LCM-00 tests.
4. Commit with the supplied message.
5. Create the supplied annotated tag.
6. Push the commit and tag.
7. Record real role assignments before any semantic or destructive phase.
8. Open side-lane amendments for every post-freeze hotfix.


## Related

- [[LCM_00_BASELINE_FREEZE_AND_GOVERNANCE]]
- [[00_LCM_HOME]]
