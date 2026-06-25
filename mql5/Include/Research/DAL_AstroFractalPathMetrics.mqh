#ifndef __DAL_ASTRO_FRACTAL_PATH_METRICS_MQH__
#define __DAL_ASTRO_FRACTAL_PATH_METRICS_MQH__

#include <Research/DAL_AstroPathCleanlinessMetrics.mqh>

// Decision Alpha Lab - Astro Fractal Path Metrics
// ------------------------------------------------
// This module expands EXP0013 from one compact raw-axis view into a fractal
// interpretation stack for M1 path-quality observation.
//
// It does NOT trade and does NOT predict direction.
// It decomposes the sky-map into multiple time-scale layers:
// - Macro layer: slow planets / broad background / structural drag.
// - Regime layer: Mars, Saturn, Jupiter, Mercury / active movement regime.
// - Lunar micro layer: Moon tempo, Moon pressure, Moon boundaries / M1 timing.
// - Path layer: compact market-path translation.
//
// All scores are normalized to 0..100 and are hypotheses for Distribution
// Engineering validation, not causal claims.

struct DAL_AstroFractalMetrics
{
   bool valid;
   datetime broker_time;
   datetime utc_time;

   // Existing Level 1 axes from DAL_AstroPathMetrics.
   double raw_flow;
   double raw_impulse;
   double raw_friction;
   double raw_pressure;
   double raw_transition;
   double raw_moon_tempo;
   double raw_saturn_drag;

   // Macro layer: slower bodies and broad background.
   double macro_flow;
   double macro_drag;
   double macro_pressure;
   double macro_transition;
   double macro_expansion;
   double macro_compression;
   double outer_station_risk;
   double structural_bias;

   // Regime layer: active regime for movement and noise.
   double mars_impulse;
   double mars_clean_impulse;
   double mars_saturn_friction;
   double mars_jupiter_expansion;
   double mercury_noise;
   double venus_mars_cohesion;
   double jupiter_support;
   double saturn_resistance;

   // Lunar / micro layer: short-term M1 timing environment.
   double moon_tempo;
   double moon_pressure;
   double moon_flow;
   double moon_drag;
   double moon_boundary;
   double moon_oob_intensity;
   double micro_noise;
   double micro_cleanliness;

   // Market path translation.
   double clean_path;
   double clean_impulse;
   double smooth_continuation;
   double breakout_followthrough;
   double pullback_risk;
   double chop_risk;
   double m1_clean_window;
   double m1_dirty_window;

   // Text keys.
   string macro_key;
   string regime_key;
   string micro_key;
   string path_key;
   string fractal_key;
   string thesis;
};

void DAL_AstroFM_Reset(DAL_AstroFractalMetrics &f)
{
   f.valid = false;
   f.broker_time = 0;
   f.utc_time = 0;

   f.raw_flow = 0.0;
   f.raw_impulse = 0.0;
   f.raw_friction = 0.0;
   f.raw_pressure = 0.0;
   f.raw_transition = 0.0;
   f.raw_moon_tempo = 0.0;
   f.raw_saturn_drag = 0.0;

   f.macro_flow = 0.0;
   f.macro_drag = 0.0;
   f.macro_pressure = 0.0;
   f.macro_transition = 0.0;
   f.macro_expansion = 0.0;
   f.macro_compression = 0.0;
   f.outer_station_risk = 0.0;
   f.structural_bias = 0.0;

   f.mars_impulse = 0.0;
   f.mars_clean_impulse = 0.0;
   f.mars_saturn_friction = 0.0;
   f.mars_jupiter_expansion = 0.0;
   f.mercury_noise = 0.0;
   f.venus_mars_cohesion = 0.0;
   f.jupiter_support = 0.0;
   f.saturn_resistance = 0.0;

   f.moon_tempo = 0.0;
   f.moon_pressure = 0.0;
   f.moon_flow = 0.0;
   f.moon_drag = 0.0;
   f.moon_boundary = 0.0;
   f.moon_oob_intensity = 0.0;
   f.micro_noise = 0.0;
   f.micro_cleanliness = 0.0;

   f.clean_path = 0.0;
   f.clean_impulse = 0.0;
   f.smooth_continuation = 0.0;
   f.breakout_followthrough = 0.0;
   f.pullback_risk = 0.0;
   f.chop_risk = 0.0;
   f.m1_clean_window = 0.0;
   f.m1_dirty_window = 0.0;

   f.macro_key = "";
   f.regime_key = "";
   f.micro_key = "";
   f.path_key = "";
   f.fractal_key = "";
   f.thesis = "";
}

