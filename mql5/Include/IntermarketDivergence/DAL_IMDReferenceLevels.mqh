#ifndef __DAL_IMD_REFERENCE_LEVELS_MQH__
#define __DAL_IMD_REFERENCE_LEVELS_MQH__

#include <IntermarketDivergence/DAL_IMDTypes.mqh>
#include <StructuralNodes/DAL_StructuralNodeEngine.mqh>

int DAL_IMD_SessionMinuteOfDay(const datetime t)
{
   MqlDateTime dt;
   TimeToStruct(t, dt);
   return dt.hour * 60 + dt.min;
}

datetime DAL_IMD_DayStart(const datetime t)
{
   MqlDateTime dt;
   TimeToStruct(t, dt);
   dt.hour = 0;
   dt.min = 0;
   dt.sec = 0;
   return StructToTime(dt);
}

datetime DAL_IMD_SessionStartForTime(const datetime t, const int start_hour, const int start_minute, const int end_hour, const int end_minute)
{
   int start_m = start_hour * 60 + start_minute;
   int end_m = end_hour * 60 + end_minute;
   int m = DAL_IMD_SessionMinuteOfDay(t);
   datetime day = DAL_IMD_DayStart(t);
   bool overnight = (end_m <= start_m);

   if(!overnight)
      return day + start_m * 60;

   if(m >= start_m)
      return day + start_m * 60;

   return day - 86400 + start_m * 60;
}

datetime DAL_IMD_SessionEndForStart(const datetime session_start, const int start_hour, const int start_minute, const int end_hour, const int end_minute)
{
   int start_m = start_hour * 60 + start_minute;
   int end_m = end_hour * 60 + end_minute;
   bool overnight = (end_m <= start_m);
   datetime day = DAL_IMD_DayStart(session_start);
   datetime end_time = day + end_m * 60;
   if(overnight)
      end_time += 86400;
   return end_time;
}

bool DAL_IMD_BarInSessionWindow(const datetime t, const int start_hour, const int start_minute, const int end_hour, const int end_minute)
{
   datetime s = DAL_IMD_SessionStartForTime(t, start_hour, start_minute, end_hour, end_minute);
   datetime e = DAL_IMD_SessionEndForStart(s, start_hour, start_minute, end_hour, end_minute);
   return (t >= s && t < e);
}

bool DAL_IMD_HighLowRange(
   const DALBar &bars[],
   const int start_index,
   const int end_index,
   double &high_out,
   double &low_out
)
{
   if(start_index < 0 || end_index < start_index || end_index >= ArraySize(bars))
      return false;

   high_out = bars[start_index].high;
   low_out = bars[start_index].low;
   for(int i=start_index+1; i<=end_index; i++)
   {
      if(bars[i].high > high_out) high_out = bars[i].high;
      if(bars[i].low < low_out) low_out = bars[i].low;
   }
   return true;
}

int DAL_IMD_FindLatestActiveNode(
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const int at_index,
   const DAL_IMDLevelSide side
)
{
   int best = -1;
   for(int i=0; i<nodes_count; i++)
   {
      if(nodes[i].active_from_index > at_index)
         continue;
      if(nodes[i].index >= at_index)
         continue;
      if(side == IMD_LEVEL_HIGH && nodes[i].type != DAL_NODE_HIGH)
         continue;
      if(side == IMD_LEVEL_LOW && nodes[i].type != DAL_NODE_LOW)
         continue;
      if(best < 0 || nodes[i].index > nodes[best].index)
         best = i;
   }
   return best;
}

bool DAL_IMD_CurrentSessionRange(
   const DALBar &bars[],
   const int at_index,
   const bool exclude_current_bar,
   const int start_hour,
   const int start_minute,
   const int end_hour,
   const int end_minute,
   double &high_out,
   double &low_out,
   datetime &session_start,
   datetime &session_end,
   int &source_index
)
{
   int end_i = exclude_current_bar ? at_index - 1 : at_index;
   if(end_i < 0)
      return false;

   session_start = DAL_IMD_SessionStartForTime(bars[at_index].time, start_hour, start_minute, end_hour, end_minute);
   session_end = DAL_IMD_SessionEndForStart(session_start, start_hour, start_minute, end_hour, end_minute);

   // If the evaluation bar is outside the configured session, clamp the reference
   // to the most recent bar that still belongs to that session. This prevents
   // after-session bars from contaminating the session high/low.
   while(end_i >= 0 && bars[end_i].time >= session_end)
      end_i--;
   if(end_i < 0 || bars[end_i].time < session_start)
      return false;

   int start_i = end_i;
   while(start_i > 0 && bars[start_i-1].time >= session_start && bars[start_i-1].time < session_end)
      start_i--;

   source_index = end_i;
   return DAL_IMD_HighLowRange(bars, start_i, end_i, high_out, low_out);
}

