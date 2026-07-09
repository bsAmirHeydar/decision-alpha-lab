//+------------------------------------------------------------------+
//| CGS_Types.mqh                                                    |
//| EXP0017 Phase 08 — Statistical Report Types                      |
//+------------------------------------------------------------------+
#ifndef __EXP0017_CGS_TYPES_MQH__
#define __EXP0017_CGS_TYPES_MQH__

#define CGS_EMPTY_VALUE 0.0

enum ECGSOutcomeWindow
{
   CGS_WINDOW_CYCLE_END = 0,
   CGS_WINDOW_PLUS_1_CYCLE = 1,
   CGS_WINDOW_PLUS_2_CYCLE = 2,
   CGS_WINDOW_PLUS_3_CYCLE = 3,
   CGS_WINDOW_DAY_END = 4,
   CGS_WINDOW_MFE = 5
};

struct SCGSReportConfig
{
   string            outcome_file;
   string            report_prefix;
   bool              use_common_files_folder;
   string            csv_delimiter;
   ECGSOutcomeWindow primary_window;
   int               minimum_sample_for_flag;
   double            bad_winrate_threshold_percent;
   double            bad_average_r_threshold;
   int               bad_stop_streak_threshold;
   bool              generate_overall;
   bool              generate_cg;
   bool              generate_direction;
   bool              generate_cg_direction;
   bool              generate_role;
   bool              generate_cg_direction_role;
   bool              generate_red_flags;
   bool              show_chart_comment;
   bool              print_summary;
   int               max_rows_to_read;
};

struct SCGSOutcomeSample
{
   string   signal_id;
   string   trading_day;
   string   confirmation_time;
   string   cg_name;
   string   direction;
   string   side;
   string   hunter_symbol;
   string   clean_symbol;
   string   role_key;

   double   stop_distance_points;

   double   cycle_end_points;
   double   cycle_end_r;
   double   plus1_points;
   double   plus1_r;
   double   plus2_points;
   double   plus2_r;
   double   plus3_points;
   double   plus3_r;
   double   day_end_points;
   double   day_end_r;

   double   mfe_points;
   double   mfe_r;
   double   mae_points;
   double   mae_r;

   bool     stop_hit;
   string   stop_hit_time;

   double   daily_range_points;
   double   day_end_normalized;
   double   mfe_normalized;

   bool     valid;
};

struct SCGSGroupStats
{
   string key;
   string dimension_name;

   int    sample_count;
   int    win_count;
   int    loss_count;
   int    zero_count;
   int    stop_count;

   double sum_r;
   double sum_points;
   double sum_norm;
   double sum_mfe_r;
   double sum_mae_r;
   double sum_stop_distance;

   double max_r;
   double min_r;
   double max_points;
   double min_points;

   int    current_stop_streak;
   int    max_stop_streak;
};

string CGS_WindowName(const ECGSOutcomeWindow window)
{
   if(window == CGS_WINDOW_CYCLE_END)      return "cycle_end";
   if(window == CGS_WINDOW_PLUS_1_CYCLE)   return "plus1_cycle";
   if(window == CGS_WINDOW_PLUS_2_CYCLE)   return "plus2_cycle";
   if(window == CGS_WINDOW_PLUS_3_CYCLE)   return "plus3_cycle";
   if(window == CGS_WINDOW_DAY_END)        return "day_end";
   if(window == CGS_WINDOW_MFE)            return "mfe";
   return "unknown";
}

string CGS_BoolText(const bool value)
{
   return value ? "true" : "false";
}

double CGS_SafeDiv(const double a,const double b)
{
   if(MathAbs(b) <= 0.0000000001)
      return 0.0;
   return a / b;
}

double CGS_StrToDoubleSafe(const string value)
{
   string v = value;
   StringTrimLeft(v);
   StringTrimRight(v);
   if(v == "" || v == "nan" || v == "NaN" || v == "NULL")
      return 0.0;
   return StringToDouble(v);
}

bool CGS_StrToBoolSafe(const string value)
{
   string v = value;
   StringToLower(v);
   StringTrimLeft(v);
   StringTrimRight(v);
   return (v == "true" || v == "1" || v == "yes" || v == "y");
}

string CGS_CsvEscape(string value)
{
   StringReplace(value, "\"", "\"\"");
   if(StringFind(value, ",") >= 0 || StringFind(value, "\"") >= 0 || StringFind(value, "\n") >= 0)
      return "\"" + value + "\"";
   return value;
}

#endif
