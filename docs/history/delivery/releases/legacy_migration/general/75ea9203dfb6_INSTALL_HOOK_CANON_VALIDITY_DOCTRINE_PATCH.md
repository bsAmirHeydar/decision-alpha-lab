# Install — Hook Canon Validity Doctrine Patch

From the project root in PowerShell:

```powershell
Expand-Archive -Path .\alpha_lab_hook_canon_validity_doctrine_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_hook_canon_validity_doctrine_patch.zip
```

Then review:

```text
00_HOOK_CANON_VALIDITY_DOCTRINE_START_HERE.md
```

Recommended Obsidian entry:

```text
docs/obsidian_hook/00_mocs/HOOK_CANON_MOC.md
```

## Suggested commit

```powershell
git add 00_HOOK_CANON_VALIDITY_DOCTRINE_START_HERE.md `
        README_HOOK_CANON_VALIDITY_DOCTRINE_PATCH.md `
        INSTALL_HOOK_CANON_VALIDITY_DOCTRINE_PATCH.md `
        docs/nds_hook_architecture `
        docs/obsidian_hook

git commit -m "docs(hook): add canonical valid hook doctrine" -m "Add the canonical Hook validity documentation and Obsidian knowledge layer.

This documentation defines the production-valid Hook families, Hook-after-F3 validity, Hook-after-Hook validity, terminal semantics, valid-only rendering policy, node/sequence label visibility, and the implementation contract for the next MQL5 patch.

Production-valid Hook families:
- Hook After Opposing F3
- Hook After Hook

When Hook-2 is valid by Hook-after-Hook, Hook-1 is rendered as the required parent companion with full detail.

Valid-only production view must render only valid Hook cycles and the node/sequence labels belonging to those visible Hook cycles. If no valid Hook exists, it draws nothing.

Documentation-only. No MQL5 logic, F-counting logic, Rally logic, Zone logic, execution behavior, broker behavior, order sending, risk sizing, or live trading behavior is changed." 
```
