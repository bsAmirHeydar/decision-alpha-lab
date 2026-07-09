#ifndef GARTAL_NEWS_TIME_MQH
#define GARTAL_NEWS_TIME_MQH

int GT_SnapOffsetSeconds(int raw_seconds)
{
   // Broker offsets are expected to be whole minutes. Auto detection can drift by
   // a few seconds around platform/network clock changes, so snap to nearest minute.
   double minutes = (double)raw_seconds / (double)GT_SECONDS_PER_MINUTE;
   int rounded_minutes = (int)MathRound(minutes);
   int snapped = rounded_minutes * GT_SECONDS_PER_MINUTE;

   if(snapped < -12 * GT_SECONDS_PER_HOUR)
      snapped = -12 * GT_SECONDS_PER_HOUR;
   if(snapped > 14 * GT_SECONDS_PER_HOUR)
      snapped = 14 * GT_SECONDS_PER_HOUR;

   return snapped;
}

int GT_DetectBrokerGmtOffsetSeconds(GT_RuntimeState &runtime)
{
   datetime server_now = TimeCurrent();
   datetime gmt_now = TimeGMT();
   datetime local_now = TimeLocal();

   int raw_delta = (int)(server_now - gmt_now);
   int detected = GT_SnapOffsetSeconds(raw_delta);

   runtime.time_snapshot_server = server_now;
   runtime.time_snapshot_gmt = gmt_now;
   runtime.time_snapshot_local = local_now;
   runtime.server_gmt_raw_delta_seconds = raw_delta;
   runtime.broker_gmt_detected_seconds = detected;
   runtime.broker_gmt_detected_hours = detected / GT_SECONDS_PER_HOUR;

   int snap_error = (int)MathAbs((double)(raw_delta - detected));
   if(snap_error <= 5)
      runtime.broker_gmt_confidence = 100;
   else if(snap_error <= 30)
      runtime.broker_gmt_confidence = 85;
   else if(snap_error <= 90)
      runtime.broker_gmt_confidence = 60;
   else
      runtime.broker_gmt_confidence = 35;

   return detected;
}

string GT_BrokerGmtModeText(int mode)
{
   if(mode == GT_BROKER_GMT_AUTO)   return "AUTO";
   if(mode == GT_BROKER_GMT_MANUAL) return "MANUAL";
   if(mode == GT_BROKER_GMT_HYBRID) return "HYBRID";
   return "UNKNOWN";
}

string GT_SourceTimeModeText(int mode)
{
   if(mode == GT_SOURCE_TIME_UTC)    return "UTC";
   if(mode == GT_SOURCE_TIME_BROKER) return "BROKER";
   if(mode == GT_SOURCE_TIME_MANUAL) return "MANUAL_SOURCE_GMT";
   return "UNKNOWN";
}

string GT_SampleTimeModeText(int mode)
{
   if(mode == GT_SAMPLE_TIME_BROKER) return "BROKER";
   if(mode == GT_SAMPLE_TIME_SOURCE) return "SOURCE";
   if(mode == GT_SAMPLE_TIME_UTC)    return "UTC";
   return "UNKNOWN";
}

