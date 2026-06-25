#ifndef __DAL_ASTRO_PURE_ASTROLOGY_SIGNALS_MQH__
#define __DAL_ASTRO_PURE_ASTROLOGY_SIGNALS_MQH__

#include <Research/DAL_AstroDoctrineContext.mqh>
#include <Research/DAL_AstroTimingDoctrine.mqh>

struct DAL_AstroPureSignal
{
   bool   valid;
   double long_bias_score;
   double short_bias_score;
   double trend_score;
   double path_score;
   double friction_score;
   double volatility_score;
   double natal_activation_score;
   double macro_timing_score;
   double meso_timing_score;
   double micro_timing_score;
   double minute_window_score;
   double minute_exhaustion_score;
   double benefic_support_score;
   double malefic_pressure_score;
   double angular_power_score;
   double house_lift_score;
   double house_drag_score;
   double entry_score;
   double exit_score;
   string regime_name;
   string direction_name;
   string sect_name;
   string macro_context;
   string meso_context;
   string micro_context;
   string minute_context;
   string doctrine_context;
   string trigger_state;
   string entry_signal;
   string exit_signal;
   string astro_language;
   string astro_trade_key;
};

double DAL_AstroPS_ElementImpulse(const string element)
{
   if(element == "fire") return 100.0;
   if(element == "air") return 75.0;
   if(element == "earth") return 40.0;
   if(element == "water") return 50.0;
   return 50.0;
}

double DAL_AstroPS_ModalityDrive(const string modality)
{
   if(modality == "cardinal") return 95.0;
   if(modality == "fixed") return 65.0;
   if(modality == "mutable") return 55.0;
   return 50.0;
}

double DAL_AstroPS_TightTransitNatalScore(const DAL_AstroMapRow &row, const string pair_name)
{
   for(int i = 0; i < DAL_ASTRO_TRANSIT_NATAL_ASPECT_COUNT; i++)
   {
      if(row.transit_natal_aspect[i].pair != pair_name)
         continue;
      if(row.transit_natal_aspect[i].aspect == "none" || row.transit_natal_aspect[i].orb > 6.0)
         return 0.0;
      double tightness = 100.0 * (1.0 - row.transit_natal_aspect[i].orb / 6.0);
      if(row.transit_natal_aspect[i].applying == 1)
         tightness *= 1.10;
      return MathMin(100.0, tightness);
   }
   return 0.0;
}

double DAL_AstroPS_DeclinationScore(const DAL_AstroDeclinationState &d, const double orb_limit)
{
   if(d.relation != "parallel" && d.relation != "contra_parallel")
      return 0.0;
   if(orb_limit <= 0.0 || d.orb > orb_limit)
      return 0.0;
   double tightness = 100.0 * (1.0 - d.orb / orb_limit);
   if(d.applying == 1)
      tightness *= 1.05;
   if(d.relation == "contra_parallel")
      tightness *= 0.95;
   return MathMin(100.0, tightness);
}

double DAL_AstroPS_FindTransitNatalDeclScore(const DAL_AstroMapRow &row, const string pair_name)
{
   for(int i = 0; i < DAL_ASTRO_TRANSIT_NATAL_DECL_COUNT; i++)
   {
      if(row.transit_natal_decl[i].pair == pair_name)
         return DAL_AstroPS_DeclinationScore(row.transit_natal_decl[i], row.parallel_orb_limit);
   }
   return 0.0;
}

void DAL_AstroPureSignal_Reset(DAL_AstroPureSignal &s)
{
   s.valid = false;
   s.long_bias_score = 0.0;
   s.short_bias_score = 0.0;
   s.trend_score = 0.0;
   s.path_score = 0.0;
   s.friction_score = 0.0;
   s.volatility_score = 0.0;
   s.natal_activation_score = 0.0;
   s.macro_timing_score = 0.0;
   s.meso_timing_score = 0.0;
   s.micro_timing_score = 0.0;
   s.minute_window_score = 0.0;
   s.minute_exhaustion_score = 0.0;
   s.benefic_support_score = 0.0;
   s.malefic_pressure_score = 0.0;
   s.angular_power_score = 0.0;
   s.house_lift_score = 0.0;
   s.house_drag_score = 0.0;
   s.entry_score = 0.0;
   s.exit_score = 0.0;
   s.regime_name = "neutral";
   s.direction_name = "flat";
   s.sect_name = "day";
   s.macro_context = "";
   s.meso_context = "";
   s.micro_context = "";
   s.minute_context = "";
   s.doctrine_context = "";
   s.trigger_state = "standby";
   s.entry_signal = "wait";
   s.exit_signal = "hold";
   s.astro_language = "";
   s.astro_trade_key = "";
}

