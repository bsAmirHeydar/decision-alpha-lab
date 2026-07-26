# Install — Canonical F-Logic Integration Patch

Place the zip file in the project root and run:

```powershell
Expand-Archive -Path .\alpha_lab_f_canonical_logic_integration_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_f_canonical_logic_integration_patch.zip
```

Then open Obsidian and start here:

```text
00_CANONICAL_F_LOGIC_INTEGRATION_START_HERE.md
```

Suggested commit:

```powershell
git add 00_CANONICAL_F_LOGIC_INTEGRATION_START_HERE.md `
        README_CANONICAL_F_LOGIC_INTEGRATION_PATCH.md `
        INSTALL_CANONICAL_F_LOGIC_INTEGRATION_PATCH.md `
        docs/zone_af `
        docs/obsidian_zone

git commit -m "docs(zone): bind zone logic to canonical F-counting definitions" -m "Add documentation and Obsidian notes locking the Zone-AF layer to the existing canonical F1/F2/F3 logic.

This patch clarifies that F logic must come from the Flag Counting canon and Phoenix implementation, while Zone-AF only interprets canonical F events as movement constraints, reversal-potential fields, parent zones, and child-zone refinement requirements.

It prevents future Zone documentation, training notes, and patches from inventing parallel F definitions.

Documentation-only. No trading logic, MQL5 code, Python code, execution behavior, or registry semantics are changed."
```
