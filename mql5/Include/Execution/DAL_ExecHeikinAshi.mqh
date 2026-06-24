#ifndef __DAL_EXEC_HEIKIN_ASHI_MQH__
#define __DAL_EXEC_HEIKIN_ASHI_MQH__

// Decision Alpha Lab — reusable Heikin Ashi execution helpers.
// Pure MQL5. No Python. No external scripts.
//
// Heikin Ashi direction is NOT read from any visual candle styling.
// It is calculated only from the Heikin Ashi body relation:
// +1 when ha_close > ha_open
// -1 when ha_close < ha_open
//  0 when ha_close == ha_open

struct DALExecHeikinAshiBar
{
   datetime time;

   double real_open;
   double real_high;
   double real_low;
   double real_close;

   double ha_open;
   double ha_high;
   double ha_low;
   double ha_close;

   // Body direction, derived only from ha_close vs ha_open.
   // +1 = ha_close > ha_open
   // -1 = ha_close < ha_open
   //  0 = equal body / doji
   int ha_dir;
};

int DAL_ExecHABodyDirection(const double ha_open, const double ha_close)
{
   if(ha_close > ha_open)
      return +1;
   if(ha_close < ha_open)
      return -1;
   return 0;
}

string DAL_ExecHABodyDirectionToString(const int ha_dir)
{
   if(ha_dir > 0)
      return "HA_CLOSE_ABOVE_OPEN";
   if(ha_dir < 0)
      return "HA_CLOSE_BELOW_OPEN";
   return "HA_CLOSE_EQUALS_OPEN";
}

void DAL_ExecHAReset(DALExecHeikinAshiBar &bar)
{
   bar.time = 0;

   bar.real_open = 0.0;
   bar.real_high = 0.0;
   bar.real_low = 0.0;
   bar.real_close = 0.0;

   bar.ha_open = 0.0;
   bar.ha_high = 0.0;
   bar.ha_low = 0.0;
   bar.ha_close = 0.0;

   bar.ha_dir = 0;
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

   int count = MathMax(seed_bars, shift + 30);
   count = MathMax(count, 120);

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

   // With series arrays, copied-1 is the oldest bar and 0 is the current bar.
   // Heikin Ashi must be calculated causally from oldest to newest.
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

   out.real_open = rates[shift].open;
   out.real_high = rates[shift].high;
   out.real_low = rates[shift].low;
   out.real_close = rates[shift].close;

   out.ha_open = ha_open[shift];
   out.ha_high = ha_high[shift];
   out.ha_low = ha_low[shift];
   out.ha_close = ha_close[shift];
   out.ha_dir = DAL_ExecHABodyDirection(out.ha_open, out.ha_close);

   reason = "ok";
   return true;
}

// Detects a closed lower-timeframe Heikin Ashi body flip.
// This is purely close/open based:
// BUY trigger:  previous_closed.ha_close < previous_closed.ha_open
//               signal_closed.ha_close   > signal_closed.ha_open
// SELL trigger: previous_closed.ha_close > previous_closed.ha_open
//               signal_closed.ha_close   < signal_closed.ha_open
bool DAL_ExecHAClosedBodyFlip(
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

   // Only completed lower-timeframe candles are eligible:
   // shift 2 = previous closed candle
   // shift 1 = last closed signal candle
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

   if(previous_closed.ha_dir == 0 || signal_closed.ha_dir == 0)
   {
      reason = "closed_ha_equal_body";
      return false;
   }

   if(previous_closed.ha_dir == signal_closed.ha_dir)
   {
      reason = "closed_ha_no_body_flip*prev=" + DAL_ExecHABodyDirectionToString(previous_closed.ha_dir)
         + "*signal=" + DAL_ExecHABodyDirectionToString(signal_closed.ha_dir);
      return false;
   }

   direction = signal_closed.ha_dir;
   reason = "closed_ha_body_flip*prev=" + DAL_ExecHABodyDirectionToString(previous_closed.ha_dir)
      + "*signal=" + DAL_ExecHABodyDirectionToString(signal_closed.ha_dir);
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
   int copied = CopyRates(symbol, timeframe, 0, lookback + 50, rates);
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
         candidate = MathMin(rates[shift].low, ha.ha_low);
      else
         candidate = MathMax(rates[shift].high, ha.ha_high);

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