string DAL_AstroFM_Bucket(const double score)
{
   return DAL_AstroPM_Bucket5(score);
}

double DAL_AstroFM_Avg2(const double a, const double b)
{
   return DAL_AstroPM_Clamp((a + b) / 2.0);
}

double DAL_AstroFM_Avg3(const double a, const double b, const double c)
{
   return DAL_AstroPM_Clamp((a + b + c) / 3.0);
}

double DAL_AstroFM_Avg4(const double a, const double b, const double c, const double d)
{
   return DAL_AstroPM_Clamp((a + b + c + d) / 4.0);
}

double DAL_AstroFM_BodySpeedIntensity(const DAL_AstroBodyState &b, const double normal_speed)
{
   double v = MathAbs(b.speed_lon);
   if(normal_speed <= 0.0)
      return 0.0;
   return DAL_AstroPM_Clamp(50.0 * v / normal_speed);
}

double DAL_AstroFM_StationRisk(const DAL_AstroBodyState &b)
{
   double eps = DAL_AstroDF_StationEpsilon(b.name);
   if(eps <= 0.0)
      return 0.0;
   double v = MathAbs(b.speed_lon);
   if(v <= eps)
      return 100.0;
   if(v <= eps * 2.0)
      return 70.0;
   if(v <= eps * 4.0)
      return 35.0;
   return 0.0;
}

double DAL_AstroFM_IngressIntensity(const DAL_AstroBodyState &b)
{
   double d0 = b.degree;
   double d1 = 30.0 - b.degree;
   double near = MathMin(d0, d1);
   if(near <= 0.25) return 100.0;
   if(near <= 0.50) return 80.0;
   if(near <= 1.00) return 60.0;
   if(near <= 2.00) return 30.0;
   return 0.0;
}

double DAL_AstroFM_DeclOobIntensity(const DAL_AstroBodyState &b)
{
   double excess = MathAbs(b.decl) - 23.44;
   if(excess <= 0.0)
      return 0.0;
   return DAL_AstroPM_Clamp(20.0 + 20.0 * excess);
}

double DAL_AstroFM_ElementExpansionBias(const DAL_AstroMapRow &row)
{
   int fire = 0, air = 0, earth = 0, water = 0;
   for(int i = 0; i < 7; i++)
   {
      string e = DAL_AstroDF_SignElement(row.body[i].sign);
      if(e == "fire") fire++;
      else if(e == "air") air++;
      else if(e == "earth") earth++;
      else if(e == "water") water++;
   }
   return DAL_AstroPM_Clamp(100.0 * (fire + air) / 7.0);
}

double DAL_AstroFM_ElementCompressionBias(const DAL_AstroMapRow &row)
{
   int earth = 0, water = 0;
   for(int i = 0; i < 7; i++)
   {
      string e = DAL_AstroDF_SignElement(row.body[i].sign);
      if(e == "earth" || e == "water") earth++;
   }
   return DAL_AstroPM_Clamp(100.0 * earth / 7.0);
}

double DAL_AstroFM_CardinalBias(const DAL_AstroMapRow &row)
{
   int cardinal = 0;
   for(int i = 0; i < 7; i++)
   {
      if(DAL_AstroDF_SignModality(row.body[i].sign) == "cardinal")
         cardinal++;
   }
   return DAL_AstroPM_Clamp(100.0 * cardinal / 7.0);
}

double DAL_AstroFM_FixedBias(const DAL_AstroMapRow &row)
{
   int fixed = 0;
   for(int i = 0; i < 7; i++)
   {
      if(DAL_AstroDF_SignModality(row.body[i].sign) == "fixed")
         fixed++;
   }
   return DAL_AstroPM_Clamp(100.0 * fixed / 7.0);
}

