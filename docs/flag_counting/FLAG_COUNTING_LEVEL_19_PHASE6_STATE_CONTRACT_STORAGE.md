# Flag Counting Phoenix — Level 19 Phase 6 State Contract Storage

## Status

Implemented as a read-only Level 19 refinement layer.

Phase 6 does **not** change any locked Phoenix anatomy engine:

```text
Node Engine
Hook / ND Engine
Flag Body Engine
Internal Count Engine
F1 Lifecycle
F2 Lifecycle
F3 Lifecycle
Ownership
Canonicalization
Renderer
Validation
Release
License
```

Phase 6 only stores and exports a stable, closed-bar State Contract generated from the already-projected State Gate snapshot.

---

## Purpose

The previous Level 19 phases created the live multi-timeframe State Gate:

```text
Phase 2 → closed-bar tracker
Phase 3 → Rally View projection from F1/F2/F3
Phase 4 → Hook View projection from Hook/ND branches
Phase 5 → right-upper dashboard polish and debug usability
```

Phase 6 makes this state consumable by the future entry layer.

It does not answer:

```text
Buy?
Sell?
Enter?
No trade?
```

It answers only:

```text
For this symbol and this closed bar, what is the stored anatomy state of each configured timeframe?
```

The core idea is:

```text
State Gate = live anatomy memory
Entry layer = future consumer of that memory
```

---

## Design rule

The State Contract is a storage contract, not a decision contract.

It may say:

```text
M1 is contract-ready as context.
M10 is partial.
H1 has no closed-bar data.
```

It must not say:

```text
entry allowed
buy
sell
fade
continue
```

All Phase 6 labels use explicit `NO_DECISION` wording when they prepare the future entry bridge.

---

## Per-timeframe contract fields

Each configured State Gate timeframe now stores these additional fields inside `FP_StateGateTimeframeState`:

```text
state_key
primary_rally_key
primary_hook_key
anatomy_status
storage_status
entry_bridge_status
contract_status
```

These fields are derived after Rally View and Hook View have been projected.

---

## `state_key`

`state_key` is a compact closed-bar fingerprint for the timeframe.

It includes:

```text
symbol
timeframe
closed-bar time
update count
primary Rally key
primary Hook key
Rally row count
Hook row count
```

Example shape:

```text
GOLD|TF=M1|T=2026.06.29_12:40|U=8|R=F2|bull|L13|E104|POST_FLAG_BODY|H=POSITIVE_HOOK_REVERSAL_UP|L21|N3|RR=6|HR=10
```

The exact key is not a trading signal. It is a reproducible state identity for debugging, export comparison, and future entry-layer consumption.

---

## `primary_rally_key`

`primary_rally_key` is built from the first projected Rally row for the timeframe.

It stores the leading F-state visible to the State Gate:

```text
F level
direction
scale L
source event id
body state
flag stage or post-flag stage when available
```

If no projected Rally row exists:

```text
NO_PROJECTED_RALLY_ROW
```

---

## `primary_hook_key`

`primary_hook_key` is built from the first projected Hook row for the timeframe.

It stores the leading Hook/ND state visible to the State Gate:

```text
hook polarity
direction
scale L
current node number
latest high node id
latest low node id
source hook id
```

If no projected Hook row exists:

```text
NO_PROJECTED_HOOK_ROW
```

---

## `anatomy_status`

`anatomy_status` tells whether Rally and Hook projections exist for the closed bar:

```text
RALLY_AND_HOOK_PROJECTED
RALLY_PROJECTED_HOOK_PENDING
HOOK_PROJECTED_RALLY_PENDING
ANATOMY_NOT_PROJECTED
NO_CLOSED_BAR_ANATOMY
```

This is still descriptive only.

---

## `storage_status`

`storage_status` tells how the current closed-bar state was stored:

```text
STORED_NEW_CLOSED_BAR_STATE
STORED_UNCHANGED_CLOSED_BAR_STATE
NO_STORAGE_WITHOUT_CLOSED_BAR
```

This helps distinguish a real new closed bar from a timer pass with unchanged state.

---

## `contract_status`

`contract_status` is a context readiness label:

```text
STATE_CONTRACT_READY_CONTEXT_ONLY
STATE_CONTRACT_PARTIAL
STATE_CONTRACT_NO_DATA
```

`STATE_CONTRACT_READY_CONTEXT_ONLY` means Rally and Hook context are both projected. It does not mean an entry exists.

---

## `entry_bridge_status`

`entry_bridge_status` is deliberately decision-neutral:

```text
ENTRY_CONTEXT_READY_NO_DECISION
ENTRY_CONTEXT_PARTIAL_NO_DECISION
ENTRY_CONTEXT_BLOCKED_NO_CLOSED_BAR
```

The wording is intentional. Phase 6 prepares a bridge to entry design but does not implement entry logic.

---

## CSV outputs

Phase 6 extends the existing State Gate CSV set.

Existing files:

```text
latest_state_gate_summary.csv
latest_state_gate_rally.csv
latest_state_gate_hooks.csv
latest_state_gate_panel.csv
latest_state_gate_manifest.csv
```

New file:

```text
latest_state_gate_contract.csv
```

The contract file has one row per configured timeframe.

It is the cleanest output for the future entry layer to consume.

---

## Summary CSV extension

`latest_state_gate_summary.csv` now also includes:

```text
state_key
primary_rally_key
primary_hook_key
anatomy_status
storage_status
entry_bridge_status
contract_status
```

---

## Panel CSV extension

`latest_state_gate_panel.csv` now also includes:

```text
state_key
contract_status
entry_bridge_status
```

---

## Dashboard addition

The right-upper dashboard can now show a compact contract line per timeframe when enabled:

```text
InpStateGatePanelShowContractKey = true
```

The line shows:

```text
contract status
entry bridge status
state key
```

The key can be long, so the panel clips it visually. The full key remains available in CSV.

---

## New inputs

```text
InpStateGatePanelShowContractKey = true
InpStateGateExportContractCsv   = true
```

`InpStateGateExportContractCsv` only works when the main State Gate CSV export is enabled.

---

## Manifest changes

`latest_state_gate_manifest.csv` now records:

```text
panel_show_contract_key
export_contract_csv
contract_rows
projection_state = phase6_rally_hook_contract_stored
```

---

## Acceptance criteria

Phase 6 is accepted when:

```text
1. Level 19 still updates only from closed bars.
2. Rally View remains a projection of existing F1/F2/F3 output.
3. Hook View remains a projection of existing Hook/ND branch output.
4. No Node, Hook/ND, F-counting, ownership, renderer, validation, release, or license logic is modified.
5. Every configured timeframe gets a state_key after snapshot finalization.
6. latest_state_gate_contract.csv is written when CSV export and contract export are enabled.
7. The right-upper dashboard can show contract state without becoming a trading signal.
8. All bridge labels include NO_DECISION language.
```

---

## Next phase

The next natural phase is:

```text
Phase 7 — Entry Geometry Readiness Fields
```

That phase should still avoid buy/sell logic. It should only start preparing fields that future entry design will need, such as selected extreme candidates, X-invalidation placeholders, X-destination placeholders, and optionality geometry placeholders.
