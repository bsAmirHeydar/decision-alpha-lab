//+------------------------------------------------------------------+
//| GartalTerminal.mq5                                               |
//| Product scaffold for gartal terminal                             |
//| Macro news dashboard + chart timeline + alert engine             |
//+------------------------------------------------------------------+
#property strict
#property indicator_chart_window
#property indicator_plots 0
#property version   "0.1"
#property description "gartal terminal - macro news terminal scaffold"

// NOTE:
// This file is a product scaffold. The production adapter must harden
// WebRequest, parser rules, cache, licensing, and broker-time validation.

#include "include/GartalNewsTypes.mqh"
#include "include/GartalNewsInputs.mqh"
#include "include/GartalNewsCalendarClient.mqh"
#include "include/GartalNewsParser.mqh"
#include "include/GartalNewsDashboard.mqh"
#include "include/GartalNewsTimeline.mqh"
#include "include/GartalNewsAlerts.mqh"

GT_Config       g_config;
GT_NewsStore    g_store;
GT_FilterState  g_filters;
GT_AlertState   g_alerts;

datetime g_last_refresh = 0;

int OnInit()
{
   GT_LoadConfig(g_config);
   GT_InitFilterState(g_filters, g_config);
   GT_InitAlertState(g_alerts);

   GT_ClearObjects(g_config.object_prefix);
   GT_RenderShell(g_config);

   EventSetTimer(MathMax(10, g_config.refresh_seconds));
   GT_RefreshCalendar(true);

   return(INIT_SUCCEEDED);
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   if(g_config.clean_objects_on_deinit)
      GT_ClearObjects(g_config.object_prefix);
}

int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
{
   GT_UpdateCountdowns(g_config, g_store, g_filters);
   return(rates_total);
}

void OnTimer()
{
   datetime now = TimeCurrent();
   bool due = (g_last_refresh == 0 || (now - g_last_refresh) >= g_config.refresh_seconds);

   if(due)
      GT_RefreshCalendar(false);

   GT_ProcessAlerts(g_config, g_store, g_filters, g_alerts);
   GT_UpdateCountdowns(g_config, g_store, g_filters);
}

void OnChartEvent(const int id,
                  const long &lparam,
                  const double &dparam,
                  const string &sparam)
{
   if(id == CHARTEVENT_OBJECT_CLICK)
   {
      if(GT_HandleDashboardClick(sparam, g_filters, g_config))
      {
         GT_RedrawAll(g_config, g_store, g_filters);
      }
   }

   if(id == CHARTEVENT_CHART_CHANGE)
   {
      GT_RedrawAll(g_config, g_store, g_filters);
   }
}

void GT_RefreshCalendar(bool first_load)
{
   string raw = "";
   bool ok = false;

   if(g_config.use_sample_data)
   {
      GT_LoadSampleEvents(g_store, g_config);
      ok = true;
   }
   else
   {
      ok = GT_FetchCalendarRaw(g_config, raw);
      if(ok)
      {
         ok = GT_ParseCalendar(raw, g_config, g_store);
         if(ok)
            GT_SaveCache(g_config, raw);
      }

      if(!ok && g_config.use_cache)
      {
         string cached = "";
         if(GT_LoadCache(g_config, cached))
            ok = GT_ParseCalendar(cached, g_config, g_store);
      }
   }

   g_store.source_ok = ok;
   g_store.last_refresh = TimeCurrent();
   g_last_refresh = TimeCurrent();

   GT_MarkRelevance(g_config, g_store);
   GT_RedrawAll(g_config, g_store, g_filters);
}

void GT_RedrawAll(GT_Config &config, GT_NewsStore &store, GT_FilterState &filters)
{
   GT_RenderDashboard(config, store, filters);
   GT_RenderTimeline(config, store, filters);
   GT_RenderVerticalLines(config, store, filters);
}
