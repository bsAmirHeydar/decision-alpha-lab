# Stage 09 Index — Cache / Fallback / Resilience Layer

## Start Here

- [[../stage_09_cache_fallback_resilience_layer|Stage 09 — Cache / Fallback / Resilience Layer]]

## Files

- [[01_resilience_contract|01 — Resilience Contract]]
- [[02_cache_bundle_model|02 — Cache Bundle Model]]
- [[03_fallback_chain|03 — Fallback Chain]]
- [[04_source_sanity_and_drift_detection|04 — Source Sanity & Drift Detection]]
- [[05_dashboard_health_states|05 — Dashboard Health States]]
- [[06_validation_checklist|06 — Validation Checklist]]
- [[07_handoff_to_stage_10|07 — Handoff to Stage 10]]

## Code Modules

```text
mql5/include/GartalNewsResilience.mqh
mql5/include/GartalNewsTypes.mqh
mql5/include/GartalNewsInputs.mqh
mql5/include/GartalNewsDiagnostics.mqh
mql5/include/GartalNewsDashboardTheme.mqh
mql5/include/GartalNewsDashboard.mqh
mql5/GartalTerminal.mq5
mql5/experts/GartalNewsDownloaderEA.mq5
```

## Acceptance Rule

Stage 09 is accepted only when the terminal can survive:

1. missing local bridge file
2. malformed live payload
3. low-byte response
4. parser failure
5. fresh cache recovery
6. stale cache recovery
7. final sample fallback
