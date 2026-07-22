# Install Hook Validity Patch

Place `alpha_lab_hook_validity_patch.zip` in the root of your project and run:

```powershell
Expand-Archive -Path .\alpha_lab_hook_validity_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_hook_validity_patch.zip
```

Then open the project root as an Obsidian vault and start here:

```text
00_HOOK_VALIDITY_START_HERE.md
```

## Suggested Commit

```powershell
git add 00_HOOK_VALIDITY_START_HERE.md `
        README_HOOK_VALIDITY_PATCH.md `
        INSTALL_HOOK_VALIDITY_PATCH.md `
        docs/hook_validity `
        docs/obsidian_hook

git commit -m "docs(hook): add hook validity and fractal-noise control architecture" -m "Add English documentation and Obsidian knowledge layer for the Alpha Lab Hook Validity Layer.

Includes:
- valid hook philosophy and filtering policy
- Hook After Hook chained-node validity rule
- Hook After Opposing F3 validity rule
- invalid hook and fractal-noise control policy
- hook-zone risk contract documentation
- hook validation dataset and learning policy
- Obsidian MOC, concept notes, policy notes, architecture maps, templates, and canvas diagrams

This commit is documentation-only. It does not change trading logic, execution behavior, MQL5 code, Python research code, registry semantics, or production rules."
```
