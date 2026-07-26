---
id: UCPS-UC01-RUNBOOK-0E8D3174
title: "UC-01 Operator Runbook"
type: runbook
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - runbook
  - operator
  - uc-01
---
# UC-01 Operator Runbook

## Preconditions

- repository worktree and index are clean before applying the static patch;
- Git and Git LFS are installed;
- required LFS objects can be materialized;
- sufficient external disk space exists for a complete source archive and Git bundle;
- the command is run from the repository root.

## Governed sequence

```text
verify static patch
→ materialize LFS
→ capture baseline
→ create tag, archive branch, Git bundle and source archive
→ execute isolated recovery drill
→ run qualification
→ finalize non-compensatory decision
→ verify every baseline hash and current-tree parity
→ stage the exact generated commit index
```

## Rerun policy

The baseline directory is immutable. A second capture is refused unless the operator intentionally removes an uncommitted failed baseline and starts again from the unchanged repository. Existing external backup artifacts are reused only when their receipts and hashes still match.
