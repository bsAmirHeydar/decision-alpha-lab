//+------------------------------------------------------------------+
//| EXP0017_CG_Ranking_Dashboard_Anatomy.mq5                         |
//| Phase 09 — Statistical Ranking & Dashboard Anatomy               |
//| Reads Phase 08 statistical report CSV files and produces          |
//| non-execution ranking/dashboard outputs.                          |
//+------------------------------------------------------------------+
#property strict
#property version   "1.00"
#property description "EXP0017 Phase 09: Statistical Ranking & Dashboard Anatomy. No trading."

#include <IntermarketDivergenceExecution/CG/CGRK_Engine.mqh>

input bool   InpRunOnInit                         = true;
input bool   InpRunOnTimer                        = false;
input int    InpTimerSeconds                      = 60;
input bool   InpShowDashboardComment              = false;
input bool   InpPrintSummary                      = true;

input string InpPhase08OverallFile                = "EXP0017_Phase08_Overall.csv";
input string InpPhase08ByCGFile                   = "EXP0017_Phase08_By_CG.csv";
input string InpPhase08ByDirectionFile            = "EXP0017_Phase08_By_Direction.csv";
input string InpPhase08ByCGDirectionFile          = "EXP0017_Phase08_By_CG_Direction.csv";
input string InpPhase08ByRoleFile                 = "EXP0017_Phase08_By_Role.csv";
input string InpPhase08ByCGDirectionRoleFile      = "EXP0017_Phase08_By_CG_Direction_Role.csv";
input string InpPhase08RedFlagsFile               = "EXP0017_Phase08_Red_Flags.csv";

input bool   InpReadOverall                       = true;
input bool   InpReadByCG                          = true;
input bool   InpReadByDirection                   = true;
input bool   InpReadByCGDirection                 = true;
input bool   InpReadByRole                        = true;
input bool   InpReadByCGDirectionRole             = true;
input bool   InpReadRedFlags                      = true;

input int    InpMinimumSampleForRanking           = 30;
input int    InpMinimumSampleForShortlist         = 50;
input double InpMinimumQualityScoreForShortlist   = 65.0;
input double InpMinimumWinRateForShortlist        = 45.0;
input double InpMinimumAverageRForShortlist       = 0.0;
input int    InpMaximumStopStreakForShortlist     = 5;

input double InpWeightWinRate                     = 0.25;
input double InpWeightAverageR                    = 0.30;
input double InpWeightNormalizedOutcome           = 0.15;
input double InpWeightSafety                      = 0.20;
input double InpWeightSampleConfidence            = 0.10;

input string InpOutputAllRankingFile              = "EXP0017_Phase09_Rankings_All.csv";
input string InpOutputTopRankingFile              = "EXP0017_Phase09_Rankings_Top.csv";
input string InpOutputBottomRankingFile           = "EXP0017_Phase09_Rankings_Bottom.csv";
input string InpOutputShortlistFile               = "EXP0017_Phase09_Shortlist.csv";
input string InpOutputDashboardHtmlFile           = "EXP0017_Phase09_Dashboard.html";
input string InpOutputDiagnosticsFile             = "EXP0017_Phase09_Diagnostics.csv";

input int    InpTopRows                           = 50;
input int    InpBottomRows                        = 50;
input bool   InpWriteHtmlDashboard                = true;
input bool   InpWriteCsvOutputs                   = true;

CCGRK_Engine g_engine;

int OnInit()
{
   SCGRKConfig cfg;
   cfg.run_on_init                         = InpRunOnInit;
   cfg.show_dashboard_comment              = InpShowDashboardComment;
   cfg.print_summary                       = InpPrintSummary;

   cfg.phase08_overall_file                = InpPhase08OverallFile;
   cfg.phase08_by_cg_file                  = InpPhase08ByCGFile;
   cfg.phase08_by_direction_file           = InpPhase08ByDirectionFile;
   cfg.phase08_by_cg_direction_file        = InpPhase08ByCGDirectionFile;
   cfg.phase08_by_role_file                = InpPhase08ByRoleFile;
   cfg.phase08_by_cg_direction_role_file   = InpPhase08ByCGDirectionRoleFile;
   cfg.phase08_red_flags_file              = InpPhase08RedFlagsFile;

   cfg.read_overall                        = InpReadOverall;
   cfg.read_by_cg                          = InpReadByCG;
   cfg.read_by_direction                   = InpReadByDirection;
   cfg.read_by_cg_direction                = InpReadByCGDirection;
   cfg.read_by_role                        = InpReadByRole;
   cfg.read_by_cg_direction_role           = InpReadByCGDirectionRole;
   cfg.read_red_flags                      = InpReadRedFlags;

   cfg.minimum_sample_for_ranking          = InpMinimumSampleForRanking;
   cfg.minimum_sample_for_shortlist        = InpMinimumSampleForShortlist;
   cfg.minimum_quality_score_for_shortlist = InpMinimumQualityScoreForShortlist;
   cfg.minimum_win_rate_for_shortlist      = InpMinimumWinRateForShortlist;
   cfg.minimum_average_r_for_shortlist     = InpMinimumAverageRForShortlist;
   cfg.maximum_stop_streak_for_shortlist   = InpMaximumStopStreakForShortlist;

   cfg.weight_win_rate                     = InpWeightWinRate;
   cfg.weight_average_r                    = InpWeightAverageR;
   cfg.weight_normalized_outcome           = InpWeightNormalizedOutcome;
   cfg.weight_safety                       = InpWeightSafety;
   cfg.weight_sample_confidence            = InpWeightSampleConfidence;

   cfg.output_all_ranking_file             = InpOutputAllRankingFile;
   cfg.output_top_ranking_file             = InpOutputTopRankingFile;
   cfg.output_bottom_ranking_file          = InpOutputBottomRankingFile;
   cfg.output_shortlist_file               = InpOutputShortlistFile;
   cfg.output_dashboard_html_file          = InpOutputDashboardHtmlFile;
   cfg.output_diagnostics_file             = InpOutputDiagnosticsFile;

   cfg.top_rows                            = InpTopRows;
   cfg.bottom_rows                         = InpBottomRows;
   cfg.write_html_dashboard                = InpWriteHtmlDashboard;
   cfg.write_csv_outputs                   = InpWriteCsvOutputs;

   g_engine.Configure(cfg);

   if(InpRunOnInit)
      g_engine.Run();

   if(InpRunOnTimer)
      EventSetTimer(MathMax(5, InpTimerSeconds));

   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   if(InpRunOnTimer)
      EventKillTimer();
   Comment("");
}

void OnTick()
{
   // Phase 09 is report-only. No tick trading action.
}

void OnTimer()
{
   if(InpRunOnTimer)
      g_engine.Run();
}
