# Hook / ND Branch Algorithm V1

## 1. Goal

This document converts the Hook / ND branch-sequence contract into a deterministic implementation algorithm.

The goal is to produce a list of Hook containers. Each Hook container can contain many branch sequences. Each branch sequence contains one to four counted same-side nodes after adaptive L normalization. A Hook qualifies as ND only when at least one branch has exactly three or four counted nodes and passes the retracement rule.

## 2. Inputs

For each symbol, timeframe, direction side, and L:

```text
rates[]
confirmed_nodes[]
optional_pending_node
base_L
max_L
allow_pending_node
nd_retrace_threshold = 0.50 by default
allow_below_threshold = false by default
```

Node engine output must include:

```text
node_id
time_start
time_end
anchor_time
price
kind = HIGH or LOW
L
confirmed
plateau_size
bar_index_start
bar_index_end
```

## 3. Direction mapping

### 3.1 Low-side Hook

```text
side = LOW
same_side_nodes = low nodes
boundary_condition = previous_low.price < active_low.price
branch_join_condition = previous_low.price > current_reference_low.price
```

### 3.2 High-side Hook

```text
side = HIGH
same_side_nodes = high nodes
boundary_condition = previous_high.price > active_high.price
branch_join_condition = previous_high.price < current_reference_high.price
```

The high-side implementation is the mirror of low-side implementation.

## 4. Main adaptive loop

```text
function BuildHooks(side, base_L, max_L):
    L = base_L

    while L <= max_L:
        nodes = BuildProjectNodes(L, allow_pending_node)
        same = FilterSameSide(nodes, side)
        hooks = BuildHookContextsAtL(same, side, L)
        max_branch_len = MaxBranchLength(hooks)

        if max_branch_len <= 4:
            return NormalizeAndClassify(hooks, L)

        L = NextHigherL(L)

    return MarkUnresolved(BuildHookContextsAtL(same, side, max_L))
```

Important: increasing L requires rebuilding nodes and branches. Do not just remove extra branch nodes.

## 5. Building Hook contexts at one L

For every possible active same-side node, including the latest pending node when enabled:

```text
function BuildHookContextForActive(active_index):
    active = same[active_index]
    floor_or_ceiling_index = FindOriginBoundary(active_index)

    if floor_or_ceiling_index < 0:
        return no bounded hook

    span = same[floor_or_ceiling_index + 1 ... active_index]
    boundary = same[floor_or_ceiling_index]

    branches = ExtractBranches(span, boundary, side)

    if branches is empty:
        return developing empty context or skip according to config

    return HookContext(boundary, active, span, branches)
```

The boundary itself is not counted as an internal branch number.

## 6. Finding the origin boundary

### 6.1 Low-side Hook

```text
function FindLowHookFloor(active_index):
    active_price = same[active_index].price

    for i = active_index - 1 downto 0:
        if same[i].price < active_price:
            return i

    return -1
```

### 6.2 High-side Hook

```text
function FindHighHookCeiling(active_index):
    active_price = same[active_index].price

    for i = active_index - 1 downto 0:
        if same[i].price > active_price:
            return i

    return -1
```

Equality is ignored. Equality is not lower, higher, or a break.

## 7. Branch extraction model

A Hook span can contain multiple internal branches.

The algorithm uses right-to-left discovery and old-to-new labeling.

### 7.1 Conceptual low-side example

Given low nodes in a Hook span, old to new:

```text
A, B, C, D, E, F
```

The active low is `F`.

Branches are discovered by starting from active/right nodes and scanning backward for same-side nodes that belong to a branch until a lower-low splitter is encountered.

The splitter does not delete the previous branch. It closes one branch and becomes a boundary for constructing the next branch path.

### 7.2 Branch object

Each branch must store:

```text
branch_id
side
L
hook_id
boundary_node_id
resolve_node_id
counted_node_ids[]
counted_node_prices[]
counted_node_times[]
count = ArraySize(counted_node_ids)
oldest_counted_node_id
newest_counted_node_id
retracement_ratio
passes_retracement
is_nd_qualified
uses_pending_node
```

## 8. Reference branch extraction pseudocode

The following pseudocode is intentionally explicit. It is designed for deterministic implementation, not speed.

### 8.1 Comparator helpers

```text
For LOW side:
    IsBoundaryBreak(candidate, reference) = candidate.price < reference.price
    IsJoinable(candidate, reference)      = candidate.price > reference.price

For HIGH side:
    IsBoundaryBreak(candidate, reference) = candidate.price > reference.price
    IsJoinable(candidate, reference)      = candidate.price < reference.price
```

### 8.2 Extract branches

```text
function ExtractBranches(span, boundary, side):
    # span is old-to-new, excludes boundary, includes active node
    branches = []
    n = len(span)

    if n <= 0:
        return branches

    # Build branch paths by using every right anchor as a possible branch resolver.
    # This preserves multiple internal Hook sequences.
    for right = n - 1 downto 0:
        branch = []
        reference = span[right]
        branch.append(reference)

        for left = right - 1 downto 0:
            candidate = span[left]

            if IsJoinable(candidate, reference, side):
                branch.append(candidate)
                reference = candidate
                continue

            if IsBoundaryBreak(candidate, reference, side):
                # candidate splits this branch path.
                # The branch is closed before the splitter.
                break

            # Equal or structurally neutral nodes do not join and do not split.
            continue

        branch_old_to_new = Reverse(branch)

        if not BranchAlreadyExists(branches, branch_old_to_new):
            branches.append(branch_old_to_new)

    return SortBranchesOldToNew(branches)
```

