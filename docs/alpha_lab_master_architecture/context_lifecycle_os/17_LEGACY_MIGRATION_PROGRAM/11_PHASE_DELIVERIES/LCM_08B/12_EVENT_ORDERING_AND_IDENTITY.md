---
title: "LCM-08B — 12 Event Ordering And Identity"
status: accepted-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-08b, pilot-migration]
phase_id: LCM-08B
---
# Event Ordering and Identity

Legacy ordering scans A-as-origin, then B-as-origin when enabled. Within a direction it scans ascending bar index and HIGH before LOW. Event IDs are sequential and adapter-owned. No random, wall-clock, or hash-based event ID is substituted because parity requires the legacy sequence.
