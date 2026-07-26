---
title: "LCM-00 Content Manifest"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-00, baseline-freeze]
phase_id: LCM-00
claim_ceiling: BASELINE_AND_GOVERNANCE_REFERENCE_ONLY
---
# LCM-00 Content Manifest

The baseline manifest is sorted by path, duplicate-free, byte-exact, and content-derived. Identity material excludes file modification time because mtime is not provenance. The baseline ID derives from path, kind, size, content digest or symlink target, and the scope-policy digest.

The manifest is immutable. Approved side-lane changes create amendments or a successor baseline; they never rewrite history.


## Related

- [[LCM_00_BASELINE_FREEZE_AND_GOVERNANCE]]
- [[00_LCM_HOME]]
