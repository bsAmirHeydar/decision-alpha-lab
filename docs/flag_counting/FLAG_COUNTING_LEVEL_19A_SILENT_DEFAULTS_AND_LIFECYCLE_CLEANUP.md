# Flag Counting Level 19A — Silent Defaults and Lifecycle Cleanup

## Purpose

Level 19A applies two operational safety changes requested after the clean Level 19 rebuild.

## Change 1 — Prints disabled by default

All EA input defaults with `InpPrint...` are now set to:

```text
false
```

The input switches are still present, so any diagnostic print can be enabled manually when needed.

Additional print controls were added:

```text
InpPrintFinalSummary = false
InpPrintFailureSummaries = false
InpPrintLicenseSanity = false
InpPrintLicenseSamples = false
InpPrintLicenseFailures = false
```

This means normal chart usage is silent by default.

## Change 2 — Lifecycle object cleanup

Object cleanup is now explicit for important lifecycle events:

```text
InpCleanObjectsOnInit = true
InpCleanObjectsOnDeinit = true
InpCleanObjectsOnChartChange = true
InpCleanObjectsOnRemove = true
InpCleanObjectsOnRecompile = true
InpCleanObjectsOnParameterChange = true
InpCleanObjectsOnTemplateApply = true
```

The EA cleans chart objects by the renderer prefix:

```text
InpObjectPrefix = DAL_FCP_
```

So when:

```text
the EA is removed
the EA is recompiled / updated
inputs are changed
the timeframe is changed
a template is applied
the EA initializes again
```

old drawings are removed and the fresh run can draw the new timeframe/state cleanly.

## Important no-touch boundary

This patch does not modify renderer source files:

```text
FP_Renderer.mqh
FP_RenderRules.mqh
FP_RenderTypes.mqh
```

It also does not change:

```text
F / Hook / Node logic
curve drawing logic
line drawing logic
RTV / zone logic
State Gate read-only contract
license logic
execution logic
```

## Why this is safe

The drawing cleanup uses the existing renderer object prefix and lifecycle hooks. It does not change how lines or curves are calculated.

The print change only changes input defaults and adds explicit print gates for summary/failure/license logs.
