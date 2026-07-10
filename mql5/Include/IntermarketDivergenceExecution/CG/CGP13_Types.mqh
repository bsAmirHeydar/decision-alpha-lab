//+------------------------------------------------------------------+
//| CGP13_Types.mqh                                                  |
//| Phase 13 — Controlled model-comparison bridge contracts          |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGP13_TYPES_MQH__
#define __CGP13_TYPES_MQH__

string CGP13_CsvEscape(const string value)
{
   string v=value;
   StringReplace(v,"\"","\"\"");
   if(StringFind(v,",")>=0 || StringFind(v,"\"")>=0 || StringFind(v,"\n")>=0 || StringFind(v,"\r")>=0)
      return "\""+v+"\"";
   return v;
}

string CGP13_JsonEscape(const string value)
{
   string v=value;
   StringReplace(v,"\\","\\\\");
   StringReplace(v,"\"","\\\"");
   StringReplace(v,"\r","\\r");
   StringReplace(v,"\n","\\n");
   StringReplace(v,"\t","\\t");
   return v;
}

struct SCGP13FileRow
{
   string stage;
   string logical_name;
   string file_name;
   bool   required;
   bool   exists;
   long   size_bytes;
   int    row_count;
   int    column_count;
   string status;
   string note;
};

struct SCGP13Config
{
   string phase10_dataset_file;
   string phase11_fold_plan_file;
   string phase12_5_readiness_file;
   string output_prefix;
   string python_script;
   string python_output_dir;
   int    deterministic_seed;
   bool   require_integrity_gate;
   bool   allow_ready_with_warnings;
   bool   show_chart_comment;
   bool   print_summary;
};

struct SCGP13Summary
{
   int    files_expected;
   int    files_found;
   int    required_missing;
   int    rows_visible;
   string integrity_status;
   bool   python_run_allowed;
   string status;
};

#endif
