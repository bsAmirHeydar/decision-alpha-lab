# Install FP-I06 Relation and Hunt Engine

## Preconditions

- FP-I00 through FP-I05 are already applied.
- Run from the repository root.
- The FP-I05 store/handoff artifacts must remain unchanged.

## Patch application

```powershell
$Zip = ".\decision-alpha-lab-exp0019-faerie-protocol-fp-i06-relation-engine-v1.0.0.zip"
Expand-Archive -LiteralPath $Zip -DestinationPath . -Force
Remove-Item -LiteralPath $Zip -Force
git add --pathspec-from-file="EXP0019_FP_I06_FILE_INDEX.txt"
git commit -F ".\COMMIT_MESSAGE.md"
git push origin main
```

## Validation

```powershell
& .\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i06\powershell\run_fp_i06_tests.ps1 -RepoRoot $PWD
& .\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i06\powershell\compile_fp_i06.ps1 -RepoRoot $PWD
```

MetaEditor status must remain pending until real compile logs exist.

## Rollback

Remove only files listed in `EXP0019_FP_I06_FILE_INDEX.txt`, restore `COMMIT_MESSAGE.md` from the previous commit if necessary, and return to accepted FP-I05.
