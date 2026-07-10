#ifndef __EXP0018_DAYE_HOST_CLOSE_CLOCK_MQH__
#define __EXP0018_DAYE_HOST_CLOSE_CLOCK_MQH__

#include <DayeTrader/EXP0018/DAYE_ConfirmationTypes.mqh>

ENUM_TIMEFRAMES DAYE_ResolveHostTimeframe(const ENUM_TIMEFRAMES configured)
{
   if(configured == PERIOD_CURRENT)
      return (ENUM_TIMEFRAMES)_Period;
   return configured;
}

string DAYE_BuildHostBarId(const ENUM_TIMEFRAMES timeframe,
                           const datetime open_time_utc,
                           const string canonical_a,
                           const string canonical_b)
{
   return "EXP0018|P06|HOST|" + IntegerToString((int)timeframe) + "|" +
          IntegerToString((long)open_time_utc) + "|" + canonical_a + "|" + canonical_b;
}

bool DAYE_ReadHostBar(const string broker_symbol,
                      const string canonical_symbol,
                      const ENUM_TIMEFRAMES timeframe,
                      const int shift,
                      const DAYE_TimeConfig &time_config,
                      DAYE_HostBarSnapshot &bar)
{
   ZeroMemory(bar);
   bar.schema_version = DAYE_CONFIRMATION_SCHEMA_VERSION;
   bar.status = DAYE_HOST_CLOCK_UNKNOWN;
   bar.broker_symbol = broker_symbol;
   bar.canonical_symbol = canonical_symbol;
   bar.timeframe = timeframe;
   bar.timeframe_seconds = PeriodSeconds(timeframe);

   if(bar.timeframe_seconds <= 0)
   {
      bar.status = DAYE_HOST_CLOCK_INVALID_TIMEFRAME;
      bar.reason_code = "host_timeframe_has_no_fixed_seconds";
      return false;
   }

   MqlRates rates[];
   ArraySetAsSeries(rates,true);
   ResetLastError();
   int copied=CopyRates(broker_symbol,timeframe,shift,1,rates);
   if(copied != 1)
   {
      bar.status = DAYE_HOST_CLOCK_SYMBOL_A_UNAVAILABLE;
      bar.reason_code = "host_bar_copy_rates_failed_" + IntegerToString(GetLastError());
      return false;
   }

   int broker_offset=0;
   bool replay_safe=true;
   string reason="";
   datetime utc_open=0;
   if(!DAYE_BrokerToUtc(rates[0].time,time_config,utc_open,broker_offset,replay_safe,reason))
   {
      bar.status = DAYE_HOST_CLOCK_TIME_CONVERSION_FAILED;
      bar.reason_code = reason;
      return false;
   }

   bar.broker_open_time = rates[0].time;
   bar.open_time_utc = utc_open;
   bar.close_time_utc = utc_open + (datetime)bar.timeframe_seconds;
   bar.open = rates[0].open;
   bar.high = rates[0].high;
   bar.low = rates[0].low;
   bar.close = rates[0].close;
   bar.tick_volume = rates[0].tick_volume;
   bar.spread = rates[0].spread;
   bar.real_volume = rates[0].real_volume;
   bar.is_replay_safe = replay_safe;
   bar.is_available = true;
   bar.status = DAYE_HOST_CLOCK_READY;
   bar.reason_code = "host_bar_ready";
   return true;
}

bool DAYE_BuildHostBarPair(const DAYE_HostBarSnapshot &a,
                           const DAYE_HostBarSnapshot &b,
                           const bool require_exact_alignment,
                           DAYE_HostBarPair &pair)
{
   ZeroMemory(pair);
   pair.schema_version = DAYE_CONFIRMATION_SCHEMA_VERSION;
   pair.timeframe = a.timeframe;
   pair.timeframe_seconds = a.timeframe_seconds;
   pair.symbol_a = a;
   pair.symbol_b = b;
   pair.is_replay_safe = a.is_replay_safe && b.is_replay_safe;

   if(!a.is_available)
   {
      pair.status = DAYE_HOST_CLOCK_SYMBOL_A_UNAVAILABLE;
      pair.reason_code = a.reason_code;
      return false;
   }
   if(!b.is_available)
   {
      pair.status = DAYE_HOST_CLOCK_SYMBOL_B_UNAVAILABLE;
      pair.reason_code = b.reason_code;
      return false;
   }
   if(a.timeframe != b.timeframe || a.timeframe_seconds != b.timeframe_seconds)
   {
      pair.status = DAYE_HOST_CLOCK_TIMESTAMP_MISMATCH;
      pair.reason_code = "host_timeframe_mismatch_between_symbols";
      return false;
   }
   if(require_exact_alignment && a.open_time_utc != b.open_time_utc)
   {
      pair.status = DAYE_HOST_CLOCK_TIMESTAMP_MISMATCH;
      pair.reason_code = "host_bar_open_timestamp_mismatch";
      return false;
   }

   pair.open_time_utc = a.open_time_utc;
   pair.close_time_utc = a.close_time_utc;
   pair.host_bar_id = DAYE_BuildHostBarId(a.timeframe,a.open_time_utc,a.canonical_symbol,b.canonical_symbol);
   pair.status = DAYE_HOST_CLOCK_READY;
   pair.reason_code = "host_bar_pair_ready";
   pair.is_ready = true;
   return true;
}

