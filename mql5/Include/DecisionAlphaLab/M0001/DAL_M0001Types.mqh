#ifndef __DAL_M0001_TYPES_MQH__
#define __DAL_M0001_TYPES_MQH__

#include <DecisionAlphaLab/Common/DAL_Common.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>

struct DALM0001Event
{
   int id;
   int node_id;
   int revisit_id;
   int node_index;
   int active_from_index;
   int entry_index;
   int exit_index;
   int consumed_index;
   int touch_confirmed_index;
   int event_length;

   datetime node_time;
   datetime active_from_time;
   datetime entry_time;
   datetime exit_time;
   datetime consumed_time;
   datetime touch_confirmed_time;

   ENUM_DALNodeType node_type;
   double node_price;
   double expansion_extreme;
   double territory_lower;
   double territory_upper;

   double mean_before;
   double mean_inside;
   double rtv;
   bool touch_confirmed;
   bool hunted;
   bool consumed;
   ENUM_DALM0001ConsumeReason consume_reason;
   bool closed;
};

#endif
