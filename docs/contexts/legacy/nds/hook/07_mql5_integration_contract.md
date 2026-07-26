# 07 — MQL5 Integration Contract

## Purpose

This file defines the implementation boundary for adding Hook display to the central expert.

## Input Contract

Recommended display selector:

```text
enum NDS_DisplayFamily
{
    NDS_DISPLAY_RALLY_ONLY = 0,
    NDS_DISPLAY_HOOK_ONLY = 1,
    NDS_DISPLAY_RALLY_AND_HOOK = 2
};
```

Recommended default:

```text
InpNDSDisplayFamily = NDS_DISPLAY_RALLY_ONLY
```

## Preservation Rule

Rally-only mode must not call Hook rendering in a way that changes existing F-counting behavior.

## Hook Calculation Contract

The Hook calculator should receive:

```text
structural peak nodes
structural valley nodes
bar times
high/low prices
L settings
max nodes per sequence
scan range
```

It should output:

```text
CycleHook records
Sequence records
X nodes
Y extremes
closure state
ND state
death state
Hook type
```

## Hook Renderer Contract

The renderer should only draw.

It must not decide trades.

It must not create orders.

It must not modify risk.

## Namespacing

Every Hook chart object must use a unique prefix.

Suggested root:

```text
NDS_HOOK_
```

## Audit Contract

Optional CSV rows should be generated only when enabled.

Suggested rows:

```text
hook_sequence_row
hook_closure_row
hook_type_row
hook_state_row
```

## Failure Policy

If Hook calculation fails:

```text
do not affect Rally/F-counting
clear Hook objects if needed
print diagnostic warning
continue expert runtime
```

## No Execution Boundary

This integration must not add:

```text
OrderSend
OrderCheck
CTrade
broker requests
risk sizing
volume sizing
live trading behavior
```
