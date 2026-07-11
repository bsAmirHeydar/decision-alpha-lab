# ADR 0105 — Contracts Fail Closed

**Status:** Accepted

Invalid identifiers, geometry, causality, type tags, versions, or stable IDs cause rejection. Core contracts do not silently coerce, repair, or guess. Recovery occurs in explicit adapters or quarantine workflows.
