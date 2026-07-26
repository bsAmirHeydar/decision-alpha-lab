# Hook / ND Branching V1

This experiment now has a dedicated Hook / ND branch-sequence specification.

Read these documents before modifying Hook / ND code:

- `docs/flag_counting/phoenix_rebuild/hook_nd_branching/README.md`
- `docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1.md`
- `docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_ALGORITHM_V1.md`
- `docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_VISUALIZATION_AND_LABEL_LAYOUT_V1.md`
- `docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_IMPLEMENTATION_CHECKLIST_V1.md`

The key correction is that Hook / ND is not a raw 3-node or 4-node window. A Hook can contain many internal branch sequences. The branch count is unlimited. The internal counted nodes inside each branch must be reduced to at most four through adaptive L. ND exists only when at least one branch has exactly three or four counted nodes and passes the retracement rule.
