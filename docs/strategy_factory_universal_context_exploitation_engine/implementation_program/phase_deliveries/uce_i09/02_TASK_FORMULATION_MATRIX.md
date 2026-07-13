# Task Formulation Matrix

| Question | Formulation | Unit | Required label | Primary evidence | Runtime output |
|---|---|---|---|---|---|
| Which opportunity should receive scarce risk? | ranking | opportunity group | net utility relevance | NDCG, pairwise accuracy, top-k utility | rank score |
| Which entry/stop/exit treatment is best here? | treatment choice | opportunity × treatment | treatment utility vector or logged reward | regret, policy value, support audit | allowed action + utility |
| How long until target, stop, or expiry? | survival | opportunity | duration + event | c-index, integrated Brier, calibration | survival curve |
| Which terminal cause occurs first? | competing risk | opportunity | duration + cause | cause-specific calibration | cumulative incidence |
| What are the return tails? | distributional | opportunity/treatment | net utility | pinball, interval coverage, CVaR error | quantiles + interval |
| Can related outcomes share signal? | multi-task | shared context row | multi-output target | head loss + balance | vector output |
| Does context regime require a specialist? | regime gating | opportunity | regime evidence | support + fallback audit | expert key |
| Can a logged policy be safely improved? | bounded policy | logged decision | action, reward, propensity, mask | value LCB + support | action/baseline/abstain |

No formulation is allowed to hide missing support behind a high aggregate score. Each task carries a non-compensatory support gate.
