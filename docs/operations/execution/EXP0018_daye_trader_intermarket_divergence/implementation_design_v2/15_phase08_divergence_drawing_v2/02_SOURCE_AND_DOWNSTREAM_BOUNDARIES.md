# Source and Downstream Boundaries

## Input authority
P08 reads `DAYE_ReferenceUseRecord` where `status=ACCEPTED` and `is_accepted=true`. Every other status is non-renderable.

## Provenance input
The exact reference anchor comes from the complete P03 reference-period snapshot of the same Hunter symbol. P04–P07 expose this store through read-only APIs; no ownership moves upstream or downstream.

## Output
- `DAYE_RenderProjection`
- owned `OBJ_TREND`
- optional owned `OBJ_TEXT` annotation for major relationships
- audit/event records

P09 and P10 must not reuse P08 objects as domain input. P11 replay may repopulate accepted uses for historical projection.
