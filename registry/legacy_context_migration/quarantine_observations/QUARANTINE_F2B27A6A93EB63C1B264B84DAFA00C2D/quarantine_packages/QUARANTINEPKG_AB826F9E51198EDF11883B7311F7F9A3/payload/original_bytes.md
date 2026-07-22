# EXP Flag Counting Phoenix

Phoenix is the active Flag Counting implementation.

## Source of truth

Read first:

```text
docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md
```

Then read:

```text
docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md
docs/flag_counting/FLAG_COUNTING_ENGINEERING_PACK_V5.md
docs/flag_counting/implementation_ladder_v1/
docs/flag_counting/phoenix_rebuild/
```

## Compile and run

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Phoenix must be used instead of all previous FlagCounting, VNext, V6, or M0007 experiments for new work.

## Recommended first settings

```text
InpBarsToScan = 5000
InpUseMultiScale = true
InpRequireF1PhaseBoundary = true
InpAllowF1FailOpenWhenNoHook = true
InpDrawHooks = true
InpDetailedLabels = true
InpVerboseAuditLogs = false
```

## Implementation rule

Do not patch from screenshots. Patch the correct implementation-ladder level, update audit evidence, and keep renderer non-authoritative.
