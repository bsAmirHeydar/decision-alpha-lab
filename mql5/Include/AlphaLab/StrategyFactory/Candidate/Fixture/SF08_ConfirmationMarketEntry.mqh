#ifndef __SF08_CONFIRMATION_MARKET_ENTRY_MQH__
#define __SF08_CONFIRMATION_MARKET_ENTRY_MQH__
#include "SF08_FeatureAccess.mqh"
#include "../ISF08_EntryPolicy.mqh"
class CSF08ConfirmationMarketEntry:public ISF08EntryPolicy
{
public:
   void Describe(SF08_PolicyDescriptor &d)const{d.policy_id="sf08.entry.confirmation_market";d.version="1.0.0";d.kind=SF08_POLICY_ENTRY;d.deterministic=true;d.fast_path_safe=true;d.replay_safe=true;d.requires_reference_price=false;d.requires_invalidation_price=false;d.required_feature_ids_csv="confirmation_price";d.description="Market candidate at the canonical confirmation price feature.";d.descriptor_hash=SF08_DerivePolicyDescriptorHash(d);}
   ENUM_SF08_POLICY_DECISION EvaluateAdmissibility(const SF01_AnatomyEvent &e,const CSF01FeatureSnapshot &s,const SF07_ContextFrame &f,const SF08_PolicyParameters &p,string &reason)const{double v;string x="";if(!SF08_GetNumericFeature(s,"confirmation_price",v,x)){reason=x;return SF08_POLICY_SKIP;}reason="";return SF08_POLICY_ADMIT;}
   bool Build(const SF01_AnatomyEvent &e,const CSF01FeatureSnapshot &s,const SF07_ContextFrame &f,const SF08_PolicyParameters &p,SF08_EntryPlan &plan,string &error)const{double price;if(!SF08_GetNumericFeature(s,"confirmation_price",price,error))return false;plan.order_kind=SF08_ORDER_MARKET;plan.requested_price=price;plan.activation_time=e.confirmation_time;plan.expiration_time=SF01_MakeUtcMilliseconds(e.confirmation_time.utc_epoch_milliseconds+MathMax((long)0,p.integer_values[0]),"UTC",0,"candidate",SF01_TIME_MILLISECONDS);plan.maximum_fill_delay_milliseconds=MathMax((long)0,p.integer_values[0]);plan.maximum_slippage_points=MathMax(0.0,p.numeric[0]);plan.geometry_hash=SF08_DeriveEntryPlanHash(plan);return SF08_ValidateEntryPlan(plan,error);}
};
#endif
