# M0001 Revisit Extreme Reset

## Decision

A revisited live node is not measured forever from the original node origin.

After a confirmed revisit in HUNT mode, the node remains alive with memory, but
its next expansion/territory cycle resets.

```text
confirmed REV#0
-> node remains alive
-> confirmed_touch_count = 1
-> next_revisit_id = 1
-> tracking_cycle_start = bar after REV#0 confirmation
-> next expansion_extreme is measured from tracking_cycle_start
```

## Why

The node is still the same structural node, but the market has already tested its
territory. For the next revisit, we want to know the expansion from the last
confirmed visit forward, not from the original node candle.

```text
same node identity
same node price
same memory
fresh post-visit expansion cycle
```

## First cycle

Before any confirmed revisit:

```text
tracking_cycle_start = active_from_index
expansion_extreme = extreme since active_from
```

## After each confirmed revisit in HUNT mode

When:

```text
outside_count >= exit_gap
```

the visit is confirmed. If the node is not consumed:

```text
tracking_cycle_start = confirmation_index + 1
tracking_extreme = initial extreme from tracking_cycle_start
```

Then the next territory is built from that reset extreme.

## TOUCH mode

TOUCH mode consumes after the first confirmed touch, so there is no post-touch
revisit cycle. If HUNT happens before confirmation, the node is consumed by HUNT.

## Visual

A revisited live label now includes reset anchor index:

```text
REVISITED LIVE revs=1 next=REV#1 age=37 reset@1234
```

`reset@1234` is the bar index where the current post-visit tracking cycle starts.

## Version

`M0001_LiveVisualLab.mq5` version: `1.42`.
