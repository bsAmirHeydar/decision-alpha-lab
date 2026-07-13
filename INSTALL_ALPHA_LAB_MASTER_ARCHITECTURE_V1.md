# Installation

## PowerShell — expand directly into the repository

```powershell
$Zip = ".\alpha-lab-master-architecture-v1.zip"
Expand-Archive -LiteralPath $Zip -DestinationPath . -Force
```

## Add only the created architecture package to Git

```powershell
git add -- "docs/alpha_lab_master_architecture" "README.md" "INSTALL_ALPHA_LAB_MASTER_ARCHITECTURE_V1.md" "PATCH_MANIFEST.json" "QA_REPORT.json" "COMMIT_MESSAGE.txt"
git commit -m "docs(alpha-lab): add canonical master architecture vault"
```

## Open in Obsidian

Open the following folder as a vault:

```text
docs/alpha_lab_master_architecture
```

Start at:

```text
00_START_HERE/00_Home.md
```
