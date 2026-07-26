---
id: SAED-FA1EAA317B
title: "Opportunity Cluster and Treatment Siblings"
type: architecture
status: canonical
domain: strategy-factory-setup-ai-edge-discovery
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - strategy-factory
  - setup-factory
  - ai-training
  - ontology
  - clustering
---

# Opportunity Cluster and Treatment Siblings

## Definition

One Context occurrence can generate many candidate Treatments. These rows are counterfactual siblings, not independent observations.

```text
Opportunity Cluster O-1042
├── P1 + Market + Wide Structural Stop + Fixed 1.2R
├── P2 + Breakout + Tight Trigger Stop + 5R Destination
├── P3 + Breakout + Tight Stop + Structural Trail
├── P5 + Limit + Tight Stop + Fixed 1.1R
└── Skip
```

## Statistical Consequences

- siblings stay in the same fold;
- bootstrap resamples opportunity clusters, not candidate rows;
- ranking metrics are computed per opportunity;
- multiplicity counts all candidate variants;
- oracle best-candidate value is descriptive only;
- mutually exclusive fill interactions are documented.

## Data Key

`opportunity_cluster_id` must be deterministic and traceable to Context occurrence and candidate-universe version.
