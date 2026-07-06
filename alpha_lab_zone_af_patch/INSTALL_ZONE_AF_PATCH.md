# Install Zone AF Patch

1. Place `alpha_lab_zone_af_patch.zip` in the root of your repository.
2. Run:

```powershell
Expand-Archive -Path .\alpha_lab_zone_af_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_zone_af_patch.zip
```

3. Open Obsidian.
4. Choose `Open folder as vault`.
5. Select the repository root folder.
6. Open:

```text
00_ZONE_AF_START_HERE.md
```

