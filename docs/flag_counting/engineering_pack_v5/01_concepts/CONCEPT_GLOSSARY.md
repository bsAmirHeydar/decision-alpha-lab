# Concept Glossary

## Candle High / Candle Low

The only raw price observations used by the structural logic. Open, close, body, candle direction, and candle color are not structural inputs.

## Node

A high or low price point that satisfies the project node definition for a given L. A node is extracted from candle highs/lows and remains historically valid after it is created.

## L

The project node clearance parameter:

```text
L = minimum number of candles on both left and right side
    that must not reach the candidate node price.
```

A high node requires at least L candles on the left and L candles on the right that do not reach that high price.

A low node requires at least L candles on the left and L candles on the right that do not reach that low price.

Equal highs/lows are handled as plateau nodes by the existing project node module.

## Node Identity

A stable reference to a specific node. Identity is not only price. It must include time, price, side, L, plateau handling, and any project-level node id if available.

## Equality

Equality is not a break. A price must pass a boundary. Equal highs/lows are merged or handled by node logic, but equality must not trigger invalidation or confirmation.

## Pass / Break / Hit

The model uses strict pass logic:

```text
Bullish upward break: high > boundary
Bullish downward invalidation: low < boundary
Bearish downward break: low < boundary
Bearish upward invalidation: high > boundary
```

Touching the same price is not enough.

## Flag Body

A two-leg structural object:

```text
Origin -> Leg1 -> Waist -> Leg2
```

The body is the common geometry behind F1, F2, and F3.

## Origin

The start of the first leg. For a bullish flag, the origin is a low node. For a bearish flag, the origin is a high node.

## Leg1

The first directional extreme before correction.

Bullish: the highest high before the correction.

Bearish: the lowest low before the correction.

## Waist

The correction extreme after Leg1 and before Leg2.

Bullish: deepest low after Leg1 before Leg2.

Bearish: highest high after Leg1 before Leg2.

The Waist is the control point of the flag body and is also the F1 post-body invalidation boundary.

## Leg2

The node that passes Leg1 and completes the two-leg body.

Bullish: a high node that passes Leg1 high.

Bearish: a low node that passes Leg1 low.

## F-Level

The role of a flag in a sequence.

- F1: first flag of a chain; requires post-flag internal numbering and confirmation.
- F2: second flag of a chain; authorized after F1 confirmation and compared to F1 size.
- F3: terminal flag; authorized after F2 confirmation and completed by a two-leg body plus F3 qualification.

## Sequence Chain

An owned ordered chain:

```text
F1 -> F2 -> F3
```

After F1 the engine searches for F2, not another F1 in the same chain. After F2 it searches for F3. F3 terminates the chain.

## Post-Flag Context

The correction region after a flag body, owned by that flag. It supplies:

- internal numbers 1/2/3/4;
- ND/Hook events;
- confirmation evidence;
- deepest correction extreme used to backfill the next F origin.

## Internal Numbering

Numbered adverse-side nodes after a flag body.

Bullish post-flag correction: numbered nodes are lows.

Bearish post-flag correction: numbered nodes are highs.

The first required minimum is 1/2. Three or four numbered nodes also create ND/Hook.

## ND / Hook

A branchable post-node cycle with 3 or 4 numbered adverse-side nodes after valid L adjustment. Two nodes are not ND. More than four nodes are compressed by increasing L until every branch has four or fewer nodes.

ND/Hook may overlap with F structures if both are logically emitted.

## Candidate

A structure that is logically alive but not yet confirmed/completed.

## Confirmed

An F1 or F2 whose required post-flag conditions are satisfied and whose Leg2 is passed again.

## Completed

An F3 whose two-leg body exists and whose F3 qualification condition is satisfied.

## Locked

A completed F3 that has ended its extension due to the first confirmed opposite F1. Locked F3 remains historically persistent.

## Invalidated

A live structure whose own invalidation boundary has been passed. It should not remain on the main chart by default.

## Rejected

A failed candidate body or failed structure that never became the intended object. Rejected structures are audit artifacts, not main chart structures.

## Backfill

The act of creating F2 or F3 after parent confirmation while using an origin that occurred earlier inside the parent post-flag correction context.

## Phase Boundary

A legitimate start boundary for a new F1. Examples include ND terminal extreme, opposite sequence end, or confirmed opposite F1 that locks an old F3.

## Renderer

A passive drawing layer. It may not create, fix, infer, or rescue logical structures.
