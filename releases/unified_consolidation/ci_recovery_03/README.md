# UC04-W1B CI Recovery 01

This hotfix repairs the UC04-W0 Git LFS verification boundary exposed by GitHub Actions. The accepted verifier previously required the working tree itself to contain pointer text. A checkout with valid hydrated LFS objects therefore failed before W1B qualification could run.

The corrected verifier treats the Git blob at `HEAD` as the canonical pointer and accepts either:

- the same pointer in the working tree; or
- a hydrated object whose byte length and SHA-256 match the pointer metadata.

The original UC04-W0 release ledger is not rewritten. Its verifier-path change is admitted through `UC04_W0_RELEASE_AMENDMENT.json`.

No workflow, market concept, MQL5 consumer, execution rule, runtime authority, order authority, capital authority, or production cutover is changed.
