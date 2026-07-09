//+------------------------------------------------------------------+
//| CGRK_Types.mqh                                                   |
//| Phase 09 — Ranking types                                         |
//+------------------------------------------------------------------+
#property strict

#ifndef __CGRK_TYPES_MQH__
#define __CGRK_TYPES_MQH__

enum ECGRKReportKind
{
   CGRK_REPORT_OVERALL = 0,
   CGRK_REPORT_BY_CG = 1,
   CGRK_REPORT_BY_DIRECTION = 2,
   CGRK_REPORT_BY_CG_DIRECTION = 3,
   CGRK_REPORT_BY_ROLE = 4,
   CGRK_REPORT_BY_CG_DIRECTION_ROLE = 5,
   CGRK_REPORT_RED_FLAGS = 6,
   CGRK_REPORT_UNKNOWN = 99
};

struct SCGRKConfig
{
   bool   run_on_init;
   bool   show_dashboard_comment;
   bool   print_summary;

   string phase08_overall_file;
   string phase08_by_cg_file;
   string phase08_by_direction_file;
   string phase08_by_cg_direction_file;
   string phase08_by_role_file;
   string phase08_by_cg_direction_role_file;
   string phase08_red_flags_file;

   bool   read_overall;
   bool   read_by_cg;
   bool   read_by_direction;
   bool   read_by_cg_direction;
   bool   read_by_role;
   bool   read_by_cg_direction_role;
   bool   read_red_flags;

   int    minimum_sample_for_ranking;
   int    minimum_sample_for_shortlist;
   double minimum_quality_score_for_shortlist;
   double minimum_win_rate_for_shortlist;
   double minimum_average_r_for_shortlist;
   int    maximum_stop_streak_for_shortlist;

   double weight_win_rate;
   double weight_average_r;
   double weight_normalized_outcome;
   double weight_safety;
   double weight_sample_confidence;

   string output_all_ranking_file;
   string output_top_ranking_file;
   string output_bottom_ranking_file;
   string output_shortlist_file;
   string output_dashboard_html_file;
   string output_diagnostics_file;

   int    top_rows;
   int    bottom_rows;
   bool   write_html_dashboard;
   bool   write_csv_outputs;
};

struct SCGRKReportRow
{
   bool   valid;
   bool   eligible_for_ranking;
   bool   eligible_for_shortlist;

   ECGRKReportKind report_kind;
   string report_name;
   string bucket_key;
   string bucket_label;

   int    sample_count;
   int    win_count;
   int    loss_count;
   int    zero_count;
   int    stop_count;
   int    max_stop_streak;

   double win_rate_percent;
   double stop_rate_percent;
   double avg_r;
   double avg_points;
   double avg_normalized;
   double avg_mfe_r;
   double avg_mae_r;
   double avg_stop_distance_points;
   double max_r;
   double min_r;
   double max_points;
   double min_points;

   double sample_confidence_score;
   double win_rate_score;
   double expectancy_score;
   double normalized_score;
   double safety_score;
   double quality_score;
   double opportunity_score;
   double stability_score;

   string grade;
   string red_flag_text;
   string recommendation_text;
};

string CGRK_ReportKindToString(const ECGRKReportKind kind)
{
   if(kind == CGRK_REPORT_OVERALL) return "overall";
   if(kind == CGRK_REPORT_BY_CG) return "by_cg";
   if(kind == CGRK_REPORT_BY_DIRECTION) return "by_direction";
   if(kind == CGRK_REPORT_BY_CG_DIRECTION) return "by_cg_direction";
   if(kind == CGRK_REPORT_BY_ROLE) return "by_role";
   if(kind == CGRK_REPORT_BY_CG_DIRECTION_ROLE) return "by_cg_direction_role";
   if(kind == CGRK_REPORT_RED_FLAGS) return "red_flags";
   return "unknown";
}

string CGRK_Clean(const string value)
{
   string out = value;
   StringReplace(out, "\r", "");
   StringReplace(out, "\n", "");
   StringReplace(out, "\t", " ");
   while(StringLen(out) > 0 && StringGetCharacter(out, 0) == ' ')
      out = StringSubstr(out, 1);
   while(StringLen(out) > 0 && StringGetCharacter(out, StringLen(out)-1) == ' ')
      out = StringSubstr(out, 0, StringLen(out)-1);
   return out;
}

double CGRK_Clamp(const double value, const double min_value, const double max_value)
{
   if(value < min_value) return min_value;
   if(value > max_value) return max_value;
   return value;
}

string CGRK_CsvEscape(string value)
{
   StringReplace(value, "\"", "'");
   StringReplace(value, "\r", " ");
   StringReplace(value, "\n", " ");
   if(StringFind(value, ",") >= 0)
      return "\"" + value + "\"";
   return value;
}

#endif
