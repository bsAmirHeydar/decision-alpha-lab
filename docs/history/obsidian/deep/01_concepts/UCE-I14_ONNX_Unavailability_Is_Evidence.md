---
title: "ONNX Unavailability Is Evidence"
tags: [uce-i14, immutable-runtime, concept]
status: canonical
---
# ONNX Unavailability Is Evidence

## Claim

Missing ONNX dependencies must be recorded explicitly rather than hidden by a fake export.

## Why it matters

Runtime failures often occur when operational convenience is allowed to alter semantic identity. UCE-I14 treats this claim as a non-negotiable invariant and attaches executable refusal tests to it.

## Consequences

- The owning field is included in canonical serialization.
- A mutation changes an owning hash or invalidates a certificate.
- Downstream consumers receive a closed contract rather than prose defaults.
- Failure remains visible in the evidence trail.
- No performance score can compensate for a critical integrity failure.

## Evidence

See [[../../strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i14/00_UCE_I14_DELIVERY_MOC|UCE-I14 Delivery MOC]] and the phase test suite.
