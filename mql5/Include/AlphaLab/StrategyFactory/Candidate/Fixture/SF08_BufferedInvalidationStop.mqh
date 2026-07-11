#ifndef __SF08_BUFFERED_INVALIDATION_STOP_MQH__
#define __SF08_BUFFERED_INVALIDATION_STOP_MQH__
#include "../ISF08_StopPolicy.mqh"
#include "SF08_FeatureAccess.mqh"
class CSF08BufferedInvalidationStop:public ISF08StopPolicy
{
public:
   void Describe(SF08_PolicyDescriptor &d)const{d.policy_id="sf08.stop.buffered_invalidation";d.version="1.0.0";d.kind=SF08_POLICY_STOP;d.deterministic=true;d.fast_path_safe=true;d.replay_safe=true;d.requires_reference_price=false;d.requires_invalidation_price=true;d.required_feature_ids_csv="confirmation_price";d.description="Anatomy invalidation with deterministic directional buffer.";d.descriptor_hash=SF08_DerivePolicyDescriptorHash(d);}
   ENUM_SF08_POLICY_DECISION EvaluateAdmissibility(const SF01_AnatomyEvent &e,const CSF01FeatureSnapshot &s,const SF07_ContextFrame &f,const SF08_PolicyParameters &p,string &reason)const{if(p.numeric[0]<0.0){reason="negative stop buffer";return SF08_POLICY_ERROR;}double entry;string x="";if(!SF08_GetNumericFeature(s,"confirmation_price",entry,x)){reason=x;return SF08_POLICY_SKIP;}reason="";return SF08_POLICY_ADMIT;}
   bool Build(const SF01_AnatomyEvent &e,const CSF01FeatureSnapshot &s,const SF07_ContextFrame &f,const SF08_PolicyParameters &p,SF08_StopPlan &plan,string &error)const{double entry;if(!SF08_GetNumericFeature(s,"confirmation_price",entry,error))return false;double buffer=p.numeric[0];plan.has_price_stop=true;plan.stop_price=(e.direction==SF01_DIRECTION_LONG)?e.invalidation_price-buffer:e.invalidation_price+buffer;plan.has_time_invalidation=false;plan.invalidation_time=e.confirmation_time;plan.initial_risk_points=MathAbs(entry-plan.stop_price);plan.geometry_hash=SF08_DeriveStopPlanHash(plan);return SF08_ValidateStopPlan(plan,error);}
};
#endif
