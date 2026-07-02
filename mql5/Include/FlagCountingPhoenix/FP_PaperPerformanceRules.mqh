#ifndef __FP_PAPER_PERFORMANCE_RULES_MQH__
#define __FP_PAPER_PERFORMANCE_RULES_MQH__
#property strict

#include "FP_PaperPerformanceTypes.mqh"
#include "FP_PaperLifecycleRules.mqh"

string FP_L23Bool(const bool v){ return (v ? "true" : "false"); }
string FP_L23Time(const datetime t){ if(t <= 0) return ""; return TimeToString(t, TIME_DATE|TIME_SECONDS); }
string FP_L23SafeCsv(string v){ StringReplace(v, "\"", "\"\""); return "\"" + v + "\""; }
string FP_L23TfLabel(const ENUM_TIMEFRAMES tf){ return EnumToString(tf); }

string FP_L23OutcomeClass(const FP_Level22PaperLifecycleRow &life)
{
   if(StringFind(life.lifecycle_status, "BLOCKED") >= 0)
      return "OUTCOME_BLOCKED";
   if(life.lifecycle_status == "PAPER_LIFECYCLE_HIT_TARGET_BY_CLOSE")
      return "OUTCOME_TARGET";
   if(life.lifecycle_status == "PAPER_LIFECYCLE_HIT_STOP_BY_CLOSE")
      return "OUTCOME_STOP";
   if(life.lifecycle_status == "PAPER_LIFECYCLE_AMBIGUOUS_TARGET_AND_STOP_SAME_CLOSE")
      return "OUTCOME_AMBIGUOUS";
   if(life.lifecycle_status == "PAPER_LIFECYCLE_EXPIRED_BEFORE_ENTRY")
      return "OUTCOME_EXPIRED_BEFORE_ENTRY";
   if(life.lifecycle_status == "PAPER_LIFECYCLE_EXPIRED_AFTER_ENTRY")
      return "OUTCOME_EXPIRED_AFTER_ENTRY";
   if(life.lifecycle_status == "PAPER_LIFECYCLE_OPEN_CLOSE_ONLY")
      return "OUTCOME_OPEN";
   if(life.lifecycle_status == "PAPER_LIFECYCLE_PENDING")
      return "OUTCOME_PENDING";
   if(life.lifecycle_status == "PAPER_LIFECYCLE_ENTERED_BY_CLOSE")
      return "OUTCOME_ENTERED_OPEN";
   return "OUTCOME_OTHER";
}

bool FP_L23OutcomeIsBlocked(const string outcome_class)
{
   return (outcome_class == "OUTCOME_BLOCKED");
}

bool FP_L23OutcomeIsOpen(const string outcome_class)
{
   return (outcome_class == "OUTCOME_OPEN" ||
           outcome_class == "OUTCOME_PENDING" ||
           outcome_class == "OUTCOME_ENTERED_OPEN");
}

bool FP_L23OutcomeIsResolved(const string outcome_class,
                             const FP_Level23PaperPerformanceConfig &cfg)
{
   if(outcome_class == "OUTCOME_TARGET" ||
      outcome_class == "OUTCOME_STOP" ||
      outcome_class == "OUTCOME_AMBIGUOUS")
      return true;

   if(cfg.count_expired_as_resolved &&
      (outcome_class == "OUTCOME_EXPIRED_BEFORE_ENTRY" ||
       outcome_class == "OUTCOME_EXPIRED_AFTER_ENTRY"))
      return true;

   return false;
}

string FP_L23BuildSampleKey(const FP_Level22PaperLifecycleRow &life)
{
   string key = life.lifecycle_id;
   key += "|STATUS=" + life.lifecycle_status;
   key += "|ENTRY_TIME=" + FP_L23Time(life.entry_time);
   key += "|EXIT_TIME=" + FP_L23Time(life.exit_time);
   key += "|EXIT_CLOSE=" + DoubleToString(life.exit_close, _Digits);
   key += "|R=" + DoubleToString(life.realized_r_like, 4);
   return key;
}

#endif // __FP_PAPER_PERFORMANCE_RULES_MQH__
