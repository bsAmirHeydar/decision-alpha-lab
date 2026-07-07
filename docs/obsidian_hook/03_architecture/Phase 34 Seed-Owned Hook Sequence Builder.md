# Phase 34 Seed-Owned Hook Sequence Builder

Phase 34 replaces production end-backward overlap enumeration with seed-owned old-to-new extension.

The builder:

1. scopes raw same-side nodes inside a Hook origin boundary context;
2. finds the first non-participated raw node;
3. assigns it as node 1;
4. scans forward to the end of the raw list;
5. accepts strict same-side continuation nodes as 2/3/4/...;
6. marks accepted branch participants;
7. blocks participants from becoming future node 1 seeds.

The renderer can optionally show only valid Hook families.
