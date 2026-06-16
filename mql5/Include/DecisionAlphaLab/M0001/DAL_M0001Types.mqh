#ifndef __DAL_M0001_TYPES_MQH__
#define __DAL_M0001_TYPES_MQH__

#include <DecisionAlphaLab/Common/DAL_Common.mqh>

struct DALM0001Event
{
   int id;
   int node_id;
   int revisit_id;
   int node_index;
   int active_from_index;
   int entry_index;
   int exit_index;

   datetime node_time;
   datetime active_from_time;
   datetime entry_time;
   datetime exit_time;

   ENUM_DALNodeType node_type;
   double node_price;
   double expansion_extreme;
   double territory_lower;
   double territory_upper;

   double mean_before;
   double mean_inside;
   double rtv;
   bool hunted;
   bool closed;
};

#endif
