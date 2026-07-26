# Valid Only Does Not Expand Same Origin Groups

Valid-only production view is exact.

Selecting one valid Hook must not make every sibling sequence from the same origin visible.

## Allowed visible rows

```text
F3H    = Hook After Opposing F3
HH     = Hook-2 After Hook-1
PARENT = Hook-1 shown only as required parent companion of HH
```

## Forbidden

```text
same-origin sibling expansion
structural fallback
unqualified sequence labels
unqualified node labels
```

## Reason

Same-origin expansion made the chart look as if every structural branch were a valid Hook. This violated the production doctrine.
