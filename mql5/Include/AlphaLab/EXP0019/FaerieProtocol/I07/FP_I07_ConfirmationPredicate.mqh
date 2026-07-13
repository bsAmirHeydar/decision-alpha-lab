#ifndef FP_I07_CONFIRMATION_PREDICATE_MQH
#define FP_I07_CONFIRMATION_PREDICATE_MQH
ENUM_FP_I07_OUTCOME FP_I07_EvaluateOutcome(const SFP_I07_Projection &projection,const SFP_I07_HostBar &bar,const SFP_I07_Observation &obs)
{
   if(!bar.is_closed || !bar.coverage_complete || obs.available_through<bar.close_time || obs.pair_state==FP_I07_DATA_INCOMPLETE) return FP_I07_OUT_UNAVAILABLE;
   if(bar.close_time>=projection.deadline) return FP_I07_OUT_DEADLINE_MISSED;
   if(obs.pair_state==FP_I07_BOTH) return FP_I07_OUT_DOUBLE_HUNT;
   if(obs.pair_state==FP_I07_PROTECTED_ONLY) return FP_I07_OUT_ROLE_CHANGED;
   if(obs.pair_state==FP_I07_NONE) return FP_I07_OUT_NO_SIGNAL;
   return FP_I07_OUT_CONFIRMED;
}
#endif
