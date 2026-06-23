#ifndef __DAL_LRULE_TYPES_MQH__
#define __DAL_LRULE_TYPES_MQH__

#include <Common/DAL_Common.mqh>

struct DALLRuleNode
{
   int id;
   int index;
   int active_from_index;
   datetime time;
   datetime active_from_time;
   ENUM_DALNodeType type;
   double price;
   bool confirmed;
};

#endif
