# CH20 — Research Translation and Future Optimization Mission

## 1. Research meaning of Chapter 20

Chapter 20 translates strategic governance into a research process.

The model is not asked to create a new trading method. It is asked to measure the current one honestly.

This means every statistical study must be separated into two layers:

1. **current statistical layer** — what the existing doctrine actually produces;
2. **future optimization layer** — what may be changed later if evidence supports it.

The first layer is mandatory. The second layer is optional and delayed.

## 2. Current statistical layer

The current layer should measure:

- raw signal count;
- confirmed signal count;
- tradeable signal count;
- cycle-group frequency;
- CG overlap frequency;
- buy/sell distribution;
- hunter/clean symbol distribution;
- win rate;
- stop rate;
- consecutive stop streaks;
- expectancy;
- dollar result;
- pip or point result;
- normalized movement result;
- maximum favorable movement;
- maximum adverse movement;
- cycle-end result;
- post-cycle continuation;
- invalidation timing;
- late-entry outcomes;
- large-stop outcomes;
- hedge cluster outcomes;
- same-CG repeated trade outcomes.

These are measurements, not rules.

## 3. Future optimization layer

The future layer may later ask:

- Should some CGs be traded and some only observed?
- Should some CGs have different target logic?
- Should some CG overlaps receive special ranking?
- Should opposite-direction CG clusters be hedged, ignored, or ranked?
- Should late-entry signals be accepted, reduced, or rejected?
- Should large-stop signals remain allowed?
- Should stop-streak families be disabled?
- Should cash session receive a higher model rank?
- Should signal density reduce position permission?
- Should the model produce live warnings?

These are not current rules. They are future questions.

## 4. Governance classification of every model output

Every model output should fall into one of these classes:

| Output type | Meaning | Can change current strategy? |
|---|---|---:|
| Measurement | A raw statistical value | No |
| Comparison | Difference between families | No |
| Ranking | Ordered family quality | No |
| Warning | Risk or weakness flag | No |
| Hypothesis | Candidate future idea | No |
| Recommendation | Proposed future rule | No, not automatically |
| Approved rule | Accepted by strategy architect | Only in future version |

This protects the strategy from accidental mutation.

## 5. Future optimization mission

The future optimization mission is not to let the model take control.

The mission is to build a disciplined path from statistics to strategy improvement:

1. collect enough data;
2. find patterns;
3. identify robust families;
4. identify fragile families;
5. produce recommendations;
6. review recommendations manually;
7. define new version scope;
8. test the changed version separately;
9. compare fixed base version vs optimized version;
10. only then decide whether optimization becomes official.

The optimized version must not overwrite the base version without comparison.

## 6. Research mission statement

Chapter 20 turns optimization into a governed future process. The current model must remain a measurement and comparison layer until the strategy architect explicitly opens the optimization gate.
