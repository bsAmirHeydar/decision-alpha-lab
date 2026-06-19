#ifndef __DAL_M0001_CONFIG_MQH__
#define __DAL_M0001_CONFIG_MQH__

enum ENUM_DALM0001ConsumeMode
{
   DAL_M0001_CONSUME_BY_HUNT = 0,  // node is consumed only when node price is broken/hunted
   DAL_M0001_CONSUME_BY_TOUCH = 1  // node is consumed on first touch/intersection of its territory zone
};

enum ENUM_DALM0001ConsumeReason
{
   DAL_M0001_CONSUMED_NONE = 0,
   DAL_M0001_CONSUMED_TOUCH = 1,
   DAL_M0001_CONSUMED_HUNT = 2
};

struct DALM0001Config
{
   int L;
   double zone_ratio;
   int exit_gap;
   ENUM_DALM0001ConsumeMode consume_mode;
   bool consume_on_touch; // backward-compatible alias for touch mode
   int max_events;
   double min_rtv;
};

void DAL_M0001DefaultConfig(DALM0001Config &config)
{
   config.L = 5;
   config.zone_ratio = 0.90;
   config.exit_gap = 6;
   config.consume_mode = DAL_M0001_CONSUME_BY_HUNT;
   config.consume_on_touch = false;
   config.max_events = 300;
   config.min_rtv = 0.0;
}

bool DAL_M0001ConsumesOnTouch(const DALM0001Config &config)
{
   return (config.consume_mode == DAL_M0001_CONSUME_BY_TOUCH || config.consume_on_touch);
}

string DAL_M0001ConsumeModeToString(const ENUM_DALM0001ConsumeMode mode)
{
   if(mode == DAL_M0001_CONSUME_BY_TOUCH)
      return "TOUCH_ZONE";

   return "HUNT_NODE_BREAK";
}

string DAL_M0001ConsumeReasonToString(const ENUM_DALM0001ConsumeReason reason)
{
   if(reason == DAL_M0001_CONSUMED_TOUCH)
      return "TOUCH";

   if(reason == DAL_M0001_CONSUMED_HUNT)
      return "HUNT";

   return "NONE";
}

#endif
