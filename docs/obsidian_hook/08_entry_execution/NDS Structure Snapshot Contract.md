# NDS Structure Snapshot Contract

## Source

The Entry transition reads the exact `FP_HookPhase02Sequence` array after F3 ownership and valid-family annotation. It does not infer structure from chart objects.

## Evidence retained

```text
sequence_id
scale_l
Hook direction
validity family
post-F3 subfamily
Hook-after-Hook parent
opposing-F3 owner and terminal
origin
crown
terminal/resolve
death boundary
completion percentage
closure and failure state
```

## Default eligibility gate

```text
valid_hook_family = true
sequence.valid = true
hook_failed = false
cycle_closed = true
```

## Current selection policy

One current pipeline row selects the latest eligible sequence by decision timestamp and sequence ID tie-breaker. This is not the final opportunity registry. The future registry must preserve all eligible structures and deduplicate by deterministic identity.

## Related

- [[NDS Setup State Machine]]
- [[NDS Entry Audit Outputs]]
