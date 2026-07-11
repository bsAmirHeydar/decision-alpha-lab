#ifndef __SF07_CONVICTION_SEED_NODE_MQH__
#define __SF07_CONVICTION_SEED_NODE_MQH__
#include "../ISF07_FeatureNode.mqh"
class CSF07ConvictionSeedNode : public ISF07FeatureNode
{
public:
   void GetDescriptor(SF07_FeatureDescriptor &d) const
   {
      SF07_ResetFeatureDescriptor(d);d.feature_id="conviction_seed";d.feature_version="1.0.0";d.owner_id="sf07.fixture.conviction_seed";d.value_type=SF01_FEATURE_DOUBLE;d.update_scope=SF07_UPDATE_EVENT;d.required=true;d.numeric=true;string e="";SF07_AddDependency(d,"event_direction",e);SF07_AddDependency(d,"normalized_risk",e);
   }
   bool Compute(const SF01_AnatomyEvent &event,const CSF07ContextState &state,SF01_FeatureValue &value,string &error)
   {
      SF01_FeatureValue direction,normalized;if(!state.Get("event_direction",direction)||!state.Get("normalized_risk",normalized)){error="conviction dependency missing";return false;}const double sign=(direction.integer_value>=0)?1.0:-1.0;const double seed=sign/(1.0+normalized.double_value);value=SF01_MakeDoubleFeature("conviction_seed","1.0.0",seed,event.known_time,event.event_id,"sf07_conviction");error="";return true;
   }
};
#endif
