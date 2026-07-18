---
title: "Dual Run and Cutover"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Dual Run and Cutover

During dual run, legacy and canonical implementations consume the same frozen events. Only one path may own external side effects. For research and visualization, both paths can emit namespaced outputs. For execution, the canonical path remains dry-run until independent parity approval.

Cutover requires zero unresolved hard mismatches, accepted tolerances for soft dimensions, performance within budget, rollback rehearsal, documentation readiness and owner approval. Cutover changes consumers; it does not delete legacy source.
