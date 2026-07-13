# AGENTS.md — Decision Alpha Lab Engineering Operating Contract

## 1. Authority and Mission

Decision Alpha Lab is an evidence-generation laboratory. The engineering mission is to convert approved market concepts into deterministic, reviewable, replayable, testable, and reversible software without inventing domain truth.

Policy precedence, from highest to lowest:

1. Explicit user/architect decision recorded in an approved specification or ADR.
2. `docs/manifesto.md`, `docs/principles.md`, and active domain doctrine.
3. This `AGENTS.md` and `docs/engineering/ALPHA_LAB_ENGINEERING_HANDBOOK.md`.
4. Experiment-, validation-, execution-, or module-specific contracts.
5. Existing implementation behavior and comments.
6. AI suggestions and generic industry conventions.

A lower authority may not silently override a higher authority. Conflicts must be surfaced, not guessed through.

## 2. Mandatory Engineering Sequence

1. Read the authoritative domain vocabulary, current specification, architecture, affected code, tests, and latest decisions.
2. State current behavior, desired behavior, constraints, non-goals, affected boundaries, facts, assumptions, unknowns, and risks.
3. Define or confirm entities, state, events, transitions, invariants, causal-time semantics, data contracts, failure behavior, and Definition of Done.
4. Propose the smallest safe vertical patch, including files to add, files to modify, files not to touch, migration, rollback, and verification commands.
5. Implement only the approved scope. Preserve unrelated behavior.
6. Compile and run the smallest relevant verification set after every bounded patch.
7. Perform hostile review for leakage, stale state, consumed references, non-determinism, cross-symbol/timeframe errors, schema drift, and hidden execution authority.
8. Deliver a root-relative ZIP patch, installation instructions, exact PowerShell staging commands, detailed commit message, documentation, Obsidian links, and residual-risk report.
9. Persist all durable decisions so the result is understandable without the original conversation.

## 3. Hard Prohibitions

- Do not invent market concepts, definitions, exceptions, filters, or execution rules.
- Do not use future-derived information in live, replay, feature, ranking, or model inputs.
- Do not reuse consumed, invalidated, stale, superseded, or cross-day references unless an approved doctrine explicitly permits it.
- Do not mix research, signal anatomy, decision authority, execution, rendering, persistence, and model promotion without approved boundaries.
- Do not stage unrelated files with `git add .` or `git add -A` in generated installation commands.
- Do not claim completion from compilation alone.
- Do not hide skipped tests, unavailable tools, warnings, assumptions, or unresolved risks.
- Do not broadly rewrite working modules to fix a local defect.
- Do not create persistent IDs, chart-object names, sample IDs, or experiment IDs from unstable randomness.
- Do not allow an AI/model/report to acquire execution authority without a versioned promotion gate and human approval.

## 4. Code Acceptance Rules

Every change must have:

- an identity and owner;
- explicit scope and non-goals;
- preserved invariants;
- deterministic inputs/outputs;
- error and partial-data behavior;
- compatibility and migration notes;
- verification evidence;
- rollback instructions;
- documentation and changelog impact.

Generated code is untrusted until the relevant compiler/runtime/tests have accepted it.

## 5. MQL5 Compatibility Rules

- `StringToUpper` and `StringToLower` mutate a writable string and return `bool`; never use them as string-returning expressions.
- Use `IntegerToString` for integer/long serialization where supported by the target compiler; do not assume `LongToString` exists.
- Validate all `CopyRates`, `CopyBuffer`, `iBarShift`, symbol-selection, history-synchronization, file, chart, and object operations.
- State whether arrays are series-indexed and preserve that convention at every boundary.
- Use closed-bar confirmation unless the approved specification explicitly requires intrabar behavior.
- Use deterministic chart-object IDs and clean them by owned prefix only.
- Draw symbol-local prices only on the matching symbol chart.
- Keep research/anatomy experts free of order placement unless the phase is explicitly an execution phase.

## 6. Research and Data Rules

- Observation → hypothesis → experiment → analysis → validation → production → monitoring → retirement.
- Every dataset has producer, schema version, availability time, timezone, null policy, lineage, and reproducibility metadata.
- Every model comparison uses fixed out-of-sample folds, train-only transformations, a simple baseline, leakage audit, calibration/error analysis, and model cards.
- Rankings, dashboards, shortlists, and models are evidence—not trading permission.

## 7. Required Final Report

- Intent and bounded scope
- Files added/modified and files deliberately untouched
- Algorithmic and architectural changes
- Preserved invariants and data contracts
- Compile/test/replay/visual/schema evidence
- Known limitations, residual risks, and rollback
- Documentation/Obsidian updates
- Exact installation and commit instructions

Canonical handbook: `docs/engineering/ALPHA_LAB_ENGINEERING_HANDBOOK.md`.
