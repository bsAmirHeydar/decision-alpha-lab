---
id: AIEOS-421F52FAF2
title: "MQL5 Patch Checklist"
type: guide
status: active
domain: mql5
version: 1.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - mql5
  - guide
---
# MQL5 Patch Checklist

> [!abstract] Purpose
> Apply a mandatory pre-delivery control set to every MQL5 patch.

This note belongs to the **11 MQL5 SPECIALIZATION** module. Its function is to apply the operating system to stateful, chart-driven, event-based MQL5 indicators and experts. The material is normative: when a project deviates from it, the deviation must be recorded as an explicit engineering decision rather than hidden inside implementation code.

## 1. Operating Position

Apply a mandatory pre-delivery control set to every MQL5 patch. The objective is not to maximize the amount of generated code. The objective is to reduce ambiguity, preserve domain truth, make changes reversible, and produce evidence that the implementation satisfies the approved intent.

### Core principles

- Treat **MQL5 Patch Checklist** as an explicit engineering contract, not an informal preference.
- Keep compilation, lifecycle, state, objects, performance, compatibility, and packaging traceable to project intent, domain rules, and measurable evidence.
- Separate confirmed facts from assumptions, unknowns, and proposed decisions.
- Prefer deterministic, reversible decisions over hidden heuristics and chat-dependent context.
- Preserve existing behavior unless the approved scope explicitly changes it.
- Zero compile errors is a gate; zero warnings is preferred and exceptions require rationale.

## 2. Required Procedure

1. Collect the minimum authoritative context required for compilation, lifecycle, state, objects, performance, compatibility, and packaging.
2. State the current behavior, desired behavior, constraints, non-goals, and affected boundaries.
3. Identify competing interpretations and resolve or register each ambiguity.
4. Produce the required artifact before implementation or release proceeds.
5. Run an adversarial review against invariants, failure modes, and regression risks.
6. Attach verification evidence and update the project knowledge graph.
7. Verify behavior on initial attach, history expansion, new tick, new bar, timeframe change, symbol change, parameter change, recompile, and removal.

A step may be skipped only when the artifact already exists and is current. “The model probably understands it” is not evidence. Link the existing artifact, identify its version, and state why it is sufficient.

## 3. Required Outputs

- A versioned record of compilation, lifecycle, state, objects, performance, compatibility, and packaging.
- A list of assumptions and unresolved questions with owners.
- A verification plan with executable commands or observable outcomes.
- Links to affected specifications, modules, tests, and decisions.
- A callback and state-lifecycle map.
- A chart-object inventory or buffer contract where applicable.

Each output must have an owner, status, and review path. Generated prose without a decision, contract, test, or next action is not considered an engineering output.

## 4. Quality Gates

- The intent and boundaries can be restated consistently by a reviewer.
- No critical term depends on undocumented conversational context.
- Every mandatory behavior has at least one verification method.
- Regression scope and rollback path are explicit.
- The artifact is linked from the relevant MOC, feature packet, or patch manifest.
- The same data sequence produces the same semantic state after reload.

A gate is binary. If the evidence is incomplete, status remains **not ready**. Avoid converting uncertainty into optimistic wording.

## 5. Failure Modes and Countermeasures

- **Vague approval:** “looks good” replaces evidence. Countermeasure: require binary gates and linked outputs.
- **Scope leakage:** unrelated cleanup enters the change. Countermeasure: enforce files-to-touch and non-goals.
- **Ontology drift:** AI substitutes familiar concepts. Countermeasure: use the project dictionary and reject undefined terms.
- **Chat dependency:** decisions exist only in conversation. Countermeasure: persist them in the vault before coding.
- **False completion:** code compiles but behavior is unverified. Countermeasure: define Done as evidence, not compilation.

## 6. AI Interaction Contract

Use AI as an accountable engineering role. Supply the current specification, relevant files, constraints, non-goals, and verification commands. Require the model to separate facts, assumptions, unknowns, and recommendations. Do not accept a code patch that cannot explain which invariant it preserves and how the change will be verified.

### Reusable prompt

```text
Review this MQL5 task for compilation, lifecycle, state, objects, performance, compatibility, and packaging. Inspect callback lifecycle, series indexing, history readiness, persistent state, object IDs, cleanup, recalculation, performance, and terminal-specific errors. Produce a minimal patch and a Strategy Tester plus manual chart verification matrix.
```

## 7. Review Questions

- What ambiguity would cause two competent engineers to implement different behavior?
- Which invariant or contract is most likely to be violated?
- What evidence proves the change works in both normal and adverse conditions?
- What existing behavior could regress?
- Is the result understandable without the original chat history?
- Can the work be rolled back or reconstructed deterministically?

## 8. Completion Record

Record the decision, linked artifacts, reviewer, unresolved risks, and next checkpoint in the project decision log. Update `updated` in frontmatter when the normative content changes.

## Related Notes

- [[04_ARCHITECTURE/04_Core_State_Signal_Renderer|Core-State-Signal-Renderer]]
- [[12_QUANT_TRADING_ALGORITHMS/07_Backtest_Live_Parity|Backtest/Live Parity]]
