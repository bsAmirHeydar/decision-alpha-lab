//+------------------------------------------------------------------+
//| EXP0017_CG_Statistical_Report_Anatomy.mq5                        |
//| Phase 08 — Statistical Report Engine                             |
//| Reads Phase 07 outcome CSV and writes aggregate statistical CSVs. |
//+------------------------------------------------------------------+
#property strict
#property version   "1.080"
#property description "EXP0017 Phase 08 — Statistical Report Engine. Measurement only; no trading."

#include <IntermarketDivergenceExecution/CG/CGS_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGS_CsvReader.mqh>
#include <IntermarketDivergenceExecution/CG/CGS_Aggregator.mqh>
#include <IntermarketDivergenceExecution/CG/CGS_Ledger.mqh>
#include <IntermarketDivergenceExecution/CG/CGS_Display.mqh>
#include <IntermarketDivergenceExecution/CG/CGS_Engine.mqh>

input string             InpPhase07OutcomeCsvFile        = "EXP0017_Phase07_Outcome_Study.csv";
input string             InpReportPrefix                 = "EXP0017_Phase08";
input bool               InpUseCommonFilesFolder         = false;
input string             InpCsvDelimiter                 = ",";

input ECGSOutcomeWindow  InpPrimaryOutcomeWindow         = CGS_WINDOW_CYCLE_END;
input int                InpMinimumSampleForFlag         = 30;
input double             InpBadWinRateThresholdPercent   = 40.0;
input double             InpBadAverageRThreshold         = 0.0;
input int                InpBadStopStreakThreshold       = 5;
input bool               InpGenerateOverallReport        = true;
input bool               InpGenerateCGReport             = true;
input bool               InpGenerateDirectionReport      = true;
input bool               InpGenerateCGDirectionReport    = true;
input bool               InpGenerateRoleReport           = true;
input bool               InpGenerateCGDirectionRoleReport= true;
input bool               InpGenerateRedFlagReport        = true;

input bool               InpShowChartComment             = false;
input bool               InpPrintSummaryToExperts        = true;
input bool               InpRunOnceOnInit                = true;
input int                InpAutoRefreshMinutes           = 0;
input int                InpMaxRowsToRead                = 200000;

CCGS_StatisticalReportEngine g_engine;

int OnInit()
{
   SCGSReportConfig cfg;
   cfg.outcome_file                  = InpPhase07OutcomeCsvFile;
   cfg.report_prefix                 = InpReportPrefix;
   cfg.use_common_files_folder       = InpUseCommonFilesFolder;
   cfg.csv_delimiter                 = InpCsvDelimiter;
   cfg.primary_window                = InpPrimaryOutcomeWindow;
   cfg.minimum_sample_for_flag       = InpMinimumSampleForFlag;
   cfg.bad_winrate_threshold_percent = InpBadWinRateThresholdPercent;
   cfg.bad_average_r_threshold       = InpBadAverageRThreshold;
   cfg.bad_stop_streak_threshold     = InpBadStopStreakThreshold;
   cfg.generate_overall              = InpGenerateOverallReport;
   cfg.generate_cg                   = InpGenerateCGReport;
   cfg.generate_direction            = InpGenerateDirectionReport;
   cfg.generate_cg_direction         = InpGenerateCGDirectionReport;
   cfg.generate_role                 = InpGenerateRoleReport;
   cfg.generate_cg_direction_role    = InpGenerateCGDirectionRoleReport;
   cfg.generate_red_flags            = InpGenerateRedFlagReport;
   cfg.show_chart_comment            = InpShowChartComment;
   cfg.print_summary                 = InpPrintSummaryToExperts;
   cfg.max_rows_to_read              = InpMaxRowsToRead;

   g_engine.Configure(cfg);

   if(InpRunOnceOnInit)
      g_engine.RunReport();

   if(InpAutoRefreshMinutes > 0)
      EventSetTimer(InpAutoRefreshMinutes * 60);

   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   if(InpShowChartComment)
      Comment("");
}

void OnTick()
{
   if(InpShowChartComment)
      g_engine.UpdateComment();
}

void OnTimer()
{
   g_engine.RunReport();
}
