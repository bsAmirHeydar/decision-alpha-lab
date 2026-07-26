# Phase 40 — Hook Validity Lite Compile Fix

## Problem

The practical valid-Hook view update added semantic-readiness checks inside the origin-group envelope builder, but the builder did not receive the Phase 02 config object.

This produced:

```text
undeclared identifier 'cfg'
```

## Decision

Pass `const FP_HookPhase02Config &cfg` into `FP_HookP02GetOriginGroupEnvelope(...)` explicitly.

## Reason

The envelope builder needs to know whether valid-only view requires semantic readiness. That policy lives in Phase 02 config and should not be accessed implicitly.

## Scope

Compile/API alignment only. No Hook validity doctrine is changed.
