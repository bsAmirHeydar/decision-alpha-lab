#ifndef __DAL_M0001_CONFIG_MQH__
#define __DAL_M0001_CONFIG_MQH__

struct DALM0001Config
{
   int L;
   double zone_ratio;
   int exit_gap;
   bool consume_on_touch;
   int max_events;
   double min_rtv;
};

void DAL_M0001DefaultConfig(DALM0001Config &config)
{
   config.L = 5;
   config.zone_ratio = 0.90;
   config.exit_gap = 6;
   config.consume_on_touch = false;
   config.max_events = 300;
   config.min_rtv = 0.0;
}

#endif
