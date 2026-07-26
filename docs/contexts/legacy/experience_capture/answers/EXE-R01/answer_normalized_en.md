# EXE-R01 — Normalized Interpretation

## Core Claim

The detailed field-level contract for ExecutionIntent is not fully known yet.

However, the upstream decision logic is known:

```text
Fractal Four-State View
→ Context
→ Zone
→ Entry
→ Quality-Based Trade Decision
→ ExecutionIntent Candidate
```

ExecutionIntent should therefore not be treated as a raw order request.

It is the final structured expression of a fractal NDS decision pipeline.

## Unknown Field-Level Contract

The user explicitly states that the detailed fields are not known.

This must be preserved honestly.

The following should remain open:

```text
exact required fields
exact structural price fields
exact adjusted price fields
exact spread adjustment representation
exact stop buffer representation
exact split intent structure
exact cancel/replace/missed encoding
exact unsafe intent taxonomy
```

These should not be over-specified prematurely.

## Known Decision Pipeline

The known part is architectural.

The system begins from the four-state view established in BASE records:

```text
bullish + Hook
bullish + Rally
bearish + Hook
bearish + Rally
```

This view is not read once at a single timeframe.

It is read fractally.

The four-state view becomes decision structure across:

```text
context
zone
entry
```

Then trade decisions are made based on the quality of those layers.

## Fractal Four-State View

The four-state view should be evaluated across scales.

Suggested interpretation:

```text
higher scale four-state view → context
middle scale four-state view → zone
entry scale four-state view → entry
```

This is not necessarily a fixed timeframe mapping.

It is a fractal role mapping.

The same native NDS logic can appear at different roles depending on scale and structural relation.

## Context, Zone, Entry Conversion

The system should convert the four-state/fractal analysis into three decision layers:

```text
Context Layer:
    What structural situation are we in?

Zone Layer:
    Where is the structural situation exploitable with lower cost and larger potential?

Entry Layer:
    Where is the precise cost-compressed entry point?
```

ExecutionIntent should be created only after these layers produce sufficient quality.

## Quality-Based Trade Decision

The final trade decision should be based on qualities.

Suggested quality layers:

```text
context_quality
zone_quality
entry_quality
aggregate_quality
```

This connects directly to earlier records:

```text
RSK-R01: risk cost at context, zone, and entry levels
RSK-R02: optionality at context, zone, and entry levels
SCN-R02: context → position → constraint → zone → entry
ENT-R01: Entry-Level Extreme as cost compression
```

ExecutionIntent should be quality-gated.

## ExecutionIntent as Candidate, Not Order

NDS should produce an intent candidate, not a broker order.

Recommended boundary:

```text
ExecutionIntentCandidate
```

The intent expresses:

```text
this scenario/zone/entry combination is tradeable according to NDS quality logic
```

It does not itself mean that the trade must be sent.

Final validation belongs to:

```text
Broker Validator
Safety Gate
Execution Validator
```

## Minimum Known Contract

The exact full field set is unknown, but based on all prior records, the minimal lineage should likely include:

```text
scenario_id
zone_id
entry_extreme_id
reason_set_id
context_quality
zone_quality
entry_quality
aggregate_quality
```

Other fields should be developed later when the execution contract is formalized.

## Intent Creation Logic

The intent should be created only when:

```text
context quality is acceptable
zone quality is acceptable
entry quality is acceptable
aggregate optionality is acceptable
risk-to-reward quality is acceptable
the decision is explainable through NDS anatomy
```

If these are not satisfied:

```text
no ExecutionIntent should be created
```

## Machine-Readable Summary

```text
known:
    - four-state view is fractal
    - fractal view becomes context, zone, and entry
    - trade decisions are based on qualities at those layers

unknown:
    - exact full ExecutionIntent field contract
    - exact adjusted/structural price representation
    - exact split/cancel/replace/missed fields

boundary:
    - ExecutionIntent is not direct order sending
    - it is a quality-gated NDS intent candidate
```

## Short Formal Statement

In NDS, the detailed ExecutionIntent contract is not fully known yet, but its upstream logic is known. The four-state view is evaluated fractally and becomes the context, zone, and entry layers. Trade decisions are then made according to the quality of those layers. ExecutionIntent should therefore be a quality-gated NDS intent candidate produced after context, zone, and entry pass their structural quality checks, not a direct broker order and not a raw price instruction.
