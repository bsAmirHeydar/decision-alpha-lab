# Phase 26 — Hook Documentation vs Code Audit Matrix

## Audit result

| Contract requirement | Previous code state | Phase 26 fix |
|---|---|---|
| Hook / ND branchable; not a single local window | Phase 02 had fixed-origin and rolling-window sequence builders | Replaced with end-backward branch builder |
| Low-side / positive counts valleys | Direction mapping was correct | Preserved and made central to builder |
| High-side / negative counts peaks | Direction mapping was correct | Preserved and made central to builder |
| Labels old-to-new as 1..4 | Visual iterations existed but origin/sequence semantics were inconsistent | X1..X4 are the counted branch labels; origin zero/O is not shown in semantic view |
| Branch length >4 must not be readable | Earlier rolling/promotion could mask over-four state | Over-four branches are rejected from readable output |
| Minimum 1/2 needs strict pass and opposite node between 1 and 2 | Strict pass existed, opposite-between requirement was not enforced | Added opposite node requirement for 1/2 |
| Opposite extreme needed for Hook arc | Later phases had Y logic, Phase 02 visual did not carry a clean crown | Phase 02 now stores `cycle_crown_*` from opposite-side nodes |
| Semantic view must not draw node wiring | Several patches still left line-like paths | Phase 26 semantic renderer only draws Hook envelopes and branch numbers |
| Labels must stack deterministically | Earlier offset was per label and visually unstable | Added deterministic lane stack by time/side/price bucket |
| Peak labels above, valley labels below | Earlier placement could depend on direction only and overlap | Positive/low labels below; negative/high labels above |
| Same branch sequence one color | Some patches colored by node index | Semantic renderer uses sequence palette for branch labels |
| Arc gray/neutral | Patches mixed sequence/arc colors | Semantic renderer uses dim gray arc unless explicitly configured otherwise |

## Known remaining engineering gap

Adaptive-L rebuild is not fully automated in Phase 26. The contract says that if any branch exceeds four counted nodes, the system should increase L and rebuild. Phase 26 rejects over-four branches from readable output and records them as rejected candidates. Full adaptive-L rebuilding should be implemented as a dedicated engine phase after this visual/branch contract is stable.
