//+------------------------------------------------------------------+
//| EXP0017_CG_Python_Research_Bridge_Anatomy.mq5                    |
//| Phase 12 — Python research bridge and experiment registry anatomy |
//+------------------------------------------------------------------+
#property strict
#property version   "1.00"
#property description "EXP0017 Phase 12: Python research bridge, file inventory, manifest, and experiment registry. No trading."

#include <IntermarketDivergenceExecution/CG/CGP12_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGP12_Engine.mqh>

input bool   InpRunOnInit = true;
input bool   InpShowChartComment = true;
input bool   InpPrintSummary = true;
input bool   InpUseCommonFiles = false;
input string InpOutputPrefix = "EXP0017_Phase12";
input bool   InpClearOutputsOnRun = true;

input string InpPhase07OutcomeFile = "EXP0017_Phase07_Outcome_Study.csv";
input string InpPhase08OverallFile = "EXP0017_Phase08_Overall.csv";
input string InpPhase08CgDirectionRoleFile = "EXP0017_Phase08_By_CG_Direction_Role.csv";
input string InpPhase09RankingsFile = "EXP0017_Phase09_Rankings_All.csv";
input string InpPhase09ShortlistFile = "EXP0017_Phase09_Shortlist.csv";
input string InpPhase10DatasetFile = "EXP0017_Phase10_Model_Dataset.csv";
input string InpPhase11PredictionsFile = "EXP0017_Phase11_Predictions.csv";
input string InpPhase11FoldMetricsFile = "EXP0017_Phase11_Fold_Metrics.csv";
input string InpPhase11BucketValidationFile = "EXP0017_Phase11_Bucket_Validation.csv";
input string InpPhase11SummaryFile = "EXP0017_Phase11_Experiment_Summary.csv";

input bool   InpWriteInventoryCsv = true;
input bool   InpWriteResearchManifest = true;
input bool   InpWriteExperimentRegistryTemplate = true;
input bool   InpWritePythonRunPlan = true;
input bool   InpWriteDiagnostics = true;
input int    InpMaxHeaderColumnsToInspect = 260;

CCGP12_Engine g_engine;
SCGP12Config  g_config;

void BuildConfig()
{
   g_config.run_on_init = InpRunOnInit;
   g_config.show_chart_comment = InpShowChartComment;
   g_config.print_summary = InpPrintSummary;
   g_config.use_common_files = InpUseCommonFiles;
   g_config.output_prefix = InpOutputPrefix;
   g_config.clear_outputs_on_run = InpClearOutputsOnRun;

   g_config.phase07_outcome_file = InpPhase07OutcomeFile;
   g_config.phase08_overall_file = InpPhase08OverallFile;
   g_config.phase08_cg_direction_role_file = InpPhase08CgDirectionRoleFile;
   g_config.phase09_rankings_file = InpPhase09RankingsFile;
   g_config.phase09_shortlist_file = InpPhase09ShortlistFile;
   g_config.phase10_dataset_file = InpPhase10DatasetFile;
   g_config.phase11_predictions_file = InpPhase11PredictionsFile;
   g_config.phase11_fold_metrics_file = InpPhase11FoldMetricsFile;
   g_config.phase11_bucket_validation_file = InpPhase11BucketValidationFile;
   g_config.phase11_summary_file = InpPhase11SummaryFile;

   g_config.write_inventory_csv = InpWriteInventoryCsv;
   g_config.write_research_manifest = InpWriteResearchManifest;
   g_config.write_experiment_registry_template = InpWriteExperimentRegistryTemplate;
   g_config.write_python_run_plan = InpWritePythonRunPlan;
   g_config.write_diagnostics = InpWriteDiagnostics;
   g_config.max_header_columns_to_inspect = InpMaxHeaderColumnsToInspect;
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
   // Phase 12 is a research bridge only. It never places, modifies, or closes orders.
}
//+------------------------------------------------------------------+
