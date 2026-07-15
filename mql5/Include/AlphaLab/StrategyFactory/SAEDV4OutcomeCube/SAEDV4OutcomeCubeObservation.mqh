#ifndef ALPHALAB_SAED_V4_OUTCOME_CUBE_OBSERVATION_MQH
#define ALPHALAB_SAED_V4_OUTCOME_CUBE_OBSERVATION_MQH
// PRODUCTION_AUTHORIZATION false
struct SAEDV408Observation{long sequence;datetime observed_at;double open;double high;double low;double close;double spread_points;};
bool SAEDV408ObservationValid(const SAEDV408Observation &x){return x.sequence>=0 && x.low>0.0 && x.high>=x.low && x.open>=x.low && x.open<=x.high && x.close>=x.low && x.close<=x.high && x.spread_points>=0.0;}
#endif
