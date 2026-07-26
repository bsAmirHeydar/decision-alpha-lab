# Test Matrix and Acceptance Gate

## Automated Python tests

- stable hashing;
- schema canonicalization and compatibility;
- safe identifier rejection;
- timestamp ordering and naive datetime rejection;
- bar geometry;
- event causal ordering;
- event and snapshot golden IDs;
- duplicate feature rejection;
- registry completeness;
- deterministic JSON;
- required MQL5 headers;
- absence of order authority.

## MQL5 self-test

`SF01_ContractSelfTest.mq5` validates kernel version, schema, cross-language event ID, future-time rejection, feature addition, snapshot ID, snapshot validation, duplicate rejection, and JSON emission.

## Acceptance evidence

- `pytest` passes;
- Python compileall passes;
- registry CLI passes;
- MQL5 compatibility static scanner reports zero errors;
- MetaEditor compile harness exists;
- user runs MetaEditor compile and Strategy Tester self-test on Windows;
- no live order authority exists.

The build environment cannot honestly claim MetaEditor compilation. That final compiler evidence remains an explicit local gate.
