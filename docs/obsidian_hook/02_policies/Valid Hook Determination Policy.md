# Valid Hook Determination Policy

## Policy

Hook validity is determined after sequence construction.

```text
Sequence construction must remain complete.
Validity filtering must remain separate.
```

## Valid families

### Immediate Hook After Opposing F3

The immediate next structural Hook after a completed/locked F3 is valid only if it is opposite to the F3 direction.

### Hook After Hook

Hook-2 is valid only when its origin node is exactly the structural terminal node of Hook-1.

## Visibility

In valid-only mode, show:

- valid Hook sequences;
- the parent companion Hook when required by a Hook-after-Hook chain.

Do not show unrelated unqualified Hook labels.
