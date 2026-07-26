---
type: canonical_architecture
id: ZONE-AF-0003
status: draft
language: english
project: Decision Alpha Lab
concepts:
  - Hook Zone
  - F1 Zone
  - F2 Zone
  - F3 Zone
  - Symmetry
  - Waist
  - Stop Stability
---

# ZONE-AF-0003 — Mechanical Zone Sources: Hook, F1, F2, and F3

## 1. Purpose

This document converts the mechanical zone sources into formal architecture.

The principle is:

> Use every structure through the movement limitations it creates. Do not worship the structure itself. Convert its limitation into a potential reversal area, then decide whether that area has a stable entry edge and stop edge.

Every source is evaluated by:

```text
Does it create a probable reversal area?
Does it define a stable entry edge?
Does it define a stable stop / expiration edge?
Does it require lower-timeframe refinement?
Does it offer enough potential relative to cost?
```

---

## 2. Hook Zone

### 2.1 Core Idea

The Hook source creates a zone through **near-death hook logic** and symmetry.

A Hook Zone is one of the cleaner zone types because it can often define:

```text
Potential entry area = near-death / symmetry-derived hook area
Stop / expiration    = behind the hook
```

### 2.2 Mechanical Logic

The hook creates a movement limitation. Price can approach the hook's critical area, but if the hook logic remains valid, the far side of the hook should not be violated.

The zone is not merely the extreme point. The zone is the bounded region around the hook-derived reversal area where limit risk is rational.

### 2.3 Stop Policy

Primary stop policy:

```text
Stop behind the hook
```

This makes Hook Zones more execution-ready than many broad F2/F3 zones.

### 2.4 Quality Conditions

Hook Zone quality increases when:

- the hook is mechanically valid;
- symmetry gives a clearer near-death area;
- the stop behind the hook is not too wide;
- the zone appears inside a higher-timeframe parent zone;
- lower-timeframe structure supports the limit plan;
- potential beyond the zone is open;
- the zone is not merely an obvious trap;
- the hook is part of a meaningful sequence or compression.

### 2.5 Weaknesses

Hook Zones become weaker when:

- the hook is too obvious and repeatedly touched;
- stop behind the hook is too expensive;
- potential is capped by nearby opposite structure;
- context is against the trade without asymmetry;
- symmetry area is vague;
- price has already consumed the area.

### 2.6 Classification

```yaml
source_type: hook
execution_stability: high_to_medium
requires_ltf_refinement: optional
stop_available: usually_yes
entry_style: limit
primary_risk_edge: behind_hook
```

---

## 3. F1 Zone

### 3.1 Core Idea

After F1 forms and its flag is taken, once points 1 and 2 are made, the system can search for entry in the direction of F1 from point 2.

The stop is placed behind the **waist of F1**.

Important principle:

> The closer price comes to the waist of F1, the narrower and more attractive the zone becomes, provided the context still supports the F1 directional thesis.

### 3.2 Mechanical Logic

F1 provides a directional structural constraint. After the flag is taken and the 1/2 structure forms, point 2 can become the area from which the system searches for continuation in the direction of F1.

### 3.3 Zone Formation

Potential entry area:

```text
Around point 2 / pullback area after F1 1-2 structure
```

Stop / expiration:

```text
Behind the waist of F1
```

The waist is the core expiration reference. As price approaches the waist, risk can compress.

### 3.4 Why It Can Be Strong

F1 can create strong zones because it has:

- directional logic;
- known structural reference;
- a waist stop;
- measurable narrowing as price approaches the waist;
- compatibility with limit entry;
- continuation potential if the F1 logic resumes.

### 3.5 Zone Quality Variables

```text
f1_flag_taken
point_1_made
point_2_made
distance_to_waist
zone_width_to_waist
potential_after_point_2
context_alignment
ltf_child_zone_presence
```

### 3.6 Classification

