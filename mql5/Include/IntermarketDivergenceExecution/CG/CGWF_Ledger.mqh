//+------------------------------------------------------------------+
//| CGWF_Ledger.mqh                                                  |
//| Phase 11 — Walk-forward output writers                           |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGWF_LEDGER_MQH__
#define __CGWF_LEDGER_MQH__

#include <IntermarketDivergenceExecution/CG/CGWF_Types.mqh>

class CCGWF_Ledger
{
private:
   string FileName(const string prefix,const string suffix)
   {
      return prefix + "_" + suffix;
   }

public:
   bool WriteFoldPlan(const string prefix, SCGWFFold &folds[])
   {
      int h = FileOpen(FileName(prefix,"Fold_Plan.csv"), FILE_WRITE | FILE_TXT | FILE_ANSI);
      if(h == INVALID_HANDLE) return false;
      FileWriteString(h,"fold_id,train_start,train_end,embargo_start,embargo_end,test_start,test_end,train_count,test_count,usable,status\r\n");
      for(int i=0;i<ArraySize(folds);i++)
      {
         SCGWFFold f = folds[i];
         FileWriteString(h,
            IntegerToString(f.fold_id) + "," +
            CGWF_CsvEscape(CGWF_Dt(f.train_start)) + "," +
            CGWF_CsvEscape(CGWF_Dt(f.train_end)) + "," +
            CGWF_CsvEscape(CGWF_Dt(f.embargo_start)) + "," +
            CGWF_CsvEscape(CGWF_Dt(f.embargo_end)) + "," +
            CGWF_CsvEscape(CGWF_Dt(f.test_start)) + "," +
            CGWF_CsvEscape(CGWF_Dt(f.test_end)) + "," +
            IntegerToString(f.train_count) + "," +
            IntegerToString(f.test_count) + "," +
            IntegerToString(f.usable ? 1 : 0) + "," +
            CGWF_CsvEscape(f.status) + "\r\n");
      }
      FileClose(h);
      return true;
   }

   bool WritePredictions(const string prefix, SCGWFPrediction &predictions[])
   {
      int h = FileOpen(FileName(prefix,"Predictions.csv"), FILE_WRITE | FILE_TXT | FILE_ANSI);
      if(h == INVALID_HANDLE) return false;
      FileWriteString(h,"fold_id,sample_id,signal_id,group,direction,role_key,bucket_key,bucket_source,train_count_for_bucket,predicted_avg_r,predicted_win_rate,predicted_edge_class,actual_r,actual_win,actual_loss,actual_stop,actual_mfe_r,actual_mae_r,directional_agreement,model_use_status\r\n");
      for(int i=0;i<ArraySize(predictions);i++)
      {
         SCGWFPrediction p = predictions[i];
         FileWriteString(h,
            IntegerToString(p.fold_id) + "," +
            CGWF_CsvEscape(p.sample_id) + "," +
            CGWF_CsvEscape(p.signal_id) + "," +
            CGWF_CsvEscape(p.group_name) + "," +
            CGWF_CsvEscape(p.direction) + "," +
            CGWF_CsvEscape(p.role_key) + "," +
            CGWF_CsvEscape(p.bucket_key) + "," +
            CGWF_CsvEscape(p.bucket_source) + "," +
            IntegerToString(p.train_count_for_bucket) + "," +
            DoubleToString(p.predicted_avg_r,6) + "," +
            DoubleToString(p.predicted_win_rate,2) + "," +
            CGWF_CsvEscape(p.predicted_edge_class) + "," +
            DoubleToString(p.actual_r,6) + "," +
            IntegerToString(p.actual_win) + "," +
            IntegerToString(p.actual_loss) + "," +
            IntegerToString(p.actual_stop) + "," +
            DoubleToString(p.actual_mfe_r,6) + "," +
            DoubleToString(p.actual_mae_r,6) + "," +
            IntegerToString(p.directional_agreement) + "," +
            CGWF_CsvEscape(p.model_use_status) + "\r\n");
      }
      FileClose(h);
      return true;
   }

   bool WriteBucketModels(const string prefix, SCGWFBucketModel &models[])
   {
      int h = FileOpen(FileName(prefix,"Bucket_Validation.csv"), FILE_WRITE | FILE_TXT | FILE_ANSI);
      if(h == INVALID_HANDLE) return false;
      FileWriteString(h,"fold_id,bucket_key,bucket_label,train_count,train_wins,train_losses,train_stops,train_avg_r,train_win_rate,train_stop_rate,train_avg_mfe_r,train_avg_mae_r,edge_class\r\n");
      for(int i=0;i<ArraySize(models);i++)
      {
         SCGWFBucketModel b = models[i];
         FileWriteString(h,
            IntegerToString(b.fold_id) + "," +
            CGWF_CsvEscape(b.bucket_key) + "," +
            CGWF_CsvEscape(b.bucket_label) + "," +
            IntegerToString(b.train_count) + "," +
            IntegerToString(b.train_wins) + "," +
            IntegerToString(b.train_losses) + "," +
            IntegerToString(b.train_stops) + "," +
            DoubleToString(b.train_avg_r,6) + "," +
            DoubleToString(b.train_win_rate,2) + "," +
            DoubleToString(b.train_stop_rate,2) + "," +
            DoubleToString(b.train_avg_mfe_r,6) + "," +
            DoubleToString(b.train_avg_mae_r,6) + "," +
            CGWF_CsvEscape(b.edge_class) + "\r\n");
      }
      FileClose(h);
      return true;
   }

