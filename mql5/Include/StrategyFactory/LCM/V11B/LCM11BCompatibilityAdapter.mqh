#ifndef __LCM11B_COMPATIBILITY_ADAPTER_MQH__
#define __LCM11B_COMPATIBILITY_ADAPTER_MQH__
#include "LCM11BVisualEvent.mqh"
class CLCM11BCompatibilityAdapter
  {
public:
   bool Enabled(const bool reference_harness,const bool blocker_free)const{return reference_harness && blocker_free;}
   void FromLegacy(const string visual_id,const string event_type,const string instance_id,const long chart_id,const string symbol,const ENUM_TIMEFRAMES timeframe,const datetime t1,const double p1,const datetime t2,const double p2,const string label,LCM11BVisualEvent &event)const
     {
      event.visual_object_id=visual_id;event.event_type=event_type;event.instance_id=instance_id;event.chart_id=chart_id;event.symbol=symbol;event.timeframe=timeframe;event.time1=t1;event.price1=p1;event.time2=t2;event.price2=p2;event.availability_time=t2;event.label=label;event.lifecycle_action="ENSURE";event.event_id=visual_id+"_"+IntegerToString((long)t1)+"_"+IntegerToString((long)t2);
     }
  };
#endif
