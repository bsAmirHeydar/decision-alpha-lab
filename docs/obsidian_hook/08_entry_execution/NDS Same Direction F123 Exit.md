# NDS Same Direction F123 Exit

## Rule

After the Hook limit fills, the position remains open until a complete F1 → F2 → F3 chain appears in the same direction as the broker position.

```text
BUY  → bullish F1 + bullish F2 + completed bullish F3
SELL → bearish F1 + bearish F2 + completed bearish F3
```

## Strict post-entry gate

Default strict mode requires:

```text
F1 origin > position open time
F2 origin > position open time
F3 completion > position open time
```

This excludes chains that began before the fill.

## Canonical F3 evidence

The F3 must be main-visible, terminal-complete, and `COMPLETED` or `LOCKED`. F1 and F2 must be visible members of the same sequence with lifecycle authority to spawn the next level.

## Exit action

The position is closed by ticket at market. The close is considered complete only when the ticket is no longer selectable as an open position.

## Related

- [[NDS Hook Limit Entry Contract]]
- [[NDS Hook Trade State Machine]]
- [[NDS Hook Trade Audit Ledger]]
