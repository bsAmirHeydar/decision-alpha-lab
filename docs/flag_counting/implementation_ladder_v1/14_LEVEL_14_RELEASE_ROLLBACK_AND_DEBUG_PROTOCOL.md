# Phoenix Flag Counting Implementation Ladder V1

This document is part of the implementation ladder for the Phoenix Flag Counting engine. The ladder is intentionally layered so that lower layers become frozen foundations before higher layers are allowed to depend on them.

Global non-negotiables:

- All structural decisions use candle `high` and `low` only.
- `open`, `close`, candle body, candle color, volume, and indicators are not structural inputs.
- Equality is not a break. A level is broken only by a strict pass beyond it.
- The renderer is non-authoritative. It may only draw logical objects emitted by engines.
- Main-chart rendering and audit rendering are separate products.
- Every layer must expose enough audit fields to prove why an object exists.
- A higher layer may never silently repair a lower-layer defect.

# Level 14 — Release, Rollback, and Debug Protocol

## Purpose

This layer prevents losing time to broken MetaTrader state, stale chart objects, and ambiguous Git rollback. It defines how to ship, test, revert, and debug Phoenix changes.

## Release steps

1. Create backup branch.
2. Apply patch.
3. Remove stale `.ex5`.
4. Compile in MetaEditor.
5. Remove expert from chart.
6. Delete `DAL_FCP_` objects.
7. Attach expert.
8. Reset inputs.
9. Run clean main chart screenshot.
10. Run audit screenshot if needed.
11. Commit with layer-aware message.
12. Push.

## Standard apply block

```powershell
cd "C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\4769098028DB821E4654DC6D5C533078\MQL5\Shared Projects\decision-alpha-lab"

git branch backup-before-<patch-name>

Expand-Archive -Path ".\<patch-name>.zip" `
  -DestinationPath "." `
  -Force

Remove-Item ".\<patch-name>.zip" -Force

Get-ChildItem -Recurse -Filter "FlagCountingPhoenixExperiment.ex5" |
  Remove-Item -Force -ErrorAction SilentlyContinue
```

## Standard chart cleanup

```text
1. Remove Expert from chart.
2. Press Ctrl+B.
3. Delete all objects with DAL_FCP_ prefix.
4. Recompile Expert.
5. Attach Expert again.
6. Reset inputs.
```

## Debug order

When chart is wrong:

```text
1. Is the compiled .ex5 fresh?
2. Are old objects deleted?
3. Are inputs reset?
4. Are clean/audit modes as expected?
5. Does audit show raw candidates?
6. Does lifecycle hide them? Why?
7. Does canonicalization hide them? Why?
8. Does renderer simply fail to draw visible objects?
```

## Rollback options

### Safe revert after push

```bash
git revert HEAD
```

Use when shared history must be preserved.

### Exact reset to known good state

```bash
git reset --hard <GOOD_SHA>
git push --force-with-lease origin main
```

Use when you own the branch and want remote to match exactly.

### Restore selected files

```bash
git checkout <GOOD_SHA> -- mql5/Include/FlagCountingPhoenix/FP_Renderer.mqh
```

Use when only one layer must be restored.

## Commit message template

```bash
git commit -m "Repair Phoenix <layer> <short purpose>

- layer: Lxx <name>
- touched modules: <files>
- preserve: <invariants>
- change: <explicit behavior change>
- tests: <compile/tests/screenshots>
- risk: <known limitation>"
```

## Failure triage examples

### Chart mostly gray

Likely failed layers:

```text
L04 Hook/ND emits too much
L11 Hook main/audit separation failed
L12 renderer draws audit hooks in main mode
```

### No colored flags

Likely failed layers:

```text
L05 flag body starved
L07 F1 root gating too strict
L10 sequence ownership hides roots
L11 canonicalization hides all winners
```

### Too many same-direction F1s

Likely failed layers:

```text
L10 sequence ownership missing
L03 identity too weak
L11 canonicalization visual duplicate rules too weak
```

### F2/F3 too early

Likely failed layers:

```text
L08 F2 authorization wrong
L09 F3 authorization wrong
L06 internal count confirmation leaked
```

### Curves broken

Likely failed layers:

```text
L01 timebase uses timestamp interpolation
L12 renderer stale segment cleanup failed
```

## Freeze condition

Release protocol is frozen when every Phoenix patch includes apply, compile, cleanup, commit, and rollback instructions.
