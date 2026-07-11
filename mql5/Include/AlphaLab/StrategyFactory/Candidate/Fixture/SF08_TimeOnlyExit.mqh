#ifndef __SF08_TIME_ONLY_EXIT_MQH__
#define __SF08_TIME_ONLY_EXIT_MQH__
#include "../ISF08_ExitPolicy.mqh"
class CSF08TimeOnlyExit:public ISF08ExitPolicy
{
public:
   void Describe(SF08_PolicyDescriptor &d)const{d.policy_id="sf08.exit.time_only";d.version="1.0.0";d.kind=SF08_POLICY_EXIT;d.deterministic=true;d.fast_path_safe=true;d.replay_safe=true;d.requires_reference_price=false;d.requires_invalidation_price=false;d.required_feature_ids_csv="";d.description="Time-only candidate exit with bounded holding horizon.";d.descriptor_hash=SF08_DerivePolicyDescriptorHash(d);}
   ENUM_SF08_POLICY_DECISION EvaluateAdmissibility(const SF01_AnatomyEvent &e,const CSF01FeatureSnapshot &s,const SF07_ContextFrame &f,const SF08_PolicyParameters &p,string &reason)const{if(p.integer_values[0]<=0){reason="time-only exit requires positive holding horizon";return SF08_POLICY_ERROR;}reason="";return SF08_POLICY_ADMIT;}
   bool Build(const SF01_AnatomyEvent &e,const CSF01FeatureSnapshot &s,const SF07_ContextFrame &f,const SF08_PolicyParameters &p,SF08_ExitPlan &plan,string &error)const{plan.exit_kind=SF08_EXIT_TIME_ONLY;plan.has_price_target=false;plan.target_price=0.0;plan.maximum_holding_milliseconds=p.integer_values[0];plan.planned_reward_points=0.0;plan.partial_fraction=0.0;plan.geometry_hash=SF08_DeriveExitPlanHash(plan);return SF08_ValidateExitPlan(plan,error);}
};
#endif
