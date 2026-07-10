//+------------------------------------------------------------------+
//| CGWF_BaselineModel.mqh                                           |
//| Phase 11 — Leakage-safe bucket baseline and OOS evaluation       |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGWF_BASELINE_MODEL_MQH__
#define __CGWF_BASELINE_MODEL_MQH__

#include <IntermarketDivergenceExecution/CG/CGWF_Types.mqh>

class CCGWF_BaselineModel
{
private:
   int FindBucket(SCGWFBucketModel &models[], const string key)
   {
      for(int i=0;i<ArraySize(models);i++)
         if(models[i].bucket_key == key)
            return i;
      return -1;
   }

   void UpdateBucket(SCGWFBucketModel &b, const SCGWFModelRow &r)
   {
      b.train_count++;
      if(r.primary_r > 0.0) b.train_wins++;
      if(r.primary_r < 0.0) b.train_losses++;
      if(r.label_stopped_intraday == 1) b.train_stops++;
      b.train_sum_r += r.primary_r;
      b.train_sum_mfe_r += r.mfe_r;
      b.train_sum_mae_r += r.mae_r;
   }

   void FinalizeBucket(SCGWFBucketModel &b, const SCGWFConfig &cfg)
   {
      if(b.train_count <= 0) return;
      b.train_avg_r = b.train_sum_r / (double)b.train_count;
      b.train_win_rate = 100.0 * (double)b.train_wins / (double)b.train_count;
      b.train_stop_rate = 100.0 * (double)b.train_stops / (double)b.train_count;
      b.train_avg_mfe_r = b.train_sum_mfe_r / (double)b.train_count;
      b.train_avg_mae_r = b.train_sum_mae_r / (double)b.train_count;
      b.edge_class = CGWF_EdgeClass(b.train_avg_r,cfg.positive_edge_threshold_r,cfg.weak_edge_threshold_r);
   }

   int AppendPrediction(SCGWFPrediction &predictions[], const SCGWFPrediction &p)
   {
      int n = ArraySize(predictions);
      ArrayResize(predictions,n+1);
      predictions[n] = p;
      return n;
   }

   void UpdateMetric(SCGWFMetricRow &m, const SCGWFPrediction &p)
   {
      m.samples++;
      if(p.actual_r > 0.0) m.wins++;
      if(p.actual_r < 0.0) m.losses++;
      if(p.actual_stop == 1) m.stops++;
      m.sum_r += p.actual_r;
      m.avg_mfe_r += p.actual_mfe_r;
      m.avg_mae_r += p.actual_mae_r;
      if(m.samples == 1 || p.actual_r > m.max_r) m.max_r = p.actual_r;
      if(m.samples == 1 || p.actual_r < m.min_r) m.min_r = p.actual_r;
   }

   int FindMetric(SCGWFMetricRow &metrics[], const string report_name, const int fold_id, const string key)
   {
      for(int i=0;i<ArraySize(metrics);i++)
         if(metrics[i].report_name == report_name && metrics[i].fold_id == fold_id && metrics[i].bucket_key == key)
            return i;
      return -1;
   }

   int EnsureMetric(SCGWFMetricRow &metrics[], const string report_name, const int fold_id, const string key, const string label)
   {
      int idx = FindMetric(metrics,report_name,fold_id,key);
      if(idx >= 0) return idx;
      SCGWFMetricRow m;
      m.report_name = report_name;
      m.fold_id = fold_id;
      m.bucket_key = key;
      m.bucket_label = label;
      m.samples = 0;
      m.wins = 0;
      m.losses = 0;
      m.stops = 0;
      m.sum_r = 0.0;
      m.avg_r = 0.0;
      m.win_rate = 0.0;
      m.stop_rate = 0.0;
      m.avg_mfe_r = 0.0;
      m.avg_mae_r = 0.0;
      m.max_r = 0.0;
      m.min_r = 0.0;
      int n = ArraySize(metrics);
      ArrayResize(metrics,n+1);
      metrics[n] = m;
      return n;
   }

public:
   void BuildTrainingModels(SCGWFModelRow &rows[], const SCGWFFold &fold, const SCGWFConfig &cfg, SCGWFBucketModel &models[])
   {
      ArrayResize(models,0);

      SCGWFBucketModel global;
      global.fold_id = fold.fold_id;
      global.bucket_key = "ALL";
      global.bucket_label = "ALL";
      global.train_count = 0;
      global.train_wins = 0;
      global.train_losses = 0;
      global.train_stops = 0;
      global.train_sum_r = 0.0;
      global.train_avg_r = 0.0;
      global.train_win_rate = 0.0;
      global.train_stop_rate = 0.0;
      global.train_avg_mfe_r = 0.0;
      global.train_avg_mae_r = 0.0;
      global.train_sum_mfe_r = 0.0;
      global.train_sum_mae_r = 0.0;
      global.edge_class = "untrained";

      ArrayResize(models,1);
      models[0] = global;

      for(int i=0;i<ArraySize(rows);i++)
      {
         if(rows[i].confirmation_time < fold.train_start || rows[i].confirmation_time >= fold.train_end) continue;
         UpdateBucket(models[0],rows[i]);

         string key = CGWF_RowKey(rows[i],cfg.primary_bucket_key_mode);
         int idx = FindBucket(models,key);
         if(idx < 0)
         {
            SCGWFBucketModel b;
            b.fold_id = fold.fold_id;
            b.bucket_key = key;
            b.bucket_label = CGWF_RowLabel(rows[i],cfg.primary_bucket_key_mode);
            b.train_count = 0;
            b.train_wins = 0;
            b.train_losses = 0;
            b.train_stops = 0;
            b.train_sum_r = 0.0;
            b.train_avg_r = 0.0;
            b.train_win_rate = 0.0;
            b.train_stop_rate = 0.0;
            b.train_avg_mfe_r = 0.0;
            b.train_avg_mae_r = 0.0;
            b.train_sum_mfe_r = 0.0;
            b.train_sum_mae_r = 0.0;
            b.edge_class = "untrained";
            int n = ArraySize(models);
            ArrayResize(models,n+1);
            models[n] = b;
            idx = n;
         }
         UpdateBucket(models[idx],rows[i]);
      }

      for(int j=0;j<ArraySize(models);j++)
         FinalizeBucket(models[j],cfg);
   }

