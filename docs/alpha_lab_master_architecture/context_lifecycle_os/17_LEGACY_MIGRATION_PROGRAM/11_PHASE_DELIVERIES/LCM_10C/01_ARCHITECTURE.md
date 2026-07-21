# Architecture

The closure is split into deterministic request fixtures, a pure lifecycle simulator, non-compensatory safety controls, authority-negative adapter proofs, residual-UNKNOWN accounting and an immutable handoff. The simulator never calls a broker adapter. Accepted dry-run requests end in `EXECUTION_BLOCKED`; unsupported or unsafe requests end in `REJECTED`.
