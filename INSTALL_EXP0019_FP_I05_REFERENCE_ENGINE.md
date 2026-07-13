# Install FP-I05

Place the patch ZIP in the repository root. Expand it directly into the root, remove the ZIP, validate the phase, stage only paths from `EXP0019_FP_I05_FILE_INDEX.txt`, commit, and push.

## MetaEditor gate

Compile these locally on Windows:

- `mql5/Experts/EXP0019/FaerieProtocol/EXP0019_FP_I05_ReferenceDiagnostic.mq5`
- `mql5/Experts/EXP0019/FaerieProtocolTests/EXP0019_FP_I05_ReferenceSelfTest.mq5`

Static validation is not a successful MetaEditor compile. Preserve compile logs and update phase evidence only after zero errors.

## Rollback

Revert only paths listed in the FP-I05 file index. Retain generated evidence for audit; stale checkpoints are ignored by the restored version.
