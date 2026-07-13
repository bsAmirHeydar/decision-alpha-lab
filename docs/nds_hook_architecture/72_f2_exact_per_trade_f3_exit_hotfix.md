# F2 Exact Per-Trade F3 Exit Hotfix

## Scope

This hotfix corrects dynamic F3-retest ownership in the dedicated F2 Waist-Break Point-2 Strategy Tester.

## Defect

Parallel positions could resolve their dynamic target from a broadly compatible confirmed F2. Direction, scale, origin, waist, and parent-waist matching were insufficient to prove that the selected F3 belonged to the trade's own source F2.

## Resolution

The execution context now carries stable F1/F2 lineage and matches the direct child F3 of that source only.

```text
Order/Position identity
→ setup hash
→ source sequence and chain
→ source F1 waist node
→ source F2 origin/waist/body
→ direct child F3 parent relation
→ exact child F3 Waist
→ exact child F3 Leg1 TP
```

Dynamic mode enables the direct child-F3 lifecycle in the shared fast detector. Fixed-target mode remains F1/F2-only.

## Safety

- no latest-F3 lookup;
- no same-direction shared target;
- no cross-position target borrowing;
- ambiguous child relationship fails closed;
- original F2 Leg2 remains the RR authority;
- Hook, renderer, CSV, and AI runtime remain excluded.
