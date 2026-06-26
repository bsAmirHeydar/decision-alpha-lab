#ifndef __DAL_ASTRO_FINAL_DOCTRINE_MQH__
#define __DAL_ASTRO_FINAL_DOCTRINE_MQH__

#include <Research/DAL_AstroPureAstrologySignals.mqh>

struct DAL_AstroFinalProfile
{
   string profile_name;
   double min_entry_score;
   double min_macro_timing;
   double min_meso_timing;
   double min_micro_timing;
   double min_minute_window;
   double max_minute_exhaustion;
   double min_benefic_edge;
   double min_malefic_edge;
   double min_lift_edge;
   double min_drag_edge;
   double exit_threshold;
};

struct DAL_AstroFinalVerdict
{
   bool   valid;
   string profile_name;
   string direction_name;
   string purity_state;
   string final_decision;
   string veto_reason;
   double readiness_score;
   double exhaustion_guard;
};

void DAL_AstroFinalProfile_LoadStrictTuned(DAL_AstroFinalProfile &p)
{
   p.profile_name = "pure_strict_tuned";
   p.min_entry_score = 66.0;
   p.min_macro_timing = 60.0;
   p.min_meso_timing = 56.0;
   p.min_micro_timing = 54.0;
   p.min_minute_window = 61.0;
   p.max_minute_exhaustion = 55.0;
   p.min_benefic_edge = 4.0;
   p.min_malefic_edge = 4.0;
   p.min_lift_edge = 2.0;
   p.min_drag_edge = 2.0;
   p.exit_threshold = 58.0;
}

void DAL_AstroFinalVerdict_Reset(DAL_AstroFinalVerdict &v)
{
   v.valid = false;
   v.profile_name = "";
   v.direction_name = "flat";
   v.purity_state = "blocked";
   v.final_decision = "wait";
   v.veto_reason = "";
   v.readiness_score = 0.0;
   v.exhaustion_guard = 0.0;
}

bool DAL_AstroFinalVerdict_Calc(const DAL_AstroMapRow &row, const DAL_AstroPureSignal &s, DAL_AstroFinalVerdict &v)
{
   DAL_AstroFinalVerdict_Reset(v);
   if(!s.valid)
      return false;

   DAL_AstroFinalProfile p;
   DAL_AstroFinalProfile_LoadStrictTuned(p);

   v.valid = true;
   v.profile_name = p.profile_name;
   v.direction_name = s.direction_name;
   v.readiness_score =
      0.28 * s.entry_score +
      0.18 * s.macro_timing_score +
      0.14 * s.meso_timing_score +
      0.14 * s.micro_timing_score +
      0.14 * s.minute_window_score +
      0.12 * s.angular_power_score;
   v.exhaustion_guard = 100.0 - s.minute_exhaustion_score;

   if(s.trigger_state == "timing_exit" || s.exit_score >= p.exit_threshold)
   {
      v.purity_state = "exit";
      v.final_decision = "exit";
      return true;
   }

   if(s.direction_name == "flat")
   {
      v.veto_reason = "no_direction";
      return true;
   }
   if(s.entry_score < p.min_entry_score)
      v.veto_reason = "entry_score_low";
   else if(s.macro_timing_score < p.min_macro_timing)
      v.veto_reason = "macro_timing_low";
   else if(s.meso_timing_score < p.min_meso_timing)
      v.veto_reason = "meso_timing_low";
   else if(s.micro_timing_score < p.min_micro_timing)
      v.veto_reason = "micro_timing_low";
   else if(s.minute_window_score < p.min_minute_window)
      v.veto_reason = "minute_window_low";
   else if(s.minute_exhaustion_score > p.max_minute_exhaustion)
      v.veto_reason = "minute_exhaustion_high";
   else if(s.direction_name == "long" &&
           (s.benefic_support_score < s.malefic_pressure_score + p.min_benefic_edge ||
            s.house_lift_score < s.house_drag_score + p.min_lift_edge))
      v.veto_reason = "doctrine_long_mismatch";
   else if(s.direction_name == "short" &&
           (s.malefic_pressure_score < s.benefic_support_score + p.min_malefic_edge ||
            s.house_drag_score < s.house_lift_score + p.min_drag_edge))
      v.veto_reason = "doctrine_short_mismatch";

   if(v.veto_reason == "")
   {
      v.purity_state = "pure_entry";
      v.final_decision = (s.direction_name == "long" ? "enter_long" : "enter_short");
      return true;
   }

   bool probe_ready =
      (s.entry_score >= p.min_entry_score - 6.0 &&
       s.macro_timing_score >= p.min_macro_timing - 4.0 &&
       s.minute_window_score >= p.min_minute_window - 4.0 &&
       s.direction_name != "flat");

   if(probe_ready)
   {
      v.purity_state = "probe";
      v.final_decision = (s.direction_name == "long" ? "armed_long" : "armed_short");
   }
   return true;
}

#endif
