# DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s

> Version: draft 0.2  
> Scope: discretionary-to-algorithmic vocabulary for Decision Alpha Lab  
> Purpose: convert the manual multi-timeframe market-reading language into precise structural concepts before turning them into code.

---

## 1. Why this glossary exists

Decision Alpha Lab uses structural market concepts that started as discretionary visual language and are gradually being converted into code. The core structural atom is the **node**: a validated high or low created by an L-rule. However, the human reading style is richer than isolated highs and lows.

The manual language includes:

- deep returns,
- hooks,
- rallies,
- flags,
- node hunts,
- internal 1/2/3 counts,
- open destinations,
- fractal nesting,
- rally continuation after structural deception.

This README defines the vocabulary before implementation. Every term should be explicit enough to become a future module. This document is not the final algorithm. It is the shared language contract.

---

## 2. Node

A node is the atomic structural object.

In code terms, a node is a validated high or low:

- `LOW node`: a confirmed structural low.
- `HIGH node`: a confirmed structural high.

A node should store at least:

- price,
- time,
- bar index,
- L value,
- activation or confirmation time,
- type: `HIGH` or `LOW`.

A node is not a trade idea by itself. The trade idea comes from what happens after the node:

- Does price move away from it?
- Does price return to it?
- Does price touch its zone?
- Does price hunt internal nodes?
- Does price break the node and reclaim it?
- Does price create a rally after the hunt?
- Does the internal 1/2/3 structure complete?

A node is a letter. Hooks, flags, rallies, and 123 structures are sentences.

---

## 3. Cycle

A cycle is the life of a node from formation to reaction, death, or transformation into a larger structure.

For a low node:

```text
LOW is created
-> price moves away from the LOW
-> price later returns toward the LOW or its zone
-> the LOW is either killed, touched and rejected, converted into a flag, or absorbed into a larger structure
```

For a high node:

```text
HIGH is created
-> price moves away from the HIGH
-> price later returns toward the HIGH or its zone
-> the HIGH is either killed, touched and rejected, converted into a flag, or absorbed into a larger structure
```

A cycle is not only the initial move away from origin. The return path is part of the cycle. The cycle becomes meaningful when we know how price behaves when it returns to origin.

---

## 4. Hook

A hook is a cycle that returns deeply toward its origin, approaches structural death, but then rejects and turns.

Mental image:

```text
origin node -> move away -> deep return near origin -> rejection / rally
```

Manual definition:

> A hook occurs when a cycle retraces roughly most of its path toward origin and then turns instead of dying.

The exact percentage should not be hard-coded too early. It can later become a parameter, but the concept is qualitative: the market comes close enough to origin that the cycle looks nearly dead.

### Bullish hook

```text
LOW origin
-> upward movement
-> deep return toward the LOW / LOW zone
-> rejection
-> rally upward
```

### Bearish hook

```text
HIGH origin
-> downward movement
-> deep return toward the HIGH / HIGH zone
-> rejection
-> rally downward
```

### Hook as a near-death zone

A hook is not a simple shallow pullback. A shallow return is usually only a pullback. A hook occurs near the boundary between survival and invalidation.

For a low cycle:

- shallow return = ordinary pullback,
- full break and continuation below the low = cycle death,
- deep return near the low followed by rejection = hook.

The hook is the border between failure and continuation.

---

## 5. Rally

A rally is a sharp directional movement that begins after a hook, flag, or deception phase resolves.

In this vocabulary, rally does not only mean upward price movement. It means a directional impulse after the market exits negotiation, uncertainty, hunt, or trap.

### Bullish rally

```text
hook near LOW
-> rejection
-> fast upward movement
```

### Bearish rally

```text
hook near HIGH
-> rejection
-> fast downward movement
```

Before a rally, the market often shows:

- revisit,
- internal hunt,
- open 1/2,
- flag,
- false hope,
- final liquidity sweep.

After a rally begins, the path is often cleaner and more one-directional.

---

## 6. Flag

A flag is a structure of deception.

Core idea:

> The market creates a node, gives hope in one direction, then hunts or breaks the same structural area, traps the wrong side, and begins the real move from there.

### Bullish flag around a LOW

