#ifndef GARTAL_NEWS_ALERTS_MQH
#define GARTAL_NEWS_ALERTS_MQH

//+------------------------------------------------------------------+
//| Stage 07 Alert Engine + State Machine                            |
//| Alerts are deterministic, event-id based, filter-aware, and        |
//| duplicate-safe. This module never mutates the event store.         |
//+------------------------------------------------------------------+

void GT_InitAlertState(GT_AlertState &state)
{
   state.sent_count = 0;
   state.last_sent_at = 0;
   state.last_sent_key = "";
   state.last_sent_stage = "";
   state.last_event_id = "";
   state.last_message = "";
   state.total_sent = 0;
   state.pre_alerts_sent = 0;
   state.release_alerts_sent = 0;
   state.actual_alerts_sent = 0;
   state.breaking_alerts_sent = 0;
   state.suppressed_count = 0;
   state.duplicate_count = 0;

   for(int i=0; i<GT_MAX_ALERT_KEYS; i++)
   {
      state.sent_keys[i] = "";
      state.sent_times[i] = 0;
      state.sent_event_ids[i] = "";
      state.sent_stages[i] = "";
   }
}

string GT_AlertStageText(string stage)
{
   if(stage == GT_ALERT_STAGE_PRE_60M)  return "60m before";
   if(stage == GT_ALERT_STAGE_PRE_30M)  return "30m before";
   if(stage == GT_ALERT_STAGE_PRE_15M)  return "15m before";
   if(stage == GT_ALERT_STAGE_PRE_5M)   return "5m before";
   if(stage == GT_ALERT_STAGE_PRE_1M)   return "1m before";
   if(stage == GT_ALERT_STAGE_RELEASE)  return "release now";
   if(stage == GT_ALERT_STAGE_ACTUAL)   return "actual released";
   if(stage == GT_ALERT_STAGE_BREAKING) return "breaking watch";
   return stage;
}

int GT_AlertStageWeight(string stage)
{
   if(stage == GT_ALERT_STAGE_BREAKING) return 800;
   if(stage == GT_ALERT_STAGE_RELEASE)  return 700;
   if(stage == GT_ALERT_STAGE_ACTUAL)   return 650;
   if(stage == GT_ALERT_STAGE_PRE_1M)   return 600;
   if(stage == GT_ALERT_STAGE_PRE_5M)   return 500;
   if(stage == GT_ALERT_STAGE_PRE_15M)  return 400;
   if(stage == GT_ALERT_STAGE_PRE_30M)  return 300;
   if(stage == GT_ALERT_STAGE_PRE_60M)  return 200;
   return 0;
}

string GT_AlertKey(GT_NewsEvent &ev, string stage)
{
   return ev.id + "_" + stage;
}

bool GT_AlertAlreadySent(GT_AlertState &state, string key)
{
   for(int i=0; i<state.sent_count; i++)
      if(state.sent_keys[i] == key)
         return true;
   return false;
}

bool GT_AlertCooldownPassed(GT_Config &config, GT_AlertState &state, datetime now)
{
   if(config.alert_cooldown_seconds <= 0)
      return true;
   if(state.last_sent_at == 0)
      return true;
   return ((now - state.last_sent_at) >= config.alert_cooldown_seconds);
}

void GT_MarkAlertSent(GT_AlertState &state, string key, GT_NewsEvent &ev, string stage, string message, datetime now)
{
   if(state.sent_count < GT_MAX_ALERT_KEYS)
   {
      int i = state.sent_count;
      state.sent_keys[i] = key;
      state.sent_times[i] = now;
      state.sent_event_ids[i] = ev.id;
      state.sent_stages[i] = stage;
      state.sent_count++;
   }

   state.last_sent_at = now;
   state.last_sent_key = key;
   state.last_sent_stage = stage;
   state.last_event_id = ev.id;
   state.last_message = message;
   state.total_sent++;

   if(stage == GT_ALERT_STAGE_RELEASE)
      state.release_alerts_sent++;
   else if(stage == GT_ALERT_STAGE_ACTUAL)
      state.actual_alerts_sent++;
   else if(stage == GT_ALERT_STAGE_BREAKING)
      state.breaking_alerts_sent++;
   else
      state.pre_alerts_sent++;
}

