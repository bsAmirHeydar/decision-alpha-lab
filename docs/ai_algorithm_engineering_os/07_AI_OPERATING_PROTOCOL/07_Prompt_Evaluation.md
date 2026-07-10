---
id: AIEOS-44BD43459F
title: "Prompt Evaluation"
type: guide
status: active
domain: ai-protocol
version: 1.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - ai-protocol
  - guide
---
# Prompt Evaluation

> [!abstract] Purpose
> Treat prompts as engineering assets measured by output quality, consistency, and failure patterns.

This note belongs to the **07 AI OPERATING PROTOCOL** module. Its function is to orchestrate AI agents as disciplined engineering roles with controlled context and evidence requirements. The material is normative: when a project deviates from it, the deviation must be recorded as an explicit engineering decision rather than hidden inside implementation code.

## 1. Operating Position

Treat prompts as engineering assets measured by output quality, consistency, and failure patterns. The objective is not to maximize the amount of generated code. The objective is to reduce ambiguity, preserve domain truth, make changes reversible, and produce evidence that the implementation satisfies the approved intent.

### Core principles

- Treat **Prompt Evaluation** as an explicit engineering contract, not an informal preference.
- Keep test cases, rubrics, versioning, and regressions for prompts traceable to project intent, domain rules, and measurable evidence.
- Separate confirmed facts from assumptions, unknowns, and proposed decisions.
- Prefer deterministic, reversible decisions over hidden heuristics and chat-dependent context.
- Preserve existing behavior unless the approved scope explicitly changes it.
- A prompt is not good because one output looked impressive.

## 2. Required Procedure

1. Collect the minimum authoritative context required for test cases, rubrics, versioning, and regressions for prompts.
2. State the current behavior, desired behavior, constraints, non-goals, and affected boundaries.
3. Identify competing interpretations and resolve or register each ambiguity.
4. Produce the required artifact before implementation or release proceeds.
5. Run an adversarial review against invariants, failure modes, and regression risks.
6. Attach verification evidence and update the project knowledge graph.
7. Assign the AI a named role and explicit authority boundary.
8. Require an output schema and stop condition before execution.
9. Run a separate acceptance review against repository evidence.

A step may be skipped only when the artifact already exists and is current. “The model probably understands it” is not evidence. Link the existing artifact, identify its version, and state why it is sufficient.

## 3. Required Outputs

- A versioned record of test cases, rubrics, versioning, and regressions for prompts.
- A list of assumptions and unresolved questions with owners.
- A verification plan with executable commands or observable outcomes.
- Links to affected specifications, modules, tests, and decisions.
- A role-tagged transcript summary containing decisions, assumptions, and evidence—not hidden chain-of-thought.

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
- **Authority confusion:** recommendation is treated as approval. Countermeasure: name the human decision owner.

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

- [[08_PROMPT_LIBRARY/_MOC|Prompt Library]]
- [[14_TEMPLATES/12_AI_Context_Packet_Template|AI Context Packet]]
