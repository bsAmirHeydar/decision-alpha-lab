# Rollback

Use the `INSTALL_STATE.json` path printed by the installer:

`APPLY.ps1 -Action Rollback -RepositoryRoot <repo> -BackupStatePath <state>`

Rollback restores every pre-existing target byte-for-byte and removes paths that did not exist before installation. Native evidence is outside the repository and does not require source rollback.
