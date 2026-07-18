---
title: "LCM-01 Survey Identity"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01]
phase_id: LCM-01
claim_ceiling: FORENSIC_SURVEY_REFERENCE_ONLY
---
# LCM-01 Survey Identity

The reference Survey ID is `SURVEY_D4EC5C533F886BC439DAEEBDE51FA080`. Identity material consists of the LCM-00 manifest digest, source handoff digest, scanner version and frozen scanner configuration digest. Filesystem enumeration order, host absolute paths, modification times and random UUIDs are excluded.

Survey identity is not a semantic version of any Context or Setup. It identifies one deterministic forensic observation package over one exact baseline.
