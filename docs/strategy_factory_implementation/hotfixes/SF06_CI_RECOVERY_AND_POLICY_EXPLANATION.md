---
title: SF06 CI Recovery and Engineering Policy Explanation
status: implemented
phase: SF06 hotfix
---

# SF06 CI Recovery and Engineering Policy Explanation

## What the red X means

The GitHub red X is the result of the single `Engineering Policy` GitHub Actions job. It does not mean that Git rejected the commit or that repository history is corrupt. The job checks the complete tree at that commit.

## Why the SF04/SF05 hotfix was still red

The Phase 04/05 hotfix corrected `LongToString(...)` in Phase 04 and Phase 05. Phase 06 had already been committed and still contained three `LongToString(...)` usages. Because the workflow scans the complete repository, the newer hotfix commit still failed on the unchanged Phase 06 files.

## Recovery

This patch:

1. replaces the remaining Phase 06 `LongToString(...)` calls with the repository-approved `IntegerToString(...)` serialization pattern;
2. scopes the Phase 06 no-order-authority unit test to Phase 06-owned modules instead of unrelated legacy programs;
3. makes local and GitHub preflight use one exact command;
4. publishes a readable GitHub Actions summary identifying the failing stage.

## History policy

Old red checks remain attached to old commit snapshots. Do not rewrite or force-push shared history merely to make old rows green. The branch is healthy when the latest corrective commit passes.
