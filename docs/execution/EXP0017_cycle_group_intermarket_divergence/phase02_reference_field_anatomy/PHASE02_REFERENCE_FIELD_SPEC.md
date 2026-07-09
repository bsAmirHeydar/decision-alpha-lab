# Phase 02 Reference Field Specification

## Purpose

The purpose of Phase 02 is to let the robot build the same reference landscape that the strategy architect expects before hunt detection begins.

For every enabled Cycle Group and for both symbols, the robot must identify all completed previous cycles inside the current New York trading day and extract their high and low values.

## Trading-day boundary

Phase 02 inherits the Phase 01 time contract:

```text
Trading day start: 18:00 New York
Trading day end:   17:00 New York
Decision field:    current same-day field only
```

The reference field is not built from broker calendar days, UTC days, or local computer time.

## Reference definition

For each completed previous cycle, each symbol has two price references:

```text
reference_high
reference_low
```

A reference is symbol-local. SPXUSD is compared only against SPXUSD references. NDXUSD is compared only against NDXUSD references.

The system does not compare absolute SPXUSD price against absolute NDXUSD price.

## Previous-cycle scope

For a current CG cycle, the candidate reference set is:

```text
all completed previous cycles of the same CG inside the same New York trading day
```

Example for `cg_30m` at 09:45 NY:

```text
current cycle: 09:30-09:59
reference candidates:
18:00-18:29
18:30-18:59
19:00-19:29
...
09:00-09:29
```

## M1 aggregation rule

The reference high/low is aggregated from M1 bars:

```text
reference_high = max(M1.high inside cycle)
reference_low  = min(M1.low inside cycle)
```

M1 is used because many CGs are not native MetaTrader timeframes.

## Current-cycle exclusion

The current cycle is never a reference for itself.

Only cycles whose end time is less than or equal to the current cycle start are eligible.

## No quality judgment

Phase 02 does not rank references. It does not know whether a nearby or far reference is stronger. It does not know whether one CG is better. It only builds the field.
