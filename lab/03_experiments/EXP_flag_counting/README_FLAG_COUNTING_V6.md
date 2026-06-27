# Flag Counting V6 Experiment

Compile and attach:

```text
mql5/Experts/FlagCounting/FlagCountingV6Experiment.mq5
```

Recommended first inputs:

```text
InpBarsToScan = 5000
InpUseMultiScale = true
InpSwingL1 = 2
InpSwingL2 = 3
InpSwingL3 = 5
InpSwingL4 = 8
InpSwingL5 = 13
InpSwingL6 = 21
InpSwingL7 = 34
InpSwingL8 = 55
InpIncludePendingNodes = false
InpShowInvalidatedInAudit = false
InpMaxEventsToDraw = 1200
InpMaxHooksToDraw = 1200
InpDrawCandidates = true
InpDetailedLabels = true
InpShowOriginLabels = true
InpShowInternalLabels = true
InpFixedLineWidth = 1
InpCurveSegments = 32
```

For audit:

```text
InpVerboseAuditLogs = true
```

For less visual noise:

```text
InpDrawHooks = false
```

or

```text
InpMaxEventsToDraw = 300
InpMaxHooksToDraw = 300
```