void GT_NormalizeConfigTime(GT_Config &config, GT_RuntimeState &runtime)
{
   int detected = GT_DetectBrokerGmtOffsetSeconds(runtime);
   int manual = GT_SnapOffsetSeconds(config.broker_gmt_offset_seconds);

   if(config.broker_gmt_mode == GT_BROKER_GMT_AUTO)
      config.broker_gmt_offset_seconds = detected;
   else if(config.broker_gmt_mode == GT_BROKER_GMT_MANUAL)
      config.broker_gmt_offset_seconds = manual;
   else
   {
      // Hybrid mode trusts auto detection when it looks coherent. If confidence is
      // weak, manual offset becomes the fallback.
      if(runtime.broker_gmt_confidence >= 60)
         config.broker_gmt_offset_seconds = detected;
      else
         config.broker_gmt_offset_seconds = manual;
   }

   config.source_gmt_offset_seconds = GT_SnapOffsetSeconds(config.source_gmt_offset_seconds);
   config.time_shift_seconds = config.time_shift_minutes * GT_SECONDS_PER_MINUTE;

   config.broker_gmt_offset_hours = config.broker_gmt_offset_seconds / GT_SECONDS_PER_HOUR;
   config.broker_gmt_offset_minutes = (config.broker_gmt_offset_seconds % GT_SECONDS_PER_HOUR) / GT_SECONDS_PER_MINUTE;

   runtime.broker_gmt_effective_seconds = config.broker_gmt_offset_seconds;
   runtime.source_gmt_effective_seconds = config.source_gmt_offset_seconds;
   runtime.time_shift_effective_seconds = config.time_shift_seconds;
   runtime.time_normalization_ok = true;

   runtime.time_summary = "broker=" + GT_FormatGmtOffsetSeconds(config.broker_gmt_offset_seconds) +
                          " mode=" + GT_BrokerGmtModeText(config.broker_gmt_mode) +
                          " source=" + GT_SourceTimeModeText(config.source_time_mode) +
                          " srcOffset=" + GT_FormatGmtOffsetSeconds(config.source_gmt_offset_seconds) +
                          " shift=" + IntegerToString(config.time_shift_minutes) + "m" +
                          " conf=" + IntegerToString(runtime.broker_gmt_confidence);
}

datetime GT_UtcToBrokerTime(datetime utc_time, GT_Config &config)
{
   return utc_time + config.broker_gmt_offset_seconds + config.time_shift_seconds;
}

datetime GT_BrokerToUtcTime(datetime broker_time, GT_Config &config)
{
   return broker_time - config.broker_gmt_offset_seconds - config.time_shift_seconds;
}

datetime GT_UtcToSourceTime(datetime utc_time, GT_Config &config)
{
   if(config.source_time_mode == GT_SOURCE_TIME_BROKER)
      return GT_UtcToBrokerTime(utc_time, config);
   if(config.source_time_mode == GT_SOURCE_TIME_MANUAL)
      return utc_time + config.source_gmt_offset_seconds;
   return utc_time;
}

datetime GT_SourceToUtcTime(datetime source_time, GT_Config &config)
{
   if(config.source_time_mode == GT_SOURCE_TIME_BROKER)
      return GT_BrokerToUtcTime(source_time, config);
   if(config.source_time_mode == GT_SOURCE_TIME_MANUAL)
      return source_time - config.source_gmt_offset_seconds;
   return source_time;
}

datetime GT_BrokerToSourceTime(datetime broker_time, GT_Config &config)
{
   datetime utc_time = GT_BrokerToUtcTime(broker_time, config);
   return GT_UtcToSourceTime(utc_time, config);
}

datetime GT_SourceToBrokerTime(datetime source_time, GT_Config &config)
{
   datetime utc_time = GT_SourceToUtcTime(source_time, config);
   return GT_UtcToBrokerTime(utc_time, config);
}

datetime GT_BrokerNow()
{
   return TimeCurrent();
}

datetime GT_UtcNow()
{
   return TimeGMT();
}

datetime GT_TodayBrokerMidnight()
{
   datetime now = GT_BrokerNow();
   return StringToTime(TimeToString(now, TIME_DATE));
}

datetime GT_TodayUtcMidnight()
{
   datetime now = GT_UtcNow();
   return StringToTime(TimeToString(now, TIME_DATE));
}

datetime GT_TodaySourceMidnight(GT_Config &config)
{
   datetime source_now = GT_BrokerToSourceTime(GT_BrokerNow(), config);
   return StringToTime(TimeToString(source_now, TIME_DATE));
}

datetime GT_DateTimeFromMinute(datetime day_start, int hour, int minute)
{
   int h = GT_ClampInt(hour, 0, 23);
   int m = GT_ClampInt(minute, 0, 59);
   return day_start + h * GT_SECONDS_PER_HOUR + m * GT_SECONDS_PER_MINUTE;
}

