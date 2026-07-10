//+------------------------------------------------------------------+
//| CGWF_Types.mqh                                                   |
//| Phase 11 — Walk-forward validation types and utilities           |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGWF_TYPES_MQH__
#define __CGWF_TYPES_MQH__

enum ECGWFKeyMode
{
   CGWF_KEY_CG = 0,
   CGWF_KEY_CG_DIRECTION = 1,
   CGWF_KEY_CG_DIRECTION_ROLE = 2,
   CGWF_KEY_ROLE = 3,
   CGWF_KEY_DIRECTION = 4
};

struct SCGWFConfig
{
   bool   run_on_init;
   bool   show_chart_comment;
   bool   print_summary;
   string phase10_dataset_file;
   string output_prefix;
   bool   clear_outputs_on_run;

   bool   use_only_model_ready_rows;
   int    max_dataset_rows_to_read;
   int    minimum_train_rows;
   int    minimum_test_rows;

   int    train_days;
   int    test_days;
   int    step_days;
   int    embargo_days;

   ECGWFKeyMode primary_bucket_key_mode;
   double positive_edge_threshold_r;
   double weak_edge_threshold_r;
   int    minimum_bucket_train_rows;
   bool   allow_global_fallback;

   bool   write_fold_plan;
   bool   write_predictions;
   bool   write_fold_metrics;
   bool   write_bucket_validation;
   bool   write_experiment_summary;
   bool   write_diagnostics;
};

struct SCGWFModelRow
{
   bool     valid;
   int      source_row_number;
   string   sample_id;
   string   outcome_id;
   string   signal_id;
   string   model_use_status;
   string   exclusion_reason;
   string   group_name;
   int      group_minutes;
   int      current_cycle;
   int      reference_cycle;
   int      reference_age_cycles;
   string   direction;
   int      direction_code;
   string   side;
   int      side_code;
   string   clean_symbol;
   string   hunter_symbol;
   string   role_key;
   string   confirmation_broker;
   string   confirmation_ny;
   datetime confirmation_time;
   int      hour_ny;
   int      minute_of_day_ny;
   string   session_ny;
   double   stop_points;
   double   daily_range_points;
   double   risk_to_daily_range;
   double   cycle_end_r;
   double   plus1_r;
   double   plus2_r;
   double   plus3_r;
   double   day_end_r;
   double   mfe_r;
   double   mae_r;
   double   primary_r;
   double   primary_points;
   double   primary_norm_daily_range;
   string   label_class;
   int      label_binary_win;
   int      label_hit_1r;
   int      label_stopped_intraday;
   int      label_adverse_1r;
   double   cg_quality_score;
   int      cg_rank;
   double   cg_direction_quality_score;
   int      cg_direction_rank;
   double   role_quality_score;
   int      role_rank;
   double   cg_direction_role_quality_score;
   int      cg_direction_role_rank;
   int      shortlist_match;
   string   notes;
};

struct SCGWFFold
{
   int      fold_id;
   datetime train_start;
   datetime train_end;
   datetime embargo_start;
   datetime embargo_end;
   datetime test_start;
   datetime test_end;
   int      train_count;
   int      test_count;
   bool     usable;
   string   status;
};

struct SCGWFBucketModel
{
   int    fold_id;
   string bucket_key;
   string bucket_label;
   int    train_count;
   int    train_wins;
   int    train_losses;
   int    train_stops;
   double train_sum_r;
   double train_avg_r;
   double train_win_rate;
   double train_stop_rate;
   double train_avg_mfe_r;
   double train_avg_mae_r;
   double train_sum_mfe_r;
   double train_sum_mae_r;
   string edge_class;
};

struct SCGWFPrediction
{
   int    fold_id;
   string sample_id;
   string signal_id;
   string group_name;
   string direction;
   string role_key;
   string bucket_key;
   string bucket_source;
   int    train_count_for_bucket;
   double predicted_avg_r;
   double predicted_win_rate;
   string predicted_edge_class;
   double actual_r;
   int    actual_win;
   int    actual_loss;
   int    actual_stop;
   double actual_mfe_r;
   double actual_mae_r;
   int    directional_agreement;
   string model_use_status;
};

