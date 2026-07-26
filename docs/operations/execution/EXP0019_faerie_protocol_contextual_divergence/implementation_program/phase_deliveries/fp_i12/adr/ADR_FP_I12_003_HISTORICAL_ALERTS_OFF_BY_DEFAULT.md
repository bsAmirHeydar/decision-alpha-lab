---
title: "Historical alerts are off by default"
status: accepted
phase_id: FP-I12
---
# Historical alerts are off by default

## Decision

Historical alerts are off by default. This preserves deterministic semantic evidence while allowing a usable operator interface.

## Consequences

The decision is enforced in Python contracts, MQL5 static checks, negative tests, and the phase authority manifest. A change requires a versioned ADR and contract migration.
