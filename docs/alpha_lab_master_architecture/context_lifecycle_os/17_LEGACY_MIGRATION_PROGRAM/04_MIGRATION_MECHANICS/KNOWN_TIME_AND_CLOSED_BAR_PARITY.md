---
title: "Known-Time and Closed-Bar Parity"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Known-Time and Closed-Bar Parity

Known-time is zero-tolerance. The canonical implementation may not observe a bar, label, session state or reference earlier than the legacy contract allows. If legacy code accidentally uses future data, the trace records that behavior but the canonical package must classify it as diagnostic or issue a versioned correction decision; it may not silently preserve future leakage in a live path.

Closed-bar variants and host-chart-timeframe variants are separate contracts when behavior differs.
