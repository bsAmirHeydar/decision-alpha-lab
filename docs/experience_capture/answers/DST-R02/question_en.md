# DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy

## Question

When several destinations or exit opportunities exist, how should take profit, partial close, runner/tail logic, and trailing behavior be handled?

## Why This Question Remains

NDS does not treat profit-taking as a single fixed TP. The strategy may have multiple destinations, multiple exit conditions, partial exits, and an optional runner/tail component. Because the broader model prioritizes low cost, open profit potential, and convex opportunity, exit logic must be trained and evaluated through the same lens.

## Answer Requirements

Please clarify:

- Should different exit variants be trained and compared?
- What metrics should decide which exit policy is better?
- Should the system prioritize potential, open profit path, low cost, or win rate?
- Is trailing stop allowed or discouraged?
- Should partial close be favored over trailing?
- Under what conditions should partial profits be taken?
- Can several partial exits occur at different logic points?
- Should a portion remain open for larger profit potential?
- Is exit policy rule-based, trainable, or both?
- What should the final output model contain?

## Expected Output

```text
take_profit_policy_v1
partial_exit_policy_v1
multi_destination_exit_model_v1
runner_tail_position_policy_v1
trailing_stop_policy_v1
exit_policy_training_model_v1
profit_openness_preservation_model_v1
```
