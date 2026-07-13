---
id: AIEOS-28CE141E11
title: "Evidence, Assumptions, and Unknowns"
type: guide
status: active
domain: foundations
version: 1.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - foundations
  - guide
---
# Evidence, Assumptions, and Unknowns

> [!abstract] Purpose
> Force every engineering claim into an explicit epistemic category.

This note belongs to the **01 FOUNDATIONS** module. Its function is to establish the principles that prevent fast AI-assisted development from becoming uncontrolled code generation. The material is normative: when a project deviates from it, the deviation must be recorded as an explicit engineering decision rather than hidden inside implementation code.

## 1. Operating Position

Force every engineering claim into an explicit epistemic category. The objective is not to maximize the amount of generated code. The objective is to reduce ambiguity, preserve domain truth, make changes reversible, and produce evidence that the implementation satisfies the approved intent.

### Core principles

- Treat **Evidence, Assumptions, and Unknowns** as an explicit engineering contract, not an informal preference.
- Keep the distinction between verified facts, assumptions, unknowns, and decisions traceable to project intent, domain rules, and measurable evidence.
- Separate confirmed facts from assumptions, unknowns, and proposed decisions.
- Prefer deterministic, reversible decisions over hidden heuristics and chat-dependent context.
- Preserve existing behavior unless the approved scope explicitly changes it.
- Never let a recommendation masquerade as an observed fact.

## 2. Required Procedure

1. Collect the minimum authoritative context required for the distinction between verified facts, assumptions, unknowns, and decisions.
2. State the current behavior, desired behavior, constraints, non-goals, and affected boundaries.
3. Identify competing interpretations and resolve or register each ambiguity.
4. Produce the required artifact before implementation or release proceeds.
5. Run an adversarial review against invariants, failure modes, and regression risks.
6. Attach verification evidence and update the project knowledge graph.
7. Classify the decision as human-owned, AI-proposed, or mechanically verifiable.

A step may be skipped only when the artifact already exists and is current. “The model probably understands it” is not evidence. Link the existing artifact, identify its version, and state why it is sufficient.

## 3. Required Outputs

- A versioned record of the distinction between verified facts, assumptions, unknowns, and decisions.
- A list of assumptions and unresolved questions with owners.
- A verification plan with executable commands or observable outcomes.
- Links to affected specifications, modules, tests, and decisions.

Each output must have an owner, status, and review path. Generated prose without a decision, contract, test, or next action is not considered an engineering output.

## 4. Quality Gates

- The intent and boundaries can be restated consistently by a reviewer.
- No critical term depends on undocumented conversational context.
- Every mandatory behavior has at least one verification method.
- Regression scope and rollback path are explicit.
- The artifact is linked from the relevant MOC, feature packet, or patch manifest.
- Authority and evidence requirements are proportional to failure cost.

A gate is binary. If the evidence is incomplete, status remains **not ready**. Avoid converting uncertainty into optimistic wording.

## 5. Failure Modes and Countermeasures

- **Vague approval:** “looks good” replaces evidence. Countermeasure: require binary gates and linked outputs.
- **Scope leakage:** unrelated cleanup enters the change. Countermeasure: enforce files-to-touch and non-goals.
- **Ontology drift:** AI substitutes familiar concepts. Countermeasure: use the project dictionary and reject undefined terms.
- **Chat dependency:** decisions exist only in conversation. Countermeasure: persist them in the vault before coding.
- **False completion:** code compiles but behavior is unverified. Countermeasure: define Done as evidence, not compilation.

## 6. AI Interaction Contract

Use AI as an accountable engineering role. Supply the current specification, relevant files, constraints, non-goals, and verification commands. Require the model to separate facts, assumptions, unknowns, and recommendations. Do not accept a code patch that cannot explain which invariant it preserves and how the change will be verified.

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

- [[00_START_HERE/02_Operating_Principles|Operating Principles]]
- [[17_GOVERNANCE/01_Hard_Rules|Hard Rules]]
