//+------------------------------------------------------------------+
//| EXP0017_CG_Model_Dataset_Anatomy.mq5                             |
//| Phase 10 — Model-Ready Dataset & Feature Store Anatomy           |
//| Reads Phase 07 outcomes and optional Phase 09 rankings. Produces |
//| row-level feature/label CSVs for research. No trading.            |
//+------------------------------------------------------------------+
#property strict
#property version   "1.00"
#property description "EXP0017 Phase 10: Model-ready dataset and feature store anatomy. No trading."

#include <IntermarketDivergenceExecution/CG/CGM_Engine.mqh>

input bool   InpRunOnInit                         = true;
input bool   InpRunOnTimer                        = false;
input int    InpTimerSeconds                      = 60;
input bool   InpShowChartComment                  = false;
input bool   InpPrintSummary                      = true;

input string InpPhase07OutcomeFile                = "EXP0017_Phase07_Outcome_Study.csv";
input string InpPhase09AllRankingFile             = "EXP0017_Phase09_Rankings_All.csv";
input string InpPhase09ShortlistFile              = "EXP0017_Phase09_Shortlist.csv";
input bool   InpUsePhase09RankingEnrichment       = true;
input bool   InpUsePhase09ShortlistEnrichment     = true;

input ECGMLabelWindow InpPrimaryLabelWindow       = CGM_LABEL_CYCLE_END;
input double InpWinThresholdR                     = 0.0;
input double InpLossThresholdR                    = 0.0;
input double InpOneRThreshold                     = 1.0;
input double InpAdverseOneRThreshold              = -1.0;
input bool   InpRequireCompleteOutcome            = true;
input bool   InpSkipZeroRiskRows                  = true;
input int    InpMaxRowsToWrite                    = 200000;

input string InpOutputDatasetFile                 = "EXP0017_Phase10_Model_Dataset.csv";
input string InpOutputFeatureDictionaryFile       = "EXP0017_Phase10_Feature_Dictionary.csv";
input string InpOutputLabelSummaryFile            = "EXP0017_Phase10_Label_Summary.csv";
input string InpOutputDiagnosticsFile             = "EXP0017_Phase10_Diagnostics.csv";
input bool   InpWriteFeatureDictionary            = true;
input bool   InpWriteLabelSummary                 = true;
input bool   InpWriteDiagnostics                  = true;
input bool   InpClearOutputsOnRun                 = true;

CCGM_Engine g_engine;

int OnInit()
{
   SCGMConfig cfg;
   cfg.run_on_init                       = InpRunOnInit;
   cfg.show_chart_comment                = InpShowChartComment;
   cfg.print_summary                     = InpPrintSummary;

   cfg.phase07_outcome_file              = InpPhase07OutcomeFile;
   cfg.phase09_all_ranking_file          = InpPhase09AllRankingFile;
   cfg.phase09_shortlist_file            = InpPhase09ShortlistFile;
   cfg.use_phase09_ranking_enrichment    = InpUsePhase09RankingEnrichment;
   cfg.use_phase09_shortlist_enrichment  = InpUsePhase09ShortlistEnrichment;

   cfg.primary_label_window              = InpPrimaryLabelWindow;
   cfg.win_threshold_r                   = InpWinThresholdR;
   cfg.loss_threshold_r                  = InpLossThresholdR;
   cfg.one_r_threshold                   = InpOneRThreshold;
   cfg.adverse_one_r_threshold           = InpAdverseOneRThreshold;
   cfg.require_complete_outcome          = InpRequireCompleteOutcome;
   cfg.skip_zero_risk_rows               = InpSkipZeroRiskRows;
   cfg.max_rows_to_write                 = InpMaxRowsToWrite;

   cfg.output_dataset_file               = InpOutputDatasetFile;
   cfg.output_feature_dictionary_file    = InpOutputFeatureDictionaryFile;
   cfg.output_label_summary_file         = InpOutputLabelSummaryFile;
   cfg.output_diagnostics_file           = InpOutputDiagnosticsFile;
   cfg.write_feature_dictionary          = InpWriteFeatureDictionary;
   cfg.write_label_summary               = InpWriteLabelSummary;
   cfg.write_diagnostics                 = InpWriteDiagnostics;
   cfg.clear_outputs_on_run              = InpClearOutputsOnRun;

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
   // Phase 10 is dataset-only. No tick trading action.
}

void OnTimer()
{
   if(InpRunOnTimer)
      g_engine.Run();
}
