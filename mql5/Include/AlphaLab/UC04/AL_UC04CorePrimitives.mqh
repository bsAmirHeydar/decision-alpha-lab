#ifndef __AL_UC04_CORE_PRIMITIVES_MQH__
#define __AL_UC04_CORE_PRIMITIVES_MQH__

// UC-04 canonical shared primitives. These functions preserve the exact
// observable behavior of the characterized legacy helpers while keeping
// domain-specific names and call sites behind local compatibility wrappers.

ENUM_TIMEFRAMES AL_UC04ResolveTimeframe(
   const ENUM_TIMEFRAMES configured_timeframe,
   const ENUM_TIMEFRAMES current_period
)
{
   if(configured_timeframe == PERIOD_CURRENT)
      return current_period;
   return configured_timeframe;
}

string AL_UC04FormatDateTime(const datetime value)
{
   MqlDateTime dt;
   TimeToStruct(value, dt);
   return StringFormat(
      "%04d.%02d.%02d %02d:%02d:%02d",
      dt.year,
      dt.mon,
      dt.day,
      dt.hour,
      dt.min,
      dt.sec
   );
}

bool AL_UC04AdvanceClosedBarClock(
   const datetime current_open_bar_time,
   datetime &last_open_bar_time
)
{
   if(current_open_bar_time <= 0)
      return false;

   if(last_open_bar_time <= 0)
   {
      last_open_bar_time = current_open_bar_time;
      return false;
   }

   if(current_open_bar_time == last_open_bar_time)
      return false;

   last_open_bar_time = current_open_bar_time;
   return true;
}

bool AL_UC04HasNewClosedCandle(
   const string symbol,
   const ENUM_TIMEFRAMES timeframe,
   datetime &last_open_bar_time
)
{
   return AL_UC04AdvanceClosedBarClock(
      iTime(symbol, timeframe, 0),
      last_open_bar_time
   );
}

int AL_UC04DeleteObjectsByPrefix(
   const long chart_id,
   const string prefix
)
{
   if(StringLen(prefix) <= 0)
      return 0;

   int deleted = 0;
   for(int i=ObjectsTotal(chart_id, -1, -1)-1; i>=0; i--)
   {
      string name = ObjectName(chart_id, i, -1, -1);
      if(StringFind(name, prefix) == 0)
      {
         if(ObjectDelete(chart_id, name))
            deleted++;
      }
   }
   return deleted;
}

bool AL_UC04CreateArrow(
   const long chart_id,
   const string name,
   const datetime t,
   const double price,
   const color c,
   const int arrow_code,
   const int width,
   int &objects_created
)
{
   ObjectDelete(chart_id, name);
   if(!ObjectCreate(chart_id, name, OBJ_ARROW, 0, t, price))
      return false;

   ObjectSetInteger(chart_id, name, OBJPROP_COLOR, c);
   ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width);
   ObjectSetInteger(chart_id, name, OBJPROP_ARROWCODE, arrow_code);
   ObjectSetInteger(chart_id, name, OBJPROP_BACK, false);
   ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(chart_id, name, OBJPROP_HIDDEN, true);
   objects_created++;
   return true;
}

bool AL_UC04ShouldRun(
   const bool enabled,
   const int display_family,
   const int rally_only_display_family
)
{
   if(!enabled)
      return false;
   if(display_family == rally_only_display_family)
      return false;
   return true;
}

bool AL_UC04DirectionAllowed(
   const bool show_positive,
   const bool show_negative,
   const int direction,
   const int positive_direction,
   const int negative_direction
)
{
   if(direction == positive_direction)
      return show_positive;
   if(direction == negative_direction)
      return show_negative;
   return false;
}

bool AL_UC04WriteLine(const int handle, const string line)
{
   if(handle == INVALID_HANDLE)
      return false;
   FileWriteString(handle, line + "\r\n");
   return true;
}

bool AL_UC04PricesCloseEnough(
   const string symbol,
   const double a,
   const double b
)
{
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   if(point <= 0.0)
      point = 0.00000001;
   return (MathAbs(a - b) <= point * 0.5);
}

void AL_UC04CloseFileHandle(int &handle, bool &enabled)
{
   if(handle != INVALID_HANDLE)
      FileClose(handle);
   handle = INVALID_HANDLE;
   enabled = false;
}

#endif
