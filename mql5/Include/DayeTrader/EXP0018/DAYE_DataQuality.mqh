
#ifndef __EXP0018_DAYE_DATA_QUALITY_MQH__
#define __EXP0018_DAYE_DATA_QUALITY_MQH__

#include <DayeTrader/EXP0018/DAYE_SymbolContract.mqh>
#include <DayeTrader/EXP0018/DAYE_Time.mqh>

bool DAYE_IsFinitePrice(const double value)
{
   return (MathIsValidNumber(value) && value > 0.0);
}

bool DAYE_ValidateMqlRate(const MqlRates &rate,string &reason_code)
{
   reason_code = "";
   if(rate.time <= 0)
   {
      reason_code = "bar_time_invalid";
      return false;
   }
   if(!DAYE_IsFinitePrice(rate.open) || !DAYE_IsFinitePrice(rate.high) ||
      !DAYE_IsFinitePrice(rate.low) || !DAYE_IsFinitePrice(rate.close))
   {
      reason_code = "bar_price_invalid";
      return false;
   }
   if(rate.high < rate.low || rate.high < rate.open || rate.high < rate.close ||
      rate.low > rate.open || rate.low > rate.close)
   {
      reason_code = "bar_ohlc_inconsistent";
      return false;
   }
   if(rate.tick_volume < 0 || rate.real_volume < 0 || rate.spread < 0)
   {
      reason_code = "bar_volume_or_spread_invalid";
      return false;
   }
   return true;
}

bool DAYE_BuildSymbolBar(const MqlRates &rate,
                         const DAYE_SymbolDescriptor &descriptor,
                         const ENUM_TIMEFRAMES timeframe,
                         const DAYE_TimeConfig &time_config,
                         const datetime current_broker_time,
                         DAYE_SymbolBar &bar)
{
   ZeroMemory(bar);
   bar.schema_version = DAYE_DATA_SCHEMA_VERSION;
   bar.status = DAYE_DATA_STATUS_INVALID_BAR;
   bar.broker_symbol = descriptor.broker_symbol;
   bar.canonical_symbol = descriptor.canonical_symbol;
   bar.timeframe = timeframe;
   bar.broker_open_time = rate.time;
   bar.open = rate.open;
   bar.high = rate.high;
   bar.low = rate.low;
   bar.close = rate.close;
   bar.tick_volume = rate.tick_volume;
   bar.spread = rate.spread;
   bar.real_volume = rate.real_volume;

   string reason = "";
   if(!DAYE_ValidateMqlRate(rate,reason))
   {
      bar.reason_code = reason;
      return false;
   }

   int resolved_broker_offset = 0;
   bool replay_safe = true;
   datetime utc_time = 0;
   if(!DAYE_BrokerToUtc(rate.time,time_config,utc_time,resolved_broker_offset,replay_safe,reason))
   {
      bar.status = DAYE_DATA_STATUS_TIME_CONVERSION_FAILED;
      bar.reason_code = reason;
      return false;
   }

   datetime ny_time = 0;
   bool is_dst = false;
   int ny_offset = 0;
   int fold = 0;
   if(!DAYE_UtcToNewYork(utc_time,time_config,ny_time,is_dst,ny_offset,fold,reason))
   {
      bar.status = DAYE_DATA_STATUS_TIME_CONVERSION_FAILED;
      bar.reason_code = reason;
      return false;
   }

   int period_seconds = PeriodSeconds(timeframe);
   if(period_seconds <= 0)
   {
      bar.reason_code = "period_seconds_invalid";
      return false;
   }

   bar.event_time_utc = utc_time;
   bar.event_time_ny = ny_time;
   bar.close_time_utc = utc_time + period_seconds;
   bar.completeness = ((long)rate.time + period_seconds <= (long)current_broker_time) ? DAYE_BAR_COMPLETENESS_CLOSED : DAYE_BAR_COMPLETENESS_OPEN;
   bar.is_replay_safe = replay_safe;
   bar.status = DAYE_DATA_STATUS_OK;
   bar.reason_code = "ok";
   bar.is_valid = true;
   return true;
}

void DAYE_InitSymbolHealth(const DAYE_SymbolDescriptor &descriptor,const DAYE_DataSyncConfig &config,DAYE_SymbolDataHealth &health)
{
   ZeroMemory(health);
   health.schema_version = DAYE_DATA_SCHEMA_VERSION;
   health.status = DAYE_DATA_STATUS_SYMBOL_UNAVAILABLE;
   health.reason_code = "not_evaluated";
   health.broker_symbol = descriptor.broker_symbol;
   health.canonical_symbol = descriptor.canonical_symbol;
   health.symbol_selected = descriptor.selected;
   health.requested_bars = config.requested_bars_per_symbol;
}

bool DAYE_ValidateChronologicalBars(DAYE_SymbolBar &bars[],DAYE_SymbolDataHealth &health)
{
   datetime previous = 0;
   for(int i=0;i<ArraySize(bars);i++)
   {
      if(!bars[i].is_valid)
      {
         health.invalid_bar_count++;
         continue;
      }
      if(previous > 0 && bars[i].event_time_utc == previous)
         health.duplicate_timestamp_count++;
      if(previous > 0 && bars[i].event_time_utc < previous)
         health.non_monotonic_count++;
      previous = bars[i].event_time_utc;
   }

   if(health.duplicate_timestamp_count > 0)
   {
      health.status = DAYE_DATA_STATUS_DUPLICATE_TIMESTAMP;
      health.reason_code = "duplicate_event_time_utc";
      return false;
   }
   if(health.non_monotonic_count > 0)
   {
      health.status = DAYE_DATA_STATUS_NON_MONOTONIC_TIME;
      health.reason_code = "non_monotonic_event_time_utc";
      return false;
   }
   return true;
}

#endif
