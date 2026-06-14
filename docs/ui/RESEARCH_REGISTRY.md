# Research Registry

The Research Registry turns files and artifacts into research entities.

## Entity types

- Observation
- Hypothesis
- Metric
- Experiment
- Analysis
- Validation
- Signal
- Monitoring
- Core module
- Document

## Entity fields

```text
id
entity_type
title
stage_id
status
summary
primary_path
document_paths
relation_ids
tags
capabilities
```

## Discovery

The backend scans:

```text
docs/
registry/
lab/01_observation/
lab/02_hypotheses/
lab/03_experiments/
lab/04_analysis/
lab/05_validation/
lab/06_production/
lab/07_monitoring/
lab/08_archive/
lab/09_execution/
lab/10_infrastructure/
lab/core/
```

Metric artifacts are discovered under:

```text
lab/cache_metrics/
```
