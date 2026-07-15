# 12 — Validation and Hostile Test Matrix

## Static source gates

`nds_hook_864_cycle_r1_contract_qa.py` verifies:

- required files and docs;
- old profile compatibility;
- exact parameter locks;
- canonical `cycle_closed`, `resolve_confirmed`, and `x_count` reuse;
- absence of a second Hook detector/node counter;
- projection and first-arrival formula;
- stable one-attempt identity;
- structural Stop and fixed Target;
- shared sizing, lock, exposure, cancellation, and broker paths;
- no F123 close for Phase 55;
- dedicated ledger;
- live defaults false;
- no Python broker/network/process authority.

## Hostile cases

| Case | Expected result |
|---|---|
| ratio 0.8639 or 0.865 | profile configuration blocked |
| X2 | blocked |
| X5 | blocked |
| unconfirmed Terminal | blocked |
| Cycle not closed | blocked |
| Terminal at 0.864 | late-level blocked |
| Terminal beyond 0.864 | late-level blocked |
| invalid Crown/Origin | blocked |
| Buy Limit not below Ask by broker distance | blocked |
| Sell Limit not above Bid by broker distance | blocked |
| SL/TP unsupported | blocked |
| setup already used | blocked |
| pending/position already owned | held/blocked, no second order |
| foreign same-symbol position | blocked |
| x3 setup later becomes x4 | same setup key, no reprice/re-entry |
| open position missing valid SL/TP | fail-closed protection state |

## Required external validation

1. MetaEditor compile with zero errors and reviewed warnings.
2. Lightweight tester run for both profile branches.
3. Python/MQL5 vector parity.
4. Visual review of Origin/Crown/Terminal/86.4 geometry.
5. Demo broker pending-fill, SL, TP, cancellation, restart, and duplicate-exposure tests.
6. Long-run report/ledger reconciliation.

## Explicit limitation

The current repository environment can perform Python and static source QA. It cannot honestly mark Windows MetaEditor, MT5 tester, or broker execution evidence as passed.
## Windows compile gate

Run from repository root on the supported Windows/MT5 host:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\flag_counting\compile_nds_hook_864_cycle_r1.ps1 -MetaEditorPath "C:\Path\To\metaeditor64.exe"
```

The script compiles the no-order contract self-test, lightweight backtest expert, and central Phoenix expert using the repository Include root. It writes source/log hashes and requires an explicit `0 errors, 0 warnings` compile summary. The generated `local_evidence/` material is external evidence and is not a source-code authority or an activation grant.
