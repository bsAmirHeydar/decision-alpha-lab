#property strict
#property version   "1.00"
#property description "Strategy Factory Phase 02 thin MQL5-first runtime host"

#include <AlphaLab\StrategyFactory\Runtime\SF02_AllRuntime.mqh>
#include <AlphaLab\StrategyFactory\Adapters\Null\SF02_AllNullAdapters.mqh>

input ENUM_SF02_RUN_MODE InpRunMode = SF02_MODE_ANATOMY_AUDIT;
input string InpStrategyId = "unbound_strategy";
input string InpStrategyVersion = "0.0.0";
input string InpRunId = "run_sf02_host";
input int InpTimerPeriodMs = 250;
input int InpMaxEventsPerCycle = 32;
input bool InpStrictFailClosed = true;

CSF02TerminalClock g_clock;
CSF02NullAnatomyProvider g_anatomy;
CSF02NullFeatureProvider g_features;
CSF02PrintResultSink g_sink;
CSF02NoSendExecutionBoundary g_execution_boundary;
CSF02StrategyRuntime g_runtime;

int OnInit()
{
   SF02_RuntimeConfig config = SF02_DefaultRuntimeConfig();
   config.strategy_id = InpStrategyId;
   config.strategy_version = InpStrategyVersion;
   config.run_id = InpRunId;
   config.run_mode = InpRunMode;
   config.timer_period_ms = InpTimerPeriodMs;
   config.max_events_per_cycle = InpMaxEventsPerCycle;
   config.strict_fail_closed = InpStrictFailClosed;

   g_runtime.BindClock(&g_clock);
   g_runtime.BindAnatomy(&g_anatomy);
   g_runtime.BindFeatures(&g_features);
   g_runtime.BindSink(&g_sink);
   g_runtime.BindExecutionBoundary(&g_execution_boundary);

   string error = "";
   if(!g_runtime.Initialize(config, error))
   {
      Print("SF02 host initialization failed: ", error);
      return INIT_FAILED;
   }
   if(!g_runtime.Start(error))
   {
      Print("SF02 host start failed: ", error);
      return INIT_FAILED;
   }
   if(!EventSetMillisecondTimer(config.timer_period_ms))
   {
      Print("SF02 host timer setup failed: ", GetLastError());
      return INIT_FAILED;
   }
   Print("SF02 host started runtime=", SF02_RuntimeVersion(),
         " mode=", SF02_RunModeToString(config.run_mode),
         " authority=", g_execution_boundary.AuthorityDescription());
   return INIT_SUCCEEDED;
}

void OnTick()
{
   MqlTick tick;
   if(!SymbolInfoTick(_Symbol, tick)) return;
   string error = "";
   if(!g_runtime.OnTick(tick, error))
      Print("SF02 OnTick failed: ", error);
}

void OnTimer()
{
   string error = "";
   if(!g_runtime.OnTimer(error))
      Print("SF02 OnTimer failed: ", error);
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   string error = "";
   g_runtime.Stop(error);
   g_runtime.Shutdown();
   Print("SF02 host stopped reason=", reason,
         " events=", g_runtime.ProcessedEvents(),
         " snapshots=", g_runtime.CreatedSnapshots(),
         " rejected=", g_runtime.RejectedEvents());
}
