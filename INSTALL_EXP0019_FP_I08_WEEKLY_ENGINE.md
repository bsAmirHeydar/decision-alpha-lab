# Install EXP0019 FP-I08 Weekly WW Engine

Apply this patch only after FP-I07 is present.

1. Place the ZIP in the repository root.
2. Expand it into the repository root.
3. Remove the ZIP from the repository root.
4. Stage only paths listed in `EXP0019_FP_I08_FILE_INDEX.txt`.
5. Run the FP-I08 Python and static validation gates.
6. Compile both FP-I08 MQL5 entry points locally in MetaEditor.
7. Commit and push only after the local compile result is clean.

The patch does not alter FP-I00 through FP-I07 implementation files. It updates only the
program registry/task ledger to record completed delivery state and adds FP-I08-owned files.
