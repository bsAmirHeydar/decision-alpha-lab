# EXP0017 — Module Dependency Map

```text
Master Doctrine
  -> Time Anatomy
    -> Symbol Pair Anatomy
      -> Reference Field
        -> Hunt Anatomy
          -> Divergence Anatomy
            -> Confirmation / Invalidation
              -> Drawing
              -> Signal Ledger
                -> Outcome Engine
                  -> Statistical Reports
                    -> Model Dataset
                      -> Ranking Layer
                        -> Decision Promotion Gate
                          -> Raw / Filtered Execution
                            -> AI Analyst Layer
```

## Dependency Rule

A module may consume the state of earlier modules, but it must not silently redefine them. The time module is the sole source of the trading-day and cycle calendar. The reference module is the sole source of reference candidates. The hunt module is the sole source of touch/break/equality hunt state. The divergence module is the sole source of hunter/clean asymmetry.
