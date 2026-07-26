# MQL5 Module Architecture

- `SessionBoxTypes`: schema and enums;
- `SessionBoxIdentity`: deterministic IDs and UTC→broker conversion;
- `SessionBoxPolicy`: registry, admission and config validation;
- `SessionBoxGeometry`: symbol-local rectangle coordinates;
- `SessionBoxChartResolver`: exact-symbol chart selection;
- `SessionBoxObjectManager`: OBJ_RECTANGLE create/verify/repair/cleanup;
- `SessionBoxStore`: bounded projection memory;
- `SessionBoxEvents`: typed transitions;
- `SessionBoxDiagnostics`: logs;
- `SessionBoxAudit`: CSV adapter;
- `SessionBoxSelfTest`: embedded contract tests;
- `SessionBoxEngine`: state owner and P03 orchestration.
