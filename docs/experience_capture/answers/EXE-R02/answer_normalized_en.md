# EXE-R02 — Normalized Interpretation

## Core Claim

Broker validation and send-gate rules are mechanical.

They are not part of the native NDS decision ontology.

Their rules are clear and deterministic.

Recommended canonical rule:

```text
BrokerValidator = Mechanical Constraint Checker
```

The broker validator should not reinterpret the market, rank scenarios, select zones, or change NDS structural reasoning.

It should only check whether an already-created ExecutionIntent is mechanically valid for broker submission.

## Separation of Responsibilities

NDS responsibility:

```text
create quality-gated ExecutionIntentCandidate from NDS anatomy
```

Broker Validator responsibility:

```text
check broker mechanical constraints
normalize executable parameters
approve, adjust mechanically, or veto
```

The validator is not an AI policy layer.

It is not a scenario layer.

It is not a zone layer.

It is not an entry-selection layer.

It is a mechanical send gate.

## Deterministic Constraint Layer

The broker validator should handle deterministic broker-side constraints such as:

```text
tick size
digits
volume step
min lot
max lot
minimum stop distance
freeze level
trade mode
market session
margin availability
spread constraints
symbol execution mode
order filling mode
order expiration support
```

These are not discretionary.

They should be implemented as explicit checks.

## Mechanical Adjust vs Veto

Some constraints may allow mechanical adjustment.

Examples:

```text
normalize price to tick size
normalize volume to lot step
split volume if max lot is exceeded
round structural price to executable price when safe
```

Other constraints should veto.

Examples:

```text
stop is invalid after broker constraints
margin is insufficient and volume cannot be safely adjusted
symbol trading is disabled
market is closed
spread is outside allowed limits
freeze level prevents modification
required order type is not supported
```

The exact adjust/veto policy is mechanical and should be encoded explicitly.

## No NDS Reasoning Mutation

The broker validator must not mutate the NDS reason.

If a mechanical adjustment changes the structural meaning of the trade, the intent should be vetoed or returned for regeneration.

Suggested rule:

```text
Mechanical adjustment is allowed only if NDS structural meaning remains intact.
```

If adjustment breaks the intended structural entry, stop, or risk geometry:

```text
VETO_MECHANICAL_ADJUSTMENT_BREAKS_NDS_STRUCTURE
```

## Audit Requirement

Even though the rules are mechanical, the validator must still audit every decision.

Every validation should record:

```text
input intent
broker constraints snapshot
normalization performed
adjustments performed
veto reasons
final validated request
```

This supports reconciliation later.

## Send Gate

The Send Gate is the final mechanical boundary before any broker request.

Suggested state:

```text
SEND_GATE_APPROVED
SEND_GATE_ADJUSTED
SEND_GATE_VETOED
```

A broker request can only be created after:

```text
NDS intent exists
safety gate passes
broker validator passes
send gate approves
```

## Machine-Readable Summary

```text
broker_constraints = mechanical
rules = clear / deterministic

validator does:
    - tick/digits normalization
    - volume step checks
    - min/max lot checks
    - minimum stop checks
    - margin checks
    - spread checks
    - freeze/trade/session checks
    - approve / mechanical adjust / veto

validator does not:
    - change scenario logic
    - choose zone
    - choose entry
    - train NDS anatomy
    - reinterpret market structure
```

## Short Formal Statement

In NDS, broker validation and send-gate handling are mechanical execution constraints with clear deterministic rules. They do not belong to scenario, zone, entry, or AI reasoning. The broker validator should only check whether an ExecutionIntentCandidate is mechanically valid for the broker, normalize prices and volumes when safe, split or adjust only when structural meaning is preserved, and veto when broker constraints would make the intent unsafe or structurally invalid.
