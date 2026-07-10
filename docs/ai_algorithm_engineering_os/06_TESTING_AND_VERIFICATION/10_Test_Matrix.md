---
id: AIEOS-7128DB7ADE
title: "Test Matrix"
type: guide
status: active
domain: verification
version: 1.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - verification
  - guide
---
# Test Matrix

> [!abstract] Purpose
> Map requirements, invariants, risks, environments, and test evidence into one auditable view.

This note belongs to the **06 TESTING AND VERIFICATION** module. Its function is to prove behavior through layered tests, replay, invariants, visual checks, and release gates. The material is normative: when a project deviates from it, the deviation must be recorded as an explicit engineering decision rather than hidden inside implementation code.

## 1. Operating Position

Map requirements, invariants, risks, environments, and test evidence into one auditable view. The objective is not to maximize the amount of generated code. The objective is to reduce ambiguity, preserve domain truth, make changes reversible, and produce evidence that the implementation satisfies the approved intent.

### Core principles

- Treat **Test Matrix** as an explicit engineering contract, not an informal preference.
- Keep coverage traceability and release readiness traceable to project intent, domain rules, and measurable evidence.
- Separate confirmed facts from assumptions, unknowns, and proposed decisions.
- Prefer deterministic, reversible decisions over hidden heuristics and chat-dependent context.
- Preserve existing behavior unless the approved scope explicitly changes it.
- Every critical requirement and invariant must have a test owner and result.

## 2. Required Procedure

1. Collect the minimum authoritative context required for coverage traceability and release readiness.
2. State the current behavior, desired behavior, constraints, non-goals, and affected boundaries.
3. Identify competing interpretations and resolve or register each ambiguity.
4. Produce the required artifact before implementation or release proceeds.
5. Run an adversarial review against invariants, failure modes, and regression risks.
6. Attach verification evidence and update the project knowledge graph.
7. Derive tests from requirements, invariants, transitions, edge cases, and prior incidents.
8. Record exact input, environment, expected result, actual result, and evidence location.

A step may be skipped only when the artifact already exists and is current. “The model probably understands it” is not evidence. Link the existing artifact, identify its version, and state why it is sufficient.

## 3. Required Outputs

- A versioned record of coverage traceability and release readiness.
- A list of assumptions and unresolved questions with owners.
- A verification plan with executable commands or observable outcomes.
- Links to affected specifications, modules, tests, and decisions.
- A requirement-to-test traceability row for each critical behavior.
- Failure diagnostics sufficient to distinguish specification, implementation, and test defects.

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

## 6. AI Interaction Contract

Use AI as an accountable engineering role. Supply the current specification, relevant files, constraints, non-goals, and verification commands. Require the model to separate facts, assumptions, unknowns, and recommendations. Do not accept a code patch that cannot explain which invariant it preserves and how the change will be verified.

### Reusable prompt

```text
Create a verification plan for coverage traceability and release readiness. Include normal, boundary, invalid, duplicate, missing, reordered, restart, replay, scale, and regression cases. For each test specify setup, event sequence, expected state, expected output, failure signal, and evidence.
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

- [[03_ALGORITHM_DESIGN/04_Invariants|Invariants]]
- [[15_CHECKLISTS/04_Test_Readiness|Test Readiness]]
