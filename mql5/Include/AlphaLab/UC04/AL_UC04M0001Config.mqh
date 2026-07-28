#ifndef __AL_UC04_M0001_CONFIG_MQH__
#define __AL_UC04_M0001_CONFIG_MQH__

#include <M0001/DAL_M0001Config.mqh>

void AL_UC04BuildM0001Config(
   DALM0001Config &config,
   const int l_value,
   const double zone_ratio,
   const int exit_gap,
   const ENUM_DALM0001ConsumeMode consume_mode
)
{
   DAL_M0001DefaultConfig(config);
   config.L = l_value;
   config.zone_ratio = zone_ratio;
   config.exit_gap = exit_gap;
   config.consume_mode = consume_mode;
   config.consume_on_touch = (consume_mode == DAL_M0001_CONSUME_BY_TOUCH);
   config.max_events = 0;
   config.min_rtv = 0.0;
}

#endif
