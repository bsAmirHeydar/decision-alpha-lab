# 56 — Hook Validity Master Doctrine

## Status

Canonical doctrine.  
This document is the source of truth for deciding which Hook cycles are production-valid.

## Purpose

The Hook subsystem must solve two different problems without mixing them:

1. **Structural Hook counting** — count Hook sequences completely and accurately.
2. **Production Hook visibility** — show only the Hook cycles that are meaningful enough to use as valid structural objects.

The mistake to avoid is making validity rules part of the counting engine too early. Hook counting should remain rich and complete. Validity must be applied later as a production-view selection layer.

## Core principle

A structural Hook candidate is not automatically a production-valid Hook.

A production-valid Hook belongs to one of exactly two families:

```text
VALID_HOOK_FAMILY = {
  HOOK_AFTER_OPPOSING_F3,
  HOOK_AFTER_HOOK
}
```

Any Hook outside these two families may exist as a structural/debug candidate, but it is not production-visible in valid-only mode and must not be treated as a primary valid Hook cycle.

---

# 1. Hook After Opposing F3

## 1.1 Concept

An F3 can lock or form at one point, but the market can continue extending inside the same F3 environment. Therefore, a Hook after F3 is not merely any Hook that appears after a historical F3 event. It is the Hook that emerges from the terminal trend-side area of the most recent opposing F3 environment.

The doctrine is:

```text
The latest opposing F3 creates the environment.
The Hook that forms from the terminal area of that F3 is valid.
```

## 1.2 Direction

A Hook after F3 is valid when the Hook direction is opposite to the latest F3 direction.

Examples:

```text
Last F3 = bullish F3
Then a negative Hook forms from the bullish F3 terminal area
=> valid Hook After Opposing F3
```

```text
Last F3 = bearish F3
Then a positive Hook forms from the bearish F3 terminal area
=> valid Hook After Opposing F3
```

## 1.3 F3 continuation

The F3 may become longer after it first forms or locks. This does not break the doctrine.

The important point is not that the F3 is finished forever. The important point is:

```text
F3 structure exists
The market is still inside / extending that F3 environment
A Hook of the opposite kind forms from the terminal extreme area
```

That Hook is considered valid.

## 1.4 Immediate relationship

“Immediate Hook after F3” means:

```text
The Hook origin starts from the terminal area of the opposing F3.
```

It does not mean that every later Hook after an old F3 is valid.

The Hook must be structurally born from the F3 terminal side, not merely occur many bars later in the same chart region.

## 1.5 Practical definition

A Hook qualifies as Hook After Opposing F3 when:

1. There is a most recent opposing F3 context.
2. The F3 has formed its flag / F3 structure.
3. The market is at or extending the terminal side of that F3 environment.
4. A Hook of the opposite type forms from that terminal side.
5. The Hook has a valid cycle/sequence structure according to the Hook sequence doctrine.

## 1.6 What does not qualify

The following do not qualify:

- any random Hook after any old F3;
- a Hook that is not structurally born from the F3 terminal area;
- a Hook that appears after the F3 context has clearly been replaced by a new dominant structure;
- a Hook whose origin has no relation to the F3 terminal extreme.

---

# 2. Hook After Hook

## 2.1 Concept

A Hook after Hook is valid when a second Hook is born from the terminal/death-near area of a previous completed Hook cycle.

The doctrine is:

```text
Hook-1 completes its sequence/cycle.
Hook-2 starts from the terminal area of Hook-1.
Hook-1 and Hook-2 are of the same kind.
Hook-2 is production-valid.
Hook-1 is rendered as the parent companion.
```

## 2.2 Same-kind requirement

Hook-after-Hook requires both Hooks to be of the same kind.

```text
positive Hook -> positive Hook
negative Hook -> negative Hook
```

A positive Hook followed by a negative Hook is not Hook-after-Hook under this doctrine.

## 2.3 Parent requirement

Hook-1 does not have to be independently valid by the F3 rule. It only needs to have completed its own sequence/cycle.

```text
Hook-1 = completed structural parent
Hook-2 = valid Hook-after-Hook child
```

Hook-1 becomes visible only because Hook-2 depends on it.

## 2.4 Start relationship

Hook-2 must begin from the terminal/death-near area of Hook-1.

This does not mean arbitrary visual closeness. It means structural continuity:

```text
Hook-2 origin is produced from the terminal extreme / near-death endpoint of Hook-1.
```

The implementation may need both:

- a structural terminal node for continuity matching;
- a raw terminal price/time for cycle rendering.

## 2.5 Rendering consequence

When Hook-2 is valid by Hook-after-Hook:

```text
Render Hook-2 with full detail.
Render Hook-1 with full detail as its parent companion.
```

Hook-1 is not promoted into an independently valid Hook. It is a required visual parent.

---

# 3. Production-valid set

In valid-only production mode, the renderer must first build a visible origin-group set:

```text
visible_hook_groups = {}

for each hook_group:
  if hook_group.family == HOOK_AFTER_OPPOSING_F3:
      visible_hook_groups.add(hook_group)

  if hook_group.family == HOOK_AFTER_HOOK:
      visible_hook_groups.add(hook_group)          // Hook-2
      visible_hook_groups.add(hook_group.parent)   // Hook-1 companion
```

Only the objects belonging to `visible_hook_groups` may be drawn.

---

# 4. Hard rules

## 4.1 Valid-only means valid-only

If valid-only mode is enabled:

```text
Draw only valid Hook cycles and required parent companions.
```

Do not draw:

- raw Hook candidates;
- unqualified structural Hooks;
- node labels from invalid Hooks;
- sequence labels from invalid Hooks;
- fallback structural Hooks;
- debug overlays;
- old stale Hook objects.

## 4.2 No fallback in production

If no valid Hook exists, valid-only production view must draw nothing.

```text
No valid Hook => no Hook cycles, no Hook labels, no Hook nodes.
```

Debug fallback can exist only in a separate explicit debug mode. It must not be part of production valid-only rendering.

## 4.3 Validity is not Zone logic

This doctrine does not define Hook zones. Zone generation will be specified separately.

For now:

```text
Hook validity controls Hook cycle visibility.
Zone logic is out of scope.
```

---

# 5. Implementation target

The next MQL5 patch must enforce this order:

1. Count all structural Hooks.
2. Group sequences into Hook origin-groups/cycles.
3. Determine terminal semantics.
4. Assign validity family:
   - Hook After Opposing F3
   - Hook After Hook
5. Build `visible_hook_groups`.
6. Render only cycles, nodes, and sequence labels belonging to `visible_hook_groups`.
7. Draw nothing if `visible_hook_groups` is empty.

This is the canonical implementation contract.