struct SCGWFMetricRow
{
   string report_name;
   int    fold_id;
   string bucket_key;
   string bucket_label;
   int    samples;
   int    wins;
   int    losses;
   int    stops;
   double sum_r;
   double avg_r;
   double win_rate;
   double stop_rate;
   double avg_mfe_r;
   double avg_mae_r;
   double max_r;
   double min_r;
};

struct SCGWFSummary
{
   int rows_loaded;
   int rows_after_filter;
   int rows_rejected;
   int folds_built;
   int folds_usable;
   int predictions_written;
   int bucket_models_built;
   double oos_avg_r;
   double oos_win_rate;
   double oos_stop_rate;
   string status;
};

string CGWF_Clean(const string v)
{
   string x = v;
   StringTrimLeft(x);
   StringTrimRight(x);
   return x;
}

string CGWF_CsvEscape(const string value)
{
   string v = value;
   bool needs = (StringFind(v, ",") >= 0 || StringFind(v, "\"") >= 0 || StringFind(v, "\n") >= 0 || StringFind(v, "\r") >= 0);
   StringReplace(v, "\"", "\"\"");
   if(needs) return "\"" + v + "\"";
   return v;
}

bool CGWF_ToBool(const string v)
{
   string x = CGWF_Clean(v);
   StringToLower(x);
   return (x == "1" || x == "true" || x == "yes" || x == "y");
}

string CGWF_Dt(const datetime t)
{
   if(t <= 0) return "";
   return TimeToString(t, TIME_DATE|TIME_MINUTES);
}

datetime CGWF_ParseTime(const string primary, const string fallback)
{
   datetime t = StringToTime(CGWF_Clean(primary));
   if(t <= 0) t = StringToTime(CGWF_Clean(fallback));
   return t;
}

string CGWF_KeyModeToString(const ECGWFKeyMode mode)
{
   if(mode == CGWF_KEY_CG) return "CG";
   if(mode == CGWF_KEY_CG_DIRECTION) return "CG_DIRECTION";
   if(mode == CGWF_KEY_CG_DIRECTION_ROLE) return "CG_DIRECTION_ROLE";
   if(mode == CGWF_KEY_ROLE) return "ROLE";
   if(mode == CGWF_KEY_DIRECTION) return "DIRECTION";
   return "UNKNOWN";
}

string CGWF_RowKey(const SCGWFModelRow &r, const ECGWFKeyMode mode)
{
   if(mode == CGWF_KEY_CG) return r.group_name;
   if(mode == CGWF_KEY_DIRECTION) return r.direction;
   if(mode == CGWF_KEY_ROLE) return r.role_key;
   if(mode == CGWF_KEY_CG_DIRECTION) return r.group_name + "|" + r.direction;
   if(mode == CGWF_KEY_CG_DIRECTION_ROLE) return r.group_name + "|" + r.direction + "|" + r.role_key;
   return "ALL";
}

string CGWF_RowLabel(const SCGWFModelRow &r, const ECGWFKeyMode mode)
{
   return CGWF_RowKey(r,mode);
}

string CGWF_EdgeClass(const double avg_r, const double positive_threshold, const double weak_threshold)
{
   if(avg_r >= positive_threshold) return "positive_research_edge";
   if(avg_r <= weak_threshold) return "weak_or_negative_research_edge";
   return "neutral_research_edge";
}

void CGWF_InitSummary(SCGWFSummary &s)
{
   s.rows_loaded = 0;
   s.rows_after_filter = 0;
   s.rows_rejected = 0;
   s.folds_built = 0;
   s.folds_usable = 0;
   s.predictions_written = 0;
   s.bucket_models_built = 0;
   s.oos_avg_r = 0.0;
   s.oos_win_rate = 0.0;
   s.oos_stop_rate = 0.0;
   s.status = "not_run";
}

#endif
