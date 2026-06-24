#ifndef __DAL_EXEC_DONCHIAN_ATR_MQH__
#define __DAL_EXEC_DONCHIAN_ATR_MQH__

// Decision Alpha Lab — reusable Donchian + ATR execution helper.
// Pure MQL5. No Python. No external scripts.
//
// Donchian breakout rule is strictly causal:
// - Signal candle is the last closed candle, shift 1.
// - Donchian upper/lower for that signal is calculated from the 20 candles BEFORE it:
//   shifts 2..21 when period=20.
// - A fresh buy breakout requires signal_close > upper and previous_close <= previous_upper.
// - A fresh sell breakout requires signal_close < lower and previous_close >= previous_lower.
//
// ATR value is read from a closed candle shift, normally shift 1.

struct DALExecDonchianBreakoutSignal
{
   bool ok;
   int direction;                  // +1 buy breakout, -1 sell breakout, 0 no signal
   datetime signal_time;
   double signal_close;
   double previous_close;
   double upper;
   double lower;
   double previous_upper;
   double previous_lower;
   int period;
   string reason;
};

void DAL_ExecDonchianResetSignal(DALExecDonchianBreakoutSignal &sig)
{
   sig.ok = false;
   sig.direction = 0;
   sig.signal_time = 0;
   sig.signal_close = 0.0;
   sig.previous_close = 0.0;
   sig.upper = 0.0;
   sig.lower = 0.0;
   sig.previous_upper = 0.0;
   sig.previous_lower = 0.0;
   sig.period = 0;
   sig.reason = "not_checked";
}

string DAL_ExecDonchianDirectionToString(const int direction)
{
   if(direction > 0)
      return "BUY";
   if(direction < 0)
      return "SELL";
   return "NONE";
}

bool DAL_ExecDonchianRange(
   const string symbol,
   const ENUM_TIMEFRAMES timeframe,
   const int first_shift,
   const int period,
   double &upper,
   double &lower,
   string &reason
)
{
   upper = 0.0;
   lower = 0.0;
   reason = "not_calculated";

   if(symbol == "")
   {
      reason = "empty_symbol";
      return false;
   }
   if(first_shift < 0)
   {
      reason = "invalid_first_shift";
      return false;
   }
   if(period <= 0)
   {
      reason = "invalid_period";
      return false;
   }

   int bars = Bars(symbol, timeframe);
   if(bars < first_shift + period + 1)
   {
      reason = "not_enough_bars";
      return false;
   }

   bool initialized = false;
   for(int i = 0; i < period; i++)
   {
      int shift = first_shift + i;
      double h = iHigh(symbol, timeframe, shift);
      double l = iLow(symbol, timeframe, shift);

      if(h <= 0.0 || l <= 0.0 || !MathIsValidNumber(h) || !MathIsValidNumber(l))
      {
         reason = "invalid_ohlc_shift_" + IntegerToString(shift);
         return false;
      }

      if(!initialized)
      {
         upper = h;
         lower = l;
         initialized = true;
      }
      else
      {
         upper = MathMax(upper, h);
         lower = MathMin(lower, l);
      }
   }

   if(!initialized)
   {
      reason = "range_not_initialized";
      return false;
   }

   reason = "ok";
   return true;
}

