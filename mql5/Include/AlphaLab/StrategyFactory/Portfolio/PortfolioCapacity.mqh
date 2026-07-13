#ifndef ALPHALAB_PORTFOLIO_CAPACITY_MQH
#define ALPHALAB_PORTFOLIO_CAPACITY_MQH
struct ALPortfolioCapacity { string candidate_id; double max_risk; double fill_ratio; double spread_bps; double impact_bps; bool market_open; };
#endif
