#property strict
#property version   "1.02"
#property description "EXP0015 legacy SPX/NDX time-divergence wrapper with offline license gate. Use IMD001_CandleSessionDivergence for the canonical CME/live-ready engine."

#include <IntermarketDivergence/DAL_IMDTypes.mqh>
#include <IntermarketDivergence/DAL_IMDSeries.mqh>
#include <IntermarketDivergence/DAL_IMDEngine.mqh>
#include <IntermarketDivergence/DAL_IMDJournal.mqh>
#include <IntermarketDivergenceExecution/STC/DAL_STC_LicenseEngine.mqh>

input string              InpSymbolA                         = "US500";
input string              InpSymbolB                         = "NAS100";
input string              InpPairLabel                       = "SPX_NDX";
input ENUM_TIMEFRAMES     InpSignalTimeframe                 = PERIOD_M5;
input int                 InpBarsToScan                      = 50000;   // broker bars to load
input DAL_IMDOriginBarMode InpOriginBarMode                  = IMD_ORIGIN_CLOSED_BARS_ONLY;

input int                 InpStepEveryBars                   = 1;
input int                 InpStepOffsetBars                  = 0;
input int                 InpDestinationLagBars              = 0;
input int                 InpSignalValidBars                 = 12;
input int                 InpStartAfterBars                  = 50;
input int                 InpOutcomeHorizonBars              = 12;

input bool                InpScanAAsOrigin                   = true;
input bool                InpScanBAsOrigin                   = true;

// Legacy file compatibility note:
// The old SPX/NDX expert used separate origin/destination level inputs and a
// node reference source. The canonical EXP0015 candle/session engine is a
// simpler compile-stable engine. If IMD_LEVEL_L_NODE is selected here, the
// level module falls back to the rolling-lookback proxy instead of failing to
// compile.
input DAL_IMDLevelSource  InpLevelSource                      = IMD_LEVEL_CURRENT_SESSION;
input int                 InpRollingLookbackBars             = 20;
input DAL_IMDTriggerMode  InpTriggerMode                     = IMD_TRIGGER_WICK_TOUCH;

// Session is expressed in the timestamp timezone of the loaded MT5 broker bars.
input int                 InpSessionStartHour                = 16;
input int                 InpSessionStartMinute              = 30;
input int                 InpSessionEndHour                  = 23;
input int                 InpSessionEndMinute                = 0;

input string              InpOutputEventsCommon              = "imd\\EXP0015\\imd001_spx_ndx_legacy_events.csv";
input string              InpOutputSummaryCommon             = "imd\\EXP0015\\imd001_spx_ndx_legacy_summary.csv";
input bool                InpRunOnceOnInit                   = true;
input bool                InpRemoveAfterBatch                = true;

input group "STC Cycle Model Runtime Profile"
input string InpCycleModelProfile = "";
input string InpCycleOperatorMemo = "";
input long InpCycleReferenceSeed = 0;
input long InpCycleDivergenceSeed = 0;
input long InpCycleExecutionSeed = 0;
input long InpCycleReleaseSeed = 0;
input int InpCycleCacheDepthMinutes = 15;

IMD_Bar g_imd001_a_raw[];
IMD_Bar g_imd001_b_raw[];
IMD_Bar g_imd001_a[];
IMD_Bar g_imd001_b[];
IMD_Event g_imd001_events[];


STC_OfflineLicenseConfig g_stc_license_cfg;
STC_OfflineLicenseReport g_stc_license_report;
bool g_stc_license_ok = false;
datetime g_stc_license_next_check = 0;

void STC_LoadOfflineLicenseConfig(STC_OfflineLicenseConfig &cfg)
{
   STC_DefaultOfflineLicenseConfig(cfg);
   cfg.enabled = true;
   cfg.fail_closed = true;
   cfg.bind_account = true;
   cfg.bind_server = true;
   cfg.require_password = true;
   cfg.require_hidden_gates = true;
   cfg.require_expiry = true;
   cfg.product_id = STC_LICENSE_PRODUCT_ID;
   cfg.build_id = "exp0015_imd_research_licensed";
   cfg.token = InpCycleModelProfile;
   cfg.passphrase = InpCycleOperatorMemo;
   cfg.gate_a = InpCycleReferenceSeed;
   cfg.gate_b = InpCycleDivergenceSeed;
   cfg.gate_c = InpCycleExecutionSeed;
   cfg.gate_d = InpCycleReleaseSeed;
   cfg.check_interval_seconds = InpCycleCacheDepthMinutes * 60;
   if(cfg.check_interval_seconds < 60)
      cfg.check_interval_seconds = 60;
   cfg.print_sanity = true;
   cfg.print_samples = false;
}

bool STC_EnsureOfflineLicense(const bool force_check=false)
{
   datetime now = TimeCurrent();
   if(now <= 0)
      now = TimeTradeServer();
   if(!force_check && g_stc_license_ok && g_stc_license_next_check > 0 && now > 0 && now < g_stc_license_next_check)
      return true;

   STC_LoadOfflineLicenseConfig(g_stc_license_cfg);
   g_stc_license_ok = STC_CheckOfflineLicenseWithReport(g_stc_license_cfg, g_stc_license_report);
   if(g_stc_license_cfg.print_sanity || !g_stc_license_ok)
      STC_PrintOfflineLicenseReport("STC_LICENSE", g_stc_license_report);
   if(g_stc_license_cfg.print_samples && g_stc_license_ok)
      STC_PrintOfflineLicenseSamples("STC_LICENSE", g_stc_license_report);

   datetime checked = g_stc_license_report.checked_at;
   if(checked <= 0)
      checked = now;
   if(checked > 0)
   {
      int recheck_sec = g_stc_license_cfg.check_interval_seconds;
      if(recheck_sec < 60)
         recheck_sec = 60;
      g_stc_license_next_check = checked + recheck_sec;
   }
   else
   {
      g_stc_license_next_check = 0;
   }

   if(!g_stc_license_ok)
      Comment("Intermarket Divergence runtime inactive. Contact issuer.");
   else
      Comment("");
   return g_stc_license_ok;
}

