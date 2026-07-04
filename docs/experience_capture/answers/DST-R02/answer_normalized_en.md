# DST-R02 — Normalized Interpretation

## Core Claim

Exit policy should be trained across multiple variants.

The evaluation criteria for exit policy should remain aligned with the broader NDS principle:

```text
potential
open profit path
low cost
```

The system should not optimize exits only for comfort, win rate, or early certainty.

It should evaluate how each exit policy affects the ability to keep profit open while reducing downside or realized opportunity loss.

## Exit Policy as Trainable

The user explicitly states:

```text
different exit states should be trained
```

Therefore, the system should not hard-code a single exit method.

It should compare families such as:

```text
single take profit
multi-destination partial close
partial close plus runner
fixed structural exits
destination-based exits
logic-based exits
trailing stop variants
no-trailing variants
```

But the preferred starting family is partial profit taking under different conditions, not trailing.

## Evaluation Criteria

Exit policies should be evaluated using the same core criteria already established for NDS opportunity selection:

```text
potential
keeping profits open
low cost
```

Suggested metrics:

```text
profit_openness_preserved
tail_capture
average_R
median_R
R_distribution_skew
realized_vs_available_profit
drawdown_after_partial_exit
giveback_after_open_profit
exit_efficiency
opportunity_cost_of_early_exit
```

The best exit is not necessarily the one with highest win rate.

The best exit is the one that preserves convex upside while controlling cost and protecting realized gains where structurally justified.

## Trailing Stop Skepticism

The user is not strongly in favor of trailing stops.

Reason:

```text
prior results have not been good
```

Therefore, trailing should not be a default exit policy.

Suggested status:

```text
TRAILING_STOP_NOT_DEFAULT
```

Trailing can still be included in experiments for comparison, but it should be treated as a skeptical/secondary family rather than the preferred method.

## Partial Close Preference

The user prefers:

```text
partial profit closing under different conditions
```

This means the system should prioritize partial exit policy over trailing as the primary exit-management research path.

Partial close allows:

```text
realizing part of profit
keeping part open
preserving potential
reducing emotional or structural giveback
allowing multi-destination logic
```

This fits the broader logic:

```text
take some profit when justified
keep some exposure open when potential remains
```

## Multi-Condition Partial Exit

Partial exits should not be purely arbitrary.

They should occur under NDS-defined conditions.

Possible condition families:

```text
destination reached
first logical target reached
opposing constraint appears
optionality decreases
reward path starts closing
parent/child structure changes
new opposite zone becomes strong
F-count / Hook / Rally destination is consumed
risk-to-open-profit becomes unfavorable
```

The exact conditions should be trained and compared.

## Keeping Profit Open

A central objective is:

```text
keep profits open
```

This does not mean never taking profit.

It means avoiding exit policies that close the entire position too early and destroy tail potential.

Therefore, a good policy may be:

```text
partial close at logic points
leave runner/tail portion open
avoid aggressive trailing unless proven useful
```

## Cost of Exit Policy

Exit has cost too.

Exit cost may include:

```text
closing too early
reducing tail capture
allowing too much giveback
over-managing
trailing stop noise
extra commissions/spread from excessive partials
complexity
```

So low cost is not only entry stop cost.

There is also:

```text
exit policy cost
```

## Runner / Tail Logic

The answer implies that keeping some profit open is important.

Therefore, the model should support a runner or tail component.

Suggested states:

```text
PARTIAL_EXIT_DONE
RUNNER_REMAINS_OPEN
TAIL_POTENTIAL_ACTIVE
FINAL_EXIT_DONE
```

The runner should not be trailed by default unless the trailing family proves useful in testing.

## Machine-Readable Summary

```text
exit_policy = trainable

evaluation_criteria:
    - potential
    - profit openness
    - low cost

trailing_stop:
    - not preferred
    - not default
    - can be tested skeptically

preferred direction:
    - partial close under different NDS conditions
    - preserve part of position for open profit potential
```

## Short Formal Statement

In NDS, exit policy should be trained across different variants using the same core criteria as opportunity selection: potential, keeping profits open, and low cost. Trailing stop should not be the default because prior results have not been satisfactory. The preferred direction is to close part of the profit under different NDS-defined conditions while keeping some exposure open for larger profit potential. The system should compare exit families by how well they preserve open profit, capture tail opportunities, reduce unnecessary giveback, and avoid premature full exits.
