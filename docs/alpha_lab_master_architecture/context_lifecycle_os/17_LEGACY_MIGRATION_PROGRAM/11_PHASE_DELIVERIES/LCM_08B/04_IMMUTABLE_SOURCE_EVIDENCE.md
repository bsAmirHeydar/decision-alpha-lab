---
title: "LCM-08B — 04 Immutable Source Evidence"
status: accepted-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-08b, pilot-migration]
phase_id: LCM-08B
---
# Immutable Source Evidence

The Python source, README, and metadata are bound by SHA-256. No source bytes are modified, moved, deleted, quarantined, or redirected. The package stores a digest witness rather than replacing the source. Installation verification recomputes the source digest.
