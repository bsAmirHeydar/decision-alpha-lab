---
title: RTHP MT5 Automation — Symbol Discovery, Alias Resolution, and Metadata Freeze
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, mt5, symbols, metadata]
---

# Symbol Discovery, Alias Resolution, and Metadata Freeze

## Operator input

The operator supplies two broker-facing symbol selections. The automation records both the literal broker symbol and the canonical instrument identity.

## Resolution hierarchy

1. Exact broker-symbol match.
2. Registered canonical-to-broker alias match.
3. Exact case-insensitive match.
4. Registered prefix/suffix pattern match.
5. Metadata-assisted candidate ranking.

Only a unique, policy-compliant match may continue automatically. Multiple valid matches require explicit operator selection.

## Frozen symbol metadata

For each symbol, record at minimum:

- broker symbol name;
- canonical instrument ID;
- description and path/group;
- digits;
- point size;
- trade tick size;
- calculation mode;
- contract size;
- currency fields;
- session/trading metadata available from the terminal;
- expiry and start time where applicable;
- terminal server and account identity;
- symbol metadata digest.

## Pair gates

- symbols must be different;
- price basis must be compatible;
- both symbols must expose M1 history;
- both symbols must satisfy the registered RTHP pair policy;
- expiring contracts require an explicit versioned identity and roll policy;
- no implicit continuous-contract stitching is allowed.
