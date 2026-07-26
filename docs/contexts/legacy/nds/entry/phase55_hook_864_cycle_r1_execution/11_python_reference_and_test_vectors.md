# 11 — Python Reference and Test Vectors

## Purpose

`tools/flag_counting/nds_hook_864_cycle_r1_reference.py` is a deterministic geometry/eligibility mirror. It has no MT5 import, broker connection, order function, subprocess, socket, file mutation, or execution authority.

## Mirrored contracts

- exact profile validation;
- positive and negative 86.4 projection;
- Origin–Crown containment;
- valid/failed/family/cycle/terminal gates;
- x3/x4 acceptance and x2/x5 rejection;
- mature/capped state gate;
- untouched level gate;
- directional tick normalization;
- structural stop plus minimum broker distance;
- exact 1R target rounded away from Entry.

## Test vectors

`lab/03_experiments/EXP_flag_counting/hook_864_cycle_r1/test_vectors.json` contains positive, negative, and hostile cases. It is a reference vector family, not a market-performance dataset.

## Unit tests

The unit suite covers deterministic projections, all critical eligibility failures, configuration-drift failures, direction ordering, minimum stop distance, and normalized R. Tests do not claim MQL5 parity until MetaEditor/Strategy Tester outputs are captured and compared.

## Future parity evidence

A Windows parity run should export canonical sequence fields and built setup fields from MQL5, evaluate the same rows in Python, and compare reason code, Entry, Stop, Target, and R at symbol tick tolerance.
## Machine-readable profile and acceptance artifacts

The experiment directory also contains:

```text
profile_contract.json
acceptance_matrix.json
```

`profile_contract.json` freezes the authoritative Phase02 fields, exact ratio, exact node window, Origin-not-counted rule, structural Stop source, fixed 1R exit, profile identity, and default-false authority. `acceptance_matrix.json` separates repository evidence from pending Windows MetaEditor, Strategy Tester, restart, and demo-broker evidence. Python tests load the profile contract and golden vectors so documentation, fixtures, and executable reference geometry cannot drift independently.
