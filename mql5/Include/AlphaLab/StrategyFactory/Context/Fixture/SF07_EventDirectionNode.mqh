#ifndef __SF07_EVENT_DIRECTION_NODE_MQH__
#define __SF07_EVENT_DIRECTION_NODE_MQH__
#include "../ISF07_FeatureNode.mqh"
class CSF07EventDirectionNode : public ISF07FeatureNode
{
public:
   void GetDescriptor(SF07_FeatureDescriptor &d) const
   {
      SF07_ResetFeatureDescriptor(d);d.feature_id="event_direction";d.feature_version="1.0.0";d.owner_id="sf07.fixture.event_direction";d.value_type=SF01_FEATURE_INTEGER;d.update_scope=SF07_UPDATE_EVENT;d.required=true;d.numeric=true;
   }
   bool Compute(const SF01_AnatomyEvent &event,const CSF07ContextState &state,SF01_FeatureValue &value,string &error)
   {
      value=SF01_MakeIntegerFeature("event_direction","1.0.0",(long)event.direction,event.known_time,event.event_id,"sf07_direction");error="";return true;
   }
};
#endif
