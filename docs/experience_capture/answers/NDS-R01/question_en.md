# NDS-R01 — Canonical NDS Object Model

## Question

Define the canonical NDS object model.

## Why This Question Remains

The answered records define ontology boundaries, but the exact object model is still open.

## Answer Requirements

- Define every core NDS object that must exist in v1: Hook, Rally, F-count, Node, Cycle, Scenario, Zone, Destination, Invalidation, Entry Family, and ExecutionIntent.
- For each object, specify required fields, optional fields, and forbidden fields.
- Separate deterministic anatomy objects from learnable policy objects.
- Define which objects can be nested across parent/current/child scales.
- Define which objects must be drawn on chart for audit.
- Define how every object should receive a stable ID.

## Expected Output

```text
canonical_state_packet_v1
nds_object_model_v1
```
