---
id: UCPS-UC01-GRAPHS-232FA57E
title: "Dependency, Consumer and Documentation Graphs"
type: implementation_standard
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - dependency
  - consumers
  - documentation
---
# Dependency, Consumer and Documentation Graphs

UC-01 builds four graph families:

- Python import edges with best-effort internal resolution;
- MQL5 include edges and external imports;
- Obsidian wikilinks and Markdown links;
- raw repository-path references found in source, scripts, configuration and documentation.

The unified consumer inventory does not claim that every external repository, terminal profile or scheduled job has been observed. External scope is recorded separately with a survey contract. Unknown external scope is never silently converted into a no-consumer claim.

Documentation records include note IDs, title, type, status, version, domain, heading count, link counts and frontmatter validity. Duplicate note IDs are preserved as explicit evidence for later consolidation rather than modified during UC-01.
