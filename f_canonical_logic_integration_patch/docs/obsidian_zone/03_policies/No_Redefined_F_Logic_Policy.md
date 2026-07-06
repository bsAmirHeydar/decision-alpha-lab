# No Redefined F Logic Policy

## Policy

Zone-AF may not redefine F1, F2, or F3.

## Reason

If Zone-AF creates its own F definitions, the project loses:

- deterministic auditability;
- canonical event identity;
- consistent training labels;
- reliable code/document alignment;
- future AI-agent safety.

## Required Action

Every F-zone patch must check canonical F docs first.

## Hard Rule

```text
If the F event is not canonical, the zone cannot be labeled as F-derived.
```
