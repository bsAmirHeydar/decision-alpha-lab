#ifndef ALPHALAB_PORTFOLIO_RUNTIME_BUNDLE_MQH
#define ALPHALAB_PORTFOLIO_RUNTIME_BUNDLE_MQH
struct ALPortfolioRuntimeBundle { string bundle_id; string plan_hash; string limits_hash; string dependence_hash; bool order_authority; bool broker_authority; bool network_authority; bool kill_switch_required; };
#endif
