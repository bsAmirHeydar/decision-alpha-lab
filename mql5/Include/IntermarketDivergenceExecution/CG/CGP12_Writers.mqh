//+------------------------------------------------------------------+
//| CGP12_Writers.mqh                                                |
//| Phase 12 — manifest, registry, run-plan, diagnostics writers     |
//+------------------------------------------------------------------+
#property strict
#ifndef __CGP12_WRITERS_MQH__
#define __CGP12_WRITERS_MQH__

#include <IntermarketDivergenceExecution/CG/CGP12_Types.mqh>

class CCGP12_Writers
{
private:
   bool m_common;

   bool DeleteIfRequested(const string file_name, const bool clear_outputs)
   {
      if(clear_outputs && FileIsExist(file_name, m_common ? FILE_COMMON : 0))
         return FileDelete(file_name, m_common ? FILE_COMMON : 0);
      return true;
   }

public:
   void Setup(const bool common_files)
   {
      m_common = common_files;
   }

   bool WriteInventory(const string file_name, const bool clear_outputs, SCGP12FileInventoryRow &rows[])
   {
      DeleteIfRequested(file_name, clear_outputs);
      int h = FileOpen(file_name, CGP12_WriteFlags(m_common));
      if(h == INVALID_HANDLE)
         return false;
      FileWriteString(h, "phase,logical_name,file_name,exists,row_count_estimate,column_count,status,header_preview,notes\n");
      for(int i=0; i<ArraySize(rows); i++)
      {
         string line = CGP12_EscapeCsv(rows[i].phase)+","+
                       CGP12_EscapeCsv(rows[i].logical_name)+","+
                       CGP12_EscapeCsv(rows[i].file_name)+","+
                       CGP12_EscapeCsv(CGP12_BoolText(rows[i].exists))+","+
                       IntegerToString(rows[i].row_count_estimate)+","+
                       IntegerToString(rows[i].column_count)+","+
                       CGP12_EscapeCsv(rows[i].status)+","+
                       CGP12_EscapeCsv(rows[i].header_preview)+","+
                       CGP12_EscapeCsv(rows[i].notes)+"\n";
         FileWriteString(h, line);
      }
      FileClose(h);
      return true;
   }

