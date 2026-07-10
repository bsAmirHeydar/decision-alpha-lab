---
id: EXP0018-P07-HF001
project: EXP0018
phase: P07
status: fixed
scope: compile-only
---

# HOTFIX001 — MQL5 reserved `protected` identifier

## Failure

`DAYE_LifecycleSelfTest.mqh` used `protected` as a function parameter. In MQL5, `protected` is a reserved access-modifier token, so the parser rejected the function signature and both assignments that referenced the parameter.

## Change

Renamed only the local test-helper parameter:

```text
protected → protected_symbol
```

The domain fields remain unchanged:

```text
protected_broker_symbol
protected_canonical_symbol
```

## Behavioral impact

None. This hotfix changes no lifecycle rule, First-Sweep key, retirement policy, persisted schema, event identity, strategy output, or runtime behavior. It only restores legal MQL5 syntax in the embedded P07 self-test helper.

## Verification

- No standalone `protected` identifier remains in `DAYE_LifecycleSelfTest.mqh`.
- Function call sites are positional and require no change.
- Include guards and all test logic remain unchanged.
- MetaEditor gate: `0 errors, 0 warnings`.
