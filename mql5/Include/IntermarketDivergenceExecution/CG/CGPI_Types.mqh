//+------------------------------------------------------------------+
//| CGPI_Types.mqh                                                   |
//| Phase 12.5 — Pipeline integrity contracts and shared types       |
//+------------------------------------------------------------------+
#property strict
#ifndef __CGPI_TYPES_MQH__
#define __CGPI_TYPES_MQH__

enum ECGPISeverity
{
   CGPI_SEVERITY_INFO = 0,
   CGPI_SEVERITY_WARNING = 1,
   CGPI_SEVERITY_ERROR = 2,
   CGPI_SEVERITY_CRITICAL = 3
};

enum ECGPIRelationMode
{
   CGPI_RELATION_EXACT = 0,
   CGPI_RELATION_CHILD_SUBSET = 1
};

struct SCGPIConfig
{
   bool   run_on_init;
   bool   show_chart_comment;
   bool   print_summary;
   bool   use_common_files;
   string output_prefix;
   bool   clear_outputs_on_run;

   string phase07_outcome_file;
   string phase08_overall_file;
   string phase08_cg_direction_role_file;
   string phase09_rankings_file;
   string phase09_shortlist_file;
   string phase10_dataset_file;
   string phase10_label_summary_file;
   string phase11_fold_plan_file;
   string phase11_predictions_file;
   string phase11_fold_metrics_file;
   string phase11_bucket_validation_file;
   string phase11_experiment_summary_file;

   bool   enable_schema_audit;
   bool   enable_primary_key_audit;
   bool   enable_lineage_reconciliation;
   bool   enable_temporal_audit;
   bool   enable_metric_reconciliation;
   int    max_rows_to_inspect_per_file;
   int    max_keys_to_reconcile;
   int    allowed_count_difference;
   double minimum_exact_lineage_coverage_percent;
   bool   block_phase13_on_critical_failure;

   bool   write_file_audit;
   bool   write_schema_issues;
   bool   write_key_reconciliation;
   bool   write_metric_reconciliation;
   bool   write_readiness_gates;
   bool   write_readiness_summary;
   bool   write_diagnostics;
};

struct SCGPIFileContract
{
   string phase;
   string logical_name;
   string file_name;
   bool   required;
   int    minimum_columns;
   string required_columns_pipe;
   string primary_key_columns_pipe;
   string timestamp_column;
   ECGPISeverity missing_file_severity;
};

struct SCGPIFileAuditRow
{
   string phase;
   string logical_name;
   string file_name;
   bool   required;
   bool   exists;
   int    row_count;
   int    inspected_rows;
   int    column_count;
   int    missing_required_columns;
   int    empty_primary_keys;
   int    duplicate_primary_keys;
   int    timestamp_parse_failures;
   int    timestamp_out_of_order;
   bool   inspection_truncated;
   string status;
   string notes;
};

struct SCGPISchemaIssue
{
   string phase;
   string logical_name;
   string file_name;
   string column_name;
   string issue_type;
   ECGPISeverity severity;
   string detail;
};

struct SCGPIReconciliationRow
{
   string relation_name;
   ECGPIRelationMode relation_mode;
   string parent_file;
   string parent_key;
   string child_file;
   string child_key;
   int    parent_unique_keys;
   int    child_unique_keys;
   int    matched_keys;
   int    missing_in_child;
   int    orphan_in_child;
   double parent_coverage_percent;
   double child_coverage_percent;
   string status;
   string notes;
};

struct SCGPIMetricCheck
{
   string check_name;
   string left_file;
   string left_metric;
   double left_value;
   string right_file;
   string right_metric;
   double right_value;
   double delta;
   double tolerance;
   string status;
   string notes;
};

struct SCGPIReadinessGate
{
   string gate_name;
   bool   required;
   bool   passed;
   ECGPISeverity severity;
   string evidence;
   string remediation;
};

struct SCGPIRunStats
{
   int contracts_total;
   int required_files;
   int files_found;
   int files_missing;
   int schema_issues;
   int critical_schema_issues;
   int duplicate_primary_keys;
   int empty_primary_keys;
   int lineage_checks;
   int lineage_failures;
   int metric_checks;
   int metric_failures;
   int readiness_gates;
   int readiness_failures;
   string readiness_status;
   string message;
};

string CGPI_BoolText(const bool value) { return value ? "true" : "false"; }

string CGPI_SeverityText(const ECGPISeverity severity)
{
   if(severity == CGPI_SEVERITY_CRITICAL) return "CRITICAL";
   if(severity == CGPI_SEVERITY_ERROR) return "ERROR";
   if(severity == CGPI_SEVERITY_WARNING) return "WARNING";
   return "INFO";
}

string CGPI_RelationModeText(const ECGPIRelationMode mode)
{
   return mode == CGPI_RELATION_EXACT ? "EXACT" : "CHILD_SUBSET";
}

string CGPI_CsvEscape(string value)
{
   StringReplace(value,"\r"," ");
   StringReplace(value,"\n"," ");
   StringReplace(value,"\"","\"\"");
   return "\"" + value + "\"";
}

int CGPI_ReadFlags(const bool common_files)
{
   int flags = FILE_READ | FILE_TXT | FILE_ANSI;
   if(common_files) flags |= FILE_COMMON;
   return flags;
}

int CGPI_WriteFlags(const bool common_files)
{
   int flags = FILE_WRITE | FILE_TXT | FILE_ANSI;
   if(common_files) flags |= FILE_COMMON;
   return flags;
}

int CGPI_FileScopeFlag(const bool common_files)
{
   return common_files ? FILE_COMMON : 0;
}

double CGPI_SafePercent(const int numerator,const int denominator)
{
   if(denominator <= 0) return 0.0;
   return 100.0 * (double)numerator / (double)denominator;
}

void CGPI_AddDiagnostic(string &diagnostics[],const string message)
{
   int n = ArraySize(diagnostics);
   ArrayResize(diagnostics,n+1);
   diagnostics[n] = message;
}

#endif
//+------------------------------------------------------------------+
