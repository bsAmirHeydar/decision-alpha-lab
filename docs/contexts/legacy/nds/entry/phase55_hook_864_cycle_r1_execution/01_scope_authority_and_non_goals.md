# 01 — Scope, Authority, and Non-Goals

## Bounded decision

The approved decision is a setup adapter over the canonical NDS Hook sequence:

- the Hook already exists;
- its family and validity already exist;
- its cycle Crown, Origin, Death Boundary, Terminal, state, and `x_count` already exist;
- the adapter may only decide whether that object qualifies for the 86.4/3-or-4/1R execution profile.

## Authority ownership

| Concern | Authoritative owner | Phase 55 role |
|---|---|---|
| F/Hook detection | existing Phoenix detectors | read only |
| Hook family | Hook Phase02 sequence | consume |
| Node count | `FP_HookPhase02Sequence.x_count` | hard gate 3/4 |
| Cycle closure | `FP_HookP02SequenceCycleClosed` | hard gate |
| Terminal confirmation | `resolve_confirmed` | hard gate |
| Entry projection | `FP_NDSHook864CycleR1Rules` | own 0.864 projection |
| Stop buffer and broker distance | existing Hook trade rules | reuse |
| Volume | existing fixed/risk-cash sizing | reuse |
| Exposure | existing magic-wide lock | reuse |
| Order placement | existing CTrade adapter | reuse |
| Position exit | attached broker SL/TP for this profile | fixed 1R |
| Audit | existing export engine, profile schema | extend |

## Non-goals

Phase 55 does not:

1. alter how Origin, Crown, X nodes, Terminal, Hook family, death, or closure are detected;
2. reinterpret `x_count` from candles or chart objects;
3. add a generic retracement optimizer;
4. make 86.4 configurable as a strategy family;
5. allow node counts other than 3 or 4;
6. move a pending order when an x3 Hook later becomes x4;
7. add re-entry for the same Hook;
8. alter the Phase 52 terminal/F123 profile;
9. bypass risk sizing, broker capability, stop/freeze distance, magic ownership, or entry locks;
10. claim MetaEditor, Strategy Tester, broker, or live profitability evidence from static tests.

## Fail-closed rule

Unknown profile, noncanonical profile configuration, missing sequence data, invalid family, unclosed cycle, unconfirmed terminal, x2/x5, touched 86.4 level, invalid geometry, insufficient broker distance, duplicate exposure, used setup identity, unsupported SL/TP, or send failure all produce a blocked/no-action state.

## Source of truth

The execution code must be understandable without chart rendering. Chart objects and labels are diagnostics only. Source fields are raw typed sequence fields and broker symbol/account state.
