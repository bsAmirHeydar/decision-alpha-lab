# Phase 48 — Post F3 Hook Recognition

## Architecture intent

Separate F3 detection from post-F3 Hook selection.

The pipeline must be:

```text
F3 detector
→ F3 terminal environment builder
→ post-F3 candidate scanner
→ direct/delayed classifier
→ structural/geometric classifier
→ selected visible set
→ renderer
```

## Candidate classifier

Each candidate needs:

```text
post_f3_family
post_f3_source_f3_id
post_f3_direct_or_delayed
post_f3_structural_or_geometric
post_f3_completion_pct
post_f3_terminal_distance
post_f3_selection_rank
```

## Rendering contract

The renderer should not infer validity from raw labels.

It should render only candidates selected by the post-F3 selection layer.
