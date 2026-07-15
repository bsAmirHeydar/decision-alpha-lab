#ifndef ALPHALAB_SAED_V4_OUTCOME_CUBE_COST_MQH
#define ALPHALAB_SAED_V4_OUTCOME_CUBE_COST_MQH
// PRODUCTION_AUTHORIZATION false
struct SAEDV408Cost{double entry_spread_points;double exit_spread_points;double slippage_points;double commission_r;double total_cost_points;double total_cost_r;};
SAEDV408Cost SAEDV408ComputeCost(const double risk,const double es,const double xs,const double slip,const double commission){SAEDV408Cost c;c.entry_spread_points=MathMax(0.0,es);c.exit_spread_points=MathMax(0.0,xs);c.slippage_points=MathMax(0.0,slip);c.commission_r=MathMax(0.0,commission);c.total_cost_points=c.entry_spread_points+c.exit_spread_points+c.slippage_points;c.total_cost_r=(risk>0.0?c.total_cost_points/risk:0.0)+c.commission_r;return c;}
#endif
