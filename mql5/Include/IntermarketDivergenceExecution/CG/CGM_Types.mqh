//+------------------------------------------------------------------+
//| CGM_Types.mqh                                                    |
//| Phase 10 — Model dataset types and utilities                     |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGM_TYPES_MQH__
#define __CGM_TYPES_MQH__

enum ECGMLabelWindow
{
   CGM_LABEL_CYCLE_END = 0,
   CGM_LABEL_PLUS_1_CYCLE = 1,
   CGM_LABEL_PLUS_2_CYCLE = 2,
   CGM_LABEL_PLUS_3_CYCLE = 3,
   CGM_LABEL_DAY_END = 4,
   CGM_LABEL_MFE = 5
};

struct SCGMConfig
{
   bool   run_on_init;
   bool   show_chart_comment;
   bool   print_summary;

   string phase07_outcome_file;
   string phase09_all_ranking_file;
   string phase09_shortlist_file;
   bool   use_phase09_ranking_enrichment;
   bool   use_phase09_shortlist_enrichment;

   ECGMLabelWindow primary_label_window;
   double win_threshold_r;
   double loss_threshold_r;
   double one_r_threshold;
   double adverse_one_r_threshold;
   bool   require_complete_outcome;
   bool   skip_zero_risk_rows;
   int    max_rows_to_write;

   string output_dataset_file;
   string output_feature_dictionary_file;
   string output_label_summary_file;
   string output_diagnostics_file;
   bool   write_feature_dictionary;
   bool   write_label_summary;
   bool   write_diagnostics;
   bool   clear_outputs_on_run;
};

struct SCGMOutcomeSample
{
   bool   valid;
   string outcome_id;
   string signal_id;
   string availability;
   string availability_note;
   string group_name;
   int    group_minutes;
   int    current_cycle;
   int    reference_cycle;
   string direction;
   string side;
   string clean_symbol;
   string hunter_symbol;
   string role_key;
   string confirmation_broker;
   string confirmation_ny;
   string entry_broker;
   double entry_price;
   double stop_price;
   double stop_points;
   string cycle_end_broker;
   double cycle_end_price;
   double cycle_end_points;
   double cycle_end_r;
   bool   cycle_stop_hit;
   double plus1_points;
   double plus1_r;
   double plus2_points;
   double plus2_r;
   double plus3_points;
   double plus3_r;
   double day_end_points;
   double day_end_r;
   double mfe_points;
   double mfe_r;
   double mae_points;
   double mae_r;
   bool   stop_hit_intraday;
   string stop_hit_time;
   double daily_range_points;
   double day_end_norm_daily_range;
   double mfe_norm_daily_range;
   string note;
};

struct SCGMRankRow
{
   bool   valid;
   int    rank;
   string report_name;
   string bucket_key;
   string bucket_label;
   int    sample_count;
   double win_rate_percent;
   double avg_r;
   double avg_points;
   double avg_normalized;
   double stop_rate_percent;
   int    max_stop_streak;
   double quality_score;
   string grade;
   double sample_confidence_score;
   bool   shortlist;
   string red_flags;
   string recommendation;
};

struct SCGMFeatureRow
{
   bool   valid;
   string model_use_status;
   string exclusion_reason;
   string sample_id;
   string outcome_id;
   string signal_id;
   string availability;
   string group_name;
   int    group_minutes;
   int    current_cycle;
   int    reference_cycle;
   int    reference_age_cycles;
   string direction;
   int    direction_code;
   string side;
   int    side_code;
   string clean_symbol;
   string hunter_symbol;
   string role_key;
   string confirmation_broker;
   string confirmation_ny;
   int    hour_ny;
   int    minute_of_day_ny;
   string session_ny;
   double entry_price;
   double stop_price;
   double stop_points;
   double daily_range_points;
   double risk_to_daily_range;
   double cycle_end_r;
   double plus1_r;
   double plus2_r;
   double plus3_r;
   double day_end_r;
   double mfe_r;
   double mae_r;
   double cycle_end_points;
   double plus1_points;
   double plus2_points;
   double plus3_points;
   double day_end_points;
   double mfe_points;
   double mae_points;
   string primary_window;
   double primary_r;
   double primary_points;
   double primary_norm_daily_range;
   string label_class;
   int    label_binary_win;
   int    label_hit_1r;
   int    label_stopped_intraday;
   int    label_adverse_1r;
   double cg_quality_score;
   int    cg_rank;
   double cg_direction_quality_score;
   int    cg_direction_rank;
   double role_quality_score;
   int    role_rank;
   double cg_direction_role_quality_score;
   int    cg_direction_role_rank;
   int    shortlist_match;
   string notes;
};

