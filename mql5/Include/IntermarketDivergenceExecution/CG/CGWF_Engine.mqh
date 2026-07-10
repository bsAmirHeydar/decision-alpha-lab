//+------------------------------------------------------------------+
//| CGWF_Engine.mqh                                                  |
//| Phase 11 — Orchestrates walk-forward model experiment            |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGWF_ENGINE_MQH__
#define __CGWF_ENGINE_MQH__

#include <IntermarketDivergenceExecution/CG/CGWF_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGWF_CsvReader.mqh>
#include <IntermarketDivergenceExecution/CG/CGWF_Splitter.mqh>
#include <IntermarketDivergenceExecution/CG/CGWF_BaselineModel.mqh>
#include <IntermarketDivergenceExecution/CG/CGWF_Ledger.mqh>
#include <IntermarketDivergenceExecution/CG/CGWF_Display.mqh>

class CCGWF_Engine
{
private:
   CCGWF_CsvReader     m_reader;
   CCGWF_Splitter      m_splitter;
   CCGWF_BaselineModel m_model;
   CCGWF_Ledger        m_ledger;
   CCGWF_Display       m_display;

   void AddDiag(string &diagnostics[], const string d)
   {
      int n = ArraySize(diagnostics);
      ArrayResize(diagnostics,n+1);
      diagnostics[n] = d;
   }

   void AppendModels(SCGWFBucketModel &all[], SCGWFBucketModel &src[])
   {
      for(int i=0;i<ArraySize(src);i++)
      {
         int n = ArraySize(all);
         ArrayResize(all,n+1);
         all[n] = src[i];
      }
   }

   void FillSummaryFromMetrics(SCGWFSummary &s, SCGWFMetricRow &metrics[])
   {
      for(int i=0;i<ArraySize(metrics);i++)
      {
         if(metrics[i].report_name == "overall_oos" && metrics[i].bucket_key == "ALL")
         {
            s.oos_avg_r = metrics[i].avg_r;
            s.oos_win_rate = metrics[i].win_rate;
            s.oos_stop_rate = metrics[i].stop_rate;
            return;
         }
      }
   }

public:
   bool Run(const SCGWFConfig &cfg)
   {
      SCGWFSummary summary;
      CGWF_InitSummary(summary);
      string diagnostics[];

      SCGWFModelRow rows[];
      int loaded=0,accepted=0,rejected=0;
      string diag="";
      bool ok = m_reader.ReadDataset(cfg.phase10_dataset_file,rows,loaded,accepted,rejected,cfg.use_only_model_ready_rows,cfg.max_dataset_rows_to_read,diag);
      AddDiag(diagnostics,diag);
      summary.rows_loaded = loaded;
      summary.rows_after_filter = accepted;
      summary.rows_rejected = rejected;

      if(!ok || accepted <= 0)
      {
         summary.status = "failed_dataset_load";
         if(cfg.write_diagnostics) m_ledger.WriteDiagnostics(cfg.output_prefix,diagnostics);
         if(cfg.write_experiment_summary) m_ledger.WriteSummary(cfg.output_prefix,summary,cfg);
         m_display.Show(summary,cfg);
         m_display.PrintSummary(summary,cfg);
         return false;
      }

      SCGWFFold folds[];
      ok = m_splitter.BuildFolds(rows,cfg,folds,diag);
      AddDiag(diagnostics,diag);
      summary.folds_built = ArraySize(folds);
      for(int f=0;f<ArraySize(folds);f++) if(folds[f].usable) summary.folds_usable++;
      if(cfg.write_fold_plan) m_ledger.WriteFoldPlan(cfg.output_prefix,folds);

      if(!ok || summary.folds_usable <= 0)
      {
         summary.status = "failed_no_usable_folds";
         if(cfg.write_diagnostics) m_ledger.WriteDiagnostics(cfg.output_prefix,diagnostics);
         if(cfg.write_experiment_summary) m_ledger.WriteSummary(cfg.output_prefix,summary,cfg);
         m_display.Show(summary,cfg);
         m_display.PrintSummary(summary,cfg);
         return false;
      }

      SCGWFPrediction predictions[];
      SCGWFBucketModel all_models[];
      for(int i=0;i<ArraySize(folds);i++)
      {
         if(!folds[i].usable) continue;
         SCGWFBucketModel fold_models[];
         m_model.BuildTrainingModels(rows,folds[i],cfg,fold_models);
         AppendModels(all_models,fold_models);
         m_model.EvaluateFold(rows,folds[i],cfg,fold_models,predictions);
      }
      summary.predictions_written = ArraySize(predictions);
      summary.bucket_models_built = ArraySize(all_models);

      SCGWFMetricRow metrics[];
      m_model.BuildMetricsFromPredictions(predictions,metrics);
      FillSummaryFromMetrics(summary,metrics);
      summary.status = "complete_research_only";

      if(cfg.write_predictions) m_ledger.WritePredictions(cfg.output_prefix,predictions);
      if(cfg.write_bucket_validation) m_ledger.WriteBucketModels(cfg.output_prefix,all_models);
      if(cfg.write_fold_metrics) m_ledger.WriteMetrics(cfg.output_prefix,metrics);
      if(cfg.write_diagnostics) m_ledger.WriteDiagnostics(cfg.output_prefix,diagnostics);
      if(cfg.write_experiment_summary) m_ledger.WriteSummary(cfg.output_prefix,summary,cfg);

      m_display.Show(summary,cfg);
      m_display.PrintSummary(summary,cfg);
      return true;
   }
};

#endif
