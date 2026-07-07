# Phase 39 — Practical Valid Hook Determination

## 1. Why this phase exists

The prior strict valid-Hook implementation became too heavy. It correctly tried to suppress fractal Hook noise, but it also combined validity with semantic readiness, scale matching, raw terminal behavior, and rendering state. The result was a production view with too few Hooks.

The corrected model separates the system into two layers:

```text
Hook sequence counting  → complete structural detection
Hook validity filtering → production visibility doctrine
```

Counting should not become the filter. The engine must still build the Hook sequences it can structurally identify. Validity is applied later as a display and zone-eligibility layer.

---

## 2. Core doctrine

A production-valid Hook is not every Hook-like structure. It belongs to one of two accepted families:

```text
Valid Hook Family A: Immediate Hook After Opposing F3
Valid Hook Family B: Hook After Hook
```

Everything else may remain available for debugging and CSV audit, but it is not a production-valid Hook source.

---

## 3. Family A — Immediate Hook After Opposing F3

### Definition

```text
F3 completes or locks
→ the immediate next structural Hook appears
→ the Hook direction is opposite to the F3 direction
→ this Hook is valid
```

### Important exclusions

An old F3 must not validate every later Hook. Only the immediate next structural Hook after that F3 may qualify.

If the immediate next Hook after F3 is not opposite in direction, that F3 validates no Hook.

### Practical implementation

The immediate Hook is selected from structural Hook sequences, not from the final semantic renderer. This is important because a Hook can be structurally valid before it passes optional near-death display strictness.

Therefore:

```text
F3 validity search uses structural Hook validity
not render_eligible-only filtering
```

### Scale strictness

Scale matching is useful for strict audits, but it can be too sparse in practice. The system now exposes it as a separate input:

```text
InpHookPhase02ValidF3RequireSameScale
```

Recommended practical default:

```text
false
```

Strict audit mode:

```text
true
```

---

## 4. Family B — Hook After Hook

### Definition

```text
Hook-2 is valid if:
Hook-2 origin node == Hook-1 structural terminal node
```

This is exact node continuity. It is not enough for a Hook to appear somewhere after another Hook.

### Parent visibility

When Hook-2 is valid by this rule, Hook-1 may be displayed as its parent companion.

Hook-1 is not independently promoted to a valid Hook just because it is visible. Its visibility exists only because Hook-2 depends on it structurally.

---

## 5. Terminal semantics

There are two terminal concepts:

### Structural terminal node

Used for Hook-after-Hook continuity.

```text
previous structural terminal node == next origin node
```

### Visual/raw terminal price

Used for drawing the cycle envelope.

```text
Positive Hook visual terminal = lowest raw low reached after the crown
Negative Hook visual terminal = highest raw high reached after the crown
```

This separation prevents two problems:

1. Hook-after-Hook continuity is not destroyed by raw candle extremes that have no Phase01 node id.
2. The visual cycle still extends to the real price extreme seen on the chart.

---

## 6. Practical valid-only view

Valid-only mode should mean:

```text
show only valid Hook families
and only the required parent companion for Hook-after-Hook
```

It should not mean:

```text
hide valid Hooks unless they also pass every semantic near-death rendering gate
```

The new input controls that strictness:

```text
InpHookPhase02ValidOnlyRequireNearDeath
```

Recommended practical default:

```text
false
```

Strict audit mode:

```text
true
```

---

## 7. Why the previous view was too sparse

A Hook could disappear because of non-core restrictions:

- the immediate-F3 search used render eligibility instead of structural validity;
- F3-to-Hook matching could require exact scale matching;
- valid-only rendering required near-death semantic readiness;
- Hook-after-Hook used one-directional sequence ordering instead of all valid prior terminal matches;
- label selection expanded or filtered at the wrong scope.

This phase keeps the core validity doctrine but removes the accidental over-filtering.

---

## 8. Inputs

### Practical production view

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyRequireNearDeath = false
InpHookPhase02ValidF3RequireSameScale = false
InpHookPhase02SeedUsedNodesCannotRestart = true
InpHookPhase02RejectRawOriginBreachBeforeTerminalConfirmation = true
```

### Strict research audit

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyRequireNearDeath = true
InpHookPhase02ValidF3RequireSameScale = true
InpHookPhase02ExportCsv = true
InpHookPhase02PrintSummary = true
```

### Full debugging

```text
InpHookPhase02ShowOnlyValidHooks = false
InpHookPhase02ExportCsv = true
InpHookPhase02PrintSummary = true
```

---

## 9. Non-goals

This phase does not change:

- canonical F-counting logic;
- Rally logic;
- order execution;
- broker requests;
- risk sizing;
- trade management;
- Zone execution.

It only changes Hook validity annotation and production Hook visibility strictness.