bool GT_EventEligibleForAlertByConfig(GT_Config &config, GT_NewsEvent &ev)
{
   if(!ev.in_date_window)
      return false;

   if(!config.alert_past_events && (ev.status == GT_EVENT_EXPIRED || ev.status == GT_EVENT_RELEASED))
   {
      // Release and actual stages do their own release-window checks.
      if(ev.time_broker < TimeCurrent() - config.alert_release_window_seconds)
         return false;
   }

   if(config.alert_high_impact_only && ev.impact != GT_IMPACT_HIGH)
      return false;

   if(ev.impact == GT_IMPACT_MEDIUM && !config.alert_include_medium)
      return false;
   if(ev.impact == GT_IMPACT_LOW && !config.alert_include_low)
      return false;
   if(ev.impact == GT_IMPACT_HOLIDAY && !config.alert_include_holiday)
      return false;

   if(ev.is_holiday && !config.alert_include_holiday)
      return false;
   if(ev.is_speech && !config.alert_speech)
      return false;
   if(ev.is_breaking && !config.alert_breaking)
      return false;
   if(ev.is_tentative && !config.alert_tentative)
      return false;

   return true;
}

bool GT_EventEligibleForAlert(GT_Config &config, GT_FilterState &filters, GT_NewsEvent &ev)
{
   if(!GT_EventEligibleForAlertByConfig(config, ev))
      return false;

   if(config.alert_respect_runtime_filters && !GT_EventPassesFilters(ev, filters))
      return false;

   return true;
}

string GT_AlertEventPayload(GT_Config &config, GT_NewsEvent &ev, string stage, datetime now)
{
   string prefix = "gartal terminal | " + GT_AlertStageText(stage);
   string impact = ev.is_breaking ? "BREAKING RED" : GT_ImpactText(ev.impact);
   string timing = "time=" + TimeToString(ev.time_broker, TIME_DATE|TIME_MINUTES) + " | in=" + GT_FormatMinutesRemaining(ev.time_broker, now);
   string msg = prefix + " | " + ev.currency + " " + impact + " | " + ev.title + " | " + timing;

   if(config.alert_include_forecast_previous)
   {
      string f = GT_IsEmpty(ev.forecast) ? "-" : ev.forecast;
      string p = GT_IsEmpty(ev.previous) ? "-" : ev.previous;
      msg += " | forecast=" + f + " previous=" + p;
   }

   if(config.alert_include_actual_row)
   {
      string a = GT_IsEmpty(ev.actual) ? "-" : ev.actual;
      msg += " | actual=" + a;
   }

   if(ev.is_tentative)
      msg += " | tentative";
   if(ev.is_speech)
      msg += " | speech";
   if(ev.is_breaking)
      msg += " | unscheduled/breaking";

   return msg;
}

bool GT_DeliverAlert(GT_Config &config, string message, GT_RuntimeState &runtime)
{
   if(!config.enable_alerts)
      return false;

   if(config.alert_log_only)
   {
      GT_RuntimeLog(runtime, GT_LOG_INFO, "Alert log-only: " + message);
      return true;
   }

   if(config.alert_popup) Alert(message);
   if(config.alert_sound) PlaySound(config.alert_sound_file);
   if(config.alert_push)  SendNotification(message);
   if(config.alert_email) SendMail("gartal terminal", message);

   GT_RuntimeLog(runtime, GT_LOG_INFO, "Alert sent: " + message);
   return true;
}

bool GT_TrySendAlert(GT_Config &config,
                     GT_AlertState &state,
                     GT_NewsEvent &ev,
                     string stage,
                     GT_RuntimeState &runtime,
                     datetime now)
{
   string key = GT_AlertKey(ev, stage);

   if(GT_AlertAlreadySent(state, key))
   {
      state.duplicate_count++;
      runtime.alert_last_suppressed_count++;
      return false;
   }

   if(!GT_AlertCooldownPassed(config, state, now))
   {
      state.suppressed_count++;
      runtime.alert_last_suppressed_count++;
      return false;
   }

   string msg = GT_AlertEventPayload(config, ev, stage, now);
   bool delivered = GT_DeliverAlert(config, msg, runtime);
   if(!delivered)
      return false;

   GT_MarkAlertSent(state, key, ev, stage, msg, now);

   runtime.alert_last_sent_count++;
   runtime.alert_last_sent_at = now;
   runtime.alert_last_stage = stage;
   runtime.alert_last_event_id = ev.id;
   runtime.alert_last_message = msg;

   return true;
}

bool GT_PreAlertBandActive(int remaining_seconds, int upper_seconds, int lower_seconds)
{
   if(remaining_seconds < 0)
      return false;
   if(remaining_seconds > upper_seconds)
      return false;
   if(remaining_seconds <= lower_seconds)
      return false;
   return true;
}

