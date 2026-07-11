#ifndef __SF08_FIXED_R_EXIT_MQH__
#define __SF08_FIXED_R_EXIT_MQH__
#include "../ISF08_ExitPolicy.mqh"
#include "SF08_FeatureAccess.mqh"
class CSF08FixedRExit:public ISF08ExitPolicy
{
public:
   void Describe(SF08_PolicyDescriptor &d)const{d.policy_id="sf08.exit.fixed_r";d.version="1.0.0";d.kind=SF08_POLICY_EXIT;d.deterministic=true;d.fast_path_safe=true;d.replay_safe=true;d.requires_reference_price=false;d.requires_invalidation_price=true;d.required_feature_ids_csv="confirmation_price";d.description="Fixed R target derived from confirmation price and invalidation geometry.";d.descriptor_hash=SF08_DerivePolicyDescriptorHash(d);}
   ENUM_SF08_POLICY_DECISION EvaluateAdmissibility(const SF01_AnatomyEvent &e,const CSF01FeatureSnapshot &s,const SF07_ContextFrame &f,const SF08_PolicyParameters &p,string &reason)const{if(!MathIsValidNumber(p.numeric[0])||p.numeric[0]<=0.0){reason="fixed R must be positive";return SF08_POLICY_ERROR;}double entry;string x="";if(!SF08_GetNumericFeature(s,"confirmation_price",entry,x)){reason=x;return SF08_POLICY_SKIP;}reason="";return SF08_POLICY_ADMIT;}
   bool Build(const SF01_AnatomyEvent &e,const CSF01FeatureSnapshot &s,const SF07_ContextFrame &f,const SF08_PolicyParameters &p,SF08_ExitPlan &plan,string &error)const{double entry;if(!SF08_GetNumericFeature(s,"confirmation_price",entry,error))return false;double risk=MathAbs(entry-e.invalidation_price);double reward=risk*p.numeric[0];plan.exit_kind=(p.integer_values[0]>0)?SF08_EXIT_PRICE_OR_TIME:SF08_EXIT_PRICE_TARGET;plan.has_price_target=true;plan.target_price=(e.direction==SF01_DIRECTION_LONG)?entry+reward:entry-reward;plan.maximum_holding_milliseconds=MathMax((long)0,p.integer_values[0]);plan.planned_reward_points=reward;plan.partial_fraction=0.0;plan.geometry_hash=SF08_DeriveExitPlanHash(plan);return SF08_ValidateExitPlan(plan,error);}
};
#endif
