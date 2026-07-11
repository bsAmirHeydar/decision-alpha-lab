# Artifact Identity and Lineage

Every materialized dataset, prediction table, report, model, fold plan, or replay trace must carry an ArtifactIdentity.

## Required lineage

- artifact type;
- run ID;
- producer and version;
- Git commit;
- strategy and version;
- manifest hash;
- source hash;
- creation timestamp;
- schema identity;
- deterministic artifact ID.

## Immutability

Artifacts are append-only by identity. A corrected artifact receives a new source hash and ID. A model trained on an artifact records that exact ID. Reports cannot claim to describe a dataset without its identity.

## Runtime use

MQL5 will later attach model artifact and plan-generation IDs to every decision. Python will use them to reconstruct the full experiment. This phase establishes the common lineage primitive.
