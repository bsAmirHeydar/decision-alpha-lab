# VAL0026 — E0009 Release 109 Multi-Level Validation

## Default test

```text
InpUseMacroModeFilter = true
InpMacroModeTF = PERIOD_H4
InpMacroModeNodeCount = 4
InpSetupTF = PERIOD_M15
InpSetupNodeCount = 4
InpExecutionTF = PERIOD_M1
InpExitTF = PERIOD_H4
InpExitNodeCount = 3
```

## Key comparisons

```text
InpUseMacroModeFilter = true / false
InpMacroModeNodeCount = 3 / 4 / 5
InpSetupNodeCount = 3 / 4 / 5
InpExitNodeCount = 2 / 3 / 4
InpUseMicroOnlyFilter = true / false
InpMaxHookRiskToSetupAmplitude = 0.04 / 0.08 / 0.12
InpMaxHookCandidatesPerBar = 1 / 3 / 6
```

Audit lines:

```text
DAL_E0009_AUDIT_A  level modes and directions
DAL_E0009_AUDIT_B  hook rejection counts
DAL_E0009_AUDIT_C  micro filter, duplicate, send counts
DAL_E0009_AUDIT_D  exit pattern and TP sync
```
