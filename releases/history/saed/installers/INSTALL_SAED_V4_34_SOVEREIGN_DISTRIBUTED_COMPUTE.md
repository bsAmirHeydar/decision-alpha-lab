# Install SAED V4-34

1. Place the ZIP patch in the repository root.
2. Expand it into the repository root with overwrite enabled.
3. Remove the ZIP from the repository root.
4. Run full QA and delivery validation.
5. Stage only the paths listed in `SAED_V4_34_FILE_INDEX.txt`.
6. Validate the staged diff, commit using `COMMIT_MESSAGE.md`, and push.

The patch expects V4-33 to have already been installed. All changes are additive except the canonical V4-34 roadmap note, which is expanded in place.
