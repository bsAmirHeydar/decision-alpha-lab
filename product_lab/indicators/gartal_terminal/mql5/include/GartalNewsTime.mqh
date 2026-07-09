#ifndef GARTAL_NEWS_TIME_MQH
#define GARTAL_NEWS_TIME_MQH

void GT_NormalizeConfigTime(GT_Config &config, GT_RuntimeState &runtime)
{
   int detected = (int)MathRound((double)(TimeCurrent() - TimeGMT()) / 3600.0);
   detected = GT_ClampInt(detected, -12, 14);
   runtime.broker_gmt_detected_hours = detected;

   if(config.auto_detect_broker_gmt)
      config.broker_gmt_offset_hours = detected;
}

datetime GT_UtcToBrokerTime(datetime utc_time, GT_Config &config)
{
   return utc_time + (config.broker_gmt_offset_hours * 3600);
}

datetime GT_BrokerToUtcTime(datetime broker_time, GT_Config &config)
{
   return broker_time - (config.broker_gmt_offset_hours * 3600);
}

datetime GT_SourceToBrokerTime(datetime source_time, GT_Config &config)
{
   // Source time is assumed to be configured by InpSourceGMTOffsetHours.
   datetime utc_time = source_time - (config.source_gmt_offset_hours * 3600);
   return GT_UtcToBrokerTime(utc_time, config);
}

datetime GT_TodayBrokerMidnight()
{
   datetime now = TimeCurrent();
   return StringToTime(TimeToString(now, TIME_DATE));
}

int GT_MinuteOfDay(datetime broker_time)
{
   datetime day_start = StringToTime(TimeToString(broker_time, TIME_DATE));
   int seconds = (int)(broker_time - day_start);
   if(seconds < 0)
      seconds = 0;
   return GT_ClampInt(seconds / 60, 0, 1439);
}

int GT_DayOffsetFromToday(datetime broker_time)
{
   datetime today = GT_TodayBrokerMidnight();
   datetime event_day = StringToTime(TimeToString(broker_time, TIME_DATE));
   return (int)((event_day - today) / 86400);
}

bool GT_InConfiguredDateWindow(datetime broker_time, GT_Config &config)
{
   datetime today = GT_TodayBrokerMidnight();
   datetime from_time = today - (config.days_back * 86400);
   datetime to_time = today + ((config.days_forward + 1) * 86400);
   return (broker_time >= from_time && broker_time < to_time);
}

void GT_UpdateEventStatuses(GT_NewsStore &store, datetime now)
{
   for(int i=0; i<store.count; i++)
   {
      int delta = (int)(now - store.events[i].time_broker);

      if(store.events[i].is_released)
         store.events[i].status = GT_EVENT_RELEASED;
      else if(delta < 0)
         store.events[i].status = GT_EVENT_UPCOMING;
      else if(delta <= GT_STATUS_ACTIVE_WINDOW_SECONDS)
         store.events[i].status = GT_EVENT_ACTIVE;
      else if(delta > GT_STATUS_EXPIRE_SECONDS)
         store.events[i].status = GT_EVENT_EXPIRED;
      else
         store.events[i].status = GT_EVENT_ACTIVE;
   }
}

#endif
