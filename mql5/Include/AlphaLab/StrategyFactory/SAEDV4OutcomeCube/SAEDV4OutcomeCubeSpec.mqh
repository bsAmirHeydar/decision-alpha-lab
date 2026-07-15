#ifndef ALPHALAB_SAED_V4_OUTCOME_CUBE_SPEC_MQH
#define ALPHALAB_SAED_V4_OUTCOME_CUBE_SPEC_MQH
// PRODUCTION_AUTHORIZATION false
struct SAEDV408ExecutionSpec{string node_id;int action_class;int direction;double entry_price;double stop_price;double target_price;long entry_expiration_ms;long maximum_holding_ms;double partial_fraction;};
bool SAEDV408SpecValid(const SAEDV408ExecutionSpec &x){if(x.action_class!=0)return true;return (x.entry_price-x.stop_price)*x.direction>0.0 && x.partial_fraction>=0.0 && x.partial_fraction<=1.0;}
#endif
