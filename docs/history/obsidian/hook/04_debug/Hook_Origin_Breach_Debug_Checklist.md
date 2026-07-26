---
type: debug_checklist
domain: hook_lifecycle
status: active
---

# Hook Origin Breach Debug Checklist

Use this checklist when M1 Hook arcs look noisy or when a semicircle appears to
start from an origin that was already hit.

## Checks

- Confirm the new input is enabled:
  `InpHookPhase02RejectRawOriginBreachBeforeTerminalConfirmation = true`
- Enable Phase 02 summary print if deeper diagnostics are needed.
- Look for `raw_origin_breach_rejects` in the Phase 02 summary.
- Compare with the old behavior only by temporarily disabling the input.
- Do not use disabled mode for production interpretation.

## Expected fixed behavior

A Hook origin breached before terminal confirmation should produce:

```text
reject_reason = RAW_ORIGIN_BREACH_BEFORE_TERMINAL_CONFIRMATION
render_eligible = false
no semantic arc
no Hook zone
```
