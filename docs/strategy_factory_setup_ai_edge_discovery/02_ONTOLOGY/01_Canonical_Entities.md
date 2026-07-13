---
id: SAED-D77FC615F3
title: "Canonical Entities and Identities"
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
  - identity
---

# Canonical Entities and Identities

## Core Entities

| Entity | Meaning | Identity components |
|---|---|---|
| ContextPackage | frozen semantic detector and views | context type/version/code/schema hashes |
| ContextOccurrence | one known-time market state | context package + symbol/time + occurrence key |
| SetupArchetype | exploitation thesis family | context compatibility + direction + trigger class |
| PayoffProfile | constrained economic objective | profile id/version/guardrails |
| EntryMechanism | activation mechanics | order type/trigger/expiry/fill policy |
| TreatmentBundle | complete executable action | all atom ids/parameters/economics versions |
| OpportunityCluster | occurrence plus sibling candidates | occurrence id + cluster policy |
| DatasetLineage | rows, features, targets and folds | source/cutoff/schema/split hashes |
| TrainerArtifact | model and preprocessing | trainer/config/fold/seed/data/code hashes |
| ExperimentLineage | complete selection process | declaration/search/budget/scheduler/compiler hashes |
| PromotionDossier | statistical and operational evidence | universe + reports + signatures |
| PolicyGeneration | manual/AI/hybrid graph | graph/fallback/authority/artifact hashes |

## Rule

Stable identities are content-derived and canonical. Display names are not identities. Any parameter capable of changing a decision must enter identity.
