//+------------------------------------------------------------------+
//| CGP13_Engine.mqh                                                 |
//| Phase 13 — MQL5 research-bridge orchestration                    |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGP13_ENGINE_MQH__
#define __CGP13_ENGINE_MQH__

#include <IntermarketDivergenceExecution/CG/CGP13_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGP13_FileInventory.mqh>
#include <IntermarketDivergenceExecution/CG/CGP13_Writers.mqh>
#include <IntermarketDivergenceExecution/CG/CGP13_Display.mqh>

class CCGP13_Engine
{
private:
   CCGP13_FileInventory inventory;
   CCGP13_Writers writers;
   CCGP13_Display display;
   SCGP13FileRow rows[];
   string diagnostics[];

   void AddDiagnostic(const string text)
   {
      int n=ArraySize(diagnostics);
      ArrayResize(diagnostics,n+1);
      diagnostics[n]=text;
   }

public:
   bool Run(const SCGP13Config &cfg,SCGP13Summary &summary)
   {
      ArrayResize(rows,0);
      ArrayResize(diagnostics,0);

      inventory.AddAndInspect(rows,"phase10","model_dataset",cfg.phase10_dataset_file,true);
      inventory.AddAndInspect(rows,"phase11","fold_plan",cfg.phase11_fold_plan_file,true);
      inventory.AddAndInspect(rows,"phase11","predictions","EXP0017_Phase11_Predictions.csv",false);
      inventory.AddAndInspect(rows,"phase11","fold_metrics","EXP0017_Phase11_Fold_Metrics.csv",false);
      inventory.AddAndInspect(rows,"phase12_5","readiness_summary",cfg.phase12_5_readiness_file,cfg.require_integrity_gate);

      summary.files_expected=ArraySize(rows);
      summary.files_found=0;
      summary.required_missing=0;
      summary.rows_visible=0;
      for(int i=0;i<ArraySize(rows);i++)
      {
         if(rows[i].exists) summary.files_found++;
         if(rows[i].required && !rows[i].exists) summary.required_missing++;
         summary.rows_visible+=rows[i].row_count;
      }

      summary.integrity_status=inventory.ReadIntegrityStatus(cfg.phase12_5_readiness_file);
      summary.python_run_allowed=inventory.PythonRunAllowed(summary.integrity_status,cfg.require_integrity_gate,cfg.allow_ready_with_warnings) && summary.required_missing==0;
      summary.status=(summary.python_run_allowed ? "BRIDGE_READY" : "BRIDGE_BLOCKED");

      if(summary.required_missing>0) AddDiagnostic("One or more required Phase 13 input files are missing.");
      if(!summary.python_run_allowed) AddDiagnostic("Phase 13 Python comparison is blocked by required-file or Phase 12.5 readiness gate state.");
      AddDiagnostic("The MQL5 bridge does not train models; Python is the canonical comparison engine.");
      AddDiagnostic("Phase 13 outputs are research evidence only and have no execution authority.");

      string p=cfg.output_prefix;
      bool ok=true;
      ok = writers.WriteInventory(p+"_File_Inventory.csv",rows) && ok;
      ok = writers.WriteManifest(p+"_Research_Manifest.json",cfg,summary,rows) && ok;
      ok = writers.WriteRegistryTemplate(p+"_Experiment_Registry_Template.csv",cfg,summary) && ok;
      ok = writers.WriteRunPlan(p+"_Python_Run_Plan.md",cfg,summary) && ok;
      ok = writers.WriteDiagnostics(p+"_Diagnostics.csv",diagnostics) && ok;
      display.Publish(summary,cfg.show_chart_comment,cfg.print_summary);
      return ok;
   }
};

#endif