   bool WriteMetrics(const string prefix, SCGWFMetricRow &metrics[])
   {
      int h = FileOpen(FileName(prefix,"Fold_Metrics.csv"), FILE_WRITE | FILE_TXT | FILE_ANSI);
      if(h == INVALID_HANDLE) return false;
      FileWriteString(h,"report_name,fold_id,bucket_key,bucket_label,samples,wins,losses,stops,avg_r,win_rate,stop_rate,avg_mfe_r,avg_mae_r,max_r,min_r\r\n");
      for(int i=0;i<ArraySize(metrics);i++)
      {
         SCGWFMetricRow m = metrics[i];
         FileWriteString(h,
            CGWF_CsvEscape(m.report_name) + "," +
            IntegerToString(m.fold_id) + "," +
            CGWF_CsvEscape(m.bucket_key) + "," +
            CGWF_CsvEscape(m.bucket_label) + "," +
            IntegerToString(m.samples) + "," +
            IntegerToString(m.wins) + "," +
            IntegerToString(m.losses) + "," +
            IntegerToString(m.stops) + "," +
            DoubleToString(m.avg_r,6) + "," +
            DoubleToString(m.win_rate,2) + "," +
            DoubleToString(m.stop_rate,2) + "," +
            DoubleToString(m.avg_mfe_r,6) + "," +
            DoubleToString(m.avg_mae_r,6) + "," +
            DoubleToString(m.max_r,6) + "," +
            DoubleToString(m.min_r,6) + "\r\n");
      }
      FileClose(h);
      return true;
   }

   bool WriteSummary(const string prefix, const SCGWFSummary &s, const SCGWFConfig &cfg)
   {
      int h = FileOpen(FileName(prefix,"Experiment_Summary.csv"), FILE_WRITE | FILE_TXT | FILE_ANSI);
      if(h == INVALID_HANDLE) return false;
      FileWriteString(h,"metric,value\r\n");
      FileWriteString(h,"status," + CGWF_CsvEscape(s.status) + "\r\n");
      FileWriteString(h,"dataset_file," + CGWF_CsvEscape(cfg.phase10_dataset_file) + "\r\n");
      FileWriteString(h,"bucket_key_mode," + CGWF_CsvEscape(CGWF_KeyModeToString(cfg.primary_bucket_key_mode)) + "\r\n");
      FileWriteString(h,"train_days," + IntegerToString(cfg.train_days) + "\r\n");
      FileWriteString(h,"test_days," + IntegerToString(cfg.test_days) + "\r\n");
      FileWriteString(h,"step_days," + IntegerToString(cfg.step_days) + "\r\n");
      FileWriteString(h,"embargo_days," + IntegerToString(cfg.embargo_days) + "\r\n");
      FileWriteString(h,"rows_loaded," + IntegerToString(s.rows_loaded) + "\r\n");
      FileWriteString(h,"rows_after_filter," + IntegerToString(s.rows_after_filter) + "\r\n");
      FileWriteString(h,"rows_rejected," + IntegerToString(s.rows_rejected) + "\r\n");
      FileWriteString(h,"folds_built," + IntegerToString(s.folds_built) + "\r\n");
      FileWriteString(h,"folds_usable," + IntegerToString(s.folds_usable) + "\r\n");
      FileWriteString(h,"predictions_written," + IntegerToString(s.predictions_written) + "\r\n");
      FileWriteString(h,"bucket_models_built," + IntegerToString(s.bucket_models_built) + "\r\n");
      FileWriteString(h,"oos_avg_r," + DoubleToString(s.oos_avg_r,6) + "\r\n");
      FileWriteString(h,"oos_win_rate," + DoubleToString(s.oos_win_rate,2) + "\r\n");
      FileWriteString(h,"oos_stop_rate," + DoubleToString(s.oos_stop_rate,2) + "\r\n");
      FileClose(h);
      return true;
   }

   bool WriteDiagnostics(const string prefix, string &diagnostics[])
   {
      int h = FileOpen(FileName(prefix,"Diagnostics.csv"), FILE_WRITE | FILE_TXT | FILE_ANSI);
      if(h == INVALID_HANDLE) return false;
      FileWriteString(h,"row,diagnostic\r\n");
      for(int i=0;i<ArraySize(diagnostics);i++)
         FileWriteString(h,IntegerToString(i+1) + "," + CGWF_CsvEscape(diagnostics[i]) + "\r\n");
      FileClose(h);
      return true;
   }
};

#endif
