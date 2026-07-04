# Index Fragment — ENT-R03

## ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace

Path:

```text
docs/experience_capture/answers/ENT-R03/
```

Summary:

In NDS, a pending limit order remains alive only while the reasons that created that trade remain valid. The order is bound to its scenario, zone, entry-level Extreme, reference node, destination, convexity profile, and risk geometry. If those reasons remain intact, the pending order can stay alive. If the reasons are invalidated, the order must be deleted or canceled. This makes pending limit lifecycle a structural reason-integrity problem rather than an arbitrary time-expiration problem.

Main derived architecture requirements:

```text
pending_limit_state_machine_v1.csv
cancel_policy_v1.csv
missed_entry_policy_v1.csv
replace_entry_policy_v1.csv
pending_order_structural_expiration_v1.csv
reason_integrity_pending_order_model_v1.csv
pending_limit_lifecycle_ledger_v1.csv
```
