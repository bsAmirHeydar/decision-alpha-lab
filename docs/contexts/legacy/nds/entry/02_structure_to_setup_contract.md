---
title: Structure to Setup Contract
status: normative
version: 1.0.0
---
# Structure to Setup Contract

## 1. Source object

The entry-transition layer reads the cached output of Hook Phase 02 after F3 ownership annotation. It does not select a generic visible chart object.

The source record contains:

```text
sequence_id
scale_l
Hook direction
validity family
post-F3 subfamily
Hook-after-Hook parent ID
opposing F3 ID and terminal evidence
origin
crown
terminal/resolve
Death boundary
completion percentage
closure state
failure state
```

## 2. Source eligibility

The default source gate requires:

```text
valid_hook_family = true
sequence.valid = true
hook_failed = false
cycle structurally closed = true
```

These gates are configurable for diagnostic research, but production promotion must preserve strict defaults unless a versioned decision changes them.

## 3. Selection policy

The current transition scaffold selects the latest eligible sequence by decision timestamp, using `resolve_time`, then `last_x_time`, then `origin_time` as fallbacks. Sequence ID is a deterministic tie-breaker.

This is an engineering selection policy for producing one current pipeline row. It is not the final portfolio/opportunity-ranking doctrine. A future Opportunity Registry should retain all eligible structures rather than only the latest one.

## 4. Direction separation

The Hook's positive/negative direction is copied as anatomy evidence. Trade direction is derived only through an explicit policy:

```text
UNRESOLVED
FOLLOW_HOOK
REVERSE_HOOK
```

Default:

```text
UNRESOLVED → block directional Setup
```

This prevents a structural label from silently becoming a buy or sell instruction.

## 5. Setup candidate identity

A Setup candidate is linked to:

```text
source Hook sequence
source Zone contract
trade-direction policy
order model
stop model
target model
creation bar
expiry policy
```

The Setup ID is deterministic for the selected structure. Later versions should include Zone revision and policy version in the ID when canonical Zone lifecycle is implemented.

## 6. Readiness gates

A Setup becomes ready only if:

1. structure is eligible;
2. trade direction is resolved;
3. Zone is available;
4. order model is resolved;
5. stop model is resolved;
6. target model is resolved;
7. the trade contract lock is satisfied.

No RR filter, score, or discretionary ranking is allowed to compensate for a failed hard gate.
