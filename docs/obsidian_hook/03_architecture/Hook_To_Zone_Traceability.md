---
type: architecture
title: Hook to Zone Traceability
status: canonical_draft
---
# Hook to Zone Traceability

Every hook-derived zone must be traceable back to its valid hook source.

## Required Trace

```text
zone_id
→ hook_id
→ hook_validity_type
→ previous_hook_id or f3_id
→ node evidence
→ zone boundaries
→ touch event
→ outcome event
```

## Purpose

Without traceability, the system cannot know whether a profitable zone came from a valid hook, invalid hook, opposing F3 context, or arbitrary fractal noise.

Traceability is mandatory for learning.
