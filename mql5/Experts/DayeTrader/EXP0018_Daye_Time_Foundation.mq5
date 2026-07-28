#property strict
#property version   "1.10"
#property description "EXP0018 P01 isolated New York Time Kernel v2. No signal, drawing, risk, or trading authority."

#include <DayeTrader/EXP0018/DAYE_Engine.mqh>
#include <AlphaLab/UC04/AL_UC04DayeTimeConfig.mqh>

input group "EXP0018 P01 — Broker Clock Adapter"
input DAYE_BrokerOffsetMode InpBrokerOffsetMode = DAYE_BROKER_OFFSET_MANUAL_FIXED;
input double InpBrokerUtcOffsetHours = 3.0;

input group "EXP0018 P01 — New York Clock"
input DAYE_NyOffsetMode InpNewYorkOffsetMode = DAYE_NY_AUTO_US_DST;
input double InpManualNewYorkUtcOffsetHours = -5.0;
input DAYE_LocalResolutionPolicy InpAmbiguousStartPolicy = DAYE_LOCAL_EARLIEST;
input DAYE_LocalResolutionPolicy InpAmbiguousEndPolicy = DAYE_LOCAL_LATEST;

input group "EXP0018 P01 — Runtime"
input int InpTimerSeconds = 1;
input bool InpRunEmbeddedSelfTestsOnInit = true;
input bool InpPrintPeriodRegistryOnInit = false;
input bool InpPrintOnUtcMinuteChange = true;
input bool InpPrintTransitionEvents = true;
input bool InpShowChartComment = false;

input group "EXP0018 P01 — Optional Audit Ledger"
input bool InpWriteAuditCsv = false;
input bool InpWriteSnapshotRows = false;
input string InpAuditCsvFilename = "EXP0018_Phase01_Time_Audit_v2.csv";

CDayeTimeKernelEngine g_daye_time_kernel;

void DAYE_BuildInputConfig(DAYE_TimeConfig &config)
{
   AL_UC04BuildDayeTimeConfig(
      config,
      InpBrokerOffsetMode,
      InpBrokerUtcOffsetHours,
      InpNewYorkOffsetMode,
      InpManualNewYorkUtcOffsetHours,
      InpAmbiguousStartPolicy,
      InpAmbiguousEndPolicy
   );
}

datetime DAYE_CurrentBrokerTime(void)
{
   datetime value = TimeTradeServer();
   if(value <= 0)
      value = TimeCurrent();
   return value;
}

int OnInit()
{
   DAYE_TimeConfig config;
   DAYE_BuildInputConfig(config);
   if(!g_daye_time_kernel.Initialize(config,
                                     InpPrintPeriodRegistryOnInit,
                                     InpRunEmbeddedSelfTestsOnInit,
                                     InpWriteAuditCsv,
                                     InpAuditCsvFilename))
      return INIT_FAILED;

   int timer_seconds = InpTimerSeconds;
   if(timer_seconds < 1)
      timer_seconds = 1;
   if(!EventSetTimer(timer_seconds))
   {
      Print("EXP0018 P01 EventSetTimer failed error=",GetLastError());
      g_daye_time_kernel.Shutdown();
      return INIT_FAILED;
   }

   datetime now = DAYE_CurrentBrokerTime();
   if(now <= 0 || !g_daye_time_kernel.Process(now,InpPrintOnUtcMinuteChange,InpPrintTransitionEvents,InpShowChartComment,InpWriteSnapshotRows))
   {
      EventKillTimer();
      g_daye_time_kernel.Shutdown();
      return INIT_FAILED;
   }
   return INIT_SUCCEEDED;
}

void OnTimer()
{
   datetime now = DAYE_CurrentBrokerTime();
   if(now > 0)
      g_daye_time_kernel.Process(now,InpPrintOnUtcMinuteChange,InpPrintTransitionEvents,InpShowChartComment,InpWriteSnapshotRows);
}

void OnTick()
{
   // P01 is timer-driven. It intentionally performs no market detection or trading work.
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   g_daye_time_kernel.Shutdown();
}
