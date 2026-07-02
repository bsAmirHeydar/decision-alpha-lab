#ifndef __FP_SAFETY_GATE_RULES_MQH__
#define __FP_SAFETY_GATE_RULES_MQH__
#property strict

#include "FP_SafetyGateTypes.mqh"
#include "FP_PaperPerformanceEngine.mqh"

string FP_L24Bool(const bool v){ return (v ? "true" : "false"); }
string FP_L24Time(const datetime t){ if(t <= 0) return ""; return TimeToString(t, TIME_DATE|TIME_SECONDS); }
string FP_L24SafeCsv(string v){ StringReplace(v, "\"", "\"\""); return "\"" + v + "\""; }
string FP_L24TfLabel(const ENUM_TIMEFRAMES tf){ return EnumToString(tf); }

bool FP_L24WildcardOrEmpty(const string v)
{
   string x = v;
   StringTrimLeft(x);
   StringTrimRight(x);
   return (StringLen(x) <= 0 || x == "*");
}

bool FP_L24TokenAllowed(const string token,const string list)
{
   if(FP_L24WildcardOrEmpty(list))
      return true;

   string cleaned = list;
   StringReplace(cleaned, ";", ",");
   StringReplace(cleaned, "|", ",");
   StringReplace(cleaned, " ", ",");

   string parts[];
   int n = StringSplit(cleaned, ',', parts);
   for(int i=0; i<n; i++)
   {
      string p = parts[i];
      StringTrimLeft(p);
      StringTrimRight(p);
      if(StringLen(p) <= 0)
         continue;
      if(p == token)
         return true;
   }

   return false;
}

bool FP_L24SymbolAllowed(const string symbol,const string allowed_symbols)
{
   return FP_L24TokenAllowed(symbol, allowed_symbols);
}

bool FP_L24TimeframeAllowed(const ENUM_TIMEFRAMES period,const string allowed_timeframes)
{
   string tf = EnumToString(period);
   return FP_L24TokenAllowed(tf, allowed_timeframes);
}

bool FP_L24SpreadOk(const string symbol,const int max_spread_points,int &current_spread_points)
{
   current_spread_points = (int)SymbolInfoInteger(symbol, SYMBOL_SPREAD);
   if(max_spread_points <= 0)
      return true;
   return (current_spread_points <= max_spread_points);
}

bool FP_L24PerformanceOk(const FP_Level24SafetyGateConfig &cfg)
{
   if(g_fp_l23_resolved_count < cfg.min_resolved_samples)
      return false;

   double hit_rate = 0.0;
   double avg_r = 0.0;

   if(g_fp_l23_resolved_count > 0)
   {
      hit_rate = (double)g_fp_l23_target_count / (double)g_fp_l23_resolved_count;
      avg_r = g_fp_l23_sum_r_like / (double)g_fp_l23_resolved_count;
   }

   if(hit_rate < cfg.min_hit_rate_like)
      return false;
   if(avg_r < cfg.min_avg_r_like)
      return false;

   return true;
}

string FP_L24FirstBlockReason(const FP_Level24SafetyGateConfig &cfg,
                              const FP_Level24SafetyGateRow &row)
{
   if(cfg.require_license_ok && !row.license_ok)
      return "BLOCK_LICENSE_NOT_OK";
   if(cfg.require_symbol_allowed && !row.symbol_allowed)
      return "BLOCK_SYMBOL_NOT_ALLOWED";
   if(cfg.require_timeframe_allowed && !row.timeframe_allowed)
      return "BLOCK_TIMEFRAME_NOT_ALLOWED";
   if(cfg.require_spread_ok && !row.spread_ok)
      return "BLOCK_SPREAD_TOO_WIDE";
   if(cfg.require_performance_ok && !row.performance_ok)
      return "BLOCK_PAPER_PERFORMANCE_NOT_OK";
   if(cfg.require_manual_arm && !row.manual_arm_ok)
      return "BLOCK_MANUAL_ARM_OFF";
   if(cfg.require_real_execution_disabled && !row.real_execution_disabled_ok)
      return "BLOCK_REAL_EXECUTION_ENABLED_INSIDE_SAFETY_GATE";
   return "none";
}

void FP_L24BuildSafetyGateRow(const string symbol,
                              const ENUM_TIMEFRAMES period,
                              const bool license_ok,
                              const FP_Level24SafetyGateConfig &cfg,
                              FP_Level24SafetyGateRow &row)
{
   FP_ResetLevel24SafetyGateRow(row);

   row.generated_at = TimeCurrent();
   row.symbol = symbol;
   row.period = period;
   row.period_label = FP_L24TfLabel(period);
   row.attempted = cfg.enabled;

   row.license_ok = license_ok;
   row.symbol_allowed = FP_L24SymbolAllowed(symbol, cfg.allowed_symbols);
   row.timeframe_allowed = FP_L24TimeframeAllowed(period, cfg.allowed_timeframes);
   row.spread_ok = FP_L24SpreadOk(symbol, cfg.max_spread_points, row.current_spread_points);
   row.performance_ok = FP_L24PerformanceOk(cfg);
   row.manual_arm_ok = cfg.manual_arm;
   row.real_execution_disabled_ok = !cfg.real_execution_enabled;

   row.max_spread_points = cfg.max_spread_points;

   row.performance_sample_total = g_fp_l23_sample_total;
   row.performance_resolved_count = g_fp_l23_resolved_count;
   row.performance_target_count = g_fp_l23_target_count;
   row.performance_stop_count = g_fp_l23_stop_count;
   row.performance_best_r_like = g_fp_l23_best_r_like;
   row.performance_worst_r_like = g_fp_l23_worst_r_like;

   if(g_fp_l23_resolved_count > 0)
   {
      row.performance_hit_rate_like = (double)g_fp_l23_target_count / (double)g_fp_l23_resolved_count;
      row.performance_avg_r_like = g_fp_l23_sum_r_like / (double)g_fp_l23_resolved_count;
   }

   row.min_resolved_samples = cfg.min_resolved_samples;
   row.min_hit_rate_like = cfg.min_hit_rate_like;
   row.min_avg_r_like = cfg.min_avg_r_like;

   row.allowed_symbols = cfg.allowed_symbols;
   row.allowed_timeframes = cfg.allowed_timeframes;

   string first_block = FP_L24FirstBlockReason(cfg, row);
   row.gate_passed = (first_block == "none");

   if(row.gate_passed)
   {
      row.gate_status = "SAFETY_GATE_PASSED_RESEARCH_ONLY";
      row.gate_block_reason = "none";
      row.next_step = "NEXT_LEVEL_25_BROKER_DRY_RUN_ONLY";
   }
   else
   {
      row.gate_status = "SAFETY_GATE_BLOCKED";
      row.gate_block_reason = first_block;
      row.next_step = "NEXT_FIX_BLOCK_REASON_BEFORE_BROKER_DRY_RUN";
   }

   row.gate_key = row.symbol;
   row.gate_key += "|TF=" + row.period_label;
   row.gate_key += "|PASSED=" + FP_L24Bool(row.gate_passed);
   row.gate_key += "|BLOCK=" + row.gate_block_reason;
   row.gate_key += "|RESOLVED=" + IntegerToString(row.performance_resolved_count);
   row.gate_key += "|HIT_RATE=" + DoubleToString(row.performance_hit_rate_like, 2);
   row.gate_key += "|AVG_R=" + DoubleToString(row.performance_avg_r_like, 2);
   row.gate_key += "|EXEC=NO";
}

#endif // __FP_SAFETY_GATE_RULES_MQH__
