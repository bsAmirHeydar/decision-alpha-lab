---
title: "State, Event and Reason-Code Parity"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# State, Event and Reason-Code Parity

Output parity alone is insufficient. The comparator checks state transitions, event ordering, consumed-reference state, deduplication identity, cancellation, expiry, no-trade and failure reason codes. A later identical signal after a different state path is not automatically equivalent.

Reason-code mappings may normalize names but must preserve meaning and severity.
