# EXP Flag Counting

This experiment studies fractal, multi-scale, multi-sequence F-counting.

## Active source of truth

Start from the current canon:

```text
docs/contexts/legacy/flag_counting/FLAG_COUNTING_CURRENT_CANON.md
```

That file resolves all Flag Counting implementation decisions. If older VNext/V6/M0007 documents conflict with it, the current canon wins.

## Active implementation path

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
mql5/Include/FlagCountingPhoenix/
```

Phoenix is the only active implementation path for this experiment.

## Core documents

Read in this order:

1. `docs/contexts/legacy/flag_counting/FLAG_COUNTING_CURRENT_CANON.md`
2. `docs/contexts/legacy/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md`
3. `docs/contexts/legacy/flag_counting/FLAG_COUNTING_ENGINEERING_PACK_V5.md`
4. `docs/contexts/legacy/flag_counting/engineering_pack_v5/`
5. `docs/contexts/legacy/flag_counting/implementation_ladder_v1/`
6. `docs/contexts/legacy/flag_counting/phoenix_rebuild/`

## Legacy documents

The old VNext, V6, sequence V2/V3, checklist V2/V3/V4, and M0007 documents remain research history. They must not be used as the decision source for new code.

## Experiment grammar

The active model is:

```text
ND/Hook -> F1 -> F2 -> F3 -> Extension/Lock
```

Core rules:

- high/low only;
- strict break only;
- equality is not break;
- L-based node streams;
- branch-based Hook/ND;
- F1/F2/F3 are lifecycle roles, not separate body shapes;
- F2/F3 origins use strict documented backfill windows;
- canonical main chart and audit output are separate;
- renderer is non-authoritative.

## Default visibility policy

Main chart is canonical-clean by default. Audit/export must preserve raw candidates, hidden duplicates, fail-open recovery roots, Hook/ND branches, sequence transitions, and hidden reasons.

## Recommended first Phoenix run

```text
InpBarsToScan = 5000
InpUseMultiScale = true
InpRequireF1PhaseBoundary = true
InpAllowF1FailOpenWhenNoHook = true
InpDrawHooks = true
InpDetailedLabels = true
InpVerboseAuditLogs = false
```

For audit work, enable verbose audit logs/export before judging the renderer.
