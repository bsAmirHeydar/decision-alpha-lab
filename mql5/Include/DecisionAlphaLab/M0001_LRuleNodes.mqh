//+------------------------------------------------------------------+
//| Decision Alpha Lab — Live-safe L-rule node detector               |
//+------------------------------------------------------------------+

bool DAL_IsLowPivot(MqlRates &rates[], int index, int L)
{
   const double value = rates[index].low;
   for(int j = index - L; j <= index + L; j++)
   {
      if(j == index)
         continue;
      if(rates[j].low <= value)
         return false;
   }
   return true;
}

bool DAL_IsHighPivot(MqlRates &rates[], int index, int L)
{
   const double value = rates[index].high;
   for(int j = index - L; j <= index + L; j++)
   {
      if(j == index)
         continue;
      if(rates[j].high >= value)
         return false;
   }
   return true;
}

int DAL_BuildLRuleNodes(MqlRates &rates[], int bars, int L, DAL_Node &nodes[])
{
   ArrayResize(nodes, 0);

   if(bars < (2 * L + 3))
      return 0;

   int count = 0;
   const int last_confirmable_index = bars - L - 1;

   for(int i = L; i <= last_confirmable_index; i++)
   {
      bool low_pivot = DAL_IsLowPivot(rates, i, L);
      bool high_pivot = DAL_IsHighPivot(rates, i, L);

      if(!low_pivot && !high_pivot)
         continue;

      if(low_pivot)
      {
         ArrayResize(nodes, count + 1);
         nodes[count].id = count;
         nodes[count].index = i;
         nodes[count].active_from = i + L;
         nodes[count].time = rates[i].time;
         nodes[count].type = DAL_NODE_LOW;
         nodes[count].price = rates[i].low;
         count++;
      }

      if(high_pivot)
      {
         ArrayResize(nodes, count + 1);
         nodes[count].id = count;
         nodes[count].index = i;
         nodes[count].active_from = i + L;
         nodes[count].time = rates[i].time;
         nodes[count].type = DAL_NODE_HIGH;
         nodes[count].price = rates[i].high;
         count++;
      }
   }

   return count;
}
