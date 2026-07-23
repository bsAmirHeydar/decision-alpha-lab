# Installation

This release is already committed as `3ce5f6140` in the repository. The ZIP is
an export artifact and can be expanded independently; it does not require the
previous uncommitted 1.0.2 paths or any unrelated ZIP files.

From the repository root, use a new destination directory:

```powershell
$destination = Join-Path $env:TEMP ("alpha-lab-rthp-expand-" + [guid]::NewGuid().ToString("N"))
Expand-Archive -LiteralPath .\ALPHA_LAB_RTHP_MT5_GOVERNANCE_DRIFT_RECOVERY_PATCH.zip -DestinationPath $destination
Get-ChildItem -LiteralPath $destination -Recurse -File
```

The four unrelated ZIP files referenced by older recovery installers are not
part of this release and must not be required for expansion. If an older
installer reports `Preserved unrelated ZIP files path mismatch`, use this
standalone expansion command or the matching installer for that older release.
