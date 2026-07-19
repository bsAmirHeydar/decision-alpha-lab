---
title: "LCM-08B — 13 No Occurrence And Missingness"
status: accepted-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-08b, pilot-migration]
phase_id: LCM-08B
---
# No Occurrence and Missingness

Unavailable references, non-triggered origin bars, or destination confirmation inside lag produce no occurrence. This is an empty result, not an error and not an implicit trade rejection. Missing aligned timestamps disappear through the inner join. No reason code is invented for rows that never become occurrences.
