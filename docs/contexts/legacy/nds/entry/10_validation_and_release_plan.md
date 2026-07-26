---
title: NDS Entry Validation and Release Plan
status: active
version: 1.0.0
---
# NDS Entry Validation and Release Plan

## 1. Static gates

- all required NDS Entry files exist;
- default profile is pre-Canon blocked;
- direction/order/stop/target defaults are unresolved;
- Zone and trade-contract locks default false;
- command preview lock defaults true;
- volume is hard zero;
- send authority is hard false;
- no execution API token exists in NDS Entry modules;
- Hook Phase 02 captures and clears the structure snapshot;
- central EA version and inputs match the package.

Run:

```powershell
python tools/flag_counting/nds_entry_contract_qa.py --root .
```

## 2. MetaEditor compile gate

Compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Required:

```text
0 errors
0 warnings
```

## 3. Runtime profile A — safe default

Expected:

```text
structure row may become eligible
Zone status = NDS_ZONE_BLOCKED_PRE_CANON_PROFILE
setup not ready
plan not ready
command not built
send_allowed = false
volume = 0
```

## 4. Runtime profile B — diagnostic manual geometry

Use only on a test chart. Set:

```text
contract profile = DIAGNOSTIC_MANUAL_GEOMETRY
direction policy explicitly
order/stop/target models explicitly
require trade contract locked = false
manual Zone lower/upper
manual entry/stop/target
```

Expected:

```text
Zone canonical = false
Setup diagnostic ready
Trade Plan diagnostic ready
Command preview ready
volume = 0
send_allowed = false
```

## 5. Negative tests

- inverted Zone boundaries;
- zero entry/stop/target;
- bullish geometry with stop above entry;
- bearish geometry with stop below entry;
- unresolved direction;
- unresolved order model;
- preview lock false;
- no valid Hook;
- Hook Phase 02 skipped;
- stale symbol/timeframe snapshot mismatch.

## 6. Promotion gate

Canonical profile must remain blocked until:

1. Hook questionnaire is closed;
2. Zone boundary and lifecycle Canon is approved;
3. entry/stop/target doctrine is approved;
4. canonical adapter tests pass;
5. persistent Setup ledger exists;
6. broker and capital modules remain independently gated.
