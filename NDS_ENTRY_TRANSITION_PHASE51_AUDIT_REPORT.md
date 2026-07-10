# NDS Entry Transition Phase 51 — Audit Report

## Executive result

Phase 51 establishes a separate NDS entry-transition boundary:

```text
annotated valid Hook
→ Zone adapter
→ Setup Candidate
→ Trade Plan
→ Command Preview
```

The implementation is fail-closed and no-send. It does not reinterpret Hook
anatomy, invent Zone geometry, authorize capital, construct an `MqlTradeRequest`,
or call a broker-send API.

## Architectural changes

### Structure handoff

`FP_HookPhase02Engine.mqh` now captures the exact post-F3-annotation sequence
array into a symbol/timeframe-scoped read-only snapshot. The Entry layer does
not scrape chart objects or rerun Hook recognition.

### Explicit downstream objects

The transition defines separate records for:

- structure evidence;
- Zone evidence and canonical status;
- Setup state;
- Trade Plan geometry;
- Command Preview;
- pipeline and export report.

### Canonical Zone seam

`FP_NDSBuildCanonicalZoneAdapter` is the single future implementation seam.
It currently returns `NDS_ZONE_CANON_ADAPTER_PENDING` and cannot produce a
canonical Zone until the questionnaire decisions are locked.

### Safe command boundary

Every command preview uses:

```text
volume = 0
send_allowed = false
PREVIEW_ONLY_NO_SEND
```

The NDS Entry modules contain no `OrderSend`, `OrderSendAsync`, `CTrade`, trade
action, buy, or sell calls.

### First-failure diagnostics

Pipeline finalization reports the earliest failing authority boundary in this
order:

```text
Structure → Zone → Setup → Trade Plan → Command
```

This prevents a downstream cascade such as "Trade Plan blocked by Setup" from
hiding the actual unresolved Zone contract.

## Documentation package

The patch adds:

- a 13-document NDS Entry architecture package plus English and Persian indexes;
- a Phase 51 NDS Hook architecture overlay;
- an Obsidian MOC;
- ten focused Obsidian Entry/Execution notes;
- a Setup review template;
- implementation roadmap through canonical Zone, lifecycle, registry, risk,
  dry-run broker adapter, paper rehearsal, and controlled execution phases.

## Validation results

```text
NDS Hook contract QA:       PASS
NDS Entry contract QA:      PASS
Engineering policy:         0 errors, 0 warnings
MQL5 compatibility scan:    0 errors, 0 warnings
Repository layout audit:    0 missing directories
AI Engineering OS vault:    0 errors, 0 warnings
MQL lexical/brace balance:  PASS
Referenced sequence fields: 29 checked, 0 missing
New Obsidian links:          0 unresolved
Static QA blocking errors:  0
```

The repository-wide static QA still reports pre-existing warning-class findings
for long `Print` calls and short aliases in older modules. No warning is located
in the new NDS Entry files, and no blocking finding was produced.

## Runtime acceptance criteria

### Default pre-Canon profile

- structure snapshot either reports no eligible valid Hook or selects one;
- if selected, stage is `STRUCTURE_CAPTURED`;
- Zone reports `NDS_ZONE_BLOCKED_PRE_CANON_PROFILE`;
- Setup, Plan, and Command are not promoted;
- all CSV files are written when export is enabled;
- command volume remains zero and send authorization remains false.

### Diagnostic manual profile

- lower/upper Zone boundaries must be positive and ordered;
- entry must lie inside the manual Zone;
- entry, stop, and target must be positive;
- bullish geometry requires `stop < entry < target`;
- bearish geometry requires `target < entry < stop`;
- RR gate is honored when configured;
- the resulting Command remains diagnostic, zero-volume, and no-send.

## Remaining Canon work

The following are deliberately not implemented:

- which valid Hooks produce Zones;
- exact positive/negative Zone boundaries;
- wick/close/node/body authority;
- Zone lifecycle;
- trade-direction doctrine;
- approved entry, stop, and target models;
- multi-timeframe conflict and nesting;
- opportunity ranking and registry;
- position sizing and portfolio limits;
- broker request, fill, cancel, replace, and reconciliation.

These items remain versioned questions rather than hidden assumptions.

## Compile limitation

MetaEditor is not available in this environment. Source-level compatibility,
contract, balance, and repository checks passed, but final MQL5 compilation must
be confirmed locally against `FlagCountingPhoenixExperiment.mq5`.
