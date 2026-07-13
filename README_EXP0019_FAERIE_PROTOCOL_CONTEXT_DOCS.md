# EXP0019 Faerie Protocol Contextual Divergence - Documentation Freeze v2.0.0

This patch is a full English, implementation-oriented Obsidian specification for the Faerie Protocol contextual-divergence family. It incorporates the owner's fifteen questionnaire responses, freezes fourteen decisions, leaves only quota-consumption timing open, and expands the architecture from a descriptive draft into a normative rulebook.

## Major changes

- Entire core documentation rewritten in English and expanded.
- Owner answer mapping with exact option text and machine-readable policies.
- Calendar-day N lookback, protected-touch reuse, strict same-session confirmation, M1-only first sweep, host-chart confirmation, New York week, WW neutralization/tradeability/recency, pair-global first-entry arbitration, SELL spread adjustment, and always-visible suppressed drawings frozen.
- Quota consumption explained and isolated as the only open live-execution decision.
- New formal algorithm, relation rulebook, edge-case catalog, reason/style registry, state-machine contract, manifest v2, formal invariants, ADRs, test obligations, and code-readiness gate.

## Start here

`docs/execution/EXP0019_faerie_protocol_contextual_divergence/00_EXP0019_MOC.md`

## Live execution status

Detection, drawing, replay, paper planning, WW gating, arbitration, and risk geometry are implementation-ready. Canonical live order submission remains disabled until `FP-DEC-012` is answered.
