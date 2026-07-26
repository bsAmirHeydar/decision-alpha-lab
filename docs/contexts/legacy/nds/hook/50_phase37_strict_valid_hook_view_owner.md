# Phase 37 — Strict Valid Hook View Owner

## Doctrine

Valid-only Hook view must have exactly one production owner:

```text
Phase 02 semantic Hook renderer after validity-family annotation.
```

The raw/core Hook renderer, Phase 01 raw nodes, and Phase 03-06 diagnostic overlays are not allowed to display Hook objects when valid-only mode is active.

## Why

The previous valid-only filter correctly filtered Phase 02 sequences, but other renderers could still draw Hook-like objects. This made it appear as if all Hooks were still visible even when `InpHookPhase02ShowOnlyValidHooks = true`.

## Runtime guard

When valid-only mode is active, the expert applies a strict view guard:

```text
raw/core hooks: off
Phase 01 raw nodes: off
Phase 03-06 diagnostic overlays: off
Phase 02 valid family renderer: on
stale Hook objects: cleaned before valid redraw
```

## Valid families

A Hook is production-visible only if it is:

```text
Hook After Opposing F3
Hook After Hook
```

For Hook-after-Hook, the parent Hook is visible only as the required companion of the valid second Hook.

## Opposing-F3 boundedness

An opposing F3 does not validate all later Hooks. It validates only the first structurally valid Hook after that completed/locked opposing F3.
