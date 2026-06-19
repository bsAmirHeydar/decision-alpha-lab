# Decision Alpha Lab project layout

This repository has one canonical root:

```text
decision-alpha-lab/
```

The repository must **not** contain another tracked project copy under:

```text
decision-alpha-lab/decision-alpha-lab/
```

## Canonical source paths

```text
mql5/Experts/DecisionAlphaLab/Execution/
mql5/Include/DecisionAlphaLab/Execution/
docs/execution/
lab/04_execution/
```

All execution code, include files, and execution documentation must be edited in the canonical root paths above.

## Why nested project copies are banned

A nested `decision-alpha-lab/` directory creates two competing source trees. That causes:

- patch context drift;
- MetaEditor compiling one copy while Git shows changes in another copy;
- duplicate include paths;
- stale execution modules surviving after a release update;
- false confidence that a fix was applied when the terminal is still reading the old file.

## Cleanup rule

If a nested project copy exists, back it up once, remove it, and commit the deletion:

```powershell
Compress-Archive -Path .\decision-alpha-lab -DestinationPath .\_backup_nested_decision_alpha_lab.zip -Force
Remove-Item .\decision-alpha-lab -Recurse -Force
git add -A
```

The backup zip is a temporary safety artifact and should not be committed.
