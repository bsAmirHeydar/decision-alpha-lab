---
id: AIEOS2-4899882D5961
title: "Artifact Identity and Registry"
type: standard
status: active
domain: alpha-lab-standard
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - alpha-lab-standard
---
# Artifact Identity and Registry

Every durable artifact has stable identity, status, version, owner, and links. IDs do not change when titles change. Registry entries are updated atomically with artifact creation, promotion, rejection, or retirement.

Persistent IDs and row keys must be derived from stable components. Random UUIDs may be used only when the identity contract explicitly requires them and reproducibility is not harmed.
