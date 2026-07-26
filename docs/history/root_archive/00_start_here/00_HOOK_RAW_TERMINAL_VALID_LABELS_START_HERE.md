# Hook Raw Terminal and Valid Labels Fix

This patch fixes two Hook rendering doctrines:

1. A positive Hook visually terminates at the lowest raw price it has actually seen after its crown, not merely at the last confirmed valley node.
2. A negative Hook visually terminates at the highest raw price it has actually seen after its crown.
3. In valid-only mode, production labels must belong only to visible valid Hook groups: immediate Hook after opposing F3, Hook-2 after Hook-1, and Hook-1 only as the required parent companion of Hook-2.

This patch updates Phase 02 to use canonical rates for visual terminal price promotion while preserving structural node ids for Hook-after-Hook continuity.
