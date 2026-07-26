# Operator Runbook

Apply the ZIP from repository root, verify ZIP SHA-256, expand atomically, remove the ZIP, compile Python modules, validate schemas, run static validation, verify the inventory package, execute direct and bounded regression tests, stage exactly the file index, check staged-path equality, commit with the supplied message and push.

Do not manually edit generated inventory artifacts. Rebuild them through the LCM-11A service when source inputs or upstream handoff change.
