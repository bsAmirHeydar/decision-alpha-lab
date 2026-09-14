# Selected Research Findings

This document summarizes working conclusions from my own research universe. These are **not universal claims about markets**, and they are not presented as audited performance results. They are research conclusions that currently guide how I design, reject, or prioritize trading ideas.

---

## Finding 1 — Trend-following has been more robust than many counter-trend ideas I tested

### Research question

Across the strategy families I explored, which ideas remained most defensible when market, timeframe, regime, and parameter assumptions changed?

### Initial hypothesis

Mean-reversion and counter-trend systems can look attractive because entries often appear precise and historical win rates can be visually compelling. Trend-following can look less efficient because it accepts late entries, false starts, and lower prediction accuracy.

### What I tested

I explored trend, breakout, pullback, mean-reversion, divergence, volatility, and regime-adaptive ideas across different research implementations and market conditions.

### What changed my view

The important distinction was not the best historical equity curve. It was how quickly the thesis became fragile when I changed assumptions, markets, timeframes, or regimes.

In my own research universe, many counter-trend ideas depended more heavily on local price behavior and parameter choices. Trend-following ideas were generally easier to justify through a persistent mechanism: markets can continue moving after information, positioning, risk transfer, or order flow has already shifted.

### Current conclusion

I currently give more weight to trend-following and continuation frameworks when the goal is robustness rather than maximizing in-sample fit.

### What would falsify this conclusion

A counter-trend framework that remains stable across markets, timeframes, regimes, parameter ranges, transaction-cost assumptions, and out-of-sample periods—with a mechanism I can defend independently of the backtest—would change my view.

---

## Finding 2 — Prediction-heavy systems often create more fragility than usable edge

### Research question

Does increasing predictive complexity actually improve a trading system once execution, model risk, and changing market conditions are included?

### Initial hypothesis

More features, filters, models, and predictive logic should allow better entry timing and reduce bad trades.

### What I observed

It is possible to build increasingly complex systems that describe historical data very well. But each added dependency creates another assumption that can fail outside the research sample.

The real cost is not only spread, commission, or slippage. There is also **research complexity cost**: more states, more parameters, more interactions, more ways to rationalize historical behavior, and more difficulty understanding why the system is currently working or failing.

### Current conclusion

I increasingly prefer **participation and confirmation** over fragile point prediction:

- define downside before entry;
- allow the market to confirm the thesis;
- increase exposure only when observed behavior supports it;
- keep upside open where possible;
- reduce dependence on being exactly right about the next move.

The goal is not to remove forecasting completely. It is to avoid making the survival of the system depend on forecasts that cannot be defended structurally.

### What would falsify this conclusion

A more predictive system that preserves interpretability, remains stable under parameter and regime changes, survives realistic execution assumptions, and produces clear incremental value out of sample would justify the additional complexity.

---

## Finding 3 — Failure outside the original sample is evidence about hidden assumptions

### Research question

What should happen when an apparently successful strategy fails on another market, timeframe, or historical period?

### Common response I wanted to avoid

A failed validation often creates pressure to add another filter, another regime rule, or another parameter until the historical result improves again.

That can convert falsification into optimization.

### Research approach

When a strategy fails elsewhere, I first ask:

- Which assumption was true in the successful sample but absent here?
- Was that assumption explicit or hidden?
- Does the failure contradict the original mechanism?
- Is the problem execution, market structure, volatility, liquidity, timeframe, or something deeper?
- Can the missing condition be explained before it is encoded?

### Current conclusion

A failed market or timeframe is often more informative than another successful backtest. It can expose the condition the original thesis silently depended on.

I therefore treat cross-market, cross-timeframe, and regime failure as a **diagnostic tool**, not automatically as a reason to optimize parameters.

### What would falsify this conclusion

If repeated failures show no coherent relationship to identifiable assumptions—and performance is indistinguishable from sample-specific noise—the correct conclusion is not to keep explaining the strategy. It is to reject the thesis.

---

## Finding 4 — Risk architecture matters more than headline win rate

### Research question

Which performance characteristics matter most when deciding whether a strategy is suitable for real capital?

### Current view

I place less weight on win rate by itself and more weight on:

- depth and duration of drawdowns;
- ability to recover;
- payoff asymmetry;
- bounded downside versus open upside;
- tail behavior;
- capacity and execution costs;
- correlation with the rest of the portfolio;
- stability across regimes.

A strategy can be wrong often and still be useful if losses are controlled and gains are allowed to expand. A strategy can also have a high win rate while hiding severe left-tail risk.

### What would falsify this conclusion

The exact weighting of these characteristics is not fixed. It should change with mandate, liquidity, leverage, investor constraints, and portfolio context. The claim is therefore not that one metric dominates universally, but that isolated hit rate is insufficient for capital allocation.

---

## Research Integrity Note

These findings are intentionally written as **working conclusions with falsification conditions**. The purpose is not to present a polished theory after the fact, but to make the assumptions behind my research visible and challengeable.
