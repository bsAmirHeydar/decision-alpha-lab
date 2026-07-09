# Hook Origin Lifecycle Fix — Start Here

This patch fixes the M1 Hook semicircle noise where Hook candidates were being
rendered even though their origin had already been breached before the terminal
node was confirmed.

Start with:

```text
docs/nds_hook_architecture/44_phase32_raw_origin_breach_lifecycle_guard.md
```

Obsidian entry:

```text
docs/obsidian_hook/00_mocs/HOOK_LIFECYCLE_MOC.md
```

Main code entry:

```text
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Rules.mqh
```

New production input:

```text
InpHookPhase02RejectRawOriginBreachBeforeTerminalConfirmation = true
```
