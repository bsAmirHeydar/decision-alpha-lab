---
title: "LCM-08B — 18 Duplicate Timestamp Case"
status: accepted-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-08b, pilot-migration]
phase_id: LCM-08B
---
# Duplicate Timestamp Case

The input contains two rows at one timestamp. Both implementations must keep the last row after sorting and generate the same event. This case prevents an apparently harmless deduplication change from altering behavior.