bool DAL_ExecDonchianFreshBreakout(
   const string symbol,
   const ENUM_TIMEFRAMES timeframe,
   const int period,
   DALExecDonchianBreakoutSignal &sig,
   string &reason
)
{
   DAL_ExecDonchianResetSignal(sig);
   reason = "not_checked";

   if(symbol == "")
   {
      reason = "empty_symbol";
      sig.reason = reason;
      return false;
   }

   int p = MathMax(1, period);
   int bars = Bars(symbol, timeframe);
   if(bars < p + 5)
   {
      reason = "not_enough_bars";
      sig.reason = reason;
      return false;
   }

   sig.period = p;
   sig.signal_time = iTime(symbol, timeframe, 1);
   sig.signal_close = iClose(symbol, timeframe, 1);
   sig.previous_close = iClose(symbol, timeframe, 2);

   if(sig.signal_time <= 0 || sig.signal_close <= 0.0 || sig.previous_close <= 0.0)
   {
      reason = "invalid_closed_bar_data";
      sig.reason = reason;
      return false;
   }

   string range_reason = "";
   // Donchian for signal candle: previous p closed bars before signal, shifts 2..p+1.
   if(!DAL_ExecDonchianRange(symbol, timeframe, 2, p, sig.upper, sig.lower, range_reason))
   {
      reason = "signal_range_failed_" + range_reason;
      sig.reason = reason;
      return false;
   }

   // Donchian for previous candle: previous p closed bars before previous candle, shifts 3..p+2.
   if(!DAL_ExecDonchianRange(symbol, timeframe, 3, p, sig.previous_upper, sig.previous_lower, range_reason))
   {
      reason = "previous_range_failed_" + range_reason;
      sig.reason = reason;
      return false;
   }

   bool buy_break = (sig.signal_close > sig.upper && sig.previous_close <= sig.previous_upper);
   bool sell_break = (sig.signal_close < sig.lower && sig.previous_close >= sig.previous_lower);

   if(buy_break && sell_break)
   {
      reason = "ambiguous_double_breakout";
      sig.reason = reason;
      return false;
   }

   if(buy_break)
   {
      sig.ok = true;
      sig.direction = 1;
      sig.reason = "ok_buy_fresh_upper_breakout";
      reason = sig.reason;
      return true;
   }

   if(sell_break)
   {
      sig.ok = true;
      sig.direction = -1;
      sig.reason = "ok_sell_fresh_lower_breakout";
      reason = sig.reason;
      return true;
   }

   reason = "no_fresh_breakout"
      + "*signalClose=" + DoubleToString(sig.signal_close, 8)
      + "*upper=" + DoubleToString(sig.upper, 8)
      + "*lower=" + DoubleToString(sig.lower, 8)
      + "*previousClose=" + DoubleToString(sig.previous_close, 8)
      + "*previousUpper=" + DoubleToString(sig.previous_upper, 8)
      + "*previousLower=" + DoubleToString(sig.previous_lower, 8);
   sig.reason = reason;
   return false;
}

bool DAL_ExecATRClosedValue(
   const string symbol,
   const ENUM_TIMEFRAMES timeframe,
   const int atr_period,
   const int shift,
   double &atr_value,
   string &reason
)
{
   atr_value = 0.0;
   reason = "not_calculated";

   if(symbol == "")
   {
      reason = "empty_symbol";
      return false;
   }

   int p = MathMax(1, atr_period);
   int sh = MathMax(1, shift);

   int handle = iATR(symbol, timeframe, p);
   if(handle == INVALID_HANDLE)
   {
      reason = "atr_handle_invalid";
      return false;
   }

   double buffer[];
   ArraySetAsSeries(buffer, true);
   int copied = CopyBuffer(handle, 0, sh, 1, buffer);
   IndicatorRelease(handle);

   if(copied != 1)
   {
      reason = "atr_copy_failed_" + IntegerToString(copied);
      return false;
   }

   atr_value = buffer[0];
   if(atr_value <= 0.0 || !MathIsValidNumber(atr_value))
   {
      reason = "atr_value_invalid";
      return false;
   }

   reason = "ok*atr=" + DoubleToString(atr_value, 8) + "*period=" + IntegerToString(p) + "*shift=" + IntegerToString(sh);
   return true;
}

string DAL_ExecDonchianSignalToLog(const DALExecDonchianBreakoutSignal &sig)
{
   return "donchianOk=" + (sig.ok ? "true" : "false")
      + "*donchianDir=" + DAL_ExecDonchianDirectionToString(sig.direction)
      + "*donchianPeriod=" + IntegerToString(sig.period)
      + "*signalTime=" + TimeToString(sig.signal_time, TIME_DATE|TIME_SECONDS)
      + "*signalClose=" + DoubleToString(sig.signal_close, 8)
      + "*upper=" + DoubleToString(sig.upper, 8)
      + "*lower=" + DoubleToString(sig.lower, 8)
      + "*previousClose=" + DoubleToString(sig.previous_close, 8)
      + "*previousUpper=" + DoubleToString(sig.previous_upper, 8)
      + "*previousLower=" + DoubleToString(sig.previous_lower, 8)
      + "*donchianReason=" + sig.reason;
}

#endif
