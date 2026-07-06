---
type: architecture_note
domain: hook_phase02
status: implemented
source_doc: docs/nds_hook_architecture/44_phase32_raw_origin_breach_lifecycle_guard.md
---

# Phase 32 — Raw Origin-Breach Lifecycle Guard

This note links the Obsidian Hook knowledge layer to the implementation patch.

## Main source

See:

```text
docs/nds_hook_architecture/44_phase32_raw_origin_breach_lifecycle_guard.md
```

## Patched implementation

```text
FP_HookP02RawOriginBreachedBeforeTerminalConfirmation(...)
```

is called before a Phase 02 sequence can become render eligible.

## Default input

```text
InpHookPhase02RejectRawOriginBreachBeforeTerminalConfirmation = true
```

## Audit counter

```text
raw_origin_breach_rejects
```

This identifies how many candidates were removed because raw high/low action
killed the Hook origin before terminal confirmation.
