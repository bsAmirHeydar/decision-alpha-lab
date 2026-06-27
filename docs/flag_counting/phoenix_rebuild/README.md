# Flag Counting Phoenix Rebuild

This package replaces the failed patch-on-patch lineage with a clean engine. The old code must be removed before applying this patch.

The design goal is not to hide complexity. The goal is to make every layer explicit:

1. Node extraction.
2. Hook/ND branch discovery.
3. Two-leg body construction.
4. Post-flag internal counting.
5. F1/F2/F3 sequence orchestration.
6. Renderer-only visualization.
7. Audit-only diagnostics.

## Why the previous attempts failed

The previous implementation failed for four root reasons:

1. Audit events were rendered as chart structures.
2. F1 roots were created from arbitrary two-leg windows instead of phase boundaries.
3. F2/F3 ownership was not hard enough, so children could drift away from their parent context.
4. Strict phase gates were applied before Hook/ND boundary extraction was strong enough, which made the chart empty.

Phoenix fixes the thinking process by making each stage independently inspectable and by keeping fallbacks explicit instead of pretending they are semantic truth.

## Apply policy

Before applying this patch, delete the old FlagCounting code folders and old experts. Use the cleanup commands in the final assistant response or run `tools/cleanup_flag_counting_code.ps1` from the project root.
