#ifndef ALPHALAB_SAED_V4_OUTCOME_CUBE_ROW_MQH
#define ALPHALAB_SAED_V4_OUTCOME_CUBE_ROW_MQH
// PRODUCTION_AUTHORIZATION false
struct SAEDV408OutcomeRow{string node_id;string node_hash;int action_class;int status;bool filled;bool ambiguous;double gross_r;double net_r;double mfe_r;double mae_r;double remaining_fraction;string row_hash;};
bool SAEDV408RowValid(const SAEDV408OutcomeRow &x){return StringLen(x.node_id)>0 && x.mfe_r>=0.0 && x.mae_r>=0.0 && x.remaining_fraction>=0.0 && x.remaining_fraction<=1.0;}
#endif
