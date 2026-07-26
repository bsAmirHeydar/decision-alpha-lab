# Pseudocode Reference

This file is intentionally language-neutral. It describes control flow.

## Pass Helpers

```text
PassAbove(price, boundary, eps=0):
  return price > boundary + eps

PassBelow(price, boundary, eps=0):
  return price < boundary - eps
```

## Build Bullish Body

```text
BuildBullishBody(origin_low, nodes):
  leg1 = none
  waist = none
  highest_high = none
  phase = SEEK_LEG1

  for node in nodes after origin_low:
    if phase == SEEK_LEG1:
      if node.side == HIGH:
        highest_high = max_by_price(highest_high, node)
      if node.side == LOW and highest_high exists:
        if PassBelow(node.price, origin_low.price):
          return INVALID
        leg1 = highest_high
        waist = node
        phase = SEEK_LEG2

    else if phase == SEEK_LEG2:
      if node.side == LOW:
        if PassBelow(node.price, origin_low.price):
          return INVALID
        if node.price < waist.price:
          waist = node
      if node.side == HIGH:
        if PassAbove(node.price, leg1.price):
          leg2 = node
          return BODY(origin_low, leg1, waist, leg2)

  return INCOMPLETE
```

## Build Bearish Body

```text
BuildBearishBody(origin_high, nodes):
  leg1 = none
  waist = none
  lowest_low = none
  phase = SEEK_LEG1

  for node in nodes after origin_high:
    if phase == SEEK_LEG1:
      if node.side == LOW:
        lowest_low = min_by_price(lowest_low, node)
      if node.side == HIGH and lowest_low exists:
        if PassAbove(node.price, origin_high.price):
          return INVALID
        leg1 = lowest_low
        waist = node
        phase = SEEK_LEG2

    else if phase == SEEK_LEG2:
      if node.side == HIGH:
        if PassAbove(node.price, origin_high.price):
          return INVALID
        if node.price > waist.price:
          waist = node
      if node.side == LOW:
        if PassBelow(node.price, leg1.price):
          leg2 = node
          return BODY(origin_high, leg1, waist, leg2)

  return INCOMPLETE
```

## F1 State

```text
OnF1Body(body):
  status = LIVE_BODY
  create PostFlagContext after body.leg2

OnPostF1Node(node):
  update context
  update hook branches

  if not context.has_valid_internal_12:
    if same_direction_passes_leg2(node):
      extend F1 leg2
      reset context after new leg2
      return

  if boundary_passes_waist(node):
    invalidate F1
    return

  if context.has_valid_internal_12 and same_direction_passes_leg2(node):
    confirm F1
    authorize F2 from context.deepest_adverse
```

## F2 State

```text
AuthorizeF2(f1):
  origin = f1.post_context.deepest_adverse
  create F2 candidate from origin

OnF2Update(node):
  if origin_passed(node):
    kill F2 candidate
    keep parent F1 context
    rebuild F2 from updated deepest adverse context
    return

  build_or_extend_body()

  if body_exists and flag_size < f1.flag_size:
    status = QUALIFYING
    allow extension

  update post-F2 context

  if waist_break_branch or valid_internal_12:
    if flag_size >= f1.flag_size and same_direction_passes_leg2(node):
      confirm F2
      authorize F3 from context.deepest_adverse
```

## F3 State

```text
AuthorizeF3(f2):
  origin = f2.post_context.deepest_adverse
  create F3 candidate from origin

OnF3Update(node):
  build_or_extend_body()

  if body_exists:
    condA = f3.leg1.L >= 0.80 * f2.leg1.L
    condB = f3.flag_size >= 0.70 * f2.flag_size
    if condA or condB:
      complete F3

  if completed and same_direction_extends(node):
    extend F3

  if completed and first_confirmed_opposite_F1_detected():
    lock F3
    close old chain
    start opposite chain from that F1
```

## Hook Branch High-Level

```text
BuildHookBranches(context, L):
  nodes = adverse_nodes(context, L)
  branches = []

  for latest in reverse(nodes):
    branch = [latest]
    for prev in reverse(nodes before latest):
      if ordering_allows(prev, branch.last):
        branch.append(prev)
      else:
        maybe_start_new_branch(prev)
    branches.add(reverse(branch))

  if max_len(branches) > 4:
    return BuildHookBranches(context, L+1)

  emit branches
```
