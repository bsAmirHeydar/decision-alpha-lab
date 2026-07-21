feat(strategy-factory): add UCE-I19 production operations control plane

Implement the UCE-I19 fail-closed reference layer for production deployment,
controlled capital ramp, live operations, rollback, and retirement.

Core contracts and controls:
- bind an exact accepted I18 release to one immutable external target
- compile stage-, time-, environment-, generation-, and risk-bounded plans
- issue short-lived runtime leases with explicit expiry and revocation
- evaluate known-time health, SLO, freshness, broker, loss, and risk state
- require exact reservation, order, position, and generation reconciliation
- recompute bounded authority before every possible action cycle
- preserve no-send paper/shadow semantics and zero-authority defaults
- deny automatic stage or capital escalation
- classify documentation, operations, derisk, invalidating, and hot changes
- govern incident, kill switch, restart, EOD, rollback, and retirement state

Evidence and conformance:
- add 28 closed JSON schemas and 10 deterministic/negative vectors
- add 22 Python modules and 221 UCE-I19 tests
- add 18 MQL5 guard headers and 4 no-order diagnostic experts
- add external Windows/MT5 evidence scaffolding and bundle tools
- add 55 phase chapters, 12 atomic concepts, phase map, gates, and status
- keep activation, broker, order, network, and automatic-ramp authority false

Verification:
- 221 UCE-I19 tests passed
- 335 combined UCE-I18/UCE-I19 tests passed
- Python authority-boundary scan passed
- MQL5 static authority scan passed
- delivery/schema/reference-block validation passed
- repository engineering policy passed with zero errors and warnings
- UCE-I19 Python/tool py_compile passed

External evidence remains pending:
- supported Windows/MetaEditor compilation
- MT5 terminal execution and restart
- exact broker/account/symbol/terminal binding
- prospective paper/shadow and any bounded live tier
- operator approvals, incident, EOD, rollback, restore, and retirement drills

Activation remains false.
