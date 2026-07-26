---
title: ADR 013 — Advanced Models Preserve Simple Fallbacks
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- adr
- governance
---

# Status

**Accepted**

# Context

SAED V4 deliberately evaluates frontier AI while preserving UCEE truth, evidence, risk and runtime authority. Without an architectural decision, research convenience can become de facto production authority.

# Decision

Every advanced representation, graph, mixture, causal, world or policy model must retain a simpler admitted fallback: manual policy, calibrated classical model, Skip or Abstain. Complexity is removable without corrupting state or evidence.

# Consequences

- Capability tier and permitted uses are machine-readable.
- Violations are boundary failures, not documentation issues.
- Promotion dossiers must show compliance and fallback behavior.
- Runtime bundles cannot exceed admitted support or authority.
- Future exceptions require a new ADR, compatibility review and signed model-risk approval.

# Rejected alternatives

- Direct end-to-end autonomous trading from a frontier model.
- Silent online adaptation.
- Synthetic or benchmark performance as production evidence.
- Human-readable policy without executable enforcement.

# Verification

- Schema and boundary tests.
- Negative authorization tests.
- Adversarial challenge and rollback test.
- Dossier and runtime-handoff review.

# Related

- [[Capability_Tier_Policy]]
- [[Multi_Agent_Authority_Matrix]]
- [[Model_Risk_Security_And_Supply_Chain]]
- [[Release_And_Production_Qualification]]
