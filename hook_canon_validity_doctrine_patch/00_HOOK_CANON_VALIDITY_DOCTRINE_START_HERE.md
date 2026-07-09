# HOOK-CANON — Start Here

This patch adds the canonical documentation layer for determining which Hook cycles are production-valid and how valid Hook cycles must be rendered.

This is a **documentation-only** patch. It does not change MQL5 logic, rendering logic, F-counting logic, Rally logic, Zone logic, order execution, risk sizing, or broker behavior.

## Primary entry points

- `docs/nds_hook_architecture/56_hook_validity_master_doctrine.md`
- `docs/nds_hook_architecture/57_hook_sequence_terminal_and_cycle_policy.md`
- `docs/nds_hook_architecture/58_valid_hook_rendering_and_label_policy.md`
- `docs/nds_hook_architecture/59_hook_implementation_contract.md`
- `docs/obsidian_hook/00_mocs/HOOK_CANON_MOC.md`

## Core doctrine

Production-visible Hook cycles must be limited to two families:

1. **Hook After Opposing F3**
2. **Hook After Hook**

When the visible Hook is a Hook-after-Hook child, the parent Hook must also be shown with full detail as the required structural companion.

If no valid Hook exists, valid-only production view must draw nothing.

## Implementation principle

Hook counting remains complete and structural. Hook validity is a later production-view filter. The system should count all structural Hook sequences internally, then select only valid Hook origin-groups for production rendering.
