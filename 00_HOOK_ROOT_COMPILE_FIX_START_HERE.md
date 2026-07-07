# HOOK ROOT COMPILE FIX — Start Here

This patch repairs a compile-time API drift introduced after the Hook root rebuild.

The root rebuild replaced Phase 02 sequence construction with the seed-owned builder, but some local Phase 03-06 engine files may still call the earlier rate-aware Phase 02 entrypoint:

```mql5
FP_HookP02BuildSequencesWithRates(rates, copied, nodes, p02_cfg, sequences, sequence_report);
```

This patch restores that public compatibility entrypoint inside `FP_HookPhase02Rules.mqh` and forwards it to the new canonical seed-owned builder.

Scope: compile compatibility only. It does not change F-counting, Rally logic, execution logic, broker behavior, order sending, or risk sizing.