bool DAL_IMD_PreviousSessionRange(
   const DALBar &bars[],
   const int at_index,
   const int start_hour,
   const int start_minute,
   const int end_hour,
   const int end_minute,
   double &high_out,
   double &low_out,
   datetime &session_start,
   datetime &session_end,
   int &source_index
)
{
   if(at_index <= 0)
      return false;

   datetime current_start = DAL_IMD_SessionStartForTime(bars[at_index].time, start_hour, start_minute, end_hour, end_minute);
   int end_i = at_index - 1;
   while(end_i >= 0)
   {
      datetime s = DAL_IMD_SessionStartForTime(bars[end_i].time, start_hour, start_minute, end_hour, end_minute);
      if(s < current_start)
         break;
      end_i--;
   }
   if(end_i < 0)
      return false;

   session_start = DAL_IMD_SessionStartForTime(bars[end_i].time, start_hour, start_minute, end_hour, end_minute);
   session_end = DAL_IMD_SessionEndForStart(session_start, start_hour, start_minute, end_hour, end_minute);
   int start_i = end_i;
   while(start_i > 0)
   {
      datetime prev_s = DAL_IMD_SessionStartForTime(bars[start_i-1].time, start_hour, start_minute, end_hour, end_minute);
      if(prev_s != session_start)
         break;
      start_i--;
   }
   source_index = end_i;
   return DAL_IMD_HighLowRange(bars, start_i, end_i, high_out, low_out);
}

bool DAL_IMD_CurrentDayRange(
   const DALBar &bars[],
   const int at_index,
   const bool exclude_current_bar,
   double &high_out,
   double &low_out,
   datetime &day_start,
   int &source_index
)
{
   int end_i = exclude_current_bar ? at_index - 1 : at_index;
   if(end_i < 0)
      return false;

   day_start = DAL_IMD_DayStart(bars[at_index].time);
   int start_i = end_i;
   while(start_i > 0 && DAL_IMD_DayStart(bars[start_i-1].time) == day_start)
      start_i--;
   source_index = end_i;
   return DAL_IMD_HighLowRange(bars, start_i, end_i, high_out, low_out);
}

bool DAL_IMD_PreviousDayRange(
   const DALBar &bars[],
   const int at_index,
   double &high_out,
   double &low_out,
   datetime &day_start,
   int &source_index
)
{
   if(at_index <= 0)
      return false;

   datetime current_day = DAL_IMD_DayStart(bars[at_index].time);
   int end_i = at_index - 1;
   while(end_i >= 0 && DAL_IMD_DayStart(bars[end_i].time) == current_day)
      end_i--;
   if(end_i < 0)
      return false;

   day_start = DAL_IMD_DayStart(bars[end_i].time);
   int start_i = end_i;
   while(start_i > 0 && DAL_IMD_DayStart(bars[start_i-1].time) == day_start)
      start_i--;

   source_index = end_i;
   return DAL_IMD_HighLowRange(bars, start_i, end_i, high_out, low_out);
}

