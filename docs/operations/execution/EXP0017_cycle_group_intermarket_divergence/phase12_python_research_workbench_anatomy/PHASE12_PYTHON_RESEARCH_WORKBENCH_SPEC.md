# Phase 12 Python Research Workbench Specification

## Purpose

Phase 12 externalizes the research layer so the project can move beyond MQL5 CSV production into reproducible Python research.

The goal is not to create a complex machine-learning model yet. The goal is to create a disciplined research surface that can inspect whether the Phase 11 out-of-sample structure is stable, fragile, or insufficient.

## Research tasks

1. Audit the Phase 10 and Phase 11 datasets.
2. Build out-of-sample bucket leaderboards.
3. Measure bucket stability across folds.
4. Inspect simple feature drift between model dataset rows and walk-forward prediction rows.
5. Produce HTML and markdown reports for human review.
6. Maintain an experiment registry template.

## Doctrine

Reports are evidence. They are not rules.

A candidate bucket can be added to the research shortlist, but it cannot become a live filter or execution permission without a later explicit promotion phase.
