# Stage 01 Index — Compile-Safe Core Skeleton

## Entry point

- [[../stage_01_compile_safe_core_skeleton|Stage 01 — Compile-Safe Core Skeleton]]

## Detailed notes

1. [[01_core_contract|Core Contract]]
2. [[02_lifecycle_map|MQL5 Lifecycle Map]]
3. [[03_module_boundaries|Module Boundaries]]
4. [[04_runtime_state_model|Runtime State Model]]
5. [[05_compile_validation_checklist|Compile Validation Checklist]]
6. [[06_handoff_to_stage_02|Handoff to Stage 02]]

## Code targets

```text
product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5
product_lab/indicators/gartal_terminal/mql5/include/*.mqh
```

## Stage promise

Stage 01 is not a feature sprint. It is a **structural contract sprint**. Every later module must be able to plug into this skeleton without rewriting the lifecycle.
