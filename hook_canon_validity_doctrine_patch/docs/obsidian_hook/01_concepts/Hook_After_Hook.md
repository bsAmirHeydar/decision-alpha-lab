# Hook After Hook

Hook After Hook is a production-valid Hook family.

## Definition

A Hook-2 is valid by the Hook-after-Hook rule when:

1. Hook-1 has completed its own sequence/cycle;
2. Hook-2 starts from the terminal / death-near endpoint of Hook-1;
3. Hook-1 and Hook-2 are of the same kind.

```text
positive Hook -> positive Hook
negative Hook -> negative Hook
```

## Parent status

Hook-1 does not need to be independently valid by the F3 rule. It only needs to be a completed structural parent.

When Hook-2 is visible, Hook-1 is shown as a parent companion with full detail.

## Label prefix

```text
HH     = valid Hook-2 child
PARENT = required Hook-1 companion
```
