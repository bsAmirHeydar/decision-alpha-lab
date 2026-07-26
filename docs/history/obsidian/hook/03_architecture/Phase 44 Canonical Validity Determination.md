# Phase 44 — Canonical Validity Determination

Phase 44 annotates structural Hook sequences with validity-family fields.

Fields:

- `valid_after_hook`
- `valid_after_opposing_f3`
- `valid_hook_family`
- `hook_validity_family`
- `previous_hook_sequence_id`
- `previous_hook_terminal_node_id`
- `opposing_f3_event_id`

Renderer layers should consume these fields. They should not recreate validity independently.
