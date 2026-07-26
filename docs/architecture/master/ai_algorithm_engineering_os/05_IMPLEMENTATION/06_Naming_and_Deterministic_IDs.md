---
id: AIEOS-7BD9B5204E
title: "Naming and Deterministic IDs"
type: guide
status: active
domain: implementation
version: 1.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - implementation
  - guide
---
# Naming and Deterministic IDs

> [!abstract] Purpose
> Use names and identifiers that encode stable domain identity and prevent duplicate side effects.

This note belongs to the **05 IMPLEMENTATION** module. Its function is to translate approved specifications into small, reversible, reviewable code changes. The material is normative: when a project deviates from it, the deviation must be recorded as an explicit engineering decision rather than hidden inside implementation code.

## 1. Operating Position

Use names and identifiers that encode stable domain identity and prevent duplicate side effects. The objective is not to maximize the amount of generated code. The objective is to reduce ambiguity, preserve domain truth, make changes reversible, and produce evidence that the implementation satisfies the approved intent.

### Core principles

- Treat **Naming and Deterministic IDs** as an explicit engineering contract, not an informal preference.
- Keep semantic naming, stable keys, namespaces, and lifecycle traceable to project intent, domain rules, and measurable evidence.
- Separate confirmed facts from assumptions, unknowns, and proposed decisions.
- Prefer deterministic, reversible decisions over hidden heuristics and chat-dependent context.
- Preserve existing behavior unless the approved scope explicitly changes it.
- Persistent or visual objects must derive identity from immutable domain keys.

## 2. Required Procedure

1. Collect the minimum authoritative context required for semantic naming, stable keys, namespaces, and lifecycle.
2. State the current behavior, desired behavior, constraints, non-goals, and affected boundaries.
3. Identify competing interpretations and resolve or register each ambiguity.
4. Produce the required artifact before implementation or release proceeds.
5. Run an adversarial review against invariants, failure modes, and regression risks.
6. Attach verification evidence and update the project knowledge graph.
7. Inspect the exact existing implementation before proposing edits.
8. After each patch, rebuild and run the smallest relevant verification set before continuing.

A step may be skipped only when the artifact already exists and is current. “The model probably understands it” is not evidence. Link the existing artifact, identify its version, and state why it is sufficient.

## 3. Required Outputs

- A versioned record of semantic naming, stable keys, namespaces, and lifecycle.
- A list of assumptions and unresolved questions with owners.
- A verification plan with executable commands or observable outcomes.
- Links to affected specifications, modules, tests, and decisions.
- A file-level change map describing additions, modifications, and deliberately untouched areas.

Each output must have an owner, status, and review path. Generated prose without a decision, contract, test, or next action is not considered an engineering output.

## 4. Quality Gates

- The intent and boundaries can be restated consistently by a reviewer.
- No critical term depends on undocumented conversational context.
- Every mandatory behavior has at least one verification method.
- Regression scope and rollback path are explicit.
- The artifact is linked from the relevant MOC, feature packet, or patch manifest.

A gate is binary. If the evidence is incomplete, status remains **not ready**. Avoid converting uncertainty into optimistic wording.

## 5. Failure Modes and Countermeasures

- **Vague approval:** “looks good” replaces evidence. Countermeasure: require binary gates and linked outputs.
- **Scope leakage:** unrelated cleanup enters the change. Countermeasure: enforce files-to-touch and non-goals.
- **Ontology drift:** AI substitutes familiar concepts. Countermeasure: use the project dictionary and reject undefined terms.
- **Chat dependency:** decisions exist only in conversation. Countermeasure: persist them in the vault before coding.
- **False completion:** code compiles but behavior is unverified. Countermeasure: define Done as evidence, not compilation.
- **Patch accumulation without consolidation:** duplicate helpers and stale paths remain. Countermeasure: schedule explicit stabilization after vertical slices.

## 6. AI Interaction Contract

Use AI as an accountable engineering role. Supply the current specification, relevant files, constraints, non-goals, and verification commands. Require the model to separate facts, assumptions, unknowns, and recommendations. Do not accept a code patch that cannot explain which invariant it preserves and how the change will be verified.

### Reusable prompt

```text
Implement only the approved scope for naming and deterministic ids. First inspect the relevant files and contracts. State assumptions, files to modify, files not to modify, preserved invariants, risks, and verification commands. Produce the smallest safe patch; do not rewrite unrelated code.
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

- [[09_PATCH_RELEASE_GIT/02_Patch_Manifest|Patch Manifest]]
- [[06_TESTING_AND_VERIFICATION/01_Test_Strategy|Test Strategy]]
