---
title: "LCM-08B — 21 Restart Determinism"
status: accepted-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-08b, pilot-migration]
phase_id: LCM-08B
---
# Restart Determinism

The context core is stateless batch logic. Replaying identical bytes and configuration twice must produce identical event arrays and canonical digests. No cache, global state, random ID, or current time may affect output.
