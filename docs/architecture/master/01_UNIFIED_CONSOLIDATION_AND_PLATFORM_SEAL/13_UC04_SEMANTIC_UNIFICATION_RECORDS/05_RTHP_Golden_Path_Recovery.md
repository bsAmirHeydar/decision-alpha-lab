---
id: UCPS-6A3236854A93
title: "RTHP Golden Path Recovery"
type: recovery-record
status: accepted
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-27
updated: 2026-07-27
tags:
  - consolidation
  - uc04
  - rthp
---
# RTHP Golden Path Recovery

## Failure after physical relocation

RTHP packages and tests still constructed paths under former Strategy Factory, ACL registry and documentation roots. The authored source remained semantically valid, but generated evidence, registration digests and one-click activation bindings no longer matched the accepted topology.

## Recovery actions

- train and MT5 activation discover the repository through the canonical path authority;
- authored and generated context roots resolve through typed `RepositoryPaths` properties;
- ACL policy modules use canonical historical registry roots;
- repository-local runs are permitted only under `.alpha/runs`;
- three ACL03 source files whose only changes were relocated path references are covered by a source-snapshot relocation amendment;
- ACL03 compiled artifacts and acceptance receipt were regenerated through the existing compiler;
- AI-input registrations and self-digests were deterministically rebuilt;
- UC-01 and UC-03 historical evidence is preserved through digest-bound amendments rather than overwritten.

## Verification boundary

The accepted suite covers:

- RTHP Context;
- RTHP AI Input;
- RTHP Train Activation;
- RTHP MT5 Activation;
- UC-01, UC-02 and UC-03 consolidation continuity.

Result: `166 passed, 7 skipped`.

## Preserved semantics

No RTHP Context rule, feature definition, task reference, label contract, Train Engine algorithm, order path or capital authority changed in W0.
