# CH08 Strategy Architect Review Checklist

## Candle Close

- [ ] Is candle close treated as mandatory before divergence confirmation?
- [ ] Is hunt still defined through high/low touch or break?
- [ ] Is close used as a time boundary, not as a price-location filter?
- [ ] Is it clear that the candle does not need to close beyond the reference?

## Potential vs Confirmed

- [ ] Is potential divergence separated from confirmed divergence?
- [ ] Is trade permission blocked before confirmation?
- [ ] Is confirmation understood as the survival of asymmetry until close?

## Invalidation

- [ ] Is double hunt treated as invalid divergence?
- [ ] Is simultaneous hunt treated as no divergence?
- [ ] Is clean-symbol hunt after initial hunter event treated as cancellation of asymmetry?

## Uniformity

- [ ] Does every cycle group use the same confirmation standard before statistical evidence?
- [ ] Are both symbols treated under the same confirmation rule?
- [ ] Are both buy and sell divergences treated under the same confirmation rule?

## Visibility

- [ ] Are all confirmed divergences displayed?
- [ ] Are all confirmed divergences preserved for study?
- [ ] Are signals not hidden because of CG, time, direction, symbol, or reference distance?

## Research Readiness

- [ ] Can the research layer later measure confirmation delay?
- [ ] Can it measure invalidation before and after confirmation?
- [ ] Can it study double hunt as a separate non-divergence condition?
- [ ] Can it compare confirmation families without changing the base doctrine?
