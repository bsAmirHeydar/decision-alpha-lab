---
title: RTHP MQL5 Static Diagnostic Mirror
status: ready
version: 1.0.2
---
# MQL5 Static Diagnostic Mirror

The MQL5 mirror pins the Context version, ACL-03 claim ceiling, identity-alias mappings, and the Detector/Occurrence/Known-Time IR digests.

## Implemented

- Compile-time constants for the exact IR digests.
- A diagnostic identity projection structure.
- An alias-consistency check.

## Not implemented

- Market-data acquisition.
- Cycle aggregation.
- Runtime detector execution.
- Event persistence.
- Trading logic or order APIs.

The mirror is intentionally static. Runtime parity belongs to later ACL phases.
