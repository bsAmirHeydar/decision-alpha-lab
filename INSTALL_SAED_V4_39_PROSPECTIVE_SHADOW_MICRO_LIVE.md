# Install SAED V4-39

1. Place the ZIP patch in the repository root.
2. Expand it with overwrite enabled.
3. Remove the ZIP from the repository root.
4. Run V4-39 full QA and delivery validation.
5. Stage only paths listed in `SAED_V4_39_FILE_INDEX.txt`.
6. Check the staged diff, commit with `COMMIT_MESSAGE.md`, and push.

V4-38 must already be installed. The patch intentionally does not fabricate MetaEditor, Terminal, broker, prospective-period or micro-live evidence.
