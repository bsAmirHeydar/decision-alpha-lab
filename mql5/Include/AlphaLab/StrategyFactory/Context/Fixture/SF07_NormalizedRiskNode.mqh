#ifndef __SF07_NORMALIZED_RISK_NODE_MQH__
#define __SF07_NORMALIZED_RISK_NODE_MQH__
#include "../ISF07_FeatureNode.mqh"
class CSF07NormalizedRiskNode : public ISF07FeatureNode
{
public:
   void GetDescriptor(SF07_FeatureDescriptor &d) const
   {
      SF07_ResetFeatureDescriptor(d);d.feature_id="normalized_risk";d.feature_version="1.0.0";d.owner_id="sf07.fixture.normalized_risk";d.value_type=SF01_FEATURE_DOUBLE;d.update_scope=SF07_UPDATE_EVENT;d.required=true;d.numeric=true;string e="";SF07_AddDependency(d,"risk_distance",e);SF07_AddDependency(d,"reference_magnitude",e);
   }
   bool Compute(const SF01_AnatomyEvent &event,const CSF07ContextState &state,SF01_FeatureValue &value,string &error)
   {
      SF01_FeatureValue risk,reference;if(!state.Get("risk_distance",risk)||!state.Get("reference_magnitude",reference)){error="normalized risk dependency missing";return false;}if(reference.double_value<=0.0){error="normalized risk denominator invalid";return false;}value=SF01_MakeDoubleFeature("normalized_risk","1.0.0",risk.double_value/reference.double_value,event.known_time,event.event_id,"sf07_normalized");error="";return true;
   }
};
#endif
