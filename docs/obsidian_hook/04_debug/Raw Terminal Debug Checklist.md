# Raw Terminal Debug Checklist

Use this checklist when a Hook envelope appears to stop early:

1. Confirm the Hook is visible in valid-only mode.
2. Check whether price made a lower low after the positive Hook crown.
3. Check whether price made a higher high after the negative Hook crown.
4. Confirm `FP_HookP02BuildSequencesWithRates` is used by Phase 02 core.
5. Export CSV and inspect `resolve_time` and `resolve_price`.
6. Remember: `resolve_node_id` may remain the structural node, while `resolve_price` may be promoted to the raw terminal price.
