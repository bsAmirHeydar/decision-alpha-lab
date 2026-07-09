# Install — gartal terminal Implementation Architecture Patch

Place the zip file in the repository root and run this in PowerShell:

```powershell
Expand-Archive -Path .\gartal_terminal_implementation_architecture_patch.zip -DestinationPath . -Force
Remove-Item .\gartal_terminal_implementation_architecture_patch.zip -Force
```

Then check:

```powershell
git status
```

Recommended commit:

```powershell
git add product_lab/indicators/gartal_terminal/obsidian docs/patches/gartal_terminal_implementation_architecture
git commit -m "docs(gartal-terminal): add implementation architecture obsidian roadmap"
```
