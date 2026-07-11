#ifndef __ALPHA_LAB_STRATEGY_FACTORY_ANATOMY_ADAPTER_MQH__
#define __ALPHA_LAB_STRATEGY_FACTORY_ANATOMY_ADAPTER_MQH__

#include "SF_Contracts.mqh"

// Anatomy adapters have no execution authority. They emit canonical events
// and feature snapshots that were fully known at the decision timestamp.
class ISF_AnatomyAdapter
  {
public:
   virtual string AdapterId(void) const=0;
   virtual string AdapterVersion(void) const=0;
   virtual bool   BuildLatestEvent(SF_AnatomyEvent &event,string &reason)=0;
   virtual bool   BuildFeatureSnapshot(const SF_AnatomyEvent &event,
                                       const datetime decision_time_utc,
                                       SF_FeatureValue &features[],
                                       string &reason)=0;
  };

bool SF_ValidateFeatureSnapshot(const SF_FeatureValue &features[],
                                const datetime decision_time_utc,
                                string &reason)
  {
   reason="";
   const int count=ArraySize(features);
   for(int i=0;i<count;i++)
     {
      if(features[i].name=="")
        { reason="empty_feature_name"; return(false); }
      if(features[i].known_time_utc>decision_time_utc)
        { reason="future_feature:"+features[i].name; return(false); }
      for(int j=i+1;j<count;j++)
        {
         if(features[i].name==features[j].name)
           { reason="duplicate_feature:"+features[i].name; return(false); }
        }
     }
   return(true);
  }

#endif
