#ifndef __SF08_REFERENCE_LIMIT_ENTRY_MQH__
#define __SF08_REFERENCE_LIMIT_ENTRY_MQH__
#include "../ISF08_EntryPolicy.mqh"
class CSF08ReferenceLimitEntry:public ISF08EntryPolicy
{
public:
   void Describe(SF08_PolicyDescriptor &d)const{d.policy_id="sf08.entry.reference_limit";d.version="1.0.0";d.kind=SF08_POLICY_ENTRY;d.deterministic=true;d.fast_path_safe=true;d.replay_safe=true;d.requires_reference_price=true;d.requires_invalidation_price=false;d.required_feature_ids_csv="";d.description="Limit candidate at the canonical anatomy reference price.";d.descriptor_hash=SF08_DerivePolicyDescriptorHash(d);}
   ENUM_SF08_POLICY_DECISION EvaluateAdmissibility(const SF01_AnatomyEvent &e,const CSF01FeatureSnapshot &s,const SF07_ContextFrame &f,const SF08_PolicyParameters &p,string &reason)const{if(!MathIsValidNumber(e.reference_price)||e.reference_price<=0.0){reason="reference price unavailable";return SF08_POLICY_SKIP;}reason="";return SF08_POLICY_ADMIT;}
   bool Build(const SF01_AnatomyEvent &e,const CSF01FeatureSnapshot &s,const SF07_ContextFrame &f,const SF08_PolicyParameters &p,SF08_EntryPlan &plan,string &error)const{plan.order_kind=SF08_ORDER_LIMIT;plan.requested_price=e.reference_price;plan.activation_time=e.confirmation_time;long ttl=MathMax((long)1,p.integer_values[0]);plan.expiration_time=SF01_MakeUtcMilliseconds(e.confirmation_time.utc_epoch_milliseconds+ttl,"UTC",0,"candidate",SF01_TIME_MILLISECONDS);plan.maximum_fill_delay_milliseconds=ttl;plan.maximum_slippage_points=MathMax(0.0,p.numeric[0]);plan.geometry_hash=SF08_DeriveEntryPlanHash(plan);return SF08_ValidateEntryPlan(plan,error);}
};
#endif
