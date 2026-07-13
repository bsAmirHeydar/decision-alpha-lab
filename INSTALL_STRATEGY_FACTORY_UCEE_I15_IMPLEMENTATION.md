# Install UCE-I15 Patch

1. Place the ZIP in Downloads.
2. Expand it into the repository root.
3. Remove the ZIP after successful expansion.
4. Run the I15 tests and delivery validation.
5. Stage only paths listed in `UCEE_I15_FILE_INDEX.txt`.
6. Commit with the supplied message and push.

The patch does not stage unrelated repository changes. Fixture evidence is intentionally classified as reference-only. MetaEditor compilation must be run locally with `compile_uce_i15_context_tournament.ps1`.
