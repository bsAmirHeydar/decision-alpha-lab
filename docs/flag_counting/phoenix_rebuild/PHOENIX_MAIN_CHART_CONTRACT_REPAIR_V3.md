# Phoenix Main-Chart Contract Repair V3

This repair re-separates the Phoenix engine into three hard layers:

1. **Structure layer**: F1/F2/F3 two-leg flag bodies are the primary chart structures.
2. **Context layer**: Hook/ND is a phase-boundary/context source. It must never erase valid flag structures.
3. **Presentation layer**: the main chart renders canonical visible structures only; audit labels remain optional.

## Red lines enforced

- Hook/ND cannot be the only source of F roots.
- Hook-derived roots are built first, but raw-origin fail-open roots are also inspected when fail-open is enabled.
- Duplicate visual bodies are hidden after detection, not before the engine has a chance to recover valid F structures.
- F2 can only be emitted from a confirmed F1.
- F3 can only be emitted from a confirmed F2.
- A body smaller than the F2/F1 size contract is not a main-chart F2 and cannot parent F3.
- A hidden root hides its descendants, so orphan F2/F3 objects cannot remain on chart.
- Hook counted-node numbers and internal 1/2/3/4 labels are audit information and are disabled by default.
- Same-direction chain pruning is available as an experiment, but is off by default in the research chart so it cannot hide later valid flags.

## Main chart defaults

The default chart is now meant to answer: **where are the visible F structures?**

Default rendering therefore keeps:

- colored F1/F2/F3 body geometry,
- concise F labels,
- gray Hook/ND arcs only when they seed a visible F1,
- no Hook branch numbers,
- no internal count labels,
- no origin-only labels,
- no detailed O/A/W/B text unless explicitly enabled.

## Audit mode

For audit/debug, manually enable:

- `InpDetailedLabels = true`
- `InpShowParentIds = true`
- `InpShowOriginLabels = true`
- `InpShowInternalLabels = true`
- `InpShowHookCountLabels = true`
- `InpVerboseAuditLogs = true`

This mode intentionally becomes dense; it is not the main-chart contract.

## Canonicalization

After all scale passes, Phoenix now canonicalizes visible structures:

- exact semantic duplicates are hidden,
- near-identical visual bodies across L-scales are hidden,
- duplicate F1 root sequences hide the whole losing sequence,
- descendants without a visible parent are hidden,
- local/lower-L structures are preferred when semantic quality is equal,
- phase-boundary roots are preferred over fail-open roots when geometry is equivalent.

This keeps raw research coverage high while preventing the renderer from becoming a gray/number dump.
