#ifndef __DAL_LRULE_DETECTOR_MQH__
#define __DAL_LRULE_DETECTOR_MQH__

#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/LRule/DAL_LRuleTypes.mqh>

bool DAL_HighLeftOk(const DALBar &bars[], const int i, const int L)
{
   double current = bars[i].high;
   for(int k = i - L; k < i; k++)
   {
      if(k < 0)
         return false;
      if(current < bars[k].high)
         return false;
   }
   return true;
}

bool DAL_HighRightOk(const DALBar &bars[], const int i, const int L)
{
   double current = bars[i].high;
   int n = ArraySize(bars);
   for(int k = i + 1; k <= i + L; k++)
   {
      if(k >= n)
         return false;
      if(current < bars[k].high)
         return false;
   }
   return true;
}

bool DAL_LowLeftOk(const DALBar &bars[], const int i, const int L)
{
   double current = bars[i].low;
   for(int k = i - L; k < i; k++)
   {
      if(k < 0)
         return false;
      if(current > bars[k].low)
         return false;
   }
   return true;
}

bool DAL_LowRightOk(const DALBar &bars[], const int i, const int L)
{
   double current = bars[i].low;
   int n = ArraySize(bars);
   for(int k = i + 1; k <= i + L; k++)
   {
      if(k >= n)
         return false;
      if(current > bars[k].low)
         return false;
   }
   return true;
}

int DAL_AppendLRuleNode(
   DALLRuleNode &nodes[],
   const int id,
   const int index,
   const int L,
   const datetime time,
   const datetime active_from_time,
   const ENUM_DALNodeType type,
   const double price
)
{
   int size = ArraySize(nodes);
   ArrayResize(nodes, size + 1);

   nodes[size].id = id;
   nodes[size].index = index;
   nodes[size].active_from_index = index + L;
   nodes[size].time = time;
   nodes[size].active_from_time = active_from_time;
   nodes[size].type = type;
   nodes[size].price = price;
   nodes[size].confirmed = true;

   return size;
}

int DAL_DetectLRuleNodes(
   const DALBar &bars[],
   const int bars_count,
   const int L,
   DALLRuleNode &nodes[]
)
{
   ArrayResize(nodes, 0);

   if(L <= 0 || bars_count <= (2 * L + 1))
      return 0;

   int next_id = 0;

   // Confirmed-only detector:
   // A node at index i becomes knowable exactly when i + L exists.
   for(int i = L; i <= bars_count - L - 1; i++)
   {
      datetime active_time = bars[i + L].time;

      if(DAL_HighLeftOk(bars, i, L) && DAL_HighRightOk(bars, i, L))
      {
         DAL_AppendLRuleNode(nodes, next_id, i, L, bars[i].time, active_time, DAL_NODE_HIGH, bars[i].high);
         next_id++;
      }

      if(DAL_LowLeftOk(bars, i, L) && DAL_LowRightOk(bars, i, L))
      {
         DAL_AppendLRuleNode(nodes, next_id, i, L, bars[i].time, active_time, DAL_NODE_LOW, bars[i].low);
         next_id++;
      }
   }

   return ArraySize(nodes);
}

#endif
