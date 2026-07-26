---
title: "LCM-08B — 08 Causal Clock And Known Time"
status: accepted-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-08b, pilot-migration]
phase_id: LCM-08B
---
# Causal Clock and Known Time

Reference windows use only indices strictly before evaluation index `i`. Destination lag includes `i` through `i + lag`. Validity begins at the clamped lag endpoint. The source does not prove timestamps are timezone-aware or that bars are closed. Those facts remain UNKNOWN and block production claims, but do not block exact legacy parity.
