---
id: AIEOS2-A25D63D479EC
title: "Source, Data, and Derived Artifact Separation"
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
# Source, Data, and Derived Artifact Separation

Classify every artifact:

- **Source:** human-authored code/specification/configuration.
- **Input data:** immutable or versioned external observations.
- **Derived evidence:** generated tables, models, reports, caches.
- **Runtime state:** broker/session/process state.
- **Secret:** environment-managed sensitive material.

Derived evidence must be reproducible from source plus declared inputs. Runtime state and secrets never enter source archives by accident.
