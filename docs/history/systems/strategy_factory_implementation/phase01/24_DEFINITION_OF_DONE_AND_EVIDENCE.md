# Definition of Done and Evidence

Phase 01 is functionally complete when all implementation deliverables exist. It is operationally accepted when local MetaEditor evidence is attached.

## Implemented evidence

- primary MQL5 headers;
- MQL5 contract self-test;
- Python mirror;
- schema registry and JSON Schemas;
- cross-language vector file;
- Python tests;
- MQL5 static tests;
- compile and test scripts;
- authority and safety ADRs;
- Phase 02 handoff.

## Local evidence still required

- MetaEditor compile with zero errors;
- Strategy Tester self-test with zero failures;
- exact terminal build number;
- Windows and terminal instance used;
- compile log hash.

## Acceptance statuses

- `IMPLEMENTED_PENDING_LOCAL_METAEDITOR_EVIDENCE`: code and automated non-MetaEditor tests pass.
- `ACCEPTED`: local compile and tester evidence attached.
- `BLOCKED`: any golden vector, causality, registry, compiler, or self-test failure.

## No silent waivers

A compiler warning or incompatibility that changes runtime behavior is not waived by documentation. The contract or code must be corrected and a new patch version issued.
