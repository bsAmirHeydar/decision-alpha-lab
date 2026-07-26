# Flag Counting Level 19 — Phase 9A Compile Fix

## Purpose

Phase 9A fixes a compile error introduced during Phase 9.

## Error

```text
undeclared identifier 'InpStateGateExportDiagnosticsCsv'
```

## Cause

The State Gate config loader referenced:

```text
InpStateGateExportDiagnosticsCsv
```

but the EA input declaration was missing.

## Fix

Add:

```text
input bool InpStateGateExportDiagnosticsCsv = true;
```

beside the other Level 19 export inputs.

## Locked boundaries

This fix only touches the Level 19 input shell and documentation.

It does not change:

- Node Engine
- Hook / ND Engine
- Flag Body
- Internal Count
- F1 / F2 / F3 lifecycle
- Ownership / Canonicalization
- Renderer
- Validation
- Release
- License
