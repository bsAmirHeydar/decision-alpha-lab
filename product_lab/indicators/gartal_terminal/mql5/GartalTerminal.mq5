//+------------------------------------------------------------------+
//| GartalTerminal.mq5                                               |
//| gartal terminal - Stage 09 cache fallback resilience            |
//| Product Lab / Commercial MT5 News Terminal                       |
//+------------------------------------------------------------------+
#property strict
#property indicator_chart_window
#property indicator_plots   0
#property indicator_buffers 0
#property version           "0.9.0"
#property description       "gartal terminal - Stage 09 cache fallback resilience"

// Stage 05 doctrine:
// - Stage 01 compile-safe lifecycle remains intact.
// - Stage 02 canonical event store remains the single source of truth.
// - Stage 03 time_broker remains the only rendering and alert time authority.
// - Stage 04 owns all chart timeline objects through the GT_TL_ namespace.
// - Stage 05 upgrades the dashboard into the sellable terminal surface.
// - Stage 06 turns dashboard filter chips into live runtime controls.
// - Stage 07 adds deterministic alert state, de-duplication, and alert diagnostics.
// - Stage 08 adds the Forex Factory/Fair Economy source adapter, XML parser, and EA bridge contract.
// - Stage 09 adds source sanity checks, verified cache bundles, freshness, and failover health states.

#include "include/GartalNewsTypes.mqh"
#include "include/GartalNewsUtils.mqh"
#include "include/GartalNewsInputs.mqh"
#include "include/GartalNewsTime.mqh"
#include "include/GartalNewsDiagnostics.mqh"
#include "include/GartalNewsStore.mqh"
#include "include/GartalNewsSampleData.mqh"
#include "include/GartalNewsCalendarClient.mqh"
#include "include/GartalNewsResilience.mqh"
#include "include/GartalNewsParser.mqh"
#include "include/GartalNewsFilters.mqh"
#include "include/GartalNewsDashboardTheme.mqh"
#include "include/GartalNewsDashboard.mqh"
#include "include/GartalNewsChartGeometry.mqh"
#include "include/GartalNewsTimeline.mqh"
#include "include/GartalNewsAlerts.mqh"

GT_Config       g_config;
GT_RuntimeState g_runtime;
GT_NewsStore    g_store;
GT_FilterState  g_filters;
GT_AlertState   g_alerts;

//+------------------------------------------------------------------+
//| Indicator lifecycle                                              |
//+------------------------------------------------------------------+
int OnInit()
{
   GT_ResetRuntime(g_runtime);
   GT_ResetStore(g_store);

   GT_LoadConfig(g_config);
   GT_InitFilterState(g_filters, g_config);
   GT_InitAlertState(g_alerts);

   GT_ClearObjects(g_config.object_prefix);
   GT_RuntimeLog(g_runtime, GT_LOG_INFO, "Stage 09 cache fallback resilience boot started.");

   if(!GT_ValidateConfig(g_config, g_runtime))
   {
      GT_RenderFatalStatus(g_config, g_runtime);
      return(INIT_FAILED);
   }

   GT_NormalizeConfigTime(g_config, g_runtime);
   GT_RuntimeLog(g_runtime, GT_LOG_INFO, "Time engine normalized: " + g_runtime.time_summary);
   GT_RenderShell(g_config, g_runtime);

   int timer_seconds = GT_ClampInt(g_config.refresh_seconds, GT_MIN_TIMER_SECONDS, GT_MAX_TIMER_SECONDS);
   EventSetTimer(timer_seconds);

   GT_RefreshCalendar(true);
   GT_RuntimeLog(g_runtime, GT_LOG_INFO, "Stage 09 cache fallback resilience boot completed.");

   return(INIT_SUCCEEDED);
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   GT_RuntimeLog(g_runtime, GT_LOG_INFO, "Deinit reason=" + IntegerToString(reason));

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
   // Stage 01 intentionally avoids heavy work in OnCalculate.
   // Rendering and refresh are timer/event-driven to keep chart scrolling light.
   g_runtime.last_calculate_at = TimeCurrent();
   return(rates_total);
}

void OnTimer()
{
   datetime now = TimeCurrent();
   g_runtime.last_timer_at = now;

   bool due = (g_runtime.last_refresh_at == 0 || (now - g_runtime.last_refresh_at) >= g_config.refresh_seconds);
   if(due)
      GT_RefreshCalendar(false);

   GT_UpdateEventStatuses(g_store, now);
   GT_UpdateStoreMetrics(g_store, g_filters);
   GT_ProcessAlerts(g_config, g_store, g_filters, g_alerts, g_runtime);
   GT_UpdateCountdowns(g_config, g_store, g_filters, g_runtime);
}

