# Phase 48 — Post-F3 Hook Recognition Doctrine

## Status

Canonical doctrine update. Documentation-only.

## Problem observed on chart

The F3 itself can be detected correctly, but the `F3H` label can be attached to the wrong Hook candidate.

This means the issue is not necessarily the F3 detector. The issue is the **post-F3 Hook recognition contract**.

Before this doctrine, the system treated the phrase "Hook after F3" too narrowly or too loosely:

- too narrowly: only a structural Hook beginning exactly at the F3 terminal endpoint is considered;
- too loosely: later structural sequences can be marked as `F3H` even if they are not the intended post-F3 Hook.

The Canon must support both direct and delayed post-F3 Hook formation.

---

# 1. Canonical terms

## Opposing F3

An F3 creates a directional terminal environment.

A valid post-F3 Hook must be **opposite** to the F3 direction.

Examples:

- bullish/up F3 environment → bearish/negative Hook candidate
- bearish/down F3 environment → bullish/positive Hook candidate

The exact direction enum may differ inside code, but the conceptual rule is fixed: **the Hook is the opposing cycle after the F3 terminal side is reached**.

## F3 terminal side

The F3 terminal side is the final side of the F3 movement from which the opposite Hook can begin or from which price can rebound before forming the delayed Hook.

Preferred implementation priority:

1. explicit F3 extension/terminal endpoint, if available;
2. confirmed F3 endpoint node;
3. final leg endpoint of the F3;
4. nearest canonical F3 terminal-side node when the above are not available.

## Post-F3 ownership window

A post-F3 Hook must be owned by the F3 that created its environment.

The F3 does **not** validate every later Hook indefinitely.

The search window begins at the F3 terminal side and ends at the first of:

- a new opposing major structure that supersedes the F3 context;
- a new F3 terminal context;
- explicit chart/range boundary;
- configured maximum bars/time window;
- hard invalidation by crossing a doctrine-specific boundary.

The exact numeric window is an implementation input, not a Canon constant.

---

# 2. Family A — Direct Terminal-Origin Post-F3 Hook

## Definition

A Direct Terminal-Origin Post-F3 Hook is a Hook whose origin is anchored at the terminal side of the opposing F3.

```text
F3 completes/reaches terminal side
→ opposite Hook starts from that terminal side
→ Hook becomes valid if it closes structurally or qualifies geometrically
```

## Recognition

A candidate belongs to this family when:

1. an F3 terminal side exists;
2. candidate Hook direction is opposite to F3 direction;
3. candidate origin is the F3 terminal endpoint or is inside the F3 terminal tolerance zone;
4. the Hook either:
   - closes as a full structural Hook, or
   - reaches the configured geometric 80% cycle threshold when geometric mode is enabled.

## Structural direct mode

In strict structural mode, this Hook is valid only if it has:

- sequence origin;
- crown/opposite extreme;
- confirmed terminal node;
- closed Hook state.

If origin is hit before terminal node confirmation, the candidate is not a Hook.

## Geometric direct mode

In geometric 80% mode, a direct post-F3 semicircle can be accepted even when full structural sequence labels are not available.

This is only allowed when:

- the cycle is inside the F3 terminal ownership window;
- the cycle is opposite to F3 direction;
- the cycle reaches at least the configured completion/near-death threshold, default candidate: `80%`;
- it does not violate the origin-death rule before qualification.

---

# 3. Family B — Delayed/Rebound Post-F3 Hook

## Definition

A Delayed/Rebound Post-F3 Hook forms after price reaches the F3 terminal side, rebounds away, and then creates a Hook slightly beyond/above/below the terminal side rather than exactly at the F3 endpoint.

The user-described example:

```text
F3 side is reached
price rebounds upward
then a smaller Hook forms a little higher
that Hook may be the intended post-F3 Hook
```

This must be recognized as a valid post-F3 family, not discarded merely because its origin is not exactly equal to the F3 terminal endpoint.

## Recognition

A candidate belongs to this family when:

1. an F3 terminal side was reached/touched;
2. price moved away from that terminal side;
3. the candidate Hook forms inside the post-F3 ownership window;
4. candidate direction is opposite to F3 direction;
5. candidate origin is not necessarily equal to the F3 endpoint, but is still semantically derived from the F3 terminal environment;
6. the Hook either:
   - closes as a full structural Hook, or
   - qualifies as a geometric 80% cycle Hook when enabled.

