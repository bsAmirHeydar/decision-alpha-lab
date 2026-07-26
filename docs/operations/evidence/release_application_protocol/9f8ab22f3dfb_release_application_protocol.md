# Release Application Protocol

This document standardizes how release ZIP/PATCH files should be applied in the project.

---

## User-facing rule

Apply commands should be short and should clean their own release files. They should not include `git status` by default.

---

## ZIP apply block

```powershell
Expand-Archive .\release_files.zip -DestinationPath . -Force

powershell -ExecutionPolicy Bypass -File .\install_release.ps1

Remove-Item .\release_files.zip -ErrorAction SilentlyContinue
Remove-Item .\release.patch -ErrorAction SilentlyContinue
Remove-Item .\install_release.ps1 -ErrorAction SilentlyContinue
```

---

## PATCH apply block

Only use this if the ZIP has not already been applied.

```powershell
git apply --check .\release.patch

git apply .\release.patch

Remove-Item .\release_files.zip -ErrorAction SilentlyContinue
Remove-Item .\release.patch -ErrorAction SilentlyContinue
Remove-Item .\install_release.ps1 -ErrorAction SilentlyContinue
```

---

## Commit rule

Commit only project files:

- source files,
- include files,
- documentation,
- registry updates,
- lab reports.

Do not commit:

- release ZIP files,
- release PATCH files,
- installer scripts,
- temporary backups,
- generated logs unless explicitly intended.

---

## MetaEditor rule

After MQL5 changes:

1. close MetaEditor,
2. apply release,
3. run installer if it syncs terminal-level includes,
4. reopen MetaEditor,
5. compile the changed Experts,
6. only then commit.

---

## Include sync rule

MetaEditor may read terminal-level includes from:

```text
MQL5\Include\DecisionAlphaLab\
```

while the repo may keep source includes in:

```text
Shared Projects\decision-alpha-lab\mql5\Include\DecisionAlphaLab\
```

Installers should sync include files when necessary.
