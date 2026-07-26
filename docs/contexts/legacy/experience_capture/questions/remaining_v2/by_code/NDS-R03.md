# NDS-R03 — Node Identity, Node Cluster, and Node Replacement

## Why This Question Remains

L2 and anchor nodes are defined, but node identity across time and clusters is still unclear.

## What Has Already Been Answered

Do not repeat or overwrite the captured answers.

Answered codes that must remain untouched:

```text
BASE-01
BASE-02
BASE-03
BASE-04
BASE-05
BASE-06
EXT-01
EXT-02
EXT-03
EXT-04
EXT-06
EXT-07
EXT-08
EXT-09
EXT-10
EXT-11
EXT-12
```

## Answer Requirements

- When do two nearby nodes remain separate nodes?
- When should nearby nodes be grouped into a cluster?
- When does a node keep its identity after price moves away?
- When is a node consumed, invalidated, replaced, merged, or archived?
- What is the difference between origin node, anchor node, destination node, and internal node?
- Should node clusters have their own IDs separate from node IDs?

## Expected Output

```text
`node_identity_and_cluster_policy_v1`.
```

## Answer Storage Convention

When answered, create a separate answer folder:

```text
docs/contexts/legacy/experience_capture/answers/NDS-R03/
  question_en.md
  answer_raw_en.md
  answer_normalized_en.md
  notes_en.md
  manifest.json
  images/
```

## Image Requirement

Use an image only if it clarifies the structure. If an image is provided, store it under the answer folder and mark all relevant NDS objects.
