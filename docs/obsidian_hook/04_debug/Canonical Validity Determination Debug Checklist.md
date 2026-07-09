# Canonical Validity Determination Debug Checklist

Use this when valid-only view shows too many or too few Hooks.

## CSV fields

Check `hook_phase02_sequences.csv`:

- `valid_after_hook`
- `valid_after_opposing_f3`
- `valid_hook_family`
- `hook_validity_family`
- `previous_hook_sequence_id`
- `previous_hook_terminal_node_id`
- `opposing_f3_event_id`

## Expected families

- `HOOK_AFTER_HOOK`
- `HOOK_AFTER_OPPOSING_F3_TERMINAL`
- `HOOK_AFTER_HOOK_AND_OPPOSING_F3_TERMINAL`

## If too few post-F3 Hooks appear

Check whether Hook origin price matches the F3 terminal endpoint.

## If too many post-F3 Hooks appear

Check whether a historical F3 is validating later non-terminal Hooks. This should not happen after Phase 44.

## If Hook-after-Hook is missing

Check whether Hook-2 origin node id equals Hook-1 structural terminal node id.