bool DAL_AstroPureSignal_Calc(const DAL_AstroMapRow &row, DAL_AstroPureSignal &s)
{
   DAL_AstroPureSignal_Reset(s);

   DAL_AstroFractalMetrics f;
   if(!DAL_AstroFM_Calc(row, f) || !f.valid)
      return false;

   DAL_AstroTimingState t;
   if(!DAL_AstroTD_Calc(row, t) || !t.valid)
      return false;

   DAL_AstroDoctrineContext d;
   if(!DAL_AstroDC_Calc(row, d) || !d.valid)
      return false;

   int mars = DAL_AstroBodyIndexByName("mars");
   int jupiter = DAL_AstroBodyIndexByName("jupiter");
   int saturn = DAL_AstroBodyIndexByName("saturn");
   int moon = DAL_AstroBodyIndexByName("moon");
   if(mars < 0 || jupiter < 0 || saturn < 0 || moon < 0)
      return false;

   string mars_element = DAL_AstroDF_SignElement(row.body[mars].sign);
   string moon_element = DAL_AstroDF_SignElement(row.body[moon].sign);
   string mars_modality = DAL_AstroDF_SignModality(row.body[mars].sign);

   s.long_bias_score =
      0.32 * f.mars_impulse +
      0.22 * f.jupiter_support +
      0.18 * f.moon_flow +
      0.18 * DAL_AstroPS_ElementImpulse(mars_element) +
      0.10 * DAL_AstroPS_ModalityDrive(mars_modality);

   s.short_bias_score =
      0.35 * f.saturn_resistance +
      0.25 * f.mars_saturn_friction +
      0.20 * f.moon_pressure +
      0.10 * (100.0 - f.jupiter_support) +
      0.10 * (moon_element == "water" ? 80.0 : 45.0);

   s.benefic_support_score = d.benefic_support_score;
   s.malefic_pressure_score = d.malefic_pressure_score;
   s.angular_power_score = d.angular_power_score;
   s.house_lift_score = d.house_lift_score;
   s.house_drag_score = d.house_drag_score;
   s.sect_name = d.sect_name;
   s.doctrine_context = d.context_key;

   s.long_bias_score += 0.12 * d.benefic_support_score + 0.10 * d.house_lift_score + 0.06 * d.angular_power_score;
   s.short_bias_score += 0.14 * d.malefic_pressure_score + 0.10 * d.house_drag_score + 0.04 * (100.0 - d.benefic_support_score);

   if(row.body[mars].oob == 1)
      s.long_bias_score += 4.0;
   if(row.body[saturn].oob == 1)
      s.short_bias_score += 4.0;

   s.trend_score = MathMin(100.0, MathAbs(s.long_bias_score - s.short_bias_score));
   s.path_score = f.clean_path;
   s.friction_score = MathMin(100.0, f.chop_risk + 0.18 * d.malefic_pressure_score + 0.08 * d.house_drag_score);
   s.volatility_score = (f.breakout_followthrough + f.raw_pressure + f.raw_transition) / 3.0;

   for(int d = 0; d < DAL_ASTRO_DECL_PAIR_COUNT; d++)
   {
      if(row.decl_pair[d].pair == "mars_saturn")
         s.friction_score += 0.25 * DAL_AstroPS_DeclinationScore(row.decl_pair[d], row.parallel_orb_limit);
      if(row.decl_pair[d].pair == "jupiter_saturn")
         s.path_score += 0.20 * DAL_AstroPS_DeclinationScore(row.decl_pair[d], row.parallel_orb_limit);
      if(row.decl_pair[d].pair == "sun_moon")
         s.volatility_score += 0.15 * DAL_AstroPS_DeclinationScore(row.decl_pair[d], row.parallel_orb_limit);
   }
   s.path_score = MathMin(100.0, s.path_score);
   s.friction_score = MathMin(100.0, s.friction_score);
   s.volatility_score = MathMin(100.0, s.volatility_score);

   if(row.natal_enabled)
   {
      s.natal_activation_score =
         0.35 * DAL_AstroPS_TightTransitNatalScore(row, "t_sun__n_sun") +
         0.10 * DAL_AstroPS_FindTransitNatalDeclScore(row, "t_sun__n_sun") +
         0.25 * DAL_AstroPS_TightTransitNatalScore(row, "t_moon__n_moon") +
         0.10 * DAL_AstroPS_FindTransitNatalDeclScore(row, "t_moon__n_moon") +
         0.20 * DAL_AstroPS_TightTransitNatalScore(row, "t_mars__n_saturn") +
         0.10 * DAL_AstroPS_FindTransitNatalDeclScore(row, "t_mars__n_saturn") +
         0.20 * DAL_AstroPS_TightTransitNatalScore(row, "t_jupiter__n_mars");
   }

   s.macro_timing_score = t.macro_alignment_score;
   s.meso_timing_score = t.meso_gate_score;
   s.micro_timing_score = t.micro_trigger_score;
   s.minute_window_score = t.minute_window_score;
   s.minute_exhaustion_score = t.minute_exhaustion_score;
   s.macro_context = t.macro_context;
   s.meso_context = t.meso_context;
   s.micro_context = t.micro_context;
   s.minute_context = t.minute_context;
   s.trigger_state = t.trigger_state;

   s.entry_score =
      0.24 * MathMax(s.long_bias_score, s.short_bias_score) +
      0.08 * s.benefic_support_score +
      0.18 * s.path_score +
      0.12 * s.volatility_score +
      0.14 * s.natal_activation_score +
      0.12 * s.macro_timing_score +
      0.10 * s.meso_timing_score +
      0.10 * s.micro_timing_score +
      0.08 * s.house_lift_score;

   s.exit_score =
      0.30 * s.friction_score +
      0.10 * s.malefic_pressure_score +
      0.22 * f.pullback_risk +
      0.16 * f.m1_dirty_window +
      0.16 * s.minute_exhaustion_score +
      0.06 * s.house_drag_score +
      0.08 * (100.0 - s.minute_window_score);

   if(t.macro_direction != "flat")
      s.direction_name = t.macro_direction;
   else if(s.long_bias_score >= s.short_bias_score + 8.0)
      s.direction_name = "long";
   else if(s.short_bias_score >= s.long_bias_score + 8.0)
      s.direction_name = "short";
   else
      s.direction_name = "flat";

   if(s.path_score >= 70.0 && s.friction_score <= 40.0 && s.minute_window_score >= 60.0)
      s.regime_name = "clean";
   else if(s.volatility_score >= 70.0 && s.micro_timing_score >= 56.0)
      s.regime_name = "volatile";
   else if(s.friction_score >= 65.0 || s.minute_exhaustion_score >= 62.0)
      s.regime_name = "frictional";
   else
      s.regime_name = "mixed";

   if(s.direction_name == "long" && s.entry_score >= 66.0 && t.trigger_state == "trigger_ready")
      s.entry_signal = "enter_long";
   else if(s.direction_name == "short" && s.entry_score >= 66.0 && t.trigger_state == "trigger_ready")
      s.entry_signal = "enter_short";
   else if(t.trigger_state == "armed")
      s.entry_signal = "arm";
   else
      s.entry_signal = "wait";

   if(t.trigger_state == "timing_exit" || s.exit_score >= 58.0)
      s.exit_signal = "exit_or_reduce";
   else
      s.exit_signal = "hold";

   s.astro_language =
      "doctrine=" + row.doctrine_id +
      "|schema=" + row.schema_version +
      "|bias=" + row.astro_bias_text +
      "|path=" + row.astro_path_text +
      "|signal=" + row.astro_signal_text +
      "|sect=" + s.sect_name +
      "|dir=" + s.direction_name +
      "|regime=" + s.regime_name +
      "|ctx=" + s.doctrine_context +
      "|macro=" + s.macro_context +
      "|meso=" + s.meso_context +
      "|micro=" + s.micro_context +
      "|minute=" + s.minute_context;

   s.astro_trade_key =
      "astro_trade{dir=" + s.direction_name +
      "|entry=" + s.entry_signal +
      "|exit=" + s.exit_signal +
      "|regime=" + s.regime_name + "}";

   s.valid = true;
   return true;
}

