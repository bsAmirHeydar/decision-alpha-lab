//+------------------------------------------------------------------+
//| CGP13_Writers.mqh                                                |
//| Phase 13 — Manifest, inventory, registry, and run-plan writers   |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGP13_WRITERS_MQH__
#define __CGP13_WRITERS_MQH__

#include <IntermarketDivergenceExecution/CG/CGP13_Types.mqh>

class CCGP13_Writers
{
private:
   string BoolText(const bool v) { return v ? "true" : "false"; }

public:
   bool WriteInventory(const string file_name,SCGP13FileRow &rows[])
   {
      int h=FileOpen(file_name,FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(h==INVALID_HANDLE) return false;
      FileWriteString(h,"stage,logical_name,file_name,required,exists,size_bytes,row_count,column_count,status,note\r\n");
      for(int i=0;i<ArraySize(rows);i++)
      {
         FileWriteString(h,
            CGP13_CsvEscape(rows[i].stage)+","+
            CGP13_CsvEscape(rows[i].logical_name)+","+
            CGP13_CsvEscape(rows[i].file_name)+","+
            IntegerToString(rows[i].required?1:0)+","+
            IntegerToString(rows[i].exists?1:0)+","+
            IntegerToString(rows[i].size_bytes)+","+
            IntegerToString(rows[i].row_count)+","+
            IntegerToString(rows[i].column_count)+","+
            CGP13_CsvEscape(rows[i].status)+","+
            CGP13_CsvEscape(rows[i].note)+"\r\n");
      }
      FileClose(h);
      return true;
   }

   bool WriteManifest(const string file_name,const SCGP13Config &cfg,const SCGP13Summary &s,SCGP13FileRow &rows[])
   {
      int h=FileOpen(file_name,FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(h==INVALID_HANDLE) return false;
      FileWriteString(h,"{\r\n");
      FileWriteString(h,"  \"experiment\": \"EXP0017 Phase 13 Controlled Model Comparison\",\r\n");
      FileWriteString(h,"  \"research_only\": true,\r\n");
      FileWriteString(h,"  \"execution_authority\": false,\r\n");
      FileWriteString(h,"  \"deterministic_seed\": "+IntegerToString(cfg.deterministic_seed)+",\r\n");
      FileWriteString(h,"  \"integrity_status\": \""+CGP13_JsonEscape(s.integrity_status)+"\",\r\n");
      FileWriteString(h,"  \"python_run_allowed\": "+BoolText(s.python_run_allowed)+",\r\n");
      FileWriteString(h,"  \"dataset_file\": \""+CGP13_JsonEscape(cfg.phase10_dataset_file)+"\",\r\n");
      FileWriteString(h,"  \"fold_plan_file\": \""+CGP13_JsonEscape(cfg.phase11_fold_plan_file)+"\",\r\n");
      FileWriteString(h,"  \"candidate_models\": [\"bucket_baseline\", \"threshold_baseline\", \"logistic_classifier\", \"ridge_regression\", \"constrained_ensemble\"],\r\n");
      FileWriteString(h,"  \"files\": [\r\n");
      for(int i=0;i<ArraySize(rows);i++)
      {
         FileWriteString(h,"    {\"stage\":\""+CGP13_JsonEscape(rows[i].stage)+"\",\"logical_name\":\""+CGP13_JsonEscape(rows[i].logical_name)+"\",\"file_name\":\""+CGP13_JsonEscape(rows[i].file_name)+"\",\"required\":"+BoolText(rows[i].required)+",\"exists\":"+BoolText(rows[i].exists)+",\"rows\":"+IntegerToString(rows[i].row_count)+"}");
         FileWriteString(h,(i+1<ArraySize(rows)?",":"")+"\r\n");
      }
      FileWriteString(h,"  ]\r\n}\r\n");
      FileClose(h);
      return true;
   }

   bool WriteRegistryTemplate(const string file_name,const SCGP13Config &cfg,const SCGP13Summary &s)
   {
      int h=FileOpen(file_name,FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(h==INVALID_HANDLE) return false;
      FileWriteString(h,"run_id,created_utc,seed,integrity_status,dataset_file,fold_plan_file,model_family,task,status,notes\r\n");
      string models[]={"bucket_baseline","threshold_baseline","logistic_classifier","ridge_regression","constrained_ensemble"};
      for(int i=0;i<ArraySize(models);i++)
      {
         string task=(models[i]=="logistic_classifier"?"classification":(models[i]=="ridge_regression"?"regression":"classification_and_regression"));
         FileWriteString(h,"PENDING,,"+IntegerToString(cfg.deterministic_seed)+","+CGP13_CsvEscape(s.integrity_status)+","+CGP13_CsvEscape(cfg.phase10_dataset_file)+","+CGP13_CsvEscape(cfg.phase11_fold_plan_file)+","+models[i]+","+task+",PLANNED,research_only\r\n");
      }
      FileClose(h);
      return true;
   }

   bool WriteRunPlan(const string file_name,const SCGP13Config &cfg,const SCGP13Summary &s)
   {
      int h=FileOpen(file_name,FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(h==INVALID_HANDLE) return false;
      FileWriteString(h,"# EXP0017 Phase 13 Python Run Plan\r\n\r\n");
      FileWriteString(h,"Integrity status: `"+s.integrity_status+"`  \r\n");
      FileWriteString(h,"Python run allowed by bridge: `"+(s.python_run_allowed?"true":"false")+"`\r\n\r\n");
      FileWriteString(h,"```powershell\r\n");
      FileWriteString(h,"python .\\research\\exp0017_phase13\\python\\phase13_controlled_model_comparison.py `\r\n");
      FileWriteString(h,"  --data-dir . `\r\n");
      FileWriteString(h,"  --out-dir .\\research\\exp0017_phase13\\outputs `\r\n");
      FileWriteString(h,"  --dataset-file \""+cfg.phase10_dataset_file+"\" `\r\n");
      FileWriteString(h,"  --fold-plan-file \""+cfg.phase11_fold_plan_file+"\" `\r\n");
      FileWriteString(h,"  --integrity-summary \"phase12_5_readiness_summary.json\" `\r\n");
      FileWriteString(h,"  --seed "+IntegerToString(cfg.deterministic_seed)+"\r\n");
      FileWriteString(h,"```\r\n\r\n");
      FileWriteString(h,"The output is research evidence only. It cannot authorize orders, filtering, risk changes, target changes, or strategy mutation.\r\n");
      FileClose(h);
      return true;
   }

   bool WriteDiagnostics(const string file_name,string &items[])
   {
      int h=FileOpen(file_name,FILE_WRITE|FILE_TXT|FILE_ANSI);
      if(h==INVALID_HANDLE) return false;
      FileWriteString(h,"row,diagnostic\r\n");
      for(int i=0;i<ArraySize(items);i++)
         FileWriteString(h,IntegerToString(i+1)+","+CGP13_CsvEscape(items[i])+"\r\n");
      FileClose(h);
      return true;
   }
};

#endif
