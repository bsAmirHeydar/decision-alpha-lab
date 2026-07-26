---
id: AIEOS-D99BEC738A
title: "Visual Bug Workflow"
type: workflow
status: active
domain: workflow
version: 1.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - workflow
  - workflow
---
# Visual Bug Workflow

> [!abstract] Purpose
> Trace a visual defect from domain state through mapping and object lifecycle.

This note belongs to the **13 WORKFLOWS** module. Its function is to define end-to-end runbooks for recurring engineering situations. The material is normative: when a project deviates from it, the deviation must be recorded as an explicit engineering decision rather than hidden inside implementation code.

## 1. Operating Position

Trace a visual defect from domain state through mapping and object lifecycle. The objective is not to maximize the amount of generated code. The objective is to reduce ambiguity, preserve domain truth, make changes reversible, and produce evidence that the implementation satisfies the approved intent.

### Core principles

- Treat **Visual Bug Workflow** as an explicit engineering contract, not an informal preference.
- Keep state-to-renderer diagnosis traceable to project intent, domain rules, and measurable evidence.
- Separate confirmed facts from assumptions, unknowns, and proposed decisions.
- Prefer deterministic, reversible decisions over hidden heuristics and chat-dependent context.
- Preserve existing behavior unless the approved scope explicitly changes it.

## 2. Required Procedure

1. Record expected state independently from expected appearance.
2. Inventory expected and actual objects/buffers with IDs and coordinates.
3. Test zoom, scroll, reload, history extension, symbol, timeframe, and parameter changes.
4. Patch the earliest divergence: detection, state, mapping, creation, update, deletion, or redraw.
5. Update all linked artifacts and close with a decision record.

A step may be skipped only when the artifact already exists and is current. “The model probably understands it” is not evidence. Link the existing artifact, identify its version, and state why it is sufficient.

## 3. Required Outputs

- A versioned record of state-to-renderer diagnosis.
- A list of assumptions and unresolved questions with owners.
- A verification plan with executable commands or observable outcomes.
- Links to affected specifications, modules, tests, and decisions.
- A workflow packet containing specification, implementation, verification, review, release, and knowledge evidence.

Each output must have an owner, status, and review path. Generated prose without a decision, contract, test, or next action is not considered an engineering output.

## 4. Quality Gates

- The intent and boundaries can be restated consistently by a reviewer.
- No critical term depends on undocumented conversational context.
- Every mandatory behavior has at least one verification method.
- Regression scope and rollback path are explicit.
- The artifact is linked from the relevant MOC, feature packet, or patch manifest.
- Every phase exit criterion is recorded before the next phase begins.

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
Execute the Visual Bug Workflow. Do not skip directly to coding. At each phase produce the required artifact, list unresolved risks, and stop on failed gates. Use repository evidence and report all tool results honestly.
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

- [[15_CHECKLISTS/01_Master_Feature_Checklist|Master Feature Checklist]]
- [[09_PATCH_RELEASE_GIT/01_Patch_Identity|Patch Identity]]