```yaml
source_type: f1
execution_stability: medium_to_high
requires_ltf_refinement: recommended_but_not_always_mandatory
stop_available: yes
primary_risk_edge: behind_f1_waist
entry_style: limit_in_f1_direction
```

---

## 4. F2 Zone

F2 is structurally more complex than F1 because it can create reversal potential but may not provide a clean stop on its own.

There are two primary F2 cases.

---

### 4.1 F2 Case A — Point 1 and 2 Without Hitting the F2 Waist

In this case, F2 creates a reversal area after points 1 and 2 form, but the waist has not been hit.

This can be a reversal zone, but the stop is not clean enough on the parent timeframe.

### 4.1.1 Interpretation

The area has potential because F2 has formed enough structure to suggest a reversal attempt. However, the lack of a stable stop means it should usually be classified as:

```text
Watch Zone / Parent Zone
```

not direct execution.

### 4.1.2 Required Policy

Lower-timeframe refinement is required.

The system must search for:

- lower-timeframe hook;
- lower-timeframe F1/F2 child zone;
- compression break;
- a narrower stop edge;
- micro-structure invalidation.

### 4.1.3 Classification

```yaml
source_type: f2_case_a_no_waist_hit
execution_stability: low_to_medium
requires_ltf_refinement: yes
stop_available: not_stable_on_parent
primary_use: parent_watch_zone
entry_style: ltf_limit_only
```

---

### 4.2 F2 Case B — Waist-Hit F2 Where the Waist Becomes Point 1

This case must be understood through the original F-counting definitions.

When F2 hits its own waist, the waist-hit is not merely an additional touch. In this specific interpretation, the F2 waist-hit can become **Point 1** of the F2 reversal structure, and the next relevant hit/extension area becomes **Point 2**.

The central idea is:

```text
F2 hits its waist
→ the waist-hit can define Point 1
→ the following hit/extension can define Point 2
→ from Point 2 and beyond, reversal potential becomes active
```

In other words, the reversal zone is not simply “the waist was touched.” The relevant reversal field begins after the F2 structure has created the new 1/2 relationship around the waist-hit logic. The area from Point 2 upward/beyond can become the active reversal potential area.

### 4.2.1 Interpretation

The important distinction is that the waist-hit changes the internal grammar of F2. It can re-anchor the F2 structure by making the waist-hit act as Point 1. After that, the market can form Point 2, and the area from Point 2 onward can become a reversal field.

This makes the case more specific than a generic broad F2 reversal area. However, it still does not automatically produce a safe parent-timeframe execution zone, because the stop/expiration edge remains structurally unstable or too broad unless a lower timeframe defines it.

The system should ask:

```text
Has the F2 waist-hit become Point 1 under the F-counting grammar?
Has the following extension/hit become Point 2?
Is the reversal potential now active from Point 2 and beyond?
Does the parent timeframe provide a stable stop edge?
If not, does the lower timeframe create a child zone with a clear start and stop?
```

### 4.2.2 Trading Meaning

This case is a **reversal-potential case**, not automatically a direct limit-entry case.

The sequence is:

```text
Waist hit = Point 1
Point 2 forms after that
From Point 2 upward/beyond = reversal potential field
Direct stop on parent = usually not stable
Lower-timeframe zone = required for execution
```

The system should not treat the whole F2 field as a tradable zone. It should treat it as a parent context that says: “from this second point onward, reversal can begin, but execution needs a smaller risk contract.”

### 4.2.3 Policy

If the parent timeframe does not provide a stable stop, the case remains a watch/parent zone.

Execution is allowed only when a child structure defines:

- a clear start edge;
- a clear stop/expiration edge;
- a reasonable width;
- a valid lower-timeframe risk contract;
- enough open reward beyond the risk.

### 4.2.4 Classification

