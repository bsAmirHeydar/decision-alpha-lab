---
title: "Baseline Freeze and Change Control"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Baseline Freeze and Change Control

LCM-00 creates an immutable baseline manifest containing path, size, SHA-256, file class and source-control identity. A migration freeze does not stop urgent production fixes; it requires them to enter a declared side lane and be rebased into the baseline through an amendment record.

## Freeze controls

- baseline tag and commit;
- full file manifest and hash set;
- explicit excluded paths;
- active branch register;
- pending uncommitted-change report;
- open-issue and known-bug snapshot;
- environment and toolchain snapshot;
- owner and reviewer roster.

A file created after freeze cannot be silently treated as part of the original legacy behavior.