void OnChartEvent(const int id,
                  const long &lparam,
                  const double &dparam,
                  const string &sparam)
{
   if(id == CHARTEVENT_OBJECT_CLICK)
   {
      if(GT_HandleDashboardClick(sparam, g_filters, g_config, g_runtime))
      {
         GT_UpdateStoreMetrics(g_store, g_filters);
         GT_RedrawAll();
      }
   }

   if(id == CHARTEVENT_CHART_CHANGE)
      GT_RedrawAll();
}

//+------------------------------------------------------------------+
//| Core orchestration                                               |
//+------------------------------------------------------------------+
void GT_RefreshCalendar(const bool first_load)
{
   string raw = "";
   bool fetched = false;
   bool parsed = false;

   g_runtime.refresh_attempts++;
   g_runtime.last_refresh_started_at = TimeCurrent();

   if(!GT_ResilienceRefreshAllowed(g_config, g_runtime, first_load))
   {
      g_runtime.last_refresh_at = TimeCurrent();
      g_runtime.last_refresh_finished_at = g_runtime.last_refresh_at;
      GT_RedrawAll();
      return;
   }

   GT_ResetStore(g_store);
   g_runtime.source_using_cache = false;
   g_runtime.source_using_stale_cache = false;
   g_runtime.source_using_sample_fallback = false;
   g_runtime.source_quality = GT_SOURCE_QUALITY_NONE;
   g_runtime.source_quality_text = "NONE";

   if(g_config.data_mode == GT_DATA_MODE_SAMPLE)
   {
      parsed = GT_LoadSampleEvents(g_store, g_config, g_runtime);
      fetched = parsed;
      if(parsed)
         GT_MarkSampleFallback(g_runtime);
   }
   else
   {
      fetched = GT_FetchCalendarRaw(g_config, raw, g_runtime);
      if(fetched && GT_CheckRawCalendarHealth(raw, g_config, g_runtime))
      {
         parsed = GT_ParseCalendar(raw, g_config, g_store, g_runtime);
         if(parsed)
         {
            GT_MarkLiveSource(g_runtime);
            if(g_config.use_cache)
               GT_SaveVerifiedCacheBundle(g_config, raw, g_runtime);
         }
      }
      else if(fetched)
      {
         GT_RuntimeLog(g_runtime, GT_LOG_WARNING, "Live source failed sanity check: " + g_runtime.source_sanity_summary);
      }

      if(!parsed && g_config.use_cache)
      {
         string cached = "";
         if(GT_LoadCacheBundle(g_config, cached, g_runtime))
            parsed = GT_ParseCalendar(cached, g_config, g_store, g_runtime);
      }

      if(!parsed && g_config.fallback_to_sample_on_source_fail)
      {
         GT_RuntimeLog(g_runtime, GT_LOG_WARNING, "Live/cache source failed. Falling back to sample data because fallback is enabled.");
         parsed = GT_LoadSampleEvents(g_store, g_config, g_runtime);
         if(parsed)
            GT_MarkSampleFallback(g_runtime);
      }
   }

   g_store.source_ok = parsed;
   g_store.last_refresh = TimeCurrent();

   if(parsed)
      GT_ApplySourceQualityToStore(g_store, g_runtime);
   else
   {
      GT_MarkSourceFailed(g_runtime);
      GT_ApplySourceQualityToStore(g_store, g_runtime);
   }

   g_runtime.last_refresh_at = TimeCurrent();
   g_runtime.last_refresh_finished_at = g_runtime.last_refresh_at;
   g_runtime.last_refresh_ok = parsed;

   GT_FinalizeStore(g_config, g_store, g_filters);
   GT_ApplySourceQualityToStore(g_store, g_runtime);

   if(!parsed)
      GT_RuntimeLog(g_runtime, GT_LOG_WARNING, "Calendar refresh failed. first_load=" + GT_BoolText(first_load));

   GT_RedrawAll();
}

void GT_RedrawAll()
{
   // Stage 09 renders timeline first, then dashboard, so the dashboard can show renderer/source diagnostics.
   GT_RenderTimeline(g_config, g_store, g_filters, g_runtime);
   GT_RenderDashboard(g_config, g_store, g_filters, g_runtime);
}
