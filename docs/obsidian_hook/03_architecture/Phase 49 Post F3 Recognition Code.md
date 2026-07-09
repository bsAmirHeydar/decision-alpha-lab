# Phase 49 Post F3 Recognition Code

This phase moves post-F3 recognition from a single direct-terminal structural matcher to a family-aware matcher.

Pipeline:

1. Build Phase02 Hook candidates.
2. Mark Hook-after-Hook families.
3. For each completed/locked F3, resolve the latest terminal endpoint.
4. Scan Phase02 candidates inside the post-F3 ownership window.
5. Classify candidates into direct/delayed and structural/geometric.
6. Select the best candidate according to priority.
7. Mark it as post-F3 valid and export the subfamily.
