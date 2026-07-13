#ifndef FP_I07_ENGINE_MQH
#define FP_I07_ENGINE_MQH
#include "FP_I07_Contracts.mqh"
#include "FP_I07_HostCloseClock.mqh"
#include "FP_I07_ConfirmationPredicate.mqh"
#include "FP_I07_LifecycleEngine.mqh"
bool FP_I07_Finalize(const SFP_I07_Projection &projection,const SFP_I07_HostBar &bar,const SFP_I07_Observation &obs,SFP_I07_Result &result)
{
   result.candidate_id=projection.candidate_id; result.outcome=FP_I07_EvaluateOutcome(projection,bar,obs); result.state=FP_I07_StateForOutcome(result.outcome); result.finalized_at=bar.close_time; result.reason_code=EnumToString(result.outcome); return true;
}
#endif
