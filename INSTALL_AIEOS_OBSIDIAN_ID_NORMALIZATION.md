# Installation

Apply the ZIP from the repository root with the supplied PowerShell block. The block creates an external backup ZIP, runs the migration transactionally, requires a second no-op planning pass, executes the vault validator and the complete engineering policy, stages exact paths from generated pathspec files, commits, and pushes.
