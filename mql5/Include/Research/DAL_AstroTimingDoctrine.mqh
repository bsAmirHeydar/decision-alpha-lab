#ifndef __DAL_ASTRO_TIMING_DOCTRINE_MQH__
#define __DAL_ASTRO_TIMING_DOCTRINE_MQH__

#include <Research/DAL_AstroFractalPathMetrics.mqh>

struct DAL_AstroTimingState
{
   bool   valid;
   double macro_bias_score;
   double macro_alignment_score;
   double meso_gate_score;
   double meso_angularity_score;
   double meso_resonance_score;
   double micro_trigger_score;
   double micro_release_score;
   double minute_window_score;
   double minute_exhaustion_score;
   string macro_direction;
   string macro_context;
   string meso_context;
   string micro_context;
   string minute_context;
   string trigger_state;
   string timing_stack;
};

void DAL_AstroTD_Reset(DAL_AstroTimingState &t)
{
   t.valid = false;
   t.macro_bias_score = 0.0;
   t.macro_alignment_score = 0.0;
   t.meso_gate_score = 0.0;
   t.meso_angularity_score = 0.0;
   t.meso_resonance_score = 0.0;
   t.micro_trigger_score = 0.0;
   t.micro_release_score = 0.0;
   t.minute_window_score = 0.0;
   t.minute_exhaustion_score = 0.0;
   t.macro_direction = "flat";
   t.macro_context = "";
   t.meso_context = "";
   t.micro_context = "";
   t.minute_context = "";
   t.trigger_state = "standby";
   t.timing_stack = "";
}

double DAL_AstroTD_Clamp(const double x)
{
   return DAL_AstroPM_Clamp(x);
}

double DAL_AstroTD_HouseAngularity(const int house)
{
   if(house == 1 || house == 10 || house == 7 || house == 4) return 100.0;
   if(house == 2 || house == 11 || house == 8 || house == 5) return 62.0;
   if(house == 3 || house == 12 || house == 9 || house == 6) return 32.0;
   return 0.0;
}

double DAL_AstroTD_BodyAngularity(const DAL_AstroBodyState &b)
{
   return DAL_AstroTD_HouseAngularity(b.house);
}

double DAL_AstroTD_FindDeclScore(const DAL_AstroMapRow &row, const string pair_name)
{
   for(int i = 0; i < DAL_ASTRO_DECL_PAIR_COUNT; i++)
   {
      if(row.decl_pair[i].pair != pair_name)
         continue;
      if(row.decl_pair[i].relation != "parallel" && row.decl_pair[i].relation != "contra_parallel")
         return 0.0;
      if(row.parallel_orb_limit <= 0.0 || row.decl_pair[i].orb > row.parallel_orb_limit)
         return 0.0;
      double tight = 100.0 * (1.0 - row.decl_pair[i].orb / row.parallel_orb_limit);
      if(row.decl_pair[i].applying == 1)
         tight *= 1.08;
      return MathMin(100.0, tight);
   }
   return 0.0;
}

double DAL_AstroTD_TransitNatalResonance(const DAL_AstroMapRow &row)
{
   if(!row.natal_enabled)
      return 0.0;

   double score = 0.0;
   for(int i = 0; i < DAL_ASTRO_NATAL_CORE_COUNT; i++)
      score += 0.08 * DAL_AstroTD_HouseAngularity(row.transit_in_natal_house[i]);

   for(int j = 0; j < DAL_ASTRO_TRANSIT_NATAL_ASPECT_COUNT; j++)
   {
      DAL_AstroAspectState a = row.transit_natal_aspect[j];
      if(a.aspect == "none" || a.orb > row.aspect_orb_limit)
         continue;
      double tight = 100.0 * (1.0 - a.orb / MathMax(0.0001, row.aspect_orb_limit));
      if(a.applying == 1)
         tight *= 1.05;
      score += 0.03 * MathMin(100.0, tight);
   }
   return DAL_AstroTD_Clamp(score);
}

