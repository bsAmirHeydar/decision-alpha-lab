---
title: "Dependency and Reachability Analysis"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Dependency and Reachability Analysis

LCM-01 builds include/import edges. LCM-03 adds entry points, compile units and runtime reachability. A file with an order API but no active caller is still security-sensitive, but it is not treated as active execution without evidence.

Analysis dimensions include static includes, dynamic registration, file-based configuration, object-name coupling, Global Variables, timers, callbacks, chart events, generated code, test-only references and documentation-only references.
