//+------------------------------------------------------------------+
//| EXP0017_CG_WalkForward_Model_Experiment_Anatomy.mq5              |
//| Phase 11 — Walk-forward validation and model-experiment anatomy   |
//+------------------------------------------------------------------+
#property strict
#property version   "1.00"
#property description "EXP0017 Phase 11: Walk-forward validation and model experiment anatomy. No trading."

#include <IntermarketDivergenceExecution/CG/CGWF_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGWF_Engine.mqh>

input bool   InpRunOnInit = true;
input bool   InpShowChartComment = true;
input bool   InpPrintSummary = true;

input string InpPhase10DatasetFile = "EXP0017_Phase10_Model_Dataset.csv";
input string InpOutputPrefix = "EXP0017_Phase11";
input bool   InpClearOutputsOnRun = true;

input bool   InpUseOnlyModelReadyRows = true;
input int    InpMaxDatasetRowsToRead = 200000;
input int    InpMinimumTrainRows = 80;
input int    InpMinimumTestRows = 20;

input int    InpTrainDays = 120;
input int    InpTestDays = 20;
input int    InpStepDays = 20;
input int    InpEmbargoDays = 1;

input ECGWFKeyMode InpPrimaryBucketKeyMode = CGWF_KEY_CG_DIRECTION_ROLE;
input double InpPositiveEdgeThresholdR = 0.00;
input double InpWeakEdgeThresholdR = -0.05;
input int    InpMinimumBucketTrainRows = 20;
input bool   InpAllowGlobalFallback = true;

input bool   InpWriteFoldPlan = true;
input bool   InpWritePredictions = true;
input bool   InpWriteFoldMetrics = true;
input bool   InpWriteBucketValidation = true;
input bool   InpWriteExperimentSummary = true;
input bool   InpWriteDiagnostics = true;

CCGWF_Engine g_engine;
SCGWFConfig  g_config;

void BuildConfig()
{
   g_config.run_on_init = InpRunOnInit;
   g_config.show_chart_comment = InpShowChartComment;
   g_config.print_summary = InpPrintSummary;
   g_config.phase10_dataset_file = InpPhase10DatasetFile;
   g_config.output_prefix = InpOutputPrefix;
   g_config.clear_outputs_on_run = InpClearOutputsOnRun;

   g_config.use_only_model_ready_rows = InpUseOnlyModelReadyRows;
   g_config.max_dataset_rows_to_read = InpMaxDatasetRowsToRead;
   g_config.minimum_train_rows = InpMinimumTrainRows;
   g_config.minimum_test_rows = InpMinimumTestRows;

   g_config.train_days = InpTrainDays;
   g_config.test_days = InpTestDays;
   g_config.step_days = InpStepDays;
   g_config.embargo_days = InpEmbargoDays;

   g_config.primary_bucket_key_mode = InpPrimaryBucketKeyMode;
   g_config.positive_edge_threshold_r = InpPositiveEdgeThresholdR;
   g_config.weak_edge_threshold_r = InpWeakEdgeThresholdR;
   g_config.minimum_bucket_train_rows = InpMinimumBucketTrainRows;
   g_config.allow_global_fallback = InpAllowGlobalFallback;

   g_config.write_fold_plan = InpWriteFoldPlan;
   g_config.write_predictions = InpWritePredictions;
   g_config.write_fold_metrics = InpWriteFoldMetrics;
   g_config.write_bucket_validation = InpWriteBucketValidation;
   g_config.write_experiment_summary = InpWriteExperimentSummary;
   g_config.write_diagnostics = InpWriteDiagnostics;
}

int OnInit()
{
   BuildConfig();
   if(g_config.run_on_init)
      g_engine.Run(g_config);
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   Comment("");
}

void OnTick()
{
   // Phase 11 is an offline research/anatomy expert. It intentionally performs no live trading.
}
//+------------------------------------------------------------------+