datetime GT_BuildBrokerTimeByOffset(int day_offset, int hour, int minute)
{
   return GT_DateTimeFromMinute(GT_TodayBrokerMidnight() + day_offset * GT_SECONDS_PER_DAY, hour, minute);
}

datetime GT_BuildSourceTimeByOffset(GT_Config &config, int day_offset, int hour, int minute)
{
   return GT_DateTimeFromMinute(GT_TodaySourceMidnight(config) + day_offset * GT_SECONDS_PER_DAY, hour, minute);
}

datetime GT_BuildUtcTimeByOffset(int day_offset, int hour, int minute)
{
   return GT_DateTimeFromMinute(GT_TodayUtcMidnight() + day_offset * GT_SECONDS_PER_DAY, hour, minute);
}

datetime GT_ConfiguredSampleBrokerTime(GT_Config &config, int day_offset, int hour, int minute)
{
   if(config.sample_time_mode == GT_SAMPLE_TIME_SOURCE)
   {
      datetime source_time = GT_BuildSourceTimeByOffset(config, day_offset, hour, minute);
      return GT_SourceToBrokerTime(source_time, config);
   }

   if(config.sample_time_mode == GT_SAMPLE_TIME_UTC)
   {
      datetime utc_time = GT_BuildUtcTimeByOffset(day_offset, hour, minute);
      return GT_UtcToBrokerTime(utc_time, config);
   }

   return GT_BuildBrokerTimeByOffset(day_offset, hour, minute);
}

int GT_MinuteOfDay(datetime broker_time)
{
   datetime day_start = StringToTime(TimeToString(broker_time, TIME_DATE));
   int seconds = (int)(broker_time - day_start);
   if(seconds < 0)
      seconds = 0;
   return GT_ClampInt(seconds / GT_SECONDS_PER_MINUTE, 0, 1439);
}

int GT_DayOffsetFromToday(datetime broker_time)
{
   datetime today = GT_TodayBrokerMidnight();
   datetime event_day = StringToTime(TimeToString(broker_time, TIME_DATE));
   return (int)((event_day - today) / GT_SECONDS_PER_DAY);
}

datetime GT_ConfigWindowFromBroker(GT_Config &config)
{
   return GT_TodayBrokerMidnight() - (config.days_back * GT_SECONDS_PER_DAY);
}

datetime GT_ConfigWindowToBroker(GT_Config &config)
{
   return GT_TodayBrokerMidnight() + ((config.days_forward + 1) * GT_SECONDS_PER_DAY);
}

bool GT_InConfiguredDateWindow(datetime broker_time, GT_Config &config)
{
   datetime from_time = GT_ConfigWindowFromBroker(config);
   datetime to_time = GT_ConfigWindowToBroker(config);
   return (broker_time >= from_time && broker_time < to_time);
}

void GT_UpdateEventTimeFields(GT_NewsEvent &ev, GT_Config &config, datetime broker_time)
{
   ev.time_broker = broker_time;
   ev.time_utc = GT_BrokerToUtcTime(broker_time, config);
   ev.time_source = GT_BrokerToSourceTime(broker_time, config);
   ev.day_start_broker = StringToTime(TimeToString(broker_time, TIME_DATE));
   ev.minute_of_day = GT_MinuteOfDay(broker_time);
   ev.day_offset = GT_DayOffsetFromToday(broker_time);
   ev.is_today = (ev.day_offset == 0);
   ev.in_date_window = GT_InConfiguredDateWindow(broker_time, config);
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

string GT_TimeDebugLine(GT_Config &config, GT_RuntimeState &runtime)
{
   return "server=" + TimeToString(runtime.time_snapshot_server, TIME_DATE|TIME_SECONDS) +
          " | utc=" + TimeToString(runtime.time_snapshot_gmt, TIME_DATE|TIME_SECONDS) +
          " | broker=" + GT_FormatGmtOffsetSeconds(config.broker_gmt_offset_seconds) +
          " | source=" + GT_SourceTimeModeText(config.source_time_mode) +
          " | shift=" + IntegerToString(config.time_shift_minutes) + "m";
}

#endif
