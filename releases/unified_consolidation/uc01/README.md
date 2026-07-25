# UC-01 — Preserve and Baseline

This release implements the first executable stage of the Unified Consolidation and Platform Seal program.

It captures a complete repository artifact inventory, Python and MQL5 symbol surfaces, dependency and consumer graphs, documentation and schema inventories, critical-logic characterization, environment and Git LFS state, external Git/source preservation receipts, an isolated recovery drill and a non-compensatory stage exit decision.

## Bounded baseline stabilization

The first full Python inventory exposed eleven pre-existing files with physically split newline string literals that could not be parsed. The patch restores only those exact literals. The manifest declares all eleven paths as `MODIFY`; every other patch path is `ADD`; deletion remains zero. The governed installer creates the pre-consolidation tag, archive branch, Git bundle and materialized pre-patch source archive before overlaying the repair-bearing patch.

No business logic, trading rule, authority, control-flow branch, identifier, path contract or output schema is changed by these repairs.

## Claim ceiling

This package performs no move, rename, semantic merge, consumer cutover or deletion. It grants no runtime, broker, order or capital authority.

## Authoritative runtime output

After installation, the real repository baseline is generated under:

`registry/consolidation/uc01/baselines/UC01_BASELINE_V1/`

The large external Git bundle, pre-patch source archive and post-repair baseline source archive remain outside Git. Only their receipts and hashes are committed.
