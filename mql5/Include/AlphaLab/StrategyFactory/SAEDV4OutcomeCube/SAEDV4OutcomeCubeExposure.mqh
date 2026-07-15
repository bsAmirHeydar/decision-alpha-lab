#ifndef ALPHALAB_SAED_V4_OUTCOME_CUBE_EXPOSURE_MQH
#define ALPHALAB_SAED_V4_OUTCOME_CUBE_EXPOSURE_MQH
// PRODUCTION_AUTHORIZATION false
struct SAEDV408Exposure{int expected_rows;int observed_rows;int missing_rows;int duplicate_rows;bool complete;};
bool SAEDV408ExposureComplete(const SAEDV408Exposure &x){return x.complete && x.expected_rows==x.observed_rows && x.missing_rows==0 && x.duplicate_rows==0;}
#endif
