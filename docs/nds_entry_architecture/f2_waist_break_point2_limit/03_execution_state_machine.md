# 03 — Execution State Machine

## 1. Canonical source lifecycle

```text
PHOENIX F2 BODY NOT READY
  ↓
PHOENIX F2 FLAG BODY READY
Origin → Leg1 → Waist → Leg2
  ↓
F2 POST-FLAG CONTEXT ACTIVE
  ├─ Phoenix internal counting develops
  ├─ F2 may create the special Waist-break branch
  ├─ F2 Origin break → source invalid
  └─ favorable re-break after valid post-flag structure → F2 confirmed
```

The setup engine observes this lifecycle. It does not write it.

## 2. Setup projection lifecycle

```text
NO PROJECTION
  ↓ exact canonical body is observable
POINT2 PROJECTION ARMED
  ├─ projected Point 1 = F2 flag Waist
  ├─ Point-2 limit = strictly beyond Waist and boundary epsilon
  ├─ Stop = behind direct parent F1 Waist
  └─ RR reference = original F2 flag end
```

A body may remain eligible across multiple bars, but a missed Entry or already-consumed flag end cannot be armed retrospectively.

## 3. Pending lifecycle

```text
PENDING_POINT2_CAPTURE(exact_f2_body_id)
  │
  ├─ limit fills
  │    └─ executable Waist-break Point 2 captured
  │
  ├─ exact source Leg2 extends
  │    └─ cancel old order; new body version may re-arm
  │
  ├─ exact source F2 confirms
  │    └─ cancel; original target event already occurred
  │
  ├─ exact source F2 invalidates or disappears
  │    └─ cancel
  │
  ├─ original F2 flag end touched before fill
  │    └─ cancel in every exit mode, including dynamic TP=0 modes
  │
  ├─ HTF gate disallows and cancellation policy is enabled
  │    └─ cancel
  │
  ├─ wider overlapping context replaces this pending
  │    └─ cancel and release reservation
  │
  └─ otherwise
       └─ hold the exact source-bound pending order
```

## 4. Fill and attempt ownership

```text
pending accepted → active source-body reservation
pending cancelled → reservation released
entry deal filled → F2 body attempt permanently consumed
```

A fill is the execution event for Point 2. It is not F2 confirmation.

## 5. Position lifecycle

```text
POSITION_OPEN(exact_setup_hash)
  ├─ Stop behind parent F1 Waist
  ├─ Fixed exit → original F2 flag end
  ├─ Local F3 exit → exact child F3 of the same source F2
  └─ HTF F3 exit → independently locked HTF F3 per position ticket
```

The HTF entry gate never force-closes an already-filled position.

## 6. Invariants

```text
F2 detector/lifecycle code is unchanged
one pending order owns one exact F2 body version
body extension cannot leave an old-target order alive
F2 confirmation cannot leave an unfilled Point-2 order alive
boundary epsilon is part of Point-2 entry geometry
no confirmed-node lookahead is used for entry
```
