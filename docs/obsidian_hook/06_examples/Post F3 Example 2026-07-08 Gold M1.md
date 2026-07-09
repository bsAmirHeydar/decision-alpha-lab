# Post F3 Example — 2026-07-08 Gold M1

## Clean screenshot

![[assets/post_f3_example_2026_07_08_clean.png]]

## Annotated screenshot

![[assets/post_f3_example_2026_07_08_annotated.png]]

## User observation

The F3 itself is recognized correctly.

The post-F3 Hook selected by the system is not necessarily the intended Hook.

## Intended candidate families visible in the chart

1. A Hook can start directly from the F3 terminal endpoint.
2. Price can reach/hit the F3 side, rebound upward, and then build a smaller Hook slightly higher.
3. The delayed smaller Hook can be accepted in two different modes:
   - geometric 80% cycle mode, even without full sequence;
   - structural-only mode, only if it has full Hook nodes and sequence closure.

## Documentation decision

This example motivates Phase 48:

- split F3 detection from post-F3 Hook recognition;
- support direct and delayed post-F3 Hook families;
- support explicit mode selection between structural-only and geometric 80% recognition;
- never show all raw sequences in valid-only view.
