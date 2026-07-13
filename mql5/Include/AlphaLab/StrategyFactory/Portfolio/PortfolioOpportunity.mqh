#ifndef ALPHALAB_PORTFOLIO_OPPORTUNITY_MQH
#define ALPHALAB_PORTFOLIO_OPPORTUNITY_MQH
struct ALPortfolioOpportunity { string candidate_id; string context_id; string symbol; int side; long known_time_ms; long expires_at_ms; double score; double requested_risk; double liquidity; };
#endif