struct SCGMSummary
{
   int outcomes_loaded;
   int rank_rows_loaded;
   int shortlist_rows_loaded;
   int rows_written;
   int rows_excluded;
   int complete_rows;
   int win_rows;
   int loss_rows;
   int flat_rows;
   int hit_1r_rows;
   int stopped_rows;
   int adverse_1r_rows;
   int shortlist_matches;
   double avg_primary_r;
};

string CGM_Clean(const string v)
{
   string out = v;
   StringTrimLeft(out);
   StringTrimRight(out);
   if(StringLen(out) >= 2 && StringSubstr(out,0,1) == "\"" && StringSubstr(out,StringLen(out)-1,1) == "\"")
      out = StringSubstr(out,1,StringLen(out)-2);
   return out;
}

string CGM_CsvEscape(const string value)
{
   string v = value;
   StringReplace(v, "\"", "\"\"");
   if(StringFind(v, ",") >= 0 || StringFind(v, "\"") >= 0 || StringFind(v, "\n") >= 0 || StringFind(v, "\r") >= 0)
      return "\"" + v + "\"";
   return v;
}

double CGM_SafeDiv(const double a,const double b)
{
   if(MathAbs(b) < 0.0000000001)
      return 0.0;
   return a / b;
}

bool CGM_ToBool(const string v)
{
   string x = StringToLower(CGM_Clean(v));
   return (x == "true" || x == "1" || x == "yes");
}

string CGM_BoolText(const bool v)
{
   return v ? "true" : "false";
}

string CGM_LabelWindowText(const ECGMLabelWindow w)
{
   if(w == CGM_LABEL_CYCLE_END) return "cycle_end";
   if(w == CGM_LABEL_PLUS_1_CYCLE) return "plus1_cycle";
   if(w == CGM_LABEL_PLUS_2_CYCLE) return "plus2_cycle";
   if(w == CGM_LABEL_PLUS_3_CYCLE) return "plus3_cycle";
   if(w == CGM_LABEL_DAY_END) return "day_end";
   if(w == CGM_LABEL_MFE) return "mfe";
   return "unknown";
}

int CGM_DirectionCode(const string direction)
{
   string d = StringToUpper(CGM_Clean(direction));
   if(d == "BUY") return 1;
   if(d == "SELL") return -1;
   return 0;
}

int CGM_SideCode(const string side)
{
   string s = StringToUpper(CGM_Clean(side));
   if(s == "LOW") return 1;
   if(s == "HIGH") return -1;
   return 0;
}

int CGM_HourFromText(const string time_text)
{
   datetime t = StringToTime(CGM_Clean(time_text));
   if(t <= 0) return -1;
   MqlDateTime dt;
   TimeToStruct(t, dt);
   return dt.hour;
}

int CGM_MinuteOfDayFromText(const string time_text)
{
   datetime t = StringToTime(CGM_Clean(time_text));
   if(t <= 0) return -1;
   MqlDateTime dt;
   TimeToStruct(t, dt);
   return dt.hour * 60 + dt.min;
}

string CGM_SessionFromNyMinute(const int minute_of_day)
{
   if(minute_of_day < 0) return "unknown";
   if(minute_of_day >= 18*60 || minute_of_day < 2*60) return "ny_evening_asia_early";
   if(minute_of_day >= 2*60 && minute_of_day < 8*60) return "london_pre_ny";
   if(minute_of_day >= 8*60 && minute_of_day < 9*60+30) return "pre_cash";
   if(minute_of_day >= 9*60+30 && minute_of_day < 16*60) return "us_cash";
   if(minute_of_day >= 16*60 && minute_of_day < 17*60) return "post_cash_settlement";
   return "pre_rollover";
}

#endif