string DAL_AstroPureSignal_ToText(const DAL_AstroMapRow &row, const DAL_AstroPureSignal &s)
{
   string t = "ASTRO PURE SIGNAL STACK\n";
   t += "Broker: " + TimeToString(row.broker_time, TIME_DATE | TIME_MINUTES) + "\n";
   t += "Direction: " + s.direction_name + " | Regime: " + s.regime_name + "\n";
   t += "Entry: " + s.entry_signal + " | Exit: " + s.exit_signal + "\n";
   t += "LongBias=" + DoubleToString(s.long_bias_score, 1) + " ShortBias=" + DoubleToString(s.short_bias_score, 1) + "\n";
   t += "Trend=" + DoubleToString(s.trend_score, 1) + " Path=" + DoubleToString(s.path_score, 1) + " Friction=" + DoubleToString(s.friction_score, 1) + "\n";
   t += "Volatility=" + DoubleToString(s.volatility_score, 1) + " NatalActivation=" + DoubleToString(s.natal_activation_score, 1) + "\n";
   t += "Sect=" + s.sect_name + " Benefic=" + DoubleToString(s.benefic_support_score, 1) + " Malefic=" + DoubleToString(s.malefic_pressure_score, 1) + "\n";
   t += "Angular=" + DoubleToString(s.angular_power_score, 1) + " HouseLift=" + DoubleToString(s.house_lift_score, 1) + " HouseDrag=" + DoubleToString(s.house_drag_score, 1) + "\n";
   t += "Macro=" + DoubleToString(s.macro_timing_score, 1) + " Meso=" + DoubleToString(s.meso_timing_score, 1) + " Micro=" + DoubleToString(s.micro_timing_score, 1) + "\n";
   t += "MinuteWindow=" + DoubleToString(s.minute_window_score, 1) + " MinuteExhaustion=" + DoubleToString(s.minute_exhaustion_score, 1) + " State=" + s.trigger_state + "\n";
   t += "BiasText=" + row.astro_bias_text + "\n";
   t += "PathText=" + row.astro_path_text + "\n";
   t += "SignalText=" + row.astro_signal_text + "\n";
   t += s.astro_trade_key;
   return t;
}

#endif
