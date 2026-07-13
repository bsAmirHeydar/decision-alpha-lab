# Install UCE-I14 Patch

1. Place the ZIP in Downloads.
2. Expand it into the repository root.
3. Remove the ZIP only after expansion succeeds.
4. Run the I14 tests and delivery validation.
5. Stage only paths listed in `UCEE_I14_FILE_INDEX.txt`.
6. Commit with the supplied commit message and push.

The patch does not stage unrelated repository changes. MetaEditor compilation must be run locally with `compile_uce_i14_immutable_runtime.ps1`.
