//+------------------------------------------------------------------+
//| EXP0017_CG_Pipeline_Integrity_Anatomy.mq5                        |
//| Phase 12.5 — Pipeline integrity and schema reconciliation        |
//+------------------------------------------------------------------+
#property strict
#property version   "1.00"
#property description "EXP0017 Phase 12.5: pipeline integrity, schema, lineage, temporal, metric, and readiness audit. No trading."

#include <IntermarketDivergenceExecution/CG/CGPI_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGPI_Engine.mqh>

input bool   InpRunOnInit = true;
input bool   InpShowChartComment = false;
input bool   InpPrintSummary = true;
input bool   InpUseCommonFiles = false;
input string InpOutputPrefix = "EXP0017_Phase12_5";
input bool   InpClearOutputsOnRun = true;

// Critical pipeline files.
input string InpPhase07OutcomeFile = "EXP0017_Phase07_Outcome_Study.csv";
input string InpPhase08OverallFile = "EXP0017_Phase08_Overall.csv";
input string InpPhase08CgDirectionRoleFile = "EXP0017_Phase08_By_CG_Direction_Role.csv";
input string InpPhase09RankingsFile = "EXP0017_Phase09_Rankings_All.csv";
input string InpPhase09ShortlistFile = "EXP0017_Phase09_Shortlist.csv";
input string InpPhase10DatasetFile = "EXP0017_Phase10_Model_Dataset.csv";
input string InpPhase10LabelSummaryFile = "EXP0017_Phase10_Label_Summary.csv";
input string InpPhase11FoldPlanFile = "EXP0017_Phase11_Fold_Plan.csv";
input string InpPhase11PredictionsFile = "EXP0017_Phase11_Predictions.csv";
input string InpPhase11FoldMetricsFile = "EXP0017_Phase11_Fold_Metrics.csv";
input string InpPhase11BucketValidationFile = "EXP0017_Phase11_Bucket_Validation.csv";
input string InpPhase11ExperimentSummaryFile = "EXP0017_Phase11_Experiment_Summary.csv";

// Audit controls.
input bool   InpEnableSchemaAudit = true;
input bool   InpEnablePrimaryKeyAudit = true;
input bool   InpEnableLineageReconciliation = true;
input bool   InpEnableTemporalAudit = true;
input bool   InpEnableMetricReconciliation = true;
input int    InpMaxRowsToInspectPerFile = 50000;
input int    InpMaxKeysToReconcile = 100000;
input int    InpAllowedCountDifference = 0;
input double InpMinimumExactLineageCoveragePercent = 99.90;
input bool   InpBlockPhase13OnCriticalFailure = true;

// Output controls.
input bool   InpWriteFileAudit = true;
input bool   InpWriteSchemaIssues = true;
input bool   InpWriteKeyReconciliation = true;
input bool   InpWriteMetricReconciliation = true;
input bool   InpWriteReadinessGates = true;
input bool   InpWriteReadinessSummary = true;
input bool   InpWriteDiagnostics = true;

CCGPI_Engine g_engine;
SCGPIConfig  g_config;

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
   g_config.phase10_label_summary_file = InpPhase10LabelSummaryFile;
   g_config.phase11_fold_plan_file = InpPhase11FoldPlanFile;
   g_config.phase11_predictions_file = InpPhase11PredictionsFile;
   g_config.phase11_fold_metrics_file = InpPhase11FoldMetricsFile;
   g_config.phase11_bucket_validation_file = InpPhase11BucketValidationFile;
   g_config.phase11_experiment_summary_file = InpPhase11ExperimentSummaryFile;

   g_config.enable_schema_audit = InpEnableSchemaAudit;
   g_config.enable_primary_key_audit = InpEnablePrimaryKeyAudit;
   g_config.enable_lineage_reconciliation = InpEnableLineageReconciliation;
   g_config.enable_temporal_audit = InpEnableTemporalAudit;
   g_config.enable_metric_reconciliation = InpEnableMetricReconciliation;
   g_config.max_rows_to_inspect_per_file = InpMaxRowsToInspectPerFile;
   g_config.max_keys_to_reconcile = InpMaxKeysToReconcile;
   g_config.allowed_count_difference = InpAllowedCountDifference;
   g_config.minimum_exact_lineage_coverage_percent = InpMinimumExactLineageCoveragePercent;
   g_config.block_phase13_on_critical_failure = InpBlockPhase13OnCriticalFailure;

   g_config.write_file_audit = InpWriteFileAudit;
   g_config.write_schema_issues = InpWriteSchemaIssues;
   g_config.write_key_reconciliation = InpWriteKeyReconciliation;
   g_config.write_metric_reconciliation = InpWriteMetricReconciliation;
   g_config.write_readiness_gates = InpWriteReadinessGates;
   g_config.write_readiness_summary = InpWriteReadinessSummary;
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
   // Phase 12.5 is an offline integrity auditor. It never sends, modifies, or closes an order.
}
//+------------------------------------------------------------------+
