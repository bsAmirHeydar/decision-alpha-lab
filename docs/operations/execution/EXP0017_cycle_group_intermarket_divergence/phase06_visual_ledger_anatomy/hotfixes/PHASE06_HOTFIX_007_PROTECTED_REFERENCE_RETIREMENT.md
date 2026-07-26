# Phase 06 Hotfix007 — Protected Reference Retirement

## Purpose

This hotfix fixes a structural lifecycle issue in EXP0017: a previous-cycle high/low reference must not keep producing new divergence drawings after the clean/protected symbol has finally hunted that same reference side.

The visual symptom was repeated divergence lines built from the same reference even after that reference had already been compromised. The strategy doctrine says this is wrong.

## New rule

A reference side has two different states:

1. **Protected but alive** — one symbol has hunted the reference side, the other symbol remains clean/protected. The same reference side may still generate repeated divergence events as long as the protected symbol remains protected.
2. **Retired** — the clean/protected symbol eventually hunts the same high/low reference. From that moment onward, that reference-side key is retired and cannot create new divergence signals or drawings again.

## Correct example

A high reference belongs to a prior `cg_30m` cycle.

- NDXUSD hunts its own reference high.
- SPXUSD does not hunt its own reference high.
- SPXUSD is protected/clean.
- SELL divergence is allowed.
- If NDXUSD later hunts again while SPXUSD still has not hunted, repeated SELL divergence may be allowed.
- If SPXUSD later hunts that high reference, the high-side reference is retired.
- After retirement, the same prior-cycle high must not be used to build another divergence.

## Incorrect behavior removed

The EA must not treat a later one-sided state as a new divergence if it only exists because the previously protected side has already crossed the reference.

## Implementation location

The fix is implemented in the confirmation layer because the problem is not only visual. Drawing must only receive eligible final signals. Therefore the lifecycle gate sits before visual output.

## Inputs

```text
InpEnableProtectedReferenceRetirement = true
InpRetireReferenceWhenProtectedHunts = true
InpAllowRepeatedDivergenceWhileProtectedSurvives = true
InpSuppressRetiredReferenceSignals = true
InpResetProtectedReferenceLifecycleAtNewTradingDay = true
InpMaxProtectedReferenceRecords = 4096
```

## Non-goals

This hotfix does not add trade execution, risk, targets, position management, statistical scoring, or AI behavior.