bool DAL_AstroTD_Calc(const DAL_AstroMapRow &row, DAL_AstroTimingState &t)
{
   DAL_AstroTD_Reset(t);

   DAL_AstroFractalMetrics f;
   if(!DAL_AstroFM_Calc(row, f) || !f.valid)
      return false;

   int idx_sun = DAL_AstroBodyIndexByName("sun");
   int idx_moon = DAL_AstroBodyIndexByName("moon");
   int idx_mercury = DAL_AstroBodyIndexByName("mercury");
   int idx_mars = DAL_AstroBodyIndexByName("mars");
   int idx_jupiter = DAL_AstroBodyIndexByName("jupiter");
   int idx_saturn = DAL_AstroBodyIndexByName("saturn");
   if(idx_sun < 0 || idx_moon < 0 || idx_mercury < 0 || idx_mars < 0 || idx_jupiter < 0 || idx_saturn < 0)
      return false;

   DAL_AstroBodyState sun = row.body[idx_sun];
   DAL_AstroBodyState moon = row.body[idx_moon];
   DAL_AstroBodyState mercury = row.body[idx_mercury];
   DAL_AstroBodyState mars = row.body[idx_mars];
   DAL_AstroBodyState jupiter = row.body[idx_jupiter];
   DAL_AstroBodyState saturn = row.body[idx_saturn];

   double mars_ang = DAL_AstroTD_BodyAngularity(mars);
   double moon_ang = DAL_AstroTD_BodyAngularity(moon);
   double sun_ang = DAL_AstroTD_BodyAngularity(sun);
   double jupiter_ang = DAL_AstroTD_BodyAngularity(jupiter);
   double saturn_ang = DAL_AstroTD_BodyAngularity(saturn);

   double macro_long = 0.42 * f.macro_flow + 0.24 * f.macro_expansion + 0.20 * f.jupiter_support + 0.14 * (100.0 - f.macro_pressure);
   double macro_short = 0.38 * f.macro_drag + 0.28 * f.macro_pressure + 0.18 * f.macro_compression + 0.16 * f.saturn_resistance;
   t.macro_bias_score = DAL_AstroTD_Clamp(MathAbs(macro_long - macro_short));
   t.macro_alignment_score = DAL_AstroTD_Clamp(0.34 * (100.0 - f.macro_transition) + 0.24 * f.structural_bias + 0.22 * MathMax(mars_ang, sun_ang) + 0.20 * MathMax(jupiter_ang, saturn_ang));

   if(macro_long >= macro_short + 6.0)
      t.macro_direction = "long";
   else if(macro_short >= macro_long + 6.0)
      t.macro_direction = "short";
   else
      t.macro_direction = "flat";

   t.meso_angularity_score = DAL_AstroTD_Clamp(0.30 * mars_ang + 0.25 * moon_ang + 0.20 * sun_ang + 0.15 * jupiter_ang + 0.10 * saturn_ang);
   t.meso_resonance_score = DAL_AstroTD_Clamp(
      0.26 * DAL_AstroTD_TransitNatalResonance(row) +
      0.18 * DAL_AstroTD_FindDeclScore(row, "sun_moon") +
      0.18 * DAL_AstroTD_FindDeclScore(row, "venus_mars") +
      0.20 * DAL_AstroTD_FindDeclScore(row, "mars_saturn") +
      0.18 * DAL_AstroTD_FindDeclScore(row, "jupiter_saturn")
   );
   t.meso_gate_score = DAL_AstroTD_Clamp(0.42 * t.meso_angularity_score + 0.28 * t.meso_resonance_score + 0.15 * f.clean_path + 0.15 * (100.0 - f.chop_risk));

   t.micro_trigger_score = DAL_AstroTD_Clamp(
      0.26 * f.moon_tempo +
      0.24 * f.moon_flow +
      0.16 * (100.0 - f.moon_boundary) +
      0.18 * (100.0 - f.micro_noise) +
      0.16 * f.breakout_followthrough
   );
   t.micro_release_score = DAL_AstroTD_Clamp(
      0.28 * f.clean_impulse +
      0.20 * f.mars_clean_impulse +
      0.18 * f.venus_mars_cohesion +
      0.18 * (100.0 - f.pullback_risk) +
      0.16 * (100.0 - f.moon_drag)
   );

   double mercury_station = DAL_AstroFM_StationRisk(mercury);
   double minute_decl = DAL_AstroTD_FindDeclScore(row, "moon_mars");
   t.minute_window_score = DAL_AstroTD_Clamp(
      0.28 * t.micro_trigger_score +
      0.22 * t.micro_release_score +
      0.20 * f.m1_clean_window +
      0.12 * minute_decl +
      0.10 * (100.0 - mercury_station) +
      0.08 * (100.0 - f.m1_dirty_window)
   );
   t.minute_exhaustion_score = DAL_AstroTD_Clamp(
      0.26 * f.m1_dirty_window +
      0.22 * f.pullback_risk +
      0.20 * f.moon_boundary +
      0.16 * f.macro_transition +
      0.16 * mercury_station
   );

   t.macro_context = "macro:" + t.macro_direction +
      "|bias=" + DAL_AstroFM_Bucket(t.macro_bias_score) +
      "|align=" + DAL_AstroFM_Bucket(t.macro_alignment_score) +
      "|flow=" + DAL_AstroFM_Bucket(f.macro_flow) +
      "|pressure=" + DAL_AstroFM_Bucket(f.macro_pressure);

   t.meso_context = "meso:gate_" + DAL_AstroFM_Bucket(t.meso_gate_score) +
      "|angular=" + DAL_AstroFM_Bucket(t.meso_angularity_score) +
      "|resonance=" + DAL_AstroFM_Bucket(t.meso_resonance_score);

   t.micro_context = "micro:trigger_" + DAL_AstroFM_Bucket(t.micro_trigger_score) +
      "|release=" + DAL_AstroFM_Bucket(t.micro_release_score) +
      "|tempo=" + DAL_AstroFM_Bucket(f.moon_tempo) +
      "|noise=" + DAL_AstroFM_Bucket(f.micro_noise);

   t.minute_context = "minute:window_" + DAL_AstroFM_Bucket(t.minute_window_score) +
      "|exhaust=" + DAL_AstroFM_Bucket(t.minute_exhaustion_score) +
      "|m1clean=" + DAL_AstroFM_Bucket(f.m1_clean_window) +
      "|m1dirty=" + DAL_AstroFM_Bucket(f.m1_dirty_window);

   t.trigger_state = "standby";
   if(t.macro_direction != "flat" && t.macro_alignment_score >= 58.0 && t.meso_gate_score >= 54.0)
      t.trigger_state = "armed";
   if(t.macro_direction != "flat" && t.macro_alignment_score >= 62.0 && t.meso_gate_score >= 60.0 && t.minute_window_score >= 64.0 && t.minute_exhaustion_score <= 44.0)
      t.trigger_state = "trigger_ready";
   if(t.minute_exhaustion_score >= 62.0)
      t.trigger_state = "timing_exit";

   t.timing_stack = t.macro_context + "|" + t.meso_context + "|" + t.micro_context + "|" + t.minute_context + "|state=" + t.trigger_state;
   t.valid = true;
   return true;
}

string DAL_AstroTD_ToText(const DAL_AstroTimingState &t)
{
   if(!t.valid)
      return "ASTRO TIMING DOCTRINE INVALID";
   string txt = "ASTRO TIMING DOCTRINE\n";
   txt += "MacroDirection: " + t.macro_direction + "\n";
   txt += "MacroBias=" + DoubleToString(t.macro_bias_score, 1) + " MacroAlign=" + DoubleToString(t.macro_alignment_score, 1) + "\n";
   txt += "MesoGate=" + DoubleToString(t.meso_gate_score, 1) + " Angular=" + DoubleToString(t.meso_angularity_score, 1) + " Resonance=" + DoubleToString(t.meso_resonance_score, 1) + "\n";
   txt += "MicroTrigger=" + DoubleToString(t.micro_trigger_score, 1) + " Release=" + DoubleToString(t.micro_release_score, 1) + "\n";
   txt += "MinuteWindow=" + DoubleToString(t.minute_window_score, 1) + " Exhaustion=" + DoubleToString(t.minute_exhaustion_score, 1) + "\n";
   txt += "State=" + t.trigger_state + "\n";
   txt += t.timing_stack;
   return txt;
}

#endif