double DAL_AstroFM_SoftPair(const DAL_AstroMapRow &row, const string pair, const double weight)
{
   return DAL_AstroPM_SoftAspectScore(row, pair, weight);
}

double DAL_AstroFM_HardPair(const DAL_AstroMapRow &row, const string pair, const double weight)
{
   return DAL_AstroPM_HardAspectScore(row, pair, weight);
}

string DAL_AstroFM_KeyAppend(string key, const string name, const double score)
{
   string item = name + "_" + DAL_AstroFM_Bucket(score);
   if(key == "") return item;
   return key + "|" + item;
}

bool DAL_AstroFM_Calc(const DAL_AstroMapRow &row, DAL_AstroFractalMetrics &f)
{
   DAL_AstroFM_Reset(f);

   DAL_AstroPathMetrics p;
   if(!DAL_AstroPathMetrics_Calc(row, p) || !p.valid)
      return false;

   f.valid = true;
   f.broker_time = row.broker_time;
   f.utc_time = row.utc_time;

   f.raw_flow = p.flow_score;
   f.raw_impulse = p.impulse_score;
   f.raw_friction = p.friction_score;
   f.raw_pressure = p.pressure_score;
   f.raw_transition = p.transition_score;
   f.raw_moon_tempo = p.moon_tempo_score;
   f.raw_saturn_drag = p.saturn_drag_score;

   int idx_moon    = DAL_AstroBodyIndexByName("moon");
   int idx_mercury = DAL_AstroBodyIndexByName("mercury");
   int idx_venus   = DAL_AstroBodyIndexByName("venus");
   int idx_mars    = DAL_AstroBodyIndexByName("mars");
   int idx_jupiter = DAL_AstroBodyIndexByName("jupiter");
   int idx_saturn  = DAL_AstroBodyIndexByName("saturn");
   int idx_uranus  = DAL_AstroBodyIndexByName("uranus");
   int idx_neptune = DAL_AstroBodyIndexByName("neptune");
   int idx_pluto   = DAL_AstroBodyIndexByName("pluto");

   DAL_AstroBodyState moon    = row.body[idx_moon];
   DAL_AstroBodyState mercury = row.body[idx_mercury];
   DAL_AstroBodyState venus   = row.body[idx_venus];
   DAL_AstroBodyState mars    = row.body[idx_mars];
   DAL_AstroBodyState jupiter = row.body[idx_jupiter];
   DAL_AstroBodyState saturn  = row.body[idx_saturn];
   DAL_AstroBodyState uranus  = row.body[idx_uranus];
   DAL_AstroBodyState neptune = row.body[idx_neptune];
   DAL_AstroBodyState pluto   = row.body[idx_pluto];

   double expansion_bias = DAL_AstroFM_ElementExpansionBias(row);
   double compression_bias = DAL_AstroFM_ElementCompressionBias(row);
   double cardinal_bias = DAL_AstroFM_CardinalBias(row);
   double fixed_bias = DAL_AstroFM_FixedBias(row);

   double js_soft = DAL_AstroFM_SoftPair(row, "jupiter_saturn", 1.0);
   double js_hard = DAL_AstroFM_HardPair(row, "jupiter_saturn", 1.0);
   double sun_sat_hard = DAL_AstroFM_HardPair(row, "sun_saturn", 0.8);
   double sun_jup_soft = DAL_AstroFM_SoftPair(row, "sun_jupiter", 0.8);

   f.outer_station_risk = DAL_AstroFM_Avg3(
      DAL_AstroFM_StationRisk(uranus),
      DAL_AstroFM_StationRisk(neptune),
      DAL_AstroFM_StationRisk(pluto)
   );

   f.macro_transition = DAL_AstroFM_Avg4(
      f.outer_station_risk,
      DAL_AstroFM_IngressIntensity(jupiter),
      DAL_AstroFM_IngressIntensity(saturn),
      DAL_AstroFM_IngressIntensity(uranus)
   );

   f.macro_flow = DAL_AstroPM_Clamp(0.45 * js_soft + 0.25 * sun_jup_soft + 0.20 * expansion_bias + 0.10 * (100.0 - f.macro_transition));
   f.macro_pressure = DAL_AstroPM_Clamp(0.55 * js_hard + 0.30 * sun_sat_hard + 0.15 * f.macro_transition);
   f.macro_drag = DAL_AstroPM_Clamp(0.45 * p.saturn_drag_score + 0.25 * compression_bias + 0.20 * fixed_bias + 0.10 * f.macro_transition);
   f.macro_expansion = DAL_AstroPM_Clamp(0.45 * expansion_bias + 0.30 * cardinal_bias + 0.25 * f.macro_flow);
   f.macro_compression = DAL_AstroPM_Clamp(0.45 * compression_bias + 0.30 * f.macro_drag + 0.25 * fixed_bias);
   f.structural_bias = DAL_AstroPM_Clamp(f.macro_expansion - 0.35 * f.macro_compression + 30.0);

   double mars_speed = DAL_AstroFM_BodySpeedIntensity(mars, 0.55);
   double mars_direct_bonus = (mars.retro == 1 ? 0.0 : 20.0);
   double mars_element_bonus = 0.0;
   string mars_element = DAL_AstroDF_SignElement(mars.sign);
   if(mars_element == "fire" || mars_element == "air") mars_element_bonus = 16.0;
   else if(mars_element == "earth") mars_element_bonus = 8.0;

   double mars_sat_hard = DAL_AstroFM_HardPair(row, "mars_saturn", 1.0);
   double mars_sat_soft = DAL_AstroFM_SoftPair(row, "mars_saturn", 0.7);
   double sun_mars_hard = DAL_AstroFM_HardPair(row, "sun_mars", 0.7);
   double sun_mars_soft = DAL_AstroFM_SoftPair(row, "sun_mars", 0.5);
   double venus_mars_soft = DAL_AstroFM_SoftPair(row, "venus_mars", 0.7);
   double venus_mars_hard = DAL_AstroFM_HardPair(row, "venus_mars", 0.4);

   f.mars_impulse = DAL_AstroPM_Clamp(0.60 * mars_speed + mars_direct_bonus + mars_element_bonus + 0.20 * cardinal_bias + 0.15 * sun_mars_soft + 0.10 * sun_mars_hard);
   f.mars_saturn_friction = DAL_AstroPM_Clamp(0.70 * mars_sat_hard + 0.20 * p.saturn_drag_score + 0.10 * DAL_AstroFM_StationRisk(saturn) - 0.20 * mars_sat_soft);
   f.jupiter_support = DAL_AstroPM_Clamp(0.45 * sun_jup_soft + 0.35 * js_soft + 0.20 * expansion_bias);
   f.mars_jupiter_expansion = DAL_AstroPM_Clamp(0.55 * f.mars_impulse + 0.45 * f.jupiter_support);
   f.saturn_resistance = DAL_AstroPM_Clamp(0.55 * p.saturn_drag_score + 0.30 * f.mars_saturn_friction + 0.15 * DAL_AstroFM_StationRisk(saturn));

   double mercury_station = DAL_AstroFM_StationRisk(mercury);
   double mercury_retro = (mercury.retro == 1 ? 70.0 : 0.0);
   double moon_mercury_hard = DAL_AstroFM_HardPair(row, "moon_mercury", 0.7);
   double sun_mercury_hard = DAL_AstroFM_HardPair(row, "sun_mercury", 0.5);
   f.mercury_noise = DAL_AstroPM_Clamp(0.35 * mercury_station + 0.30 * mercury_retro + 0.20 * moon_mercury_hard + 0.15 * sun_mercury_hard);

   f.venus_mars_cohesion = DAL_AstroPM_Clamp(0.65 * venus_mars_soft + 0.20 * (100.0 - venus_mars_hard) + 0.15 * (100.0 - f.mercury_noise));
   f.mars_clean_impulse = DAL_AstroPM_Clamp(0.55 * f.mars_impulse + 0.20 * f.venus_mars_cohesion + 0.15 * f.jupiter_support - 0.35 * f.mars_saturn_friction - 0.20 * f.mercury_noise + 25.0);

   double moon_speed = DAL_AstroFM_BodySpeedIntensity(moon, 13.2);
   double moon_mars_hard = DAL_AstroFM_HardPair(row, "moon_mars", 1.0);
   double moon_sat_hard = DAL_AstroFM_HardPair(row, "moon_saturn", 1.0);
   double moon_jup_soft = DAL_AstroFM_SoftPair(row, "moon_jupiter", 0.8);
   double moon_venus_soft = DAL_AstroFM_SoftPair(row, "moon_venus", 0.6);
   double sun_moon_soft = DAL_AstroFM_SoftPair(row, "sun_moon", 0.7);
   double sun_moon_hard = DAL_AstroFM_HardPair(row, "sun_moon", 0.5);

   f.moon_tempo = DAL_AstroPM_Clamp(moon_speed);
   f.moon_pressure = DAL_AstroPM_Clamp(0.45 * moon_mars_hard + 0.35 * moon_sat_hard + 0.20 * sun_moon_hard);
   f.moon_flow = DAL_AstroPM_Clamp(0.40 * sun_moon_soft + 0.35 * moon_jup_soft + 0.25 * moon_venus_soft);
   f.moon_drag = DAL_AstroPM_Clamp(0.65 * moon_sat_hard + 0.25 * p.saturn_drag_score + 0.10 * DAL_AstroFM_StationRisk(saturn));
   f.moon_boundary = DAL_AstroFM_Avg3(DAL_AstroFM_IngressIntensity(moon), DAL_AstroPM_PhaseBoundaryNear(row.moon_phase_angle, 5.0) ? 80.0 : 0.0, DAL_AstroFM_StationRisk(moon));
   f.moon_oob_intensity = DAL_AstroFM_DeclOobIntensity(moon);
   f.micro_noise = DAL_AstroPM_Clamp(0.30 * f.moon_pressure + 0.25 * f.moon_boundary + 0.20 * f.mercury_noise + 0.15 * f.moon_oob_intensity + 0.10 * f.raw_pressure);
   f.micro_cleanliness = DAL_AstroPM_Clamp(0.35 * f.moon_flow + 0.25 * f.moon_tempo + 0.20 * (100.0 - f.micro_noise) + 0.20 * (100.0 - f.moon_drag));

   f.clean_impulse = DAL_AstroPM_Clamp(0.35 * p.clean_impulse_score + 0.30 * f.mars_clean_impulse + 0.20 * f.micro_cleanliness + 0.15 * (100.0 - f.macro_drag));
   f.smooth_continuation = DAL_AstroPM_Clamp(0.35 * p.smooth_continuation_score + 0.25 * f.macro_flow + 0.25 * f.moon_flow + 0.15 * (100.0 - f.saturn_resistance));
   f.breakout_followthrough = DAL_AstroPM_Clamp(0.35 * p.breakout_followthrough_score + 0.30 * f.mars_jupiter_expansion + 0.20 * f.moon_tempo + 0.15 * (100.0 - f.micro_noise));
   f.pullback_risk = DAL_AstroPM_Clamp(0.30 * p.pullback_risk_score + 0.25 * f.micro_noise + 0.20 * f.mars_saturn_friction + 0.15 * f.moon_drag + 0.10 * f.macro_drag);
   f.chop_risk = DAL_AstroPM_Clamp(0.30 * p.chop_risk_score + 0.25 * f.macro_transition + 0.20 * f.mercury_noise + 0.15 * f.moon_boundary + 0.10 * f.micro_noise);
   f.clean_path = DAL_AstroPM_Clamp(0.30 * p.clean_path_score + 0.20 * f.clean_impulse + 0.20 * f.smooth_continuation + 0.15 * (100.0 - f.pullback_risk) + 0.15 * (100.0 - f.chop_risk));
   f.m1_clean_window = DAL_AstroPM_Clamp(0.35 * f.clean_path + 0.25 * f.micro_cleanliness + 0.20 * f.breakout_followthrough + 0.20 * (100.0 - f.pullback_risk));
   f.m1_dirty_window = DAL_AstroPM_Clamp(0.35 * f.pullback_risk + 0.35 * f.chop_risk + 0.20 * f.micro_noise + 0.10 * f.macro_transition);

   f.macro_key = "macro=";
   f.macro_key = DAL_AstroFM_KeyAppend(f.macro_key, "flow", f.macro_flow);
   f.macro_key = DAL_AstroFM_KeyAppend(f.macro_key, "drag", f.macro_drag);
   f.macro_key = DAL_AstroFM_KeyAppend(f.macro_key, "pressure", f.macro_pressure);
   f.macro_key = DAL_AstroFM_KeyAppend(f.macro_key, "transition", f.macro_transition);
   f.macro_key = DAL_AstroFM_KeyAppend(f.macro_key, "expansion", f.macro_expansion);
   f.macro_key = DAL_AstroFM_KeyAppend(f.macro_key, "compression", f.macro_compression);

   f.regime_key = "regime=";
   f.regime_key = DAL_AstroFM_KeyAppend(f.regime_key, "mars_impulse", f.mars_impulse);
   f.regime_key = DAL_AstroFM_KeyAppend(f.regime_key, "clean_impulse", f.mars_clean_impulse);
   f.regime_key = DAL_AstroFM_KeyAppend(f.regime_key, "ms_friction", f.mars_saturn_friction);
   f.regime_key = DAL_AstroFM_KeyAppend(f.regime_key, "mercury_noise", f.mercury_noise);
   f.regime_key = DAL_AstroFM_KeyAppend(f.regime_key, "jupiter_support", f.jupiter_support);

   f.micro_key = "micro=";
   f.micro_key = DAL_AstroFM_KeyAppend(f.micro_key, "moon_tempo", f.moon_tempo);
   f.micro_key = DAL_AstroFM_KeyAppend(f.micro_key, "moon_pressure", f.moon_pressure);
   f.micro_key = DAL_AstroFM_KeyAppend(f.micro_key, "moon_flow", f.moon_flow);
   f.micro_key = DAL_AstroFM_KeyAppend(f.micro_key, "boundary", f.moon_boundary);
   f.micro_key = DAL_AstroFM_KeyAppend(f.micro_key, "clean", f.micro_cleanliness);

   f.path_key = "path=";
   f.path_key = DAL_AstroFM_KeyAppend(f.path_key, "clean", f.clean_path);
   f.path_key = DAL_AstroFM_KeyAppend(f.path_key, "brk", f.breakout_followthrough);
   f.path_key = DAL_AstroFM_KeyAppend(f.path_key, "pb", f.pullback_risk);
   f.path_key = DAL_AstroFM_KeyAppend(f.path_key, "chop", f.chop_risk);
   f.path_key = DAL_AstroFM_KeyAppend(f.path_key, "m1clean", f.m1_clean_window);

   f.fractal_key = f.macro_key + "|" + f.regime_key + "|" + f.micro_key + "|" + f.path_key;

   if(f.m1_clean_window >= 70.0 && f.m1_dirty_window <= 35.0)
      f.thesis = "M1 thesis: clean window candidate; watch independent market signals for low-pullback follow-through.";
   else if(f.breakout_followthrough >= 70.0 && f.pullback_risk <= 40.0)
      f.thesis = "M1 thesis: breakout follow-through candidate; impulse context is stronger than smooth-flow context.";
   else if(f.smooth_continuation >= 70.0 && f.chop_risk <= 40.0)
      f.thesis = "M1 thesis: smooth continuation candidate; flow context is stronger than impulse context.";
   else if(f.m1_dirty_window >= 65.0)
      f.thesis = "M1 thesis: dirty-window warning; expect chop/pullback unless market structure is very strong.";
   else
      f.thesis = "M1 thesis: mixed/neutral; use as observation layer only.";

   return true;
}

