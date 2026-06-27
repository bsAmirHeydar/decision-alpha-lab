# Backfill and Context Explained

## The Core Backfill Problem

F2 is allowed only after F1 confirms. But the origin of F2 is located inside the correction that occurred before F1 confirmation.

This creates a temporal backfill requirement.

The engine must not simply start F2 after the confirmation bar.

## F2 Backfill Example

Bullish chain:

```text
F1 Leg2 high appears.
Market corrects downward.
Deepest post-F1 correction low appears.
Market rallies and passes F1 Leg2 again.
F1 confirms.
```

At the moment F1 confirms, the engine must look back into the owned post-F1 correction context and select:

```text
F2 Origin = deepest low after F1 Leg2
```

Then F2 development can be evaluated from that origin.

## F3 Backfill

F3 works the same way after F2 confirmation.

```text
F2 confirms now.
F3 origin may already exist in the post-F2 correction context.
```

## What Must Be Stored

For each F object after its body appears, store a post-flag context:

```text
context start node/time
all adverse-side nodes
all opposite interstitial nodes
current deepest adverse extreme
hook branches
whether valid internal 1/2 exists
whether ND exists
whether confirmation break occurred
```

Without this context, the engine will either:

- start F2/F3 too late;
- choose wrong origin;
- lose branches;
- create orphan lines.

## Candidate Death and Parent Continuity

When F2 candidate dies by passing its own origin, the candidate identity dies.

But the parent F1 context does not die.

The parent post-F1 correction context remains the source for a future F2 candidate.

This means:

```text
old F2 body rejected
F1 context still active
post-F1 correction context updated
new F2 candidate may be created from deepest updated correction
```

## Why This Is Not Reusing Dead Origin

The context survives, not the dead F2 body.

If a deeper correction appears after F2 death, that new deepest node can become the next candidate origin.

The old candidate id must not be resurrected.

## F3 Extension Context

After F3 completes, the same-direction movement remains inside F3 extension.

The old sequence closes only when a confirmed opposite F1 appears.

That opposite F1 starts a new sequence and locks the previous F3.
