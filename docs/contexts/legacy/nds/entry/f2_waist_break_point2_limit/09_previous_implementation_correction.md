# 09 — Correction of the Previous Implementation

## Previous incorrect trigger

```text
Confirmed F2
→ place limit around F2 waist
```

This was temporally wrong because confirmed F2 means price has already returned to and re-broken the F2 Leg2 endpoint after internal structure. That endpoint is the intended target.

## Correct trigger

```text
Complete unconfirmed F2 two-leg body
→ stage limit strictly behind F2 waist
→ fill = waist-break Point 2
→ target = F2 Leg2 endpoint
```

## Previous semantic error

The implementation treated the F2 waist as the entry reference without representing the waist-break branch grammar.

## Correct semantic mapping

```text
F2 Waist = Point 1
Strict break beyond F2 Waist = Point 2
Pending fill beyond Waist = executable Point 2
```

## Previous performance mismatch

The fast detector called the general per-scale detector, which still built Hook branches internally.

## Correct performance path

The dedicated detector now calls canonical node/F1/F2 builders directly and never constructs Hook branches.