```text
LOW is created
-> price moves up and creates bullish hope
-> price returns and hunts/breaks the LOW
-> sellers become active
-> price reclaims and begins the true upward rally
```

### Bearish flag around a HIGH

```text
HIGH is created
-> price moves down and creates bearish hope
-> price returns and hunts/breaks the HIGH
-> buyers become active
-> price rejects and begins the true downward rally
```

### Flag is not the same as invalidation

A hunt has two possible meanings:

```text
hunt + continuation through the node = true node death
hunt + reclaim/rejection = flag / trap
```

Therefore a hunt is not always death. Sometimes it is the fuel for the rally.

---

## 7. 123 Flag

A 123 flag is an internal counting structure before the flag resolves into a rally.

The purpose of the count is to avoid treating every noisy pullback as a full flag. The 1/2/3 structure gives the market time to build internal deception and then resolve it.

A generic bullish 123 flag may look like:

```text
LOW origin
-> first upward hope
-> internal 1
-> internal 2
-> final sweep/hunt
-> reclaim
-> rally upward
```

A generic bearish 123 flag may look like:

```text
HIGH origin
-> first downward hope
-> internal 1
-> internal 2
-> final sweep/hunt
-> rejection
-> rally downward
```

The exact mechanical implementation depends on the detector being built. The language rule is that a 123 flag contains an internal sequence, not just one immediate sweep.

---

## 8. Open 1 and Open 2

Open 1 and Open 2 are unresolved internal destinations or counts that remain active after part of a structure is formed.

They are important because they show that the structure is not fully closed. The market may still need to visit, test, or resolve those internal points before the larger move completes.

In visual tools, open 1 and open 2 may be displayed as numeric labels only, without drawing extra path lines, if the purpose is to keep the chart clean.

Example visual contract:

```text
Core F1 body is drawn.
Internal 1 and 2 are displayed only as numbers.
No extra line is drawn from leg2 to 1/2 unless the specific experiment requires it.
```

---

## 9. Fractal nesting

The same vocabulary can exist at multiple scales:

```text
small node inside large hook
small flag inside larger rally
M1 open 1/2 inside M10 flag
M10 flag inside H1 cycle
```

Fractal nesting does not mean every timeframe is identical. It means the same structural grammar can appear inside larger structures.

A future implementation should explicitly record:

- parent structure,
- child structure,
- timeframe or L-scale,
- whether the child confirms or contradicts the parent.

---

## 10. Engineering rules

When converting this language into code, the following rules should be respected:

1. Keep origin nodes explicit. Do not let renderers invent origins.
2. Separate detection from rendering.
3. Store every important point with time, price, index, and type.
4. Keep incomplete and confirmed structures separate.
5. Treat hunts as ambiguous until reclaim/continuation decides their meaning.
6. Avoid hard-coding discretionary language too early.
7. Prefer audit columns over hidden logic.
8. Build minimal visual contracts first, then add complexity only when necessary.

---

## 11. Relationship to M0007 F1

M0007 F1 is one concrete implementation of a flag-counting structure.

The current visual contract for M0007 is:

```text
Start -> Leg1 = straight line
Leg1 -> correction / waist -> Leg2 = curved body
F1 label = shown
internal 1 and 2 = numeric labels only
no visual lines from Leg2 to 1/2
```

The calculation contract remains richer than the visual contract:

```text
true Start is stored
Leg2 is formed
internal 1 and 2 are formed after Leg2
internal 1/2 must not break the waist
final rebreak of Leg2 confirms the F1
pending and confirmed states have different colors
```

This separation is important: the chart should remain readable, while the detector still keeps all structural logic.

---

## 12. Future modules

This glossary can later become the base for separate modules:

```text
NodeCycleTracker
HookDetector
FlagDetector
Open12Tracker
RallyDetector
FractalNestMapper
StructureLanguageRenderer
```

Each module should start with a README-level contract before code is written.

---

## 13. Summary

This vocabulary is intended to turn manual market reading into code without destroying the original structural intuition.

The language is:

```text
Node -> Cycle -> Hook / Flag -> Open 1/2 -> Rally -> Fractal nesting
```

The engineering goal is to make every term testable, auditable, and eventually executable.
