#ifndef FP_I07_PROJECTION_ENGINE_MQH
#define FP_I07_PROJECTION_ENGINE_MQH
bool FP_I07_IsEligibleTarget(const datetime candidate_time,const SFP_I07_HostBar &bar) { return bar.close_time>candidate_time; }
#endif
