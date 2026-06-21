# VAL0016 — H6 standalone optionality edge map

This validation separates H0006 from H0004.

Run:

```text
Experts/DecisionAlphaLab/M0006/M0006_ReversalExplosiveOptionality.mq5
```

Important output lines:

```text
DAL_M0006_BUILD_SANITY
DAL_M0006_AUDIT
DAL_H0006_OPTIONALITY_FAST
DAL_H0006_OPTIONALITY_MAIN
DAL_H0006_OPTIONALITY_SLOW
DAL_H0006_EDGE_MAP_AUDIT_FAST
DAL_H0006_EDGE_BUCKET_FAST
DAL_H0006_EDGE_MAP_AUDIT_MAIN
DAL_H0006_EDGE_BUCKET_MAIN
DAL_H0006_EDGE_MAP_AUDIT_SLOW
DAL_H0006_EDGE_BUCKET_SLOW
```

Use the edge buckets to decide whether a state is:

- an actual optionality candidate
- too sparse
- neutral / unimportant
- negative versus the unconditional batch population

Recommended first settings:

```text
InpH6HorizonBarsFast = 5
InpH6HorizonBarsMain = 20
InpH6HorizonBarsSlow = 50
InpH6AtrPeriod = 14
InpH6TailAtr1 = 2.0
InpH6TailAtr2 = 4.0
InpH6TailAtr3 = 8.0
InpPrintH6EdgeMap = true
InpH6MinBucketN = 50
InpPermutationIterations = 100
```

For publication-quality stress, raise `InpPermutationIterations` to 500 or 1000.
