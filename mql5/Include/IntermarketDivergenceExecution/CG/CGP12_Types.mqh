//+------------------------------------------------------------------+
//| CGP12_Types.mqh                                                  |
//| Phase 12 — Python research bridge types                          |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGP12_TYPES_MQH__
#define __CGP12_TYPES_MQH__

struct SCGP12Config
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
   string phase11_predictions_file;
   string phase11_fold_metrics_file;
   string phase11_bucket_validation_file;
   string phase11_summary_file;

   bool   write_inventory_csv;
   bool   write_research_manifest;
   bool   write_experiment_registry_template;
   bool   write_python_run_plan;
   bool   write_diagnostics;
   int    max_header_columns_to_inspect;
};

struct SCGP12FileInventoryRow
{
   string phase;
   string logical_name;
   string file_name;
   bool   exists;
   int    row_count_estimate;
   int    column_count;
   string header_preview;
   string status;
   string notes;
};

struct SCGP12RunStats
{
   int inventory_rows;
   int files_found;
   int files_missing;
   int manifest_written;
   int registry_written;
   int run_plan_written;
   int diagnostics_written;
   string status;
   string message;
};

string CGP12_BoolText(const bool value)
{
   return value ? "true" : "false";
}

string CGP12_EscapeCsv(string value)
{
   StringReplace(value, "\r", " ");
   StringReplace(value, "\n", " ");
   StringReplace(value, "\"", "\"\"");
   return "\"" + value + "\"";
}

string CGP12_JsonEscape(string value)
{
   StringReplace(value, "\\", "\\\\");
   StringReplace(value, "\"", "\\\"");
   StringReplace(value, "\r", " ");
   StringReplace(value, "\n", " ");
   return value;
}

string CGP12_NormalizeHeaderPreview(string value, const int max_len=420)
{
   StringReplace(value, "\r", "");
   StringReplace(value, "\n", "");
   if(StringLen(value) > max_len)
      return StringSubstr(value, 0, max_len) + "...";
   return value;
}

int CGP12_FileFlags(const bool common_files)
{
   int flags = FILE_READ|FILE_TXT|FILE_ANSI;
   if(common_files)
      flags |= FILE_COMMON;
   return flags;
}

int CGP12_WriteFlags(const bool common_files)
{
   int flags = FILE_WRITE|FILE_TXT|FILE_ANSI;
   if(common_files)
      flags |= FILE_COMMON;
   return flags;
}

#endif
//+------------------------------------------------------------------+
