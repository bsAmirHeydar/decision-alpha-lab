# F1 / F2 / F3 Explained

## Shared Body, Different Role

F1, F2, and F3 all have the same body:

```text
Origin -> Leg1 -> Waist -> Leg2
```

The difference is not the shape. The difference is what the market must do after that body and where the object lives in the sequence.

## F1 Explained

F1 is the first flag of a chain. It must not begin in the middle of movement.

It begins after a legitimate boundary, such as ND/Hook or opposite-sequence end.

After F1 body forms, it must not be trusted immediately. It must produce post-flag internal correction numbering.

Bullish F1:

```text
F1 body: Low -> High -> Low -> Higher High
Then correction lows must create 1/2 or more.
Then price must pass F1 Leg2 again.
```

F1 invalidation uses Waist because F1 is fragile after its first body. If the correction after body passes the flag's Waist before confirmation, the F1 candidate failed.

Why Waist, not Origin?

Because F1's role is to prove that the post-flag correction can exist without destroying the internal flag structure. If the Waist is passed before confirmation, the F1 logic is broken even if the original origin is not yet passed.

## F1 Leg2 Extension

If F1 body forms but post-flag 1/2 has not appeared, and price passes Leg2 again, this is not confirmation and not a new F.

It is Leg2 extension.

The earlier Leg2 is replaced by the later extreme.

This prevents false F1 completion before internal correction exists.

## F2 Explained

F2 is the second flag of the same chain. It only becomes authorized after F1 confirms.

But its origin is not necessarily after the confirmation time. It is backfilled from the correction after F1 body.

This is important because the correction that confirms F1 also supplies the origin of F2.

If F2 candidate dies by passing its own origin, F2 was not F2. But F1 remains the parent. The engine continues to search for F2 from the same post-F1 context.

F2 is compared to F1 by size:

```text
F2 flag_size >= F1 flag_size
```

If it has not yet reached that size, it remains candidate. It does not die unless its origin is passed.

F2 may break its Waist. This creates a special branch, not invalidation, as long as Origin remains safe.

## F3 Explained

F3 is the terminal flag.

F3 is authorized after F2 confirms, and its origin is backfilled from the correction after F2 body. F2 is not considered finished until its flag end is re-hit/confirmed, so F3 Leg1 is the F2 confirmation node, not an earlier favorable node inside the unfinished F2 hit process.

F3 does not need internal 1/2 after itself. Its job is different: it completes the chain. Still, it must have a complete F3 body before the OR qualification can make it terminal.

F3 must still satisfy a same-scale/size relation to F2 by OR condition:

```text
F3 Leg1 L >= 0.8 * F2 Leg1 L
OR
F3 flag_size >= 0.7 * F2 flag_size
```

If not yet satisfied, it continues as candidate.

After F3 completes, same-direction movement is F3 extension.

The extension ends only when the first confirmed F1 in the opposite direction appears.

That opposite F1 both locks the old F3 and begins a new opposite sequence.

## Why F3 Must Persist

F3 has done its job once completed/locked. Even if the market later reverses through the old structure, the historical fact remains.

Therefore locked F3 must not be deleted from the chart unless explicitly hidden by input.
