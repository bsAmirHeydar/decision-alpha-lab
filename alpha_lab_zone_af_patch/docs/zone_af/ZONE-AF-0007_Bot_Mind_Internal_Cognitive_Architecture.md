---
type: canonical_architecture
id: ZONE-AF-0007
status: draft
language: english
project: Decision Alpha Lab
concepts:
  - Bot Mind
  - Cognitive Architecture
  - Scenario Engine
  - Antifragile Logger
  - Zone Decision Policy
---

# ZONE-AF-0007 — Bot Mind Internal Cognitive Architecture

## 1. Purpose

The robot should not behave like a blind pattern matcher. Its internal decision model should behave like a risk-contract evaluator.

The bot must think in this sequence:

```text
Context -> Constraint -> Zone -> Risk Contract -> Scenario -> Limit Plan -> Outcome -> Learning
```

---

## 2. Cognitive Layers

### 2.1 Context Reader

Reads mechanical state:

- Hook state;
- F1/F2/F3 state;
- rally state;
- directional structure;
- timeframe hierarchy;
- compression/expansion;
- session/time;
- intermarket inputs later.

### 2.2 Constraint Mapper

Transforms context into movement limitations.

Examples:

- Hook creates a stop behind the hook.
- F1 creates a waist-based expiration point.
- F2 creates reversal potential but often lacks stop clarity.
- F3 creates broad potential but is too open for direct execution.

### 2.3 Zone Generator

Creates zone candidates from constraints.

Each candidate receives:

- source type;
- entry edge estimate;
- stop edge estimate;
- execution stability class;
- lower-timeframe refinement requirement.

### 2.4 Risk Contract Builder

Decides whether the zone can become a tradeable contract.

Questions:

```text
Is the entry edge clear?
Is the stop edge clear?
Is the width acceptable?
Is potential open enough?
Is LTF refinement required?
```

### 2.5 Scenario Builder

Builds scenarios for each zone:

```text
Hold
Failure
Fake Break
Continuation
No Trade
Wait for Child
```

A zone should not be reduced to one prediction. It should be evaluated as a scenario portfolio with bounded costs.

### 2.6 Limit Order Planner

Plans:

- entry type;
- entry price;
- stop edge;
- risk allocation;
- order expiration;
- child-zone dependency;
- no-trade reason if rejected.

### 2.7 Failure Interpreter

If the zone fails, the bot asks:

- was the source weak?
- was the stop too tight?
- was the zone too broad?
- was LTF refinement missing?
- did failure create a better opposite scenario?
- was the area an obvious trap?

### 2.8 Learning Logger

Logs every decision, including no-trades.

The system must learn from:

- accepted zones;
- rejected zones;
- missed zones;
- stopped zones;
- tail zones;
- dead zones.

---

## 3. Default State

The default state should be:

```text
No Trade
```

The bot earns permission to trade only when a risk contract is clear.

This prevents overtrading and pattern worship.

---

## 4. Bot Personality

The bot's trading personality should be:

```text
patient
limit-oriented
risk-contract-first
anti-win-rate-obsession
tail-seeking
no-trade tolerant
context-sensitive
antifragile
```

It should not fear small predefined losses. It should fear undefined risk, vague zones, and chasing after convexity is gone.

---

## 5. Decision Tree

```text
1. Is there mechanical context?
   No -> no trade.

2. Does context create a movement constraint?
   No -> no zone.

3. Does the constraint create a price range?
   No -> no zone.

4. Does the range have a stable entry and stop?
   Yes -> execution zone candidate.
   No -> watch zone or context zone.

5. Is potential large enough relative to cost?
   No -> no trade.

6. Is lower-timeframe refinement required?
   Yes -> wait for child zone.
   No -> limit plan allowed.

7. Did price touch the zone?
   Log touch event.

8. Did trade trigger?
   Log trade event.

9. What was the outcome?
   Label and learn.
```

---

## 6. Human Feedback Integration

Manual labels should be allowed:

```text
beautiful_zone
ugly_zone
too_obvious
felt_convex
dead_zone
missed_tail
bad_management
```

The bot should not blindly obey manual labels, but it should store them as subjective research features.

---

## 7. Disagreement Logging

If the bot rejects a zone and the user trades it manually, log disagreement.

If the bot accepts a zone and the user rejects it manually, log disagreement.

Disagreement is a valuable learning source.

---

## 8. Summary

The bot must not be a signal machine. It must be an antifragile risk-contract evaluator.

