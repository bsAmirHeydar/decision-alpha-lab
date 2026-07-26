# Hook Canon Step 3 — Family Rendering Patch

## Purpose

This patch completes the next layer after canonical visible-set filtering and canonical validity determination.

The goal is not to find more or fewer Hooks. The goal is to make the Hooks that are already selected by the canonical valid-visible-set layer readable as families:

- Hook After Opposing F3
- Hook After Hook
- Parent companion Hook

## What changes

### 1. Family label prefixes

Node/sequence labels now receive a canonical family prefix in valid-only mode:

```text
F3H H123B1:1
HH H128B1:2
PARENT H124B1:1
F3H+HH H131B1:3
```

These prefixes are only a production-view decoration. They do not change sequence counting.

### 2. Family colors

Valid-only cycle arcs and labels use family-level colors:

| Family | Tag | Color doctrine |
|---|---|---|
| Hook After Opposing F3 | `F3H` | distinct post-F3 color |
| Hook After Hook | `HH` | distinct chained-Hook color |
| Both families | `F3H+HH` | priority/highlight color |
| Parent companion | `PARENT` | neutral companion color |

### 3. Parent companion rendering

If Hook-2 is valid because it starts from Hook-1 terminal, Hook-1 remains visible as the required parent companion.

Parent companion labels are marked with:

```text
PARENT
```

This prevents the parent from being confused with an independently valid production Hook.

## Files changed

```text
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Visual.mqh
```

## Documentation added

```text
docs/nds_hook_architecture/62_phase45_canonical_family_rendering_step3.md
docs/obsidian_hook/00_mocs/HOOK_CANON_STEP3_MOC.md
docs/obsidian_hook/02_policies/Canonical Hook Family Labels.md
docs/obsidian_hook/02_policies/Parent Companion Is Rendered But Not Promoted.md
docs/obsidian_hook/03_architecture/Phase 45 Canonical Family Rendering.md
docs/obsidian_hook/04_debug/Family Rendering Debug Checklist.md
```

## Recommended settings

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyFallbackToStructural = false
InpHookPhase02ValidOnlyRequireNearDeath = false
InpHookPhase02ValidF3RequireSameScale = false
InpHookPhase02ValidF3RequireOppositeDirection = true
InpHookPhase02SeedUsedNodesCannotRestart = true
InpHookPhase02RejectRawOriginBreachBeforeTerminalConfirmation = true
InpHookPhase02ShowHookSequenceIdsInLabels = true
```

