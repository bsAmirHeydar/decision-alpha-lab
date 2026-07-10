# Hostile review and limitations

Known limits:

- live recovery without checkpoint cannot infer exact historical breach ordering;
- aggregate P05 observations do not expose the first intrabar touch timestamp;
- P07 trusts immutable P06 result geometry;
- Weekly and WW remain blocked by the weekly-boundary ADR;
- reference migration across schema versions requires explicit tooling;
- live and replay equivalence must be proven in P11 before production promotion.
