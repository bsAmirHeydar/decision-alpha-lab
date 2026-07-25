# Install UC-01

Use the governed PowerShell command distributed with the release response.

The command first verifies a clean repository, materializes Git LFS, and protects the exact pre-patch `HEAD` with an immutable tag, archive branch, verified Git bundle and materialized source archive. Only after that protection succeeds does it overlay the static patch containing the UC-01 implementation and eleven bounded syntax restorations.

It then captures the repository baseline in six resumable scanner steps, produces the post-repair source archive, executes the recovery drill and qualification matrix, evaluates non-compensatory gates, verifies the generated baseline and stages the exact generated commit index.

Do not manually create or edit baseline outputs. Do not run UC-02 unless the generated stage exit decision is `ACCEPTED`.
