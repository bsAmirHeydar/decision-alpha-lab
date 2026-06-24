#ifndef __DAL_EXEC_HEIKIN_ASHI_MQH__
#define __DAL_EXEC_HEIKIN_ASHI_MQH__

// Decision Alpha Lab — reusable Heikin Ashi execution helpers.
// Pure MQL5. No Python or external scripts.

struct DALExecHeikinAshiBar
{
   datetime time;
   double open;
   double high;
   double low;
   double close;
   int color; // +1 green, -1 red, 0 doji
};

int DAL_ExecHASign(const double value)
{
   if(value > 0.0)
      return +1;
   if(value < 0.0)
      return -1;
   return 0;
}

string DAL_ExecHAColorToString(const int color)
{
   if(color > 0)
      return "GREEN";
   if(color < 0)
      return "RED";
   return "DOJI";
}

void DAL_ExecHAReset(DALExecHeikinAshiBar &bar)
{
   bar.time = 0;
   bar.open = 0.0;
   bar.high = 0.0;
   bar.low = 0.0;
   bar.close = 0.0;
   bar.color = 0;
}

bool DAL_ExecHAComputeAtShift(
   const string symbol,
   const ENUM_TIMEFRAMES timeframe,
   const int shift,
   const int seed_bars,
   DALExecHeikinAshiBar &out,
   string &reason
)
{
   DAL_ExecHAReset(out);
   reason = "not_computed";

   if(symbol == "")
   {
      reason = "empty_symbol";
      return false;
   }
   if(shift < 0)
   {
      reason = "bad_shift";
      return false;
   }

   int count = MathMax(seed_bars, shift + 20);
   count = MathMax(count, 80);

   MqlRates rates[];
   int copied = CopyRates(symbol, timeframe, 0, count, rates);
   if(copied <= shift + 2)
   {
      reason = "not_enough_rates";
      return false;
   }

   ArraySetAsSeries(rates, true);

   double ha_open[];
   double ha_close[];
   double ha_high[];
   double ha_low[];
   ArrayResize(ha_open, copied);
   ArrayResize(ha_close, copied);
   ArrayResize(ha_high, copied);
   ArrayResize(ha_low, copied);
   ArraySetAsSeries(ha_open, true);
   ArraySetAsSeries(ha_close, true);
   ArraySetAsSeries(ha_high, true);
   ArraySetAsSeries(ha_low, true);

   for(int i = copied - 1; i >= 0; i--)
   {
      ha_close[i] = (rates[i].open + rates[i].high + rates[i].low + rates[i].close) / 4.0;
      if(i == copied - 1)
         ha_open[i] = (rates[i].open + rates[i].close) / 2.0;
      else
         ha_open[i] = (ha_open[i + 1] + ha_close[i + 1]) / 2.0;

      ha_high[i] = MathMax(rates[i].high, MathMax(ha_open[i], ha_close[i]));
      ha_low[i] = MathMin(rates[i].low, MathMin(ha_open[i], ha_close[i]));
   }

   out.time = rates[shift].time;
   out.open = ha_open[shift];
   out.close = ha_close[shift];
   out.high = ha_high[shift];
   out.low = ha_low[shift];
   out.color = DAL_ExecHASign(out.close - out.open);

   reason = "ok";
   return true;
}

bool DAL_ExecHAClosedColorFlip(
   const string symbol,
   const ENUM_TIMEFRAMES timeframe,
   int &direction,
   DALExecHeikinAshiBar &previous_closed,
   DALExecHeikinAshiBar &signal_closed,
   string &reason
)
{
   direction = 0;
   reason = "not_checked";

   string r1 = "";
   string r2 = "";
   if(!DAL_ExecHAComputeAtShift(symbol, timeframe, 2, 150, previous_closed, r1))
   {
      reason = "previous_closed_ha_failed_" + r1;
      return false;
   }
   if(!DAL_ExecHAComputeAtShift(symbol, timeframe, 1, 150, signal_closed, r2))
   {
      reason = "signal_closed_ha_failed_" + r2;
      return false;
   }

   if(previous_closed.color == 0 || signal_closed.color == 0)
   {
      reason = "closed_ha_doji";
      return false;
   }

   if(previous_closed.color == signal_closed.color)
   {
      reason = "closed_ha_no_flip*prev=" + DAL_ExecHAColorToString(previous_closed.color)
         + "*signal=" + DAL_ExecHAColorToString(signal_closed.color);
      return false;
   }

   direction = signal_closed.color;
   reason = "closed_ha_flip*prev=" + DAL_ExecHAColorToString(previous_closed.color)
      + "*signal=" + DAL_ExecHAColorToString(signal_closed.color);
   return true;
}

bool DAL_ExecHAStopFromClosedBars(
   const string symbol,
   const ENUM_TIMEFRAMES timeframe,
   const int direction,
   const int closed_bars_lookback,
   const int buffer_points,
   double &stop_price,
   string &reason
)
{
   stop_price = 0.0;
   reason = "not_calculated";

   if(direction == 0)
   {
      reason = "zero_direction";
      return false;
   }

   int lookback = MathMax(1, closed_bars_lookback);
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   if(point <= 0.0)
      point = _Point;
   double buffer = MathMax(0, buffer_points) * point;

   MqlRates rates[];
   int copied = CopyRates(symbol, timeframe, 0, lookback + 20, rates);
   if(copied <= lookback)
   {
      reason = "not_enough_rates_for_stop";
      return false;
   }
   ArraySetAsSeries(rates, true);

   bool initialized = false;
   double level = 0.0;

   for(int shift = 1; shift <= lookback; shift++)
   {
      DALExecHeikinAshiBar ha;
      string ha_reason = "";
      if(!DAL_ExecHAComputeAtShift(symbol, timeframe, shift, 150, ha, ha_reason))
      {
         reason = "ha_stop_failed_" + ha_reason;
         return false;
      }

      double candidate = 0.0;
      if(direction > 0)
         candidate = MathMin(rates[shift].low, ha.low);
      else
         candidate = MathMax(rates[shift].high, ha.high);

      if(!initialized)
      {
         level = candidate;
         initialized = true;
      }
      else
      {
         if(direction > 0)
            level = MathMin(level, candidate);
         else
            level = MathMax(level, candidate);
      }
   }

   if(!initialized)
   {
      reason = "stop_not_initialized";
      return false;
   }

   int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   if(direction > 0)
      stop_price = NormalizeDouble(level - buffer, digits);
   else
      stop_price = NormalizeDouble(level + buffer, digits);

   reason = "ok";
   return true;
}

#endif
