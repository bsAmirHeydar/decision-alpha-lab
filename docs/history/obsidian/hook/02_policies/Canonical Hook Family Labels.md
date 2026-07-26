# Canonical Hook Family Labels

In valid-only production view, every visible Hook sequence label must state why it is visible.

## Labels

| Prefix | Meaning |
|---|---|
| `F3H` | Hook After Opposing F3 |
| `HH` | Hook-2 After Hook-1 |
| `F3H+HH` | Hook qualifies by both families |
| `PARENT` | Hook-1 companion required to read Hook-2 |

## Examples

```text
F3H H123B1:1
HH H130B1:2
PARENT H129B1:1
```

## Rule

A Hook label without one of these tags must not appear in valid-only production view.

