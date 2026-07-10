# Phase 12.5 Readiness Gate Contract

## Statuses

### READY_FOR_PHASE13

All required critical gates pass. Model comparison may begin, but no model gains execution authority.

### READY_WITH_WARNINGS

No critical block exists, but evidence is incomplete or weak. Phase 13 may run for engineering validation, while conclusions remain provisional.

### BLOCKED_FOR_PHASE13

At least one required critical gate failed. Model comparison would produce untrustworthy evidence.

## Required gates

1. critical files present;
2. schemas complete;
3. primary keys unique and present;
4. cross-phase lineage reconciled;
5. semantic invariants valid;
6. walk-forward temporal boundaries valid;
7. writer metrics reconciled;
8. OOS predictions available.

## Advisory gate

At least three usable folds are recommended. Fewer folds do not always indicate a code defect, but they are insufficient for stability claims.

## Governance

Readiness authorizes only Phase 13 research. It never authorizes filtering, risk changes, or live execution.