This algorithm intentionally permits several branches in one Hook. The active node can participate in several branches if different older branch paths resolve into it.

### 8.3 Branch deduplication

Two branches are duplicates only if their counted node identities are exactly identical.

Price similarity is not enough.

Time similarity is not enough.

Node identity matters.

## 9. Branch numbering

After a branch is extracted, numbers are assigned old-to-new.

```text
for k in 0 .. branch.count - 1:
    label_number = k + 1
```

Examples:

```text
count = 2 -> labels 1,2
count = 3 -> labels 1,2,3
count = 4 -> labels 1,2,3,4
```

A branch with count 2 is not ND.

A branch with count 3 or 4 can become ND if it passes retracement.

A branch with count 5 or more is invalid at this L and triggers L escalation.

## 10. Cycle retracement computation

### 10.1 Low-side Hook

```text
hook_floor_price = boundary.price
cycle_extreme = highest HIGH node or candle high between boundary time and branch resolve time
final_node_price = branch.newest_counted_node.price
range = cycle_extreme - hook_floor_price
retraced = cycle_extreme - final_node_price
ratio = retraced / range
```

The branch passes default retracement if:

```text
ratio > 0.50
```

If `range <= 0`, the branch cannot pass semantic ND.

### 10.2 High-side Hook

```text
hook_ceiling_price = boundary.price
cycle_extreme = lowest LOW node or candle low between boundary time and branch resolve time
final_node_price = branch.newest_counted_node.price
range = hook_ceiling_price - cycle_extreme
retraced = final_node_price - cycle_extreme
ratio = retraced / range
```

The branch passes default retracement if:

```text
ratio > 0.50
```

## 11. Classifying branches

```text
if count <= 2:
    status = DEVELOPING_HOOK_BRANCH
    is_nd_qualified = false

if count == 3 or count == 4:
    if passes_retracement:
        status = ND_BRANCH
        is_nd_qualified = true
    else:
        status = HOOK_BRANCH_BELOW_RETRACE_THRESHOLD
        is_nd_qualified = false unless below-threshold mode is enabled

if count > 4:
    status = OVEREXTENDED_BRANCH
    force_adaptive_L = true
```

## 12. Classifying the Hook container

```text
if any branch.count > 4:
    hook.status = NEEDS_HIGHER_L

else if any branch.is_nd_qualified:
    hook.status = ND

else if any branch.count >= 1:
    hook.status = DEVELOPING_HOOK

else:
    hook.status = EMPTY_OR_UNBOUNDED
```

## 13. Rendering event emission

The Hook engine should emit structured events, not chart objects.

Expected events:

```text
HOOK_CONTEXT
HOOK_BRANCH
ND_BRANCH
HOOK_NUMBER_LABEL
HOOK_ARC
HOOK_DEBUG_LABEL
```

The renderer chooses which to draw based on inputs.

The engine must include enough metadata to prove why each branch exists.

## 14. Required audit fields

Every emitted Hook / ND event should include:

```text
hook_id
branch_id
side
L
base_L
final_L
boundary_node_id
active_node_id
counted_node_ids
counted_node_prices
counted_node_times
branch_count
max_branch_count_in_hook
adaptive_L_iterations
retracement_ratio
passes_retracement
uses_pending_node
reason
```

## 15. Safety rules

The implementation must reject these incorrect behaviors:

1. Drawing `ND` for a 1-node or 2-node branch.
2. Keeping a 5-node branch without increasing L.
3. Counting highs inside low-side Hook branch numbers.
4. Counting lows inside high-side Hook branch numbers.
5. Using close price for Hook branch qualification.
6. Treating equality as a break.
7. Rendering a Hook branch that the Hook engine did not emit.

## Phoenix code alignment note - branch-sequence implementation

The Phoenix code patch that follows this document replaces the earlier alternating-window hook scanner with the same-side branch sequence engine described here.

Implementation consequences:

1. A low-side hook is built from LOW nodes only. Opposite HIGH nodes are used only to find the cycle extreme for retracement and arc drawing.
2. A high-side hook is built from HIGH nodes only. Opposite LOW nodes are used only to find the cycle extreme for retracement and arc drawing.
3. Counted hook branches are strict adverse staircases:
   - low-side branch: each newer LOW must be strictly lower than the previous counted LOW;
   - high-side branch: each newer HIGH must be strictly higher than the previous counted HIGH.
4. Equality is ignored and never extends or validates a counted branch.
5. A branch with 3 or 4 counted same-side nodes can qualify as ND after the retracement rule is satisfied.
6. A same-side run with more than 4 counted nodes is not emitted at that L. It must be represented by a higher-L compressed node view.
7. The renderer displays the branch numbers on the counted same-side nodes and renders the ND label as `ND Lx #n`, where `n` is the counted-node count.
8. Main chart labels are registered through a time/price cluster stacker so older labels stay closer to price and newer labels are pushed into deterministic lanes.

## 16. Implementation repair note

The Phoenix implementation now follows this bounded-context algorithm directly. The old failure mode was treating same-side runs as global structures. That could emit many ND arcs while starving the F engine of usable phase origins. The repaired implementation evaluates every active same-side node as a potential bounded Hook context, finds the nearest strict floor/ceiling boundary, extracts branches only inside that span, rejects over-four-node contexts at the current L, and uses the Hook resolve node as the F1 phase boundary.

Main-chart Hook rendering is also curated by default: only Hook branches whose resolve node seeds a visible F1 are drawn, while full Hook rendering remains available through the experiment input layer.
