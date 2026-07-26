# 16 — Definition of Done, Limitations, and Residual Risk

## Repository Definition of Done

- profile enum/config/setup fields implemented;
- exact canonical parameter validation implemented;
- canonical sequence eligibility implemented without duplicate detection;
- direction-independent 86.4 projection implemented;
- structural Stop and attached normalized 1R Target implemented;
- stable Hook-level one-attempt identity implemented;
- shared execution core and Phase 52 compatibility wrappers implemented;
- fixed-R pending and position protection verification implemented;
- invalid fixed-R pending protection cancellation implemented;
- restart-safe profile recovery after Magic ownership implemented;
- recovered-profile ledger routing and broker-geometry audit implemented;
- dedicated ledger implemented;
- central/tester wiring implemented with safe defaults;
- Python mirror, vectors, unit tests, and static contract QA pass;
- Obsidian and engineering docs are linked;
- root-relative patch, hashes, install, commit, rollback, and QA report are delivered.

## External acceptance still required

- MetaEditor compilation on supported Windows/MT5 build;
- Strategy Tester run for both old and new profiles;
- Python/MQL5 parity artifact;
- demo broker order placement and fill;
- stop/freeze/spread/tick-size boundary evidence;
- restart and used-registry evidence;
- x3→x4 no-reprice evidence;
- structural death cancellation evidence;
- attached SL/TP and exact broker-side 1R evidence;
- long-run ledger and broker reconciliation.

## Residual risks

1. Broker normalization may cause realized R slightly above 1R; code forbids below-1R normalization.
2. Broker fill price/slippage can alter position-level realized R. The open-position guard detects invalid protection but does not automatically modify it.
3. Pending-order cancellation relies on the existing canonical death lifecycle and broker availability.
4. Netting accounts and foreign same-symbol positions remain intentionally conservative.
5. Static source QA cannot prove MQL5 compiler compatibility.
6. No profitability or edge claim is made.

## Production status

The implementation is an opt-in execution profile with live defaults false. Production promotion requires the project’s normal compile, tester, broker, risk, human approval, and evidence gates.
