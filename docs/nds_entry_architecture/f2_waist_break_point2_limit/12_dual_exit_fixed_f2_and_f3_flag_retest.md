# 12 — Dual Exit Contract: Fixed F2 End or F3 Flag Retest

## 1. Decision

The F2 Waist-Break Point-2 setup now supports two explicit exit modes.

```text
Mode A — FIXED_F2_FLAG_END
Entry  = behind F2 Waist
Stop   = behind parent F1 Waist
TP     = original F2 Leg2 endpoint

Mode B — F3_FLAG_RETEST
Entry  = behind F2 Waist
Stop   = behind parent F1 Waist
RR Ref = original F2 Leg2 endpoint
TP     = F2-confirm node / F3 Leg1, armed only after correction
```

The entry setup, Stop authority, overlap arbitration, hedge policy and one-attempt identity do not change.

## 2. Why Mode B does not know its final TP at entry

At entry time the F2 body exists but F2 is not yet confirmed. Therefore the node that will hit the F2 flag end does not exist yet.

The initial body provides only:

```text
F2 Origin → F2 Leg1 → F2 Waist → F2 Leg2
```

Later:

```text
price hits/re-breaks F2 Leg2
→ F2 confirmation node is created
→ canonical F3 Leg1 is that same node
```

After price corrects away from this node, a return to it is the executable F3 flag-hit exit.

## 3. Reward/Risk remains based on the old fixed target

The dynamic F3 exit has no known price at entry. Therefore minimum RR and entry repricing must not use future F3 information.

Both modes calculate:

```text
RR Reference Target = original F2 Leg2 at setup creation
Risk                 = abs(Entry - Stop)
Reference Reward     = abs(F2 Leg2 - Entry)
Reference RR         = Reference Reward / Risk
```

If reference RR is below the configured minimum, Entry may be moved toward Stop exactly as before. Stop and the original F2 Leg2 RR reference remain fixed.

The eventual dynamic TP may produce a realized reward larger or smaller than the reference RR. That does not retroactively change setup eligibility.

## 4. Mode A — fixed F2 flag-end exit

This is the existing behavior.

```text
Pending order:
SL = parent F1 Waist ± stop buffer
TP = original F2 Leg2
```

The broker/tester owns the exit immediately after fill.

## 5. Mode B — F3 flag-retest exit

### 5.1 Order creation

The pending order is sent with:

```text
SL = parent F1 Waist ± stop buffer
TP = 0
```

The original F2 Leg2 is retained internally as:

- RR reference target;
- pending-consumption boundary;
- source-body identity.

### 5.2 F2 confirmation capture

After the pending fills, the runtime waits for the exact source F2 chain to confirm.

Matching requires:

- same symbol and timeframe;
- same direction;
- same scale L;
- same F2 Origin time;
- same F2 Waist time;
- same direct parent F1 Waist time;
- confirmed F2 lifecycle with `f2_can_spawn_f3=true`.

Pre-confirmation Leg2 extensions remain part of the same F2 chain. The final confirmed version is selected, not a stale body snapshot.

The captured target node is:

```text
Dynamic Target = F2.confirm.price
               = canonical F3 Leg1 price
```

### 5.3 Correction gate

The TP is not attached while price is still at the confirmation node. It is armed only after price moves away in the adverse direction.

Default correction gate:

```text
1 executable tick away from the F2-confirm / F3-Leg1 node
```

This threshold is configurable through `InpF2BTF3ExitCorrectionTicks`.

### 5.4 Retest exit

After correction:

```text
Bullish position:
TP = F2-confirm / F3-Leg1 node above current Bid

Bearish position:
TP = F2-confirm / F3-Leg1 node below current Ask
```

The return to this node is the F3 flag-hit exit.

If the target has already been re-hit before the broker TP can be attached, the default policy closes the position immediately at market rather than silently missing the structural exit.

## 6. Canonical F3 equivalence without a heavy F3 runtime

The lightweight tester does not build the full F3 ownership, OR-gate, lock, renderer or audit pipeline.

It does not need those layers for this exit because Phoenix already defines:

```text
F3 Leg1 = F2 confirmation node
```

Therefore the minimal causal exit contract is:

```text
capture F2 confirmation node
→ observe adverse correction
→ exit on retest of the same node
```

This preserves the intended F3 flag-hit semantics while keeping the runtime F1/F2-only and fast.

## 7. Dynamic-mode eligibility boundary

Mode B requires the source F2 to pass the canonical F2 size authority needed to spawn F3 after confirmation.

```text
F3 exit mode + F2 size gate failed
→ setup is not authorized
```

This requirement is enforced even when the general entry input `InpF2BTRequireF2SizeGate` is false, because a trade cannot wait for a canonical F3 path that the source F2 is not allowed to create.

## 8. Pending-order lifecycle

In both exit modes, if the original F2 Leg2 RR reference is consumed before the limit fills:

```text
pending order → cancelled
```

In dynamic mode this cancellation is managed by the in-memory context registry because the pending order intentionally has no broker TP.

## 9. Parallel contexts

Each dynamic position keeps its own:

- setup hash;
- source F1/F2 identity;
- order ticket;
- position identifier/ticket;
- F2 confirmation node;
- correction state;
- dynamic TP state.

Same-direction and opposite-direction contexts therefore remain independently managed on MT5 hedging accounts.

## 10. Inputs

```text
InpF2BTExitMode
  FP_NDS_F2_EXIT_FIXED_F2_FLAG_END
  FP_NDS_F2_EXIT_F3_FLAG_RETEST

InpF2BTF3ExitCorrectionTicks = 1.0
InpF2BTCloseAtMarketIfF3TargetAlreadyReached = true
```

## 11. State machine

```text
DYNAMIC ORDER PENDING
  ├─ original F2 Leg2 touched before fill → cancel
  └─ filled → WAIT_F2_CONFIRM

WAIT_F2_CONFIRM
  ├─ Stop hit → closed
  └─ exact source F2 confirms → capture F2.confirm / F3 Leg1

WAIT_CORRECTION
  ├─ Stop hit → closed
  └─ price moves adversely by correction threshold → WAIT_RETEST

WAIT_RETEST
  ├─ target already re-hit → market close
  ├─ broker TP geometry valid → arm TP at F2.confirm
  └─ otherwise → retry on next tick

TP_ARMED
  ├─ Stop hit → closed
  └─ F3 flag retests F2.confirm node → TP exit
```

## 12. Non-repainting and no-lookahead rules

- RR uses only the F2 Leg2 known at setup creation.
- Dynamic TP is unknown and unset at entry.
- F2 confirmation is consumed only when emitted by the canonical closed-bar detector.
- Correction is observed from current executable Bid/Ask after confirmation capture.
- No future F3 terminal, lock or opposite-F1 information is used.
