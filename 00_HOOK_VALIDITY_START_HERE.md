# Hook Validity Layer — Start Here

This patch adds the formal English documentation and Obsidian knowledge layer for the **Hook Validity Layer** of Alpha Lab.

The central idea is simple and strict:

> Not every hook-like structure is valid. Because market structure is fractal, hooks can be counted in too many ways. Without a validity filter, the system becomes noisy, inconsistent, and over-fitted. Therefore, only two hook families are considered structurally valid for zone generation.

## The Two Valid Hook Families

1. **Hook After Hook**  
   A second hook is valid only when its starting node is exactly the terminal node of the previous hook. The last node of Hook-1 must become the first node of Hook-2.

2. **Hook After Opposing F3**  
   A hook is valid after an opposing F3 sequence. For example, after a bearish F3 is completed/printed, a following bullish hook becomes structurally meaningful because it emerges from the exhaustion or broad reversal field created by the opposing F3.

## Core Rule

> Only these valid hook families may generate tradable hook zones. Other hook-like structures may be observed, but they must not be trusted as primary zone sources.

Start reading here:

- [[docs/hook_validity/HOOK-VAL-0001_Valid_Hook_Philosophy_and_Filtering_Policy|HOOK-VAL-0001 — Valid Hook Philosophy]]
- [[docs/hook_validity/HOOK-VAL-0002_Hook_After_Hook_Chained_Node_Architecture|HOOK-VAL-0002 — Hook After Hook]]
- [[docs/hook_validity/HOOK-VAL-0003_Hook_After_Opposing_F3_Architecture|HOOK-VAL-0003 — Hook After Opposing F3]]
- [[docs/hook_validity/HOOK-VAL-0004_Invalid_Hooks_and_Fractal_Noise_Control|HOOK-VAL-0004 — Invalid Hooks and Fractal Noise]]
- [[docs/obsidian_hook/00_mocs/HOOK_VALIDITY_MOC|Obsidian Hook Validity MOC]]
