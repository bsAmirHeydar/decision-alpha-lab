# Phoenix Level 17 — Ambiguity Resolution / Final Decision Lock

## Status

Implemented in Phoenix Level 17.

Runtime modules:

```text
mql5/Include/FlagCountingPhoenix/FP_AmbiguityTypes.mqh
mql5/Include/FlagCountingPhoenix/FP_AmbiguityRules.mqh
mql5/Include/FlagCountingPhoenix/FP_AmbiguityAudit.mqh
mql5/Include/FlagCountingPhoenix/FP_AmbiguityEngine.mqh
```

EA support:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

The old purpose of this document was to list unresolved questions before code.
That is now closed. Level 17 turns those decisions into a runtime decision
registry and emits `FP_LEVEL17` after Level 16 acceptance and before
`FP_SUMMARY`.

## Source of truth

The canonical source remains:

```text
docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md
```

Level 17 does not replace the canon. It audits whether the active EA inputs and
runtime reports are aligned with the canon decisions.

## Runtime position

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
-> Level 16 acceptance matrix
-> Level 17 ambiguity / decision lock
-> FP_SUMMARY
```

## Level 17 decisions checked

Level 17 checks the following decision families:

1. Canon source is `FLAG_COUNTING_CURRENT_CANON.md`.
2. `identity_generation_pass` is `phoenix_level17`.
3. Closed-bar timebase remains default.
4. Confirmed F bodies do not consume live pending nodes by default.
5. F1 remains phase-boundary gated.
6. Fail-open remains diagnostic-only.
7. Pre-internal favorable breaks are absorbed as Leg2 extension, not confirmation.
8. F2 main chart requires size qualification by default.
9. OR-rejected F3 candidates are hidden by default.
10. Main-chart Hook/ND requires seeded visible F1 by default.
11. Unseeded Hook display is debug-only.
12. Strict main-chart ownership is enabled.
13. Canonical invariants are strict before renderer/export trust.
14. Renderer strict visibility is enabled.
15. Renderer object names use canonical identity.
16. Export/validation/release/acceptance/interface report alignment is checked.
17. Release-like profiles must not carry blocking failures when strict decision lock is requested.

## EA inputs

```mql5
InpAmbiguityEnabled = true
InpAmbiguityMode = FP_AMBIGUITY_MODE_OBSERVE
InpAmbiguityStrict = false
InpAmbiguityWriteCsv = false
InpAmbiguityOverwriteLatest = true
InpAmbiguityFolder = "FlagCountingPhoenix"
InpAmbiguityRunTag = ""
InpAmbiguityCaseId = "manual"
```

Strict decision inputs:

```mql5
InpAmbiguityRequireDecisionLock = true
InpAmbiguityRequireNoReleaseBlockers = false
InpAmbiguityRequireCanonicalSource = true
InpAmbiguityRequireClosedBarDefault = true
InpAmbiguityRequireConfirmedFBodies = true
InpAmbiguityRequireStrictRendererVisibility = true
InpAmbiguityRequireCanonicalObjectNames = true
InpAmbiguityRequireSeededHookMainChart = true
InpAmbiguityRequireExportBeforeRenderer = true
InpAmbiguityRequireValidationBeforeRelease = true
InpAmbiguityRequireAcceptanceBeforeSummary = true
InpAmbiguityRequireInterfacePassAlignment = false
```

Diagnostic variant inputs:

```mql5
InpAmbiguityAllowFailOpenDiagnostic = true
InpAmbiguityAllowCandidateDisplayDiagnostic = true
InpAmbiguityAllowORRejectedF3Diagnostic = false
InpAmbiguityAllowDebugUnseededHooks = false
```

## Optional CSV

When `InpAmbiguityWriteCsv=true`, Level 17 writes:

```text
MQL5/Files/FlagCountingPhoenix/latest_ambiguity.csv
```

CSV rows contain:

```text
run_id, case_id, mode, decision_id, category, severity, status, actual, expected, canon_source, reason
```

## Non-authority rule

Level 17 is read-only. It must not:

```text
create events
create hooks
mutate identity
repair parent links
change visible_main
change hidden_reason
change lifecycle/ownership/canonical state
alter renderer/export/validation/release/acceptance/interface decisions
```

It only reports whether the final runtime configuration and reports match the
resolved decision record.

## Acceptance

A Level 17 run is accepted when:

```text
FP_LEVEL17 ok=true
ambiguity_fail=0 in FP_SUMMARY
ambiguity_conflicts=0 in FP_SUMMARY
```

Warnings may exist in observe/debug profiles when they represent explicitly
allowed diagnostics.