string DAL_AstroFM_ScoreLine(const string label, const double score, const string note = "")
{
   string s = StringFormat("%-18s %6.1f  %-9s", label, score, DAL_AstroFM_Bucket(score));
   if(note != "") s += " | " + note;
   return s;
}

string DAL_AstroFM_ToText(const DAL_AstroFractalMetrics &f, const bool show_keys = true)
{
   if(!f.valid)
      return "ASTRO FRACTAL METRICS INVALID";

   string t = "ASTRO FRACTAL PATH METRICS\n";
   t += "Broker: " + TimeToString(f.broker_time, TIME_DATE|TIME_MINUTES) + "\n";
   t += "UTC:    " + TimeToString(f.utc_time, TIME_DATE|TIME_MINUTES) + "\n\n";

   t += "RAW AXES\n";
   t += DAL_AstroFM_ScoreLine("RawFlow", f.raw_flow) + "\n";
   t += DAL_AstroFM_ScoreLine("RawImpulse", f.raw_impulse) + "\n";
   t += DAL_AstroFM_ScoreLine("RawFriction", f.raw_friction) + "\n";
   t += DAL_AstroFM_ScoreLine("RawPressure", f.raw_pressure) + "\n";
   t += DAL_AstroFM_ScoreLine("RawTransition", f.raw_transition) + "\n\n";

   t += "MACRO LAYER\n";
   t += DAL_AstroFM_ScoreLine("MacroFlow", f.macro_flow, "outer/slow smooth background") + "\n";
   t += DAL_AstroFM_ScoreLine("MacroDrag", f.macro_drag, "slow structural drag") + "\n";
   t += DAL_AstroFM_ScoreLine("MacroPressure", f.macro_pressure, "slow hard-pressure background") + "\n";
   t += DAL_AstroFM_ScoreLine("MacroTransition", f.macro_transition, "station/ingress background") + "\n";
   t += DAL_AstroFM_ScoreLine("Expansion", f.macro_expansion, "fire/air/cardinal expansion") + "\n";
   t += DAL_AstroFM_ScoreLine("Compression", f.macro_compression, "earth/water/fixed compression") + "\n\n";

   t += "REGIME LAYER\n";
   t += DAL_AstroFM_ScoreLine("MarsImpulse", f.mars_impulse, "active movement force") + "\n";
   t += DAL_AstroFM_ScoreLine("MarsCleanImpulse", f.mars_clean_impulse, "movement after friction control") + "\n";
   t += DAL_AstroFM_ScoreLine("MarsSatFriction", f.mars_saturn_friction, "Mars-Saturn drag") + "\n";
   t += DAL_AstroFM_ScoreLine("MercuryNoise", f.mercury_noise, "short decision/noise disturbance") + "\n";
   t += DAL_AstroFM_ScoreLine("JupiterSupport", f.jupiter_support, "expansion support") + "\n\n";

   t += "MOON / MICRO LAYER\n";
   t += DAL_AstroFM_ScoreLine("MoonTempo", f.moon_tempo, "M1 timing speed") + "\n";
   t += DAL_AstroFM_ScoreLine("MoonPressure", f.moon_pressure, "micro hard pressure") + "\n";
   t += DAL_AstroFM_ScoreLine("MoonFlow", f.moon_flow, "micro soft flow") + "\n";
   t += DAL_AstroFM_ScoreLine("MoonBoundary", f.moon_boundary, "phase/sign boundary") + "\n";
   t += DAL_AstroFM_ScoreLine("MicroClean", f.micro_cleanliness, "short-term clean path context") + "\n\n";

   t += "M1 PATH TRANSLATION\n";
   t += DAL_AstroFM_ScoreLine("CleanPath", f.clean_path) + "\n";
   t += DAL_AstroFM_ScoreLine("CleanImpulse", f.clean_impulse) + "\n";
   t += DAL_AstroFM_ScoreLine("SmoothCont", f.smooth_continuation) + "\n";
   t += DAL_AstroFM_ScoreLine("BreakoutFT", f.breakout_followthrough) + "\n";
   t += DAL_AstroFM_ScoreLine("PullbackRisk", f.pullback_risk, "higher is worse") + "\n";
   t += DAL_AstroFM_ScoreLine("ChopRisk", f.chop_risk, "higher is worse") + "\n";
   t += DAL_AstroFM_ScoreLine("M1CleanWindow", f.m1_clean_window) + "\n";
   t += DAL_AstroFM_ScoreLine("M1DirtyWindow", f.m1_dirty_window, "higher is worse") + "\n\n";

   t += f.thesis + "\n";
   t += "No causality claim. Validate with MAE_R, pullback_depth_R, path_efficiency, bars_to_target.\n";

   if(show_keys)
   {
      t += "\nFEATURE KEYS\n";
      t += f.macro_key + "\n";
      t += f.regime_key + "\n";
      t += f.micro_key + "\n";
      t += f.path_key + "\n";
   }

   return t;
}

#endif