void GT_ProcessPreAlertsForEvent(GT_Config &config,
                                 GT_AlertState &state,
                                 GT_NewsEvent &ev,
                                 GT_RuntimeState &runtime,
                                 datetime now)
{
   int remaining = (int)(ev.time_broker - now);
   if(remaining < 0)
      return;

   // Fixed non-overlap bands prevent a 5-minute timer boot from firing 60/30/15/5 together.
   if(config.alert_before_60 && GT_PreAlertBandActive(remaining, 60*60, 30*60))
      GT_TrySendAlert(config, state, ev, GT_ALERT_STAGE_PRE_60M, runtime, now);

   if(config.alert_before_30 && GT_PreAlertBandActive(remaining, 30*60, 15*60))
      GT_TrySendAlert(config, state, ev, GT_ALERT_STAGE_PRE_30M, runtime, now);

   if(config.alert_before_15 && GT_PreAlertBandActive(remaining, 15*60, 5*60))
      GT_TrySendAlert(config, state, ev, GT_ALERT_STAGE_PRE_15M, runtime, now);

   if(config.alert_before_5 && GT_PreAlertBandActive(remaining, 5*60, 60))
      GT_TrySendAlert(config, state, ev, GT_ALERT_STAGE_PRE_5M, runtime, now);

   if(config.alert_before_1 && remaining <= 60 && remaining >= 0)
      GT_TrySendAlert(config, state, ev, GT_ALERT_STAGE_PRE_1M, runtime, now);
}

void GT_ProcessReleaseAlertForEvent(GT_Config &config,
                                    GT_AlertState &state,
                                    GT_NewsEvent &ev,
                                    GT_RuntimeState &runtime,
                                    datetime now)
{
   if(!config.alert_at_release)
      return;

   int delta = (int)(now - ev.time_broker);
   if(delta < 0)
      return;
   if(delta > config.alert_release_window_seconds)
      return;

   GT_TrySendAlert(config, state, ev, GT_ALERT_STAGE_RELEASE, runtime, now);
}

void GT_ProcessActualAlertForEvent(GT_Config &config,
                                   GT_AlertState &state,
                                   GT_NewsEvent &ev,
                                   GT_RuntimeState &runtime,
                                   datetime now)
{
   if(!config.alert_after_actual)
      return;
   if(!ev.is_released && GT_IsEmpty(ev.actual))
      return;
   if(now < ev.time_broker)
      return;

   GT_TrySendAlert(config, state, ev, GT_ALERT_STAGE_ACTUAL, runtime, now);
}

void GT_ProcessBreakingAlertForEvent(GT_Config &config,
                                     GT_AlertState &state,
                                     GT_NewsEvent &ev,
                                     GT_RuntimeState &runtime,
                                     datetime now)
{
   if(!config.alert_breaking)
      return;
   if(!ev.is_breaking)
      return;

   // Breaking news gets one immediate watch alert when the event appears in the visible tape.
   if(ev.time_broker < now - config.alert_release_window_seconds)
      return;

   GT_TrySendAlert(config, state, ev, GT_ALERT_STAGE_BREAKING, runtime, now);
}

void GT_ProcessAlerts(GT_Config &config,
                      GT_NewsStore &store,
                      GT_FilterState &filters,
                      GT_AlertState &state,
                      GT_RuntimeState &runtime)
{
   datetime now = TimeCurrent();

   runtime.alert_scan_count++;
   runtime.alert_last_scan_at = now;
   runtime.alert_last_scanned_events = store.count;
   runtime.alert_last_visible_candidates = 0;
   runtime.alert_last_sent_count = 0;
   runtime.alert_last_suppressed_count = 0;

   if(!config.enable_alerts || !filters.alerts_enabled)
   {
      runtime.alert_last_summary = "disabled | sent=" + IntegerToString(state.total_sent) + " | keys=" + IntegerToString(state.sent_count);
      return;
   }

   for(int i=0; i<store.count; i++)
   {
      GT_NewsEvent ev = store.events[i];
      if(!GT_EventEligibleForAlert(config, filters, ev))
         continue;

      runtime.alert_last_visible_candidates++;

      // Priority order: breaking watch, release/actual, then pre-alert bands.
      GT_ProcessBreakingAlertForEvent(config, state, ev, runtime, now);
      GT_ProcessReleaseAlertForEvent(config, state, ev, runtime, now);
      GT_ProcessActualAlertForEvent(config, state, ev, runtime, now);
      GT_ProcessPreAlertsForEvent(config, state, ev, runtime, now);
   }

   runtime.alert_last_summary = "scan=" + IntegerToString(runtime.alert_scan_count) +
                                " candidates=" + IntegerToString(runtime.alert_last_visible_candidates) +
                                " sent_now=" + IntegerToString(runtime.alert_last_sent_count) +
                                " total=" + IntegerToString(state.total_sent) +
                                " dup=" + IntegerToString(state.duplicate_count) +
                                " suppressed=" + IntegerToString(state.suppressed_count) +
                                " last=" + state.last_sent_stage;
}

#endif
