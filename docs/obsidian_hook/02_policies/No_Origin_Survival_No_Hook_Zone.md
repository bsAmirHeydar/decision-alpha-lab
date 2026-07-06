---
type: policy
domain: hook_zone
status: canonical
---

# No Origin Survival, No Hook Zone

A Hook-derived zone is valid only if the Hook itself survives structurally.
Survival means the origin was not breached before the terminal node confirmed.

## Production rule

```text
if raw_origin_breach_before_terminal_confirmation:
    reject candidate
    draw nothing
    generate no Hook zone
```

## Diagnostic exception

The expert input below may be disabled only to compare old permissive behavior
against the corrected lifecycle behavior:

```text
InpHookPhase02RejectRawOriginBreachBeforeTerminalConfirmation = false
```

Production doctrine keeps it enabled.