int IMD001_SessionMinute(const int h, const int m)
{
   return MathMax(0, MathMin(23, h)) * 60 + MathMax(0, MathMin(59, m));
}

bool IMD001_LoadAlignedBrokerBars()
{
   ArrayResize(g_imd001_a_raw, 0);
   ArrayResize(g_imd001_b_raw, 0);
   ArrayResize(g_imd001_a, 0);
   ArrayResize(g_imd001_b, 0);

   int max_bars = MathMax(100, InpBarsToScan);
   if(!IMD_LoadBrokerBars(InpSymbolA, InpSignalTimeframe, max_bars, g_imd001_a_raw))
   {
      Print("IMD001 legacy: failed to load SymbolA broker bars: ", InpSymbolA);
      return false;
   }
   if(!IMD_LoadBrokerBars(InpSymbolB, InpSignalTimeframe, max_bars, g_imd001_b_raw))
   {
      Print("IMD001 legacy: failed to load SymbolB broker bars: ", InpSymbolB);
      return false;
   }

   // Closed-bars-only mode removes the most recent bar after loading. This is a
   // conservative compatibility behavior for old .set files.
   if(InpOriginBarMode == IMD_ORIGIN_CLOSED_BARS_ONLY)
   {
      if(ArraySize(g_imd001_a_raw) > 1) ArrayResize(g_imd001_a_raw, ArraySize(g_imd001_a_raw) - 1);
      if(ArraySize(g_imd001_b_raw) > 1) ArrayResize(g_imd001_b_raw, ArraySize(g_imd001_b_raw) - 1);
   }

   int aligned = IMD_AlignByTime(g_imd001_a_raw, g_imd001_b_raw, g_imd001_a, g_imd001_b);
   if(aligned <= 10)
   {
      Print("IMD001 legacy: too few aligned bars: ", aligned,
            " A=", InpSymbolA, " B=", InpSymbolB,
            " tf=", EnumToString(InpSignalTimeframe));
      return false;
   }

   Print("IMD001 legacy: loaded aligned bars=", aligned,
         " A=", InpSymbolA,
         " B=", InpSymbolB,
         " level=", DAL_IMD_LevelSourceToString(InpLevelSource));
   return true;
}

bool IMD001_RunBatch()
{
   if(InpSymbolA == "" || InpSymbolB == "")
   {
      Print("IMD001 legacy: symbols must not be empty");
      return false;
   }
   if(InpSymbolA == InpSymbolB)
   {
      Print("IMD001 legacy: SymbolA and SymbolB must be different");
      return false;
   }
   if(!IMD001_LoadAlignedBrokerBars())
      return false;

   ArrayResize(g_imd001_events, 0);
   int start_minute = IMD001_SessionMinute(InpSessionStartHour, InpSessionStartMinute);
   int end_minute = IMD001_SessionMinute(InpSessionEndHour, InpSessionEndMinute);

   if(InpScanAAsOrigin)
   {
      int added = IMD_DetectOriginDestination(InpPairLabel, InpSymbolA, InpSymbolB,
                                              g_imd001_a, g_imd001_b,
                                              InpLevelSource, InpTriggerMode,
                                              MathMax(1, InpRollingLookbackBars),
                                              start_minute, end_minute,
                                              MathMax(1, InpStepEveryBars), InpStepOffsetBars,
                                              MathMax(0, InpDestinationLagBars),
                                              MathMax(1, InpSignalValidBars),
                                              MathMax(1, InpStartAfterBars),
                                              MathMax(1, InpOutcomeHorizonBars),
                                              g_imd001_events);
      Print("IMD001 legacy: A-as-origin events=", added);
   }

   if(InpScanBAsOrigin)
   {
      int added = IMD_DetectOriginDestination(InpPairLabel, InpSymbolB, InpSymbolA,
                                              g_imd001_b, g_imd001_a,
                                              InpLevelSource, InpTriggerMode,
                                              MathMax(1, InpRollingLookbackBars),
                                              start_minute, end_minute,
                                              MathMax(1, InpStepEveryBars), InpStepOffsetBars,
                                              MathMax(0, InpDestinationLagBars),
                                              MathMax(1, InpSignalValidBars),
                                              MathMax(1, InpStartAfterBars),
                                              MathMax(1, InpOutcomeHorizonBars),
                                              g_imd001_events);
      Print("IMD001 legacy: B-as-origin events=", added);
   }

   IMD_WriteEventsCsv(InpOutputEventsCommon, g_imd001_events);
   IMD_WriteSummaryCsv(InpOutputSummaryCommon,
                       "IMD001_SPX_NDX_LEGACY_WRAPPER",
                       InpSymbolA,
                       InpSymbolB,
                       ArraySize(g_imd001_a),
                       g_imd001_events);

   Print("IMD001 legacy result: events=", ArraySize(g_imd001_events),
         " events_csv=", InpOutputEventsCommon,
         " summary_csv=", InpOutputSummaryCommon,
         " common_files=true");
   return true;
}

int OnInit()
{
   if(!STC_EnsureOfflineLicense(true))
      return INIT_FAILED;

   if(InpRunOnceOnInit)
   {
      IMD001_RunBatch();
      if(InpRemoveAfterBatch)
         ExpertRemove();
   }
   return INIT_SUCCEEDED;
}

void OnTick()
{
   // Legacy batch wrapper. No tick-driven execution.
}
