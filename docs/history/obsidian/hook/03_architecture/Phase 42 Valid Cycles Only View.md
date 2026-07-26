# Phase 42 Valid Cycles Only View

The Hook renderer now follows a strict production selection contract:

1. Build all Hook sequences structurally.
2. Annotate valid Hook families.
3. Select only valid Hook origin groups for rendering.
4. Expand with parent companion only for Hook-after-Hook.
5. Draw arcs, nodes, and labels only for the selected groups.
6. Do not fall back to structural hooks unless the debug fallback input is manually enabled.
