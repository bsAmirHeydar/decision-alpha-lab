#ifndef ALPHALAB_PORTFOLIO_LIMITS_MQH
#define ALPHALAB_PORTFOLIO_LIMITS_MQH
struct ALPortfolioLimits { double total_risk; double per_symbol_risk; double per_context_risk; double max_gross; double max_net; int max_positions; int min_contexts; };
#endif