## Structural delayed mode

Structural delayed mode accepts only delayed Hooks with full Hook anatomy:

- sequence nodes;
- crown;
- confirmed terminal node;
- closed Hook state.

This is the cleanest production mode.

## Geometric delayed mode

Geometric delayed mode accepts small post-F3 semicircles above the 80% threshold even if no full sequence has formed.

This is a research/visual mode and must be explicitly enabled. It must never leak all structural sequences into valid-only rendering.

---

# 4. Structural Hook vs Geometric 80% Cycle Hook

## Structural Hook

A Structural Hook is a fully formed Hook according to Phase02 sequence doctrine.

It owns:

- Hook ID;
- branch/sequence ID;
- node labels;
- confirmed terminal node;
- closed Hook lifecycle status.

## Geometric 80% Cycle Hook

A Geometric 80% Cycle Hook is a visible near-death semicircle/cycle candidate that may not own a full structural sequence yet.

It can be accepted only in an explicit mode.

It must be represented as a distinct family, not as if it were a normal full structural sequence.

Suggested labels:

```text
F3H80-DIR   direct F3 geometric 80% Hook
F3H80-REB   delayed/rebound F3 geometric 80% Hook
```

Suggested structural labels:

```text
F3H-DIR     direct F3 structural Hook
F3H-REB     delayed/rebound F3 structural Hook
```

---

# 5. Search priority

When the system is asked to show valid post-F3 Hooks, candidate selection should follow a deterministic priority.

Recommended priority:

1. Direct structural Hook from the F3 terminal endpoint.
2. Direct geometric 80% cycle from the F3 terminal endpoint, if geometric mode is enabled.
3. Delayed/rebound structural Hook inside the F3 ownership window.
4. Delayed/rebound geometric 80% cycle inside the F3 ownership window, if geometric mode is enabled.

If multiple candidates qualify in one family, selection policy must be explicit:

- earliest qualifying candidate;
- strongest completion percent;
- closest to F3 terminal side;
- highest structural completeness.

Default production recommendation:

```text
structural completeness > directness > earliest qualification > geometric completion
```

Research mode may compare all candidates, but production valid-only mode must render only the selected candidates.

---

# 6. Valid-only rendering rule

When valid-only is enabled:

```text
Render only selected post-F3 Hook candidates and their own nodes/labels/arcs.
Do not render all sequences in the F3 environment.
Do not render same-origin siblings.
Do not render non-selected delayed candidates.
Do not render geometric 80% candidates unless geometric mode is explicitly enabled.
```

If no post-F3 Hook qualifies:

```text
Draw nothing for that F3 context.
```

---

# 7. Required future implementation inputs

Suggested inputs for the next code patch:

```text
InpHookPostF3RecognitionMode
  STRUCTURAL_ONLY
  STRUCTURAL_OR_GEOMETRIC_80

InpHookPostF3AllowDirectTerminalHook = true
InpHookPostF3AllowDelayedReboundHook = true
InpHookPostF3GeometricMinCompletionPct = 80.0
InpHookPostF3TerminalToleranceBars = configurable
InpHookPostF3TerminalTolerancePricePoints = configurable
InpHookPostF3MaxSearchBars = configurable
InpHookPostF3SelectionPriority = STRUCTURAL_FIRST
```

This phase intentionally does not hard-code these numbers because the user still plans to provide more chart examples.

---

# 8. Implementation contract

The next code patch must not simply widen existing `F3H` selection.

It must introduce a clear post-F3 candidate classifier:

```text
candidate.family:
  F3H_DIRECT_STRUCTURAL
  F3H_DIRECT_GEOMETRIC_80
  F3H_DELAYED_STRUCTURAL
  F3H_DELAYED_GEOMETRIC_80
```

Then the renderer must use only the final selected family set.

No raw Phase02 sequence renderer should bypass that selected set.

---

# 9. Chart example interpretation

In the provided Gold M1 example:

- F3 detection is accepted as correct.
- The displayed `F3H` label is not necessarily the intended post-F3 Hook.
- Valid post-F3 candidates include:
  - a direct Hook from the F3 terminal endpoint if it falls deep enough / closes structurally;
  - a small delayed rebound cycle above the terminal area if geometric 80% mode is enabled;
  - a later full structural Hook if it forms after rebound and still belongs to the F3 ownership window.

The doctrine now distinguishes these cases instead of forcing them into a single `F3H` bucket.
