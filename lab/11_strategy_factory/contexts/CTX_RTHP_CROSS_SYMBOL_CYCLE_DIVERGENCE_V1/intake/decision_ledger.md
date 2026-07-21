# RTHP Context Decision Ledger

All questionnaire items without an explicit owner answer adopt the assistant's recommended option. Explicit owner answers override defaults. This rule applies only to the Context layer; Entry, Treatment, Execution, Stop, Target, Risk, Position Sizing, and Trade Management remain out of scope.

## Explicit owner decisions

- Q8: Record intrinsic relationship polarity. Low-side divergence is Bullish; High-side divergence is Bearish. Polarity is not a trade instruction and does not guarantee reversal.
- Q14: The relationship is invalid when the two symbols use different price bases.
- Q32, Q33, Q35, Q37, Q38: Preserve the owner's inclusive-second wording in human presentation, while canonical machine storage uses equivalent half-open intervals.
- Q50 final resolution: when one symbol lacks synchronized M15 data, retain the last available observation only as `STALE_OR_IMPUTED`; keep the relationship `UNCONFIRMED`; set `confirmed_context_event=false`; re-evaluate when synchronized real data arrives.
- Q51: All eleven named families are Context relationship-event families. The belief that WW, NN, NL, NA, LN, and AN may be stronger is stored only as an unverified research hypothesis.

## Final authority rule

This ledger is decision evidence. Canonical authority belongs to `context_manifest.yaml` and the versioned contracts referenced by it.
