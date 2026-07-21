#ifndef __LCM11B_VISUAL_EVENT_MQH__
#define __LCM11B_VISUAL_EVENT_MQH__
struct LCM11BVisualEvent
  {
   string event_id;
   string visual_object_id;
   string event_type;
   string instance_id;
   long   chart_id;
   string symbol;
   ENUM_TIMEFRAMES timeframe;
   datetime availability_time;
   datetime time1;
   datetime time2;
   double price1;
   double price2;
   string label;
   string lifecycle_action;
  };
#endif
