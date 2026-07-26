---
id: AIEOS-A1EB4B6C12
title: "Engineering Maturity Model"
type: guide
status: active
domain: governance
version: 1.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - governance
  - guide
---
# Engineering Maturity Model

> [!abstract] Purpose
> Provide a staged roadmap from prompt-driven coding to governed AI engineering.

This note belongs to the **17 GOVERNANCE** module. Its function is to control quality, authority, exceptions, metrics, and maturity across the engineering system. The material is normative: when a project deviates from it, the deviation must be recorded as an explicit engineering decision rather than hidden inside implementation code.

## 1. Operating Position

Provide a staged roadmap from prompt-driven coding to governed AI engineering. The objective is not to maximize the amount of generated code. The objective is to reduce ambiguity, preserve domain truth, make changes reversible, and produce evidence that the implementation satisfies the approved intent.

### Core principles

- Treat **Engineering Maturity Model** as an explicit engineering contract, not an informal preference.
- Keep capability progression traceable to project intent, domain rules, and measurable evidence.
- Separate confirmed facts from assumptions, unknowns, and proposed decisions.
- Prefer deterministic, reversible decisions over hidden heuristics and chat-dependent context.
- Preserve existing behavior unless the approved scope explicitly changes it.
- Advance only when the prior level is habitual and evidenced.

## 2. Required Procedure

1. Collect the minimum authoritative context required for capability progression.
2. State the current behavior, desired behavior, constraints, non-goals, and affected boundaries.
3. Identify competing interpretations and resolve or register each ambiguity.
4. Produce the required artifact before implementation or release proceeds.
5. Run an adversarial review against invariants, failure modes, and regression risks.
6. Attach verification evidence and update the project knowledge graph.

A step may be skipped only when the artifact already exists and is current. “The model probably understands it” is not evidence. Link the existing artifact, identify its version, and state why it is sufficient.

## 3. Required Outputs

- A versioned record of capability progression.
- A list of assumptions and unresolved questions with owners.
- A verification plan with executable commands or observable outcomes.
- Links to affected specifications, modules, tests, and decisions.
- A named approver or owner for every exception and gate result.

Each output must have an owner, status, and review path. Generated prose without a decision, contract, test, or next action is not considered an engineering output.

## 4. Quality Gates

- The intent and boundaries can be restated consistently by a reviewer.
- No critical term depends on undocumented conversational context.
- Every mandatory behavior has at least one verification method.
- Regression scope and rollback path are explicit.
- The artifact is linked from the relevant MOC, feature packet, or patch manifest.
- Exceptions include scope, rationale, risk, expiration, and verification.

A gate is binary. If the evidence is incomplete, status remains **not ready**. Avoid converting uncertainty into optimistic wording.

## 5. Failure Modes and Countermeasures

- **Vague approval:** “looks good” replaces evidence. Countermeasure: require binary gates and linked outputs.
- **Scope leakage:** unrelated cleanup enters the change. Countermeasure: enforce files-to-touch and non-goals.
- **Ontology drift:** AI substitutes familiar concepts. Countermeasure: use the project dictionary and reject undefined terms.
- **Chat dependency:** decisions exist only in conversation. Countermeasure: persist them in the vault before coding.
- **False completion:** code compiles but behavior is unverified. Countermeasure: define Done as evidence, not compilation.

## 6. Concrete Examples

### Level 0 — Prompt Coding

AI generates code from informal requests; little traceability.

### Level 1 — Bounded Tasks

Context, scope, compile, and manual checks are explicit.

### Level 2 — Specification First

Formal specs, invariants, patch manifests, and test matrices exist.

### Level 3 — Role-Based AI

Architect, builder, reviewer, tester, and documenter protocols operate.

### Level 4 — Governed Delivery

Quality gates, metrics, versioning, rollback, and knowledge validation are systematic.

### Level 5 — Self-Improving System

Incidents, prompt performance, test gaps, and architecture signals continuously improve the operating system.


## 7. AI Interaction Contract

Use AI as an accountable engineering role. Supply the current specification, relevant files, constraints, non-goals, and verification commands. Require the model to separate facts, assumptions, unknowns, and recommendations. Do not accept a code patch that cannot explain which invariant it preserves and how the change will be verified.

## 8. Review Questions

- What ambiguity would cause two competent engineers to implement different behavior?
- Which invariant or contract is most likely to be violated?
- What evidence proves the change works in both normal and adverse conditions?
- What existing behavior could regress?
- Is the result understandable without the original chat history?
- Can the work be rolled back or reconstructed deterministically?

## 9. Completion Record

Record the decision, linked artifacts, reviewer, unresolved risks, and next checkpoint in the project decision log. Update `updated` in frontmatter when the normative content changes.

## Related Notes

- [[01_FOUNDATIONS/07_Definition_of_Done|Definition of Done Foundation]]
- [[15_CHECKLISTS/_MOC|Checklists]]