   void EvaluateFold(SCGWFModelRow &rows[], const SCGWFFold &fold, const SCGWFConfig &cfg, SCGWFBucketModel &models[], SCGWFPrediction &predictions[])
   {
      for(int i=0;i<ArraySize(rows);i++)
      {
         if(rows[i].confirmation_time < fold.test_start || rows[i].confirmation_time >= fold.test_end) continue;

         string key = CGWF_RowKey(rows[i],cfg.primary_bucket_key_mode);
         int idx = FindBucket(models,key);
         string source = "bucket";
         if(idx < 0 || models[idx].train_count < cfg.minimum_bucket_train_rows)
         {
            if(cfg.allow_global_fallback)
            {
               idx = FindBucket(models,"ALL");
               source = "global_fallback";
            }
            else
            {
               idx = -1;
               source = "unscored_no_bucket";
            }
         }

         SCGWFPrediction p;
         p.fold_id = fold.fold_id;
         p.sample_id = rows[i].sample_id;
         p.signal_id = rows[i].signal_id;
         p.group_name = rows[i].group_name;
         p.direction = rows[i].direction;
         p.role_key = rows[i].role_key;
         p.bucket_key = key;
         p.bucket_source = source;
         p.train_count_for_bucket = 0;
         p.predicted_avg_r = 0.0;
         p.predicted_win_rate = 0.0;
         p.predicted_edge_class = "unscored";
         if(idx >= 0)
         {
            p.train_count_for_bucket = models[idx].train_count;
            p.predicted_avg_r = models[idx].train_avg_r;
            p.predicted_win_rate = models[idx].train_win_rate;
            p.predicted_edge_class = models[idx].edge_class;
         }
         p.actual_r = rows[i].primary_r;
         p.actual_win = (rows[i].primary_r > 0.0 ? 1 : 0);
         p.actual_loss = (rows[i].primary_r < 0.0 ? 1 : 0);
         p.actual_stop = rows[i].label_stopped_intraday;
         p.actual_mfe_r = rows[i].mfe_r;
         p.actual_mae_r = rows[i].mae_r;
         p.directional_agreement = ((p.predicted_avg_r >= cfg.positive_edge_threshold_r && p.actual_r > 0.0) ? 1 : 0);
         p.model_use_status = rows[i].model_use_status;
         AppendPrediction(predictions,p);
      }
   }

   void BuildMetricsFromPredictions(SCGWFPrediction &predictions[], SCGWFMetricRow &metrics[])
   {
      ArrayResize(metrics,0);
      for(int i=0;i<ArraySize(predictions);i++)
      {
         SCGWFPrediction p = predictions[i];
         int all_idx = EnsureMetric(metrics,"overall_oos",0,"ALL","ALL");
         UpdateMetric(metrics[all_idx],p);

         int fold_idx = EnsureMetric(metrics,"by_fold",p.fold_id,"FOLD_" + IntegerToString(p.fold_id),"FOLD_" + IntegerToString(p.fold_id));
         UpdateMetric(metrics[fold_idx],p);

         int bucket_idx = EnsureMetric(metrics,"by_bucket",0,p.bucket_key,p.bucket_key);
         UpdateMetric(metrics[bucket_idx],p);

         int fold_bucket_idx = EnsureMetric(metrics,"by_fold_bucket",p.fold_id,p.bucket_key,p.bucket_key);
         UpdateMetric(metrics[fold_bucket_idx],p);
      }

      for(int j=0;j<ArraySize(metrics);j++)
      {
         if(metrics[j].samples <= 0) continue;
         metrics[j].avg_r = metrics[j].sum_r / (double)metrics[j].samples;
         metrics[j].win_rate = 100.0 * (double)metrics[j].wins / (double)metrics[j].samples;
         metrics[j].stop_rate = 100.0 * (double)metrics[j].stops / (double)metrics[j].samples;
         metrics[j].avg_mfe_r = metrics[j].avg_mfe_r / (double)metrics[j].samples;
         metrics[j].avg_mae_r = metrics[j].avg_mae_r / (double)metrics[j].samples;
      }
   }
};

#endif
