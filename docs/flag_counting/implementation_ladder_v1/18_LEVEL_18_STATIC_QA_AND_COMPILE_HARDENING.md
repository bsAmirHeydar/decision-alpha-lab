# Level 18 — Static QA / Compile Hardening

Level 18 is an extension after the original Level 17 decision lock. It exists because the Phoenix engine became large enough that runtime logic can be correct while MQL5 compile hazards still break execution.

This layer is **read-only**. It does not create, mutate, hide, reveal, confirm, invalidate, lock, re-parent, export, render, validate, release, accept, or reinterpret market structures.

## Purpose

Level 18 hardens Phoenix against recurring MQL5 failure modes:

- empty `Print()` calls
- oversized multi-argument `Print(...)` calls
- duplicate `input` declarations
- stale `identity_generation_pass` values
- stale interface contract versions
- stale short report alias references
- missing public Level modules
- final runtime partition or counter drift after all reporting layers

## Runtime modules

```text
mql5/Include/FlagCountingPhoenix/FP_StaticQaTypes.mqh
mql5/Include/FlagCountingPhoenix/FP_StaticQaRules.mqh
mql5/Include/FlagCountingPhoenix/FP_StaticQaAudit.mqh
mql5/Include/FlagCountingPhoenix/FP_StaticQaEngine.mqh
```

The EA emits:

```text
FP_LEVEL18
```

Optional CSV:

```text
MQL5/Files/FlagCountingPhoenix/latest_static_qa.csv
```

## Source-side tool

Runtime MQL cannot inspect its own source files reliably. Therefore Level 18 also ships a dependency-free Python scanner:

```text
tools/flag_counting/static_qa.py
```

Run it from repository root:

```powershell
python tools/flag_counting/static_qa.py --root . --csv reports/flag_counting_static_qa.csv
```

Strict mode:

```powershell
python tools/flag_counting/static_qa.py --root . --strict
```

## Execution order

```text
Level 14 profile pre-apply
-> Level 15 preflight
-> Level 01 timebase
-> Levels 02-11 detection/canonicalization
-> Level 11.5 export
-> Level 12 renderer
-> Level 13 validation
-> Level 14 release gate
-> Level 15 postflight
-> Level 16 acceptance
-> Level 17 decision lock
-> Level 18 static QA
-> FP_SUMMARY
```

## Acceptance

Level 18 passes when:

- `FP_STATIC_QA_CONTRACT_VERSION == 18.00`
- `identity_generation_pass == phoenix_level18`
- `FP_INTERFACE_CONTRACT_VERSION == 18.00`
- visible + hidden event counts equal total events
- important counters are non-negative
- export/render/validation reports do not contain required I/O errors
- interface/acceptance/ambiguity reports are available when alignment is required
- the Python source scanner reports no blocking findings

Warnings are allowed in observe mode. Use strict mode for release-hardening.
