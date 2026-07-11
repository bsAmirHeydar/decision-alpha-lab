#ifndef __SF07_RISK_DISTANCE_NODE_MQH__
#define __SF07_RISK_DISTANCE_NODE_MQH__
#include "../ISF07_FeatureNode.mqh"
class CSF07RiskDistanceNode : public ISF07FeatureNode
{
public:
   void GetDescriptor(SF07_FeatureDescriptor &d) const
   {
      SF07_ResetFeatureDescriptor(d);d.feature_id="risk_distance";d.feature_version="1.0.0";d.owner_id="sf07.fixture.risk_distance";d.value_type=SF01_FEATURE_DOUBLE;d.update_scope=SF07_UPDATE_EVENT;d.required=true;d.numeric=true;
   }
   bool Compute(const SF01_AnatomyEvent &event,const CSF07ContextState &state,SF01_FeatureValue &value,string &error)
   {
      const double risk=MathAbs(event.reference_price-event.invalidation_price);if(!MathIsValidNumber(risk)||risk<=0.0){error="invalid event risk distance";return false;}value=SF01_MakeDoubleFeature("risk_distance","1.0.0",risk,event.known_time,event.event_id,"sf07_risk");error="";return true;
   }
};
#endif
