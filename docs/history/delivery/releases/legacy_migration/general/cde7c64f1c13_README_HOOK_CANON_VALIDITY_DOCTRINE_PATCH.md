# Hook Canon Validity Doctrine Patch

This patch adds the definitive English documentation and Obsidian knowledge layer for the Alpha Lab Hook validity model.

It resolves the ambiguity around:

- what a valid Hook is;
- when a Hook after F3 is valid;
- when a Hook after Hook is valid;
- how positive and negative Hook terminals are defined;
- what valid-only rendering must show;
- what must be hidden in valid-only mode;
- how node labels, sequence labels, and cycle arcs must be filtered.

## Scope

Documentation only.

No code is changed.

## Important doctrine

A Hook is production-visible only if it belongs to one of these two families:

1. **Hook After Opposing F3**  
   A Hook formed from the terminal area of the most recent opposing F3.

2. **Hook After Hook**  
   A second Hook of the same kind whose origin starts from the terminal/death-near area of a completed previous Hook cycle.

When Hook-2 is valid by the Hook-after-Hook rule, Hook-1 must also be rendered with full detail as its parent companion.

## Install

Expand this patch into the project root.

```powershell
Expand-Archive -Path .\alpha_lab_hook_canon_validity_doctrine_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_hook_canon_validity_doctrine_patch.zip
```

Then open:

```text
00_HOOK_CANON_VALIDITY_DOCTRINE_START_HERE.md
```

or in Obsidian:

```text
docs/obsidian_hook/00_mocs/HOOK_CANON_MOC.md
```
