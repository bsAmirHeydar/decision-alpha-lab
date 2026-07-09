#ifndef GARTAL_NEWS_ALERTS_MQH
#define GARTAL_NEWS_ALERTS_MQH

void GT_InitAlertState(GT_AlertState &state)
{
   state.sent_count = 0;
   for(int i=0; i<GT_MAX_ALERT_KEYS; i++)
      state.sent_keys[i] = "";
}

bool GT_AlertAlreadySent(GT_AlertState &state, string key)
{
   for(int i=0; i<state.sent_count; i++)
      if(state.sent_keys[i] == key)
         return true;
   return false;
}

void GT_MarkAlertSent(GT_AlertState &state, string key)
{
   if(state.sent_count >= GT_MAX_ALERT_KEYS)
      return;

   state.sent_keys[state.sent_count] = key;
   state.sent_count++;
}

void GT_SendAlert(GT_Config &config, string message, GT_RuntimeState &runtime)
{
   if(!config.enable_alerts)
      return;

   if(config.alert_popup) Alert(message);
   if(config.alert_sound) PlaySound(config.alert_sound_file);
   if(config.alert_push)  SendNotification(message);
   if(config.alert_email) SendMail("gartal terminal", message);

   GT_RuntimeLog(runtime, GT_LOG_INFO, "Alert sent: " + message);
}

void GT_ProcessThreshold(GT_Config &config,
                         GT_AlertState &state,
                         GT_NewsEvent &ev,
                         int seconds_before,
                         string key_suffix,
                         GT_RuntimeState &runtime)
{
   datetime now = TimeCurrent();
   int remaining = (int)(ev.time_broker - now);

   if(remaining < 0)
      return;
   if(remaining > seconds_before)
      return;

   string key = ev.id + "_" + key_suffix;
   if(GT_AlertAlreadySent(state, key))
      return;

   string msg = "gartal terminal | " + GT_ImpactText(ev.impact) + " " + ev.currency + " | " + ev.title + " | " + GT_FormatMinutesRemaining(ev.time_broker, now) + " remaining";
   GT_SendAlert(config, msg, runtime);
   GT_MarkAlertSent(state, key);
}

void GT_ProcessReleaseAlert(GT_Config &config,
                            GT_AlertState &state,
                            GT_NewsEvent &ev,
                            GT_RuntimeState &runtime)
{
   if(!config.alert_at_release)
      return;

   datetime now = TimeCurrent();
   int delta = (int)MathAbs((double)(now - ev.time_broker));
   if(delta > 10)
      return;

   string key = ev.id + "_RELEASE";
   if(GT_AlertAlreadySent(state, key))
      return;

   string msg = "gartal terminal | RELEASE NOW | " + ev.currency + " " + GT_ImpactText(ev.impact) + " | " + ev.title;
   GT_SendAlert(config, msg, runtime);
   GT_MarkAlertSent(state, key);
}

void GT_ProcessAlerts(GT_Config &config,
                      GT_NewsStore &store,
                      GT_FilterState &filters,
                      GT_AlertState &state,
                      GT_RuntimeState &runtime)
{
   if(!config.enable_alerts || !filters.alerts_enabled)
      return;

   for(int i=0; i<store.count; i++)
   {
      GT_NewsEvent ev = store.events[i];
      if(!GT_EventPassesFilters(ev, filters))
         continue;

      if(config.alert_before_60) GT_ProcessThreshold(config, state, ev, 60*60, "PRE_60M", runtime);
      if(config.alert_before_30) GT_ProcessThreshold(config, state, ev, 30*60, "PRE_30M", runtime);
      if(config.alert_before_15) GT_ProcessThreshold(config, state, ev, 15*60, "PRE_15M", runtime);
      if(config.alert_before_5)  GT_ProcessThreshold(config, state, ev, 5*60,  "PRE_5M", runtime);
      if(config.alert_before_1)  GT_ProcessThreshold(config, state, ev, 60,    "PRE_1M", runtime);
      GT_ProcessReleaseAlert(config, state, ev, runtime);
   }
}

#endif
