#ifndef __SF07_REFERENCE_MAGNITUDE_NODE_MQH__
#define __SF07_REFERENCE_MAGNITUDE_NODE_MQH__
#include "../ISF07_FeatureNode.mqh"
class CSF07ReferenceMagnitudeNode : public ISF07FeatureNode
{
public:
   void GetDescriptor(SF07_FeatureDescriptor &d) const
   {
      SF07_ResetFeatureDescriptor(d);d.feature_id="reference_magnitude";d.feature_version="1.0.0";d.owner_id="sf07.fixture.reference_magnitude";d.value_type=SF01_FEATURE_DOUBLE;d.update_scope=SF07_UPDATE_EVENT;d.required=true;d.numeric=true;
   }
   bool Compute(const SF01_AnatomyEvent &event,const CSF07ContextState &state,SF01_FeatureValue &value,string &error)
   {
      const double magnitude=MathAbs(event.reference_price);if(!MathIsValidNumber(magnitude)||magnitude<=0.0){error="invalid reference magnitude";return false;}value=SF01_MakeDoubleFeature("reference_magnitude","1.0.0",magnitude,event.known_time,event.event_id,"sf07_reference");error="";return true;
   }
};
#endif
