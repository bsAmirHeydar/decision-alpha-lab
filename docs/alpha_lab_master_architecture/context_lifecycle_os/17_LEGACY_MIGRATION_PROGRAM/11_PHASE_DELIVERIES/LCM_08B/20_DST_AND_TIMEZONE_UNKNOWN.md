---
title: "LCM-08B — 20 Dst And Timezone Unknown"
status: accepted-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-08b, pilot-migration]
phase_id: LCM-08B
---
# DST and Timezone Unknown

A fixture crosses the spring-forward clock gap using naive timestamp strings. Parity requires preservation of input timestamps, not timezone correction. The source has no timezone identity or DST conversion rule. Any later timezone standardization requires explicit doctrine and a new version.
