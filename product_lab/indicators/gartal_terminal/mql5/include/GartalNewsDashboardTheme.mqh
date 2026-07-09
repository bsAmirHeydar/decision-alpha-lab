#ifndef GARTAL_NEWS_DASHBOARD_THEME_MQH
#define GARTAL_NEWS_DASHBOARD_THEME_MQH

string GT_DashboardModeText(int mode)
{
   if(mode == GT_DASHBOARD_MODE_COMPACT)  return "COMPACT";
   if(mode == GT_DASHBOARD_MODE_STANDARD) return "STANDARD";
   if(mode == GT_DASHBOARD_MODE_PRO)      return "PRO";
   return "UNKNOWN";
}

color GT_DashBg(GT_Config &config)
{
   if(config.dashboard_use_luxury_theme)
      return clrBlack;
   return config.dashboard_bg_color;
}

color GT_DashPanel(GT_Config &config)
{
   if(config.dashboard_use_luxury_theme)
      return clrMidnightBlue;
   return config.dashboard_panel_color;
}

color GT_DashBorder(GT_Config &config)
{
   if(config.dashboard_use_luxury_theme)
      return clrDarkSlateGray;
   return config.dashboard_border_color;
}

color GT_DashText(GT_Config &config)
{
   if(config.dashboard_use_luxury_theme)
      return clrWhite;
   return config.dashboard_text_color;
}

color GT_DashMuted(GT_Config &config)
{
   if(config.dashboard_use_luxury_theme)
      return clrSilver;
   return config.dashboard_muted_color;
}

color GT_DashAccent(GT_Config &config)
{
   if(config.dashboard_use_luxury_theme)
      return clrDeepSkyBlue;
   return config.dashboard_accent_color;
}

color GT_DashSoftBorder(GT_Config &config)
{
   if(config.dashboard_use_luxury_theme)
      return clrSteelBlue;
   return config.dashboard_border_color;
}

color GT_DashDanger()
{
   return clrTomato;
}

color GT_DashWarning()
{
   return clrOrange;
}

color GT_DashSuccess()
{
   return clrMediumSeaGreen;
}

color GT_DashboardHealthColor(GT_NewsStore &store, GT_RuntimeState &runtime)
{
   if(!GT_IsEmpty(runtime.last_error))
      return GT_DashDanger();
   if(!store.source_ok || !runtime.last_refresh_ok)
      return GT_DashWarning();
   if(!GT_IsEmpty(runtime.last_warning))
      return clrGold;
   return GT_DashSuccess();
}

string GT_DashboardHealthText(GT_NewsStore &store, GT_RuntimeState &runtime)
{
   if(!GT_IsEmpty(runtime.last_error))
      return "ERROR";
   if(!store.source_ok || !runtime.last_refresh_ok)
      return "SOURCE WARNING";
   if(!GT_IsEmpty(runtime.last_warning))
      return "WARNING";
   return "LIVE";
}

int GT_DashboardHeight(GT_Config &config)
{
   int height = 24;
   if(config.dashboard_show_header)     height += 46;
   if(config.dashboard_show_health_bar) height += 22;
   if(config.dashboard_show_next_card)  height += 72;
   if(config.dashboard_show_high_card && config.dashboard_mode == GT_DASHBOARD_MODE_PRO) height += 48;
   if(config.dashboard_show_metrics)    height += 48;
   if(config.dashboard_show_filter_bar) height += 44;
   if(config.dashboard_show_mini_tape)  height += 42;
   if(config.dashboard_show_event_table) height += 28 + config.dashboard_rows * config.dashboard_row_height;
   if(config.show_time_debug || config.show_timeline_debug) height += 22;
   return height;
}

string GT_DashboardSpecialFlags(GT_NewsEvent &ev)
{
   string flags = "";
   if(ev.is_breaking)  flags += " BRK";
   if(ev.is_speech)   flags += " SPC";
   if(ev.is_tentative) flags += " TENT";
   if(ev.is_holiday)  flags += " HOL";
   return GT_Trim(flags);
}

string GT_DashboardEventTitle(GT_NewsEvent &ev, int max_len)
{
   string special = GT_DashboardSpecialFlags(ev);
   string title = GT_CompactTitle(ev.title, max_len);
   if(!GT_IsEmpty(special))
      return title + "  [" + special + "]";
   return title;
}

string GT_DashboardCountdown(datetime event_time)
{
   int seconds = (int)(event_time - TimeCurrent());
   if(seconds < 0)
      return "released";

   int hours = seconds / GT_SECONDS_PER_HOUR;
   int minutes = (seconds % GT_SECONDS_PER_HOUR) / GT_SECONDS_PER_MINUTE;
   int secs = seconds % GT_SECONDS_PER_MINUTE;

   if(hours > 0)
      return IntegerToString(hours) + "h " + GT_TwoDigits(minutes) + "m";
   if(minutes > 0)
      return IntegerToString(minutes) + "m " + GT_TwoDigits(secs) + "s";
   return IntegerToString(secs) + "s";
}

string GT_DashboardTableHeader()
{
   return "  TIME   CCY  IMP   STATE      ACTUAL     FORECAST   PREVIOUS   EVENT";
}

string GT_DashboardTableRow(GT_NewsEvent &ev)
{
   string time_txt = TimeToString(ev.time_broker, TIME_MINUTES);
   string impact = GT_ImpactText(ev.impact);
   while(StringLen(impact) < 5) impact += " ";

   string status = GT_EventStatusText(ev.status);
   while(StringLen(status) < 10) status += " ";

   string actual = GT_CompactTitle(GT_IsEmpty(ev.actual) ? "-" : ev.actual, 9);
   string forecast = GT_CompactTitle(GT_IsEmpty(ev.forecast) ? "-" : ev.forecast, 9);
   string previous = GT_CompactTitle(GT_IsEmpty(ev.previous) ? "-" : ev.previous, 9);

   while(StringLen(actual) < 9) actual += " ";
   while(StringLen(forecast) < 9) forecast += " ";
   while(StringLen(previous) < 9) previous += " ";

   return "  " + time_txt + "  " + ev.currency + "  " + impact + " " + status + " " + actual + "  " + forecast + "  " + previous + "  " + GT_DashboardEventTitle(ev, 34);
}

#endif
