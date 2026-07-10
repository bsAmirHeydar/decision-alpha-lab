//+------------------------------------------------------------------+
//| CGPI_Contracts.mqh                                               |
//| Phase 12.5 — Canonical inter-phase CSV contracts                 |
//+------------------------------------------------------------------+
#property strict
#ifndef __CGPI_CONTRACTS_MQH__
#define __CGPI_CONTRACTS_MQH__

#include <IntermarketDivergenceExecution/CG/CGPI_Types.mqh>

class CCGPI_Contracts
{
private:
   void Add(SCGPIFileContract &rows[],const string phase,const string logical_name,
            const string file_name,const bool required,const int minimum_columns,
            const string required_columns,const string primary_key_columns,
            const string timestamp_column,const ECGPISeverity missing_severity)
   {
      int n = ArraySize(rows);
      ArrayResize(rows,n+1);
      rows[n].phase = phase;
      rows[n].logical_name = logical_name;
      rows[n].file_name = file_name;
      rows[n].required = required;
      rows[n].minimum_columns = minimum_columns;
      rows[n].required_columns_pipe = required_columns;
      rows[n].primary_key_columns_pipe = primary_key_columns;
      rows[n].timestamp_column = timestamp_column;
      rows[n].missing_file_severity = missing_severity;
   }

public:
   int Build(const SCGPIConfig &cfg,SCGPIFileContract &rows[])
   {
      ArrayResize(rows,0);

      Add(rows,"07","outcome_study",cfg.phase07_outcome_file,true,20,
          "outcome_id|signal_id|availability|group|group_minutes|current_cycle|reference_cycle|direction|side|clean_symbol|hunter_symbol|confirmation_ny|entry_price|stop_price|stop_points|cycle_end_r|mfe_r|mae_r|stop_hit_intraday|daily_range_points",
          "outcome_id","confirmation_ny",CGPI_SEVERITY_CRITICAL);

      Add(rows,"08","overall_statistics",cfg.phase08_overall_file,true,12,
          "dimension|key|sample_count|win_count|loss_count|win_rate_percent|stop_count|stop_rate_percent|max_stop_streak|avg_r|avg_mfe_r|avg_mae_r",
          "dimension|key","",CGPI_SEVERITY_ERROR);

      Add(rows,"08","cg_direction_role_statistics",cfg.phase08_cg_direction_role_file,true,12,
          "dimension|key|sample_count|win_rate_percent|stop_rate_percent|max_stop_streak|avg_r|avg_normalized|avg_mfe_r|avg_mae_r|max_r|min_r",
          "dimension|key","",CGPI_SEVERITY_ERROR);

      Add(rows,"09","rankings_all",cfg.phase09_rankings_file,true,12,
          "rank|report_name|bucket_key|sample_count|win_rate_percent|avg_r|stop_rate_percent|max_stop_streak|quality_score|grade|shortlist|red_flags",
          "report_name|bucket_key","",CGPI_SEVERITY_ERROR);

      Add(rows,"09","shortlist",cfg.phase09_shortlist_file,false,8,
          "rank|report_name|bucket_key|sample_count|avg_r|quality_score|grade|shortlist",
          "report_name|bucket_key","",CGPI_SEVERITY_WARNING);

      Add(rows,"10","model_dataset",cfg.phase10_dataset_file,true,30,
          "sample_id|outcome_id|signal_id|model_use_status|availability|group|group_minutes|current_cycle|reference_cycle|reference_age_cycles|direction|side|clean_symbol|hunter_symbol|role_key|confirmation_ny|stop_points|daily_range_points|primary_window|primary_r|label_class|label_binary_win|label_stopped_intraday",
          "sample_id","confirmation_ny",CGPI_SEVERITY_CRITICAL);

      Add(rows,"10","label_summary",cfg.phase10_label_summary_file,true,2,
          "metric|value","metric","",CGPI_SEVERITY_ERROR);

      Add(rows,"11","fold_plan",cfg.phase11_fold_plan_file,true,10,
          "fold_id|train_start|train_end|embargo_start|embargo_end|test_start|test_end|train_count|test_count|usable|status",
          "fold_id","test_start",CGPI_SEVERITY_CRITICAL);

      Add(rows,"11","predictions",cfg.phase11_predictions_file,true,16,
          "fold_id|sample_id|signal_id|group|direction|role_key|bucket_key|bucket_source|train_count_for_bucket|predicted_avg_r|predicted_win_rate|predicted_edge_class|actual_r|actual_win|actual_loss|actual_stop|model_use_status",
          "fold_id|sample_id","",CGPI_SEVERITY_CRITICAL);

      Add(rows,"11","fold_metrics",cfg.phase11_fold_metrics_file,true,12,
          "report_name|fold_id|bucket_key|bucket_label|samples|wins|losses|stops|avg_r|win_rate|stop_rate|avg_mfe_r|avg_mae_r",
          "report_name|fold_id|bucket_key","",CGPI_SEVERITY_ERROR);

      Add(rows,"11","bucket_validation",cfg.phase11_bucket_validation_file,true,10,
          "fold_id|bucket_key|bucket_label|train_count|train_wins|train_losses|train_stops|train_avg_r|train_win_rate|train_stop_rate|edge_class",
          "fold_id|bucket_key","",CGPI_SEVERITY_ERROR);

      Add(rows,"11","experiment_summary",cfg.phase11_experiment_summary_file,true,2,
          "metric|value","metric","",CGPI_SEVERITY_ERROR);

      return ArraySize(rows);
   }
};

#endif
//+------------------------------------------------------------------+
