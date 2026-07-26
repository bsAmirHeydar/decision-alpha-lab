# Hook Valid Cycles Only View Patch

## Purpose

The previous practical-valid view could still show many Hook labels because `InpHookPhase02ValidOnlyFallbackToStructural` was enabled by default. When the valid-family selector returned zero candidates, the renderer fell back to structural Hook candidates. That was useful for debugging, but it violated the production doctrine:

> valid-only means valid cycles only.

## Production doctrine

When `InpHookPhase02ShowOnlyValidHooks = true`:

- draw only valid Hook cycles;
- draw only the sequence/node labels belonging to those selected valid Hook origin groups;
- show Hook-1 only when it is the parent companion of a valid Hook-after-Hook child;
- hide unqualified Hook candidates;
- hide raw Phase 01 nodes and later diagnostic overlays;
- do not fall back to structural hooks unless a debug input explicitly enables that behavior.

## Valid families

A production-visible Hook cycle belongs to one of these families:

1. **Immediate Hook After Opposing F3**
2. **Hook After Hook**, where Hook-2 starts from Hook-1 terminal.

The first Hook in a Hook-after-Hook pair may be visible only as a parent companion. It is not promoted into an independently valid family.

## Changed defaults

```text
InpHookPhase02ValidOnlyFallbackToStructural = false
```

Debug fallback remains available, but it is no longer the default.
