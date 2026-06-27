# Flag Counting Glossary

## F-counting

A structural market movement grammar that counts movement as F1 -> F2 -> F3 sequences, with ND/Hook phases between or around them.

## F1

The root flag in a sequence. It must form Origin -> Leg1 -> Waist -> Leg2, then Internal 1/2, then rebreak Leg2 before Waist invalidation.

## F2

Mandatory continuation after a valid F1. Its Origin is the parent F1 Internal 2. It invalidates at its own Origin, not its Waist. Its size must be at least the parent F1 size.

## F3

Mandatory continuation after F2. Its Origin is parent F2 Internal 2. After its two-leg body is formed, the sequence becomes terminal/locked and the following movement is special.

## Origin

The starting point of a flag body. For F1 it must be a legitimate root after ND/opposite completion/reset. For F2/F3 it is Internal 2 of the parent.

## Leg1

The first impulse away from Origin in the direction of the sequence.

## Waist

The correction after Leg1 and before Leg2. For F1, Waist is the invalidation boundary. For F2/F3, Waist can be broken and become Internal 1 in the waist-break branch.

## Leg2

The second impulse in the direction of Leg1. It must break Leg1. It can extend while the sequence is live.

## Internal 1

A post-Leg2 counting point. In normal bullish structures it is the first low after Leg2. In normal bearish structures it is the first high after Leg2.

## Internal 2

A later post-Leg2 counting point beyond Internal 1 but still within the valid boundary. For F2/F3 waist-break branch, Internal 2 is the node that breaks Waist while Origin remains protected.

## Rebreak

The market breaks the current Leg2 endpoint again after the required counting condition.

## Confirmation

For F1/F2, confirmation is own Leg2 rebreak before invalidation. For F1 this requires Internal 1/2 before rebreak. F3 is terminal after its two-leg body.

## Invalidation

The boundary that kills the structure. F1 invalidates at Waist. F2 invalidates at Origin. F3 becomes terminal after body completion; normal post-body invalidation is not the same concept.

## ND / Hook

A cyclic, non-flag, or hook-like phase. Usually 3 or 4 nodes around an extreme after adaptive L selection. ND is part of market partitioning, not a decorative label.

## Scale L

The swing detection scale. Smaller L shows smaller structures; larger L shows broader structures. The system is fractal and supports multiple L values in parallel.

## Sequence

A parent/child movement chain such as F1 -> F2 -> F3. Multiple sequences can exist in parallel across scales.

## Terminal F3

A completed F3 two-leg body. After this, the market can reverse or transition. The sequence is considered to have done its job.