```yaml
source_type: f2_case_b_waist_hit_point1_point2
meaning: reversal_potential_after_point_2
waist_role: can_become_point_1
point_2_role: activates_reversal_field_from_point_2_and_beyond
execution_stability: medium_as_context_low_as_direct_trade
requires_ltf_refinement: yes
stop_available: not_stable_on_parent_by_default
primary_use: parent_reversal_potential_zone
entry_style: lower_timeframe_child_limit_only
```

---

## 5. F2 Symmetry with F1

### 5.1 Core Idea

Another F2 limitation comes from symmetry with F1.

From the moment F2 exceeds the symmetry of F1, the area can become a potential reversal region until one of the following occurs:

- F2 makes point 1 and point 2;
- price returns toward the waist of F2;
- lower-timeframe structure defines a safer risk contract.

### 5.2 Important Limitation

This area is broad and does not naturally provide a stable stop.

Therefore:

```text
F2 symmetry extension = potential area, not execution zone by itself
```

### 5.3 Policy

This source should usually be classified as:

```text
Broad Watch Zone
```

It requires lower-timeframe refinement before limit execution.

### 5.4 Safety Note

If this source is examined directly on a low timeframe, it can still be unsafe if no stable stop exists. A zone with no stop is not a trade. It is only a context clue.

### 5.5 Classification

```yaml
source_type: f2_symmetry_with_f1
execution_stability: low
requires_ltf_refinement: yes
stop_available: no_on_parent
primary_use: reversal_potential_estimation
entry_style: only_after_child_zone
```

---

## 6. F3 Zone

### 6.1 Core Idea

After F3 is hit, reversal can happen from many places. However, F3 does not give a clean symmetry reference and does not define how far continuation can extend.

Even if F3 is locked, the structure remains in F3 and the system still does not know exactly where the reliable reversal start or stop should be.

### 6.2 Consequence

F3 creates a very broad potential environment, not a precise execution zone.

```text
F3 = broad reversal environment
not automatically = tradable zone
```

### 6.3 Main Weakness

For F3:

- the start of the zone is unclear;
- the stop of the zone is unclear;
- continuation can extend unexpectedly;
- reversal can occur from many points;
- parent timeframe execution is unsafe without refinement.

### 6.4 Required Policy

F3 requires lower-timeframe structure before entry.

The system should search inside the F3 environment for:

- lower-timeframe Hook Zone;
- lower-timeframe F1/F2 zone;
- compression/release area;
- narrow child zone;
- clear stop edge.

### 6.5 Classification

```yaml
source_type: f3
execution_stability: very_low_on_parent
requires_ltf_refinement: mandatory
stop_available: no_on_parent
primary_use: broad_context_zone
entry_style: only_after_child_zone
```

---

## 7. Comparative Table

| Source | Reversal Potential | Entry Edge | Stop Edge | Direct Tradability | LTF Required? |
|---|---:|---:|---:|---:|---:|
| Hook | High | Often clear | Behind hook | Often possible | Optional/recommended |
| F1 | Medium/High | Around point 2 / pullback | Behind F1 waist | Possible if narrow | Recommended |
| F2 Case A | Medium | Broad | Unclear | No | Yes |
| F2 Case B | Medium | From Point 2 onward/beyond | Not stable by default | No direct parent trade | Yes |
| F2 Symmetry | Medium | Broad | No stable stop | No | Yes |
| F3 | Broad but vague | Unclear | Unclear | No | Mandatory |

---

## 8. Core Rule from All Sources

The alphabet of the system is:

```text
Potential area is not enough.
A tradable zone needs a start and a stop.
```

The system can observe every structure across multiple timeframes. But only areas where the start of the zone and the expiration/stop edge become stable should become execution zones.

This is why lower-timeframe fractal refinement is central.

---

## 9. Implementation Implication

Each source should generate a zone candidate with an execution-stability class:

```text
execution_ready
needs_ltf_refinement
context_only
unsafe_no_stop
```

This protects the system from treating every reversal potential as a trade.

