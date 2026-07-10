//+------------------------------------------------------------------+
//| CGP12_FileInventory.mqh                                          |
//| Phase 12 — research file inventory                               |
//+------------------------------------------------------------------+
#property strict
#ifndef __CGP12_FILE_INVENTORY_MQH__
#define __CGP12_FILE_INVENTORY_MQH__

#include <IntermarketDivergenceExecution/CG/CGP12_Types.mqh>

class CCGP12_FileInventory
{
private:
   bool m_common;
   int  m_max_header_columns;

   int EstimateRows(const string file_name, string &header_preview, int &column_count)
   {
      header_preview = "";
      column_count = 0;
      int handle = FileOpen(file_name, CGP12_FileFlags(m_common));
      if(handle == INVALID_HANDLE)
         return 0;

      int rows = 0;
      bool header_seen = false;
      while(!FileIsEnding(handle))
      {
         string line = FileReadString(handle);
         if(StringLen(line) == 0 && FileIsEnding(handle))
            break;
         if(!header_seen)
         {
            header_preview = CGP12_NormalizeHeaderPreview(line);
            string cols[];
            column_count = StringSplit(line, ',', cols);
            if(column_count > m_max_header_columns)
               column_count = m_max_header_columns;
            header_seen = true;
         }
         rows++;
      }
      FileClose(handle);
      if(rows <= 0)
         return 0;
      return rows - 1;
   }

   void AddRow(SCGP12FileInventoryRow &rows[], const string phase, const string logical_name, const string file_name)
   {
      SCGP12FileInventoryRow row;
      row.phase = phase;
      row.logical_name = logical_name;
      row.file_name = file_name;
      row.exists = FileIsExist(file_name, m_common ? FILE_COMMON : 0);
      row.header_preview = "";
      row.column_count = 0;
      row.row_count_estimate = 0;
      row.status = row.exists ? "available" : "missing";
      row.notes = "";
      if(row.exists)
      {
         row.row_count_estimate = EstimateRows(file_name, row.header_preview, row.column_count);
         if(row.row_count_estimate <= 0)
            row.status = "available_empty_or_header_only";
      }
      int n = ArraySize(rows);
      ArrayResize(rows, n+1);
      rows[n] = row;
   }

public:
   void Setup(const bool common_files, const int max_header_columns)
   {
      m_common = common_files;
      m_max_header_columns = MathMax(1, max_header_columns);
   }

   int Build(const SCGP12Config &config, SCGP12FileInventoryRow &rows[])
   {
      ArrayResize(rows, 0);
      AddRow(rows, "Phase07", "outcome_study", config.phase07_outcome_file);
      AddRow(rows, "Phase08", "overall_statistics", config.phase08_overall_file);
      AddRow(rows, "Phase08", "cg_direction_role_statistics", config.phase08_cg_direction_role_file);
      AddRow(rows, "Phase09", "rankings_all", config.phase09_rankings_file);
      AddRow(rows, "Phase09", "shortlist", config.phase09_shortlist_file);
      AddRow(rows, "Phase10", "model_dataset", config.phase10_dataset_file);
      AddRow(rows, "Phase11", "walk_forward_predictions", config.phase11_predictions_file);
      AddRow(rows, "Phase11", "fold_metrics", config.phase11_fold_metrics_file);
      AddRow(rows, "Phase11", "bucket_validation", config.phase11_bucket_validation_file);
      AddRow(rows, "Phase11", "experiment_summary", config.phase11_summary_file);
      return ArraySize(rows);
   }
};

#endif
//+------------------------------------------------------------------+
