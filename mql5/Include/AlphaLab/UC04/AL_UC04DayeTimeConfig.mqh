#ifndef __AL_UC04_DAYE_TIME_CONFIG_MQH__
#define __AL_UC04_DAYE_TIME_CONFIG_MQH__

#include <DayeTrader/EXP0018/DAYE_Types.mqh>

void AL_UC04BuildDayeTimeConfig(
   DAYE_TimeConfig &config,
   const DAYE_BrokerOffsetMode broker_offset_mode,
   const double broker_utc_offset_hours,
   const DAYE_NyOffsetMode ny_offset_mode,
   const double manual_new_york_utc_offset_hours,
   const DAYE_LocalResolutionPolicy ambiguous_start_policy,
   const DAYE_LocalResolutionPolicy ambiguous_end_policy
)
{
   config.schema_version = DAYE_TIME_SCHEMA_VERSION;
   config.broker_offset_mode = broker_offset_mode;
   config.broker_utc_offset_minutes = (int)MathRound(broker_utc_offset_hours * 60.0);
   config.ny_offset_mode = ny_offset_mode;
   config.manual_new_york_utc_offset_minutes = (int)MathRound(manual_new_york_utc_offset_hours * 60.0);
   config.ambiguous_start_policy = ambiguous_start_policy;
   config.ambiguous_end_policy = ambiguous_end_policy;
}

#endif