bool DAL_IMD_ResolveReferenceLevel(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const int at_index,
   const DAL_IMDLevelSide side,
   const DAL_IMDLevelSource source,
   const int rolling_lookback_bars,
   const bool exclude_current_bar,
   const int session_start_hour,
   const int session_start_minute,
   const int session_end_hour,
   const int session_end_minute,
   DAL_IMDReferenceLevel &level
)
{
   level.ok = false;
   level.price = 0.0;
   level.source = DAL_IMD_LevelSourceToString(source);
   level.source_index = -1;
   level.source_time = 0;
   level.node_id = -1;
   level.active_from_time = 0;
   level.session_high = 0.0;
   level.session_low = 0.0;
   level.session_start = 0;
   level.session_end = 0;

   if(at_index < 0 || at_index >= bars_count)
      return false;

   int end_i = exclude_current_bar ? at_index - 1 : at_index;

   if(source == IMD_LEVEL_PREVIOUS_CANDLE)
   {
      if(at_index <= 0)
         return false;
      int idx = at_index - 1;
      level.ok = true;
      level.source_index = idx;
      level.source_time = bars[idx].time;
      level.price = (side == IMD_LEVEL_HIGH ? bars[idx].high : bars[idx].low);
      return true;
   }

   if(source == IMD_LEVEL_ROLLING_LOOKBACK)
   {
      if(end_i < 0)
         return false;
      int lookback = MathMax(1, rolling_lookback_bars);
      int start_i = MathMax(0, end_i - lookback + 1);
      double h=0.0, l=0.0;
      if(!DAL_IMD_HighLowRange(bars, start_i, end_i, h, l))
         return false;
      level.ok = true;
      level.source_index = end_i;
      level.source_time = bars[end_i].time;
      level.price = (side == IMD_LEVEL_HIGH ? h : l);
      return true;
   }

   if(source == IMD_LEVEL_L_NODE)
   {
      int node_idx = DAL_IMD_FindLatestActiveNode(nodes, nodes_count, at_index, side);
      if(node_idx < 0)
         return false;
      level.ok = true;
      level.source_index = nodes[node_idx].index;
      level.source_time = nodes[node_idx].time;
      level.node_id = nodes[node_idx].id;
      level.active_from_time = nodes[node_idx].active_from_time;
      level.price = nodes[node_idx].price;
      return true;
   }

   if(source == IMD_LEVEL_CURRENT_SESSION)
   {
      double h=0.0, l=0.0;
      datetime s=0, e=0;
      int idx=-1;
      if(!DAL_IMD_CurrentSessionRange(bars, at_index, exclude_current_bar, session_start_hour, session_start_minute, session_end_hour, session_end_minute, h, l, s, e, idx))
         return false;
      level.ok = true;
      level.source_index = idx;
      level.source_time = bars[idx].time;
      level.session_high = h;
      level.session_low = l;
      level.session_start = s;
      level.session_end = e;
      level.price = (side == IMD_LEVEL_HIGH ? h : l);
      return true;
   }

   if(source == IMD_LEVEL_PREVIOUS_SESSION)
   {
      double h=0.0, l=0.0;
      datetime s=0, e=0;
      int idx=-1;
      if(!DAL_IMD_PreviousSessionRange(bars, at_index, session_start_hour, session_start_minute, session_end_hour, session_end_minute, h, l, s, e, idx))
         return false;
      level.ok = true;
      level.source_index = idx;
      level.source_time = bars[idx].time;
      level.session_high = h;
      level.session_low = l;
      level.session_start = s;
      level.session_end = e;
      level.price = (side == IMD_LEVEL_HIGH ? h : l);
      return true;
   }

   if(source == IMD_LEVEL_CURRENT_DAY)
   {
      double h=0.0, l=0.0;
      datetime d=0;
      int idx=-1;
      if(!DAL_IMD_CurrentDayRange(bars, at_index, exclude_current_bar, h, l, d, idx))
         return false;
      level.ok = true;
      level.source_index = idx;
      level.source_time = bars[idx].time;
      level.session_high = h;
      level.session_low = l;
      level.session_start = d;
      level.session_end = d + 86400;
      level.price = (side == IMD_LEVEL_HIGH ? h : l);
      return true;
   }

   if(source == IMD_LEVEL_PREVIOUS_DAY)
   {
      double h=0.0, l=0.0;
      datetime d=0;
      int idx=-1;
      if(!DAL_IMD_PreviousDayRange(bars, at_index, h, l, d, idx))
         return false;
      level.ok = true;
      level.source_index = idx;
      level.source_time = bars[idx].time;
      level.session_high = h;
      level.session_low = l;
      level.session_start = d;
      level.session_end = d + 86400;
      level.price = (side == IMD_LEVEL_HIGH ? h : l);
      return true;
   }

   return false;
}

#endif