bool DAYE_ReadHostClock(const DAYE_ConfirmationConfig &config,
                        const DAYE_TimeConfig &time_config,
                        const datetime processing_time_utc,
                        DAYE_HostClockSnapshot &clock)
{
   ZeroMemory(clock);
   clock.schema_version = DAYE_CONFIRMATION_SCHEMA_VERSION;
   clock.processing_time_utc = processing_time_utc;
   clock.timeframe = DAYE_ResolveHostTimeframe(config.host_timeframe);
   clock.timeframe_seconds = PeriodSeconds(clock.timeframe);
   if(clock.timeframe_seconds <= 0)
   {
      clock.status = DAYE_HOST_CLOCK_INVALID_TIMEFRAME;
      clock.reason_code = "resolved_host_timeframe_invalid";
      return false;
   }

   string broker_a=config.hunt_config.relationship_config.period_config.data_config.broker_symbol_a;
   string broker_b=config.hunt_config.relationship_config.period_config.data_config.broker_symbol_b;
   string canonical_a=config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_a;
   string canonical_b=config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_b;

   DAYE_HostBarSnapshot current_a,current_b,closed_a,closed_b;
   bool current_a_ok=DAYE_ReadHostBar(broker_a,canonical_a,clock.timeframe,0,time_config,current_a);
   bool current_b_ok=DAYE_ReadHostBar(broker_b,canonical_b,clock.timeframe,0,time_config,current_b);
   bool closed_a_ok=DAYE_ReadHostBar(broker_a,canonical_a,clock.timeframe,1,time_config,closed_a);
   bool closed_b_ok=DAYE_ReadHostBar(broker_b,canonical_b,clock.timeframe,1,time_config,closed_b);

   if(!current_a_ok || !closed_a_ok)
   {
      clock.status = DAYE_HOST_CLOCK_SYMBOL_A_UNAVAILABLE;
      clock.reason_code = !closed_a_ok ? closed_a.reason_code : current_a.reason_code;
      return false;
   }
   if(!current_b_ok || !closed_b_ok)
   {
      clock.status = DAYE_HOST_CLOCK_SYMBOL_B_UNAVAILABLE;
      clock.reason_code = !closed_b_ok ? closed_b.reason_code : current_b.reason_code;
      return false;
   }

   if(!DAYE_BuildHostBarPair(current_a,current_b,config.require_exact_host_symbol_alignment,clock.current_open_bar))
   {
      clock.status = clock.current_open_bar.status;
      clock.reason_code = "current_" + clock.current_open_bar.reason_code;
      return false;
   }
   if(!DAYE_BuildHostBarPair(closed_a,closed_b,config.require_exact_host_symbol_alignment,clock.latest_closed_bar))
   {
      clock.status = clock.latest_closed_bar.status;
      clock.reason_code = "closed_" + clock.latest_closed_bar.reason_code;
      return false;
   }

   if(clock.current_open_bar.open_time_utc < clock.latest_closed_bar.open_time_utc)
   {
      clock.status = DAYE_HOST_CLOCK_DATA_REGRESSION;
      clock.reason_code = "current_host_bar_precedes_latest_closed_bar";
      return false;
   }

   clock.is_ready = true;
   clock.is_replay_safe = clock.current_open_bar.is_replay_safe && clock.latest_closed_bar.is_replay_safe;
   clock.status = DAYE_HOST_CLOCK_READY;
   clock.reason_code = "host_clock_ready";
   return true;
}

bool DAYE_SelectHunterHostBar(const DAYE_HostBarPair &pair,const string hunter_canonical_symbol,DAYE_HostBarSnapshot &bar)
{
   if(pair.symbol_a.canonical_symbol == hunter_canonical_symbol)
   {
      bar=pair.symbol_a;
      return true;
   }
   if(pair.symbol_b.canonical_symbol == hunter_canonical_symbol)
   {
      bar=pair.symbol_b;
      return true;
   }
   ZeroMemory(bar);
   return false;
}

#endif