   bool WriteManifest(const string file_name, const bool clear_outputs, const SCGP12Config &config, SCGP12FileInventoryRow &rows[])
   {
      DeleteIfRequested(file_name, clear_outputs);
      int h = FileOpen(file_name, CGP12_WriteFlags(m_common));
      if(h == INVALID_HANDLE)
         return false;

      FileWriteString(h, "{\n");
      FileWriteString(h, "  \"project\": \"EXP0017 Cycle Group Intermarket Divergence\",\n");
      FileWriteString(h, "  \"phase\": \"Phase 12 - Python Research Bridge and Experiment Registry\",\n");
      FileWriteString(h, "  \"created_broker_time\": \""+CGP12_JsonEscape(TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS))+"\",\n");
      FileWriteString(h, "  \"doctrine\": {\n");
      FileWriteString(h, "    \"no_trading\": true,\n");
      FileWriteString(h, "    \"no_strategy_mutation\": true,\n");
      FileWriteString(h, "    \"research_only\": true\n");
      FileWriteString(h, "  },\n");
      FileWriteString(h, "  \"files\": [\n");
      for(int i=0; i<ArraySize(rows); i++)
      {
         FileWriteString(h, "    {\"phase\": \""+CGP12_JsonEscape(rows[i].phase)+"\", ");
         FileWriteString(h, "\"logical_name\": \""+CGP12_JsonEscape(rows[i].logical_name)+"\", ");
         FileWriteString(h, "\"file_name\": \""+CGP12_JsonEscape(rows[i].file_name)+"\", ");
         FileWriteString(h, "\"exists\": "+CGP12_BoolText(rows[i].exists)+", ");
         FileWriteString(h, "\"row_count_estimate\": "+IntegerToString(rows[i].row_count_estimate)+", ");
         FileWriteString(h, "\"status\": \""+CGP12_JsonEscape(rows[i].status)+"\"}");
         if(i < ArraySize(rows)-1) FileWriteString(h, ",");
         FileWriteString(h, "\n");
      }
      FileWriteString(h, "  ]\n");
      FileWriteString(h, "}\n");
      FileClose(h);
      return true;
   }

   bool WriteRegistryTemplate(const string file_name, const bool clear_outputs)
   {
      DeleteIfRequested(file_name, clear_outputs);
      int h = FileOpen(file_name, CGP12_WriteFlags(m_common));
      if(h == INVALID_HANDLE)
         return false;
      FileWriteString(h, "experiment_id,created_at,research_question,dataset_file,walk_forward_file,label_window,train_days,test_days,embargo_days,bucket_key,features_used,exclusions,metric_primary,metric_secondary,result_summary,decision,notes\n");
      FileWriteString(h, "EXP0017-P12-0001,"+CGP12_EscapeCsv(TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS))+",\"Does CG-direction-role bucket stability survive walk-forward?\",EXP0017_Phase10_Model_Dataset.csv,EXP0017_Phase11_Predictions.csv,cycle_end,120,20,1,cg_direction_role,baseline_fields,not_model_ready_rows,oos_avg_r,oos_win_rate,pending,research_only,populate_after_python_run\n");
      FileClose(h);
      return true;
   }

   bool WritePythonRunPlan(const string file_name, const bool clear_outputs)
   {
      DeleteIfRequested(file_name, clear_outputs);
      int h = FileOpen(file_name, CGP12_WriteFlags(m_common));
      if(h == INVALID_HANDLE)
         return false;
      FileWriteString(h, "# EXP0017 Phase 12 Python Run Plan\n\n");
      FileWriteString(h, "This run plan is generated by the MQL5 research bridge. It is a research handoff, not a trading command.\n\n");
      FileWriteString(h, "```powershell\n");
      FileWriteString(h, "python .\\research\\exp0017_phase12\\python\\phase12_research_workbench.py --data-dir . --out-dir .\\research\\exp0017_phase12\\outputs\n");
      FileWriteString(h, "```\n\n");
      FileWriteString(h, "Expected outputs:\n\n");
      FileWriteString(h, "- phase12_data_audit.csv\n- phase12_bucket_stability.csv\n- phase12_oos_leaderboard.csv\n- phase12_feature_drift.csv\n- phase12_html_report.html\n- phase12_research_summary.md\n");
      FileClose(h);
      return true;
   }

   bool WriteDiagnostics(const string file_name, const bool clear_outputs, const SCGP12RunStats &stats)
   {
      DeleteIfRequested(file_name, clear_outputs);
      int h = FileOpen(file_name, CGP12_WriteFlags(m_common));
      if(h == INVALID_HANDLE)
         return false;
      FileWriteString(h, "key,value\n");
      FileWriteString(h, "inventory_rows,"+IntegerToString(stats.inventory_rows)+"\n");
      FileWriteString(h, "files_found,"+IntegerToString(stats.files_found)+"\n");
      FileWriteString(h, "files_missing,"+IntegerToString(stats.files_missing)+"\n");
      FileWriteString(h, "manifest_written,"+IntegerToString(stats.manifest_written)+"\n");
      FileWriteString(h, "registry_written,"+IntegerToString(stats.registry_written)+"\n");
      FileWriteString(h, "run_plan_written,"+IntegerToString(stats.run_plan_written)+"\n");
      FileWriteString(h, "diagnostics_written,"+IntegerToString(stats.diagnostics_written)+"\n");
      FileWriteString(h, "status,"+CGP12_EscapeCsv(stats.status)+"\n");
      FileWriteString(h, "message,"+CGP12_EscapeCsv(stats.message)+"\n");
      FileClose(h);
      return true;
   }
};

#endif
//+------------------------------------------------------------------+
