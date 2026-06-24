#ifndef __DAL_ASTRO_PATH_CLEANLINESS_METRICS_MQH__
#define __DAL_ASTRO_PATH_CLEANLINESS_METRICS_MQH__

#include <Research/DAL_AstroMapTypes.mqh>
#include <Research/DAL_AstroDerivedFeatures.mqh>

// Decision Alpha Lab - Astro Path Cleanliness Metrics
// ---------------------------------------------------
// This module does NOT trade and does NOT predict direction.
// It converts a candle-aligned astrological sky map into explicit, testable
// path-cleanliness features. The goal is to observe whether some sky states
// are associated with cleaner market paths after an independent execution signal.
//
// Runtime contract:
// - Python builds the candle-aligned astro CSV/XLSX.
// - MQL5 loads the CSV mirror.
// - This module derives interpretation scores on every candle.
// - The scores are displayed in visual tester/live mode and can later be
//   appended to Distribution Engineering feature keys.

#define DAL_ASTRO_PM_MAX_LINES 80

struct DAL_AstroPathMetrics
{
   bool     valid;
   datetime broker_time;
   datetime utc_time;

   // Core path axes, all normalized to 0..100.
   double flow_score;
   double impulse_score;
   double friction_score;
   double pressure_score;
   double transition_score;
   double moon_tempo_score;
   double saturn_drag_score;
   double mercury_disturbance_score;

   // Composite scores, all normalized to 0..100.
   double clean_path_score;
   double clean_impulse_score;
   double smooth_continuation_score;
   double breakout_followthrough_score;
   double pullback_risk_score;
   double chop_risk_score;

   // Human-readable buckets.
   string flow_bucket;
   string impulse_bucket;
   string friction_bucket;
   string pressure_bucket;
   string transition_bucket;
   string moon_tempo_bucket;
   string saturn_drag_bucket;
   string clean_path_bucket;
   string pullback_risk_bucket;
   string chop_risk_bucket;
   string astro_path_regime;

   // Interpreted state summaries.
   string element_bias;
   string modality_bias;
   string moon_phase_group;
   string moon_decl_zone;
   string mars_state;
   string saturn_state;
   string mercury_state;
   string sun_moon_state;
   string moon_mars_state;
   string moon_saturn_state;
   string venus_mars_state;
   string mars_saturn_state;
   string jupiter_saturn_state;

   // Compact keys for later Distribution Engineering.
   string astro_path_key;
   string clean_gate_key;
   string diagnostic_key;

   // Text blocks for display.
   string thesis;
   string warning;
};

// -------------------------
// Generic numeric helpers
// -------------------------

double DAL_AstroPM_Clamp(const double value, const double lo = 0.0, const double hi = 100.0)
{
   if(value < lo) return lo;
   if(value > hi) return hi;
   return value;
}

double DAL_AstroPM_SafeDiv(const double a, const double b, const double fallback = 0.0)
{
   if(MathAbs(b) <= 0.0000000001)
      return fallback;
   return a / b;
}

string DAL_AstroPM_Double1(const double v)
{
   return DoubleToString(v, 1);
}

string DAL_AstroPM_Bucket3(const double score)
{
   if(score < 33.0) return "low";
   if(score < 66.0) return "mid";
   return "high";
}

string DAL_AstroPM_Bucket5(const double score)
{
   if(score < 20.0) return "very_low";
   if(score < 40.0) return "low";
   if(score < 60.0) return "mid";
   if(score < 80.0) return "high";
   return "very_high";
}

string DAL_AstroPM_BoolText(const bool v)
{
   return v ? "true" : "false";
}

string DAL_AstroPM_ShortBody(const string name)
{
   if(name == "sun") return "su";
   if(name == "moon") return "mo";
   if(name == "mercury") return "me";
   if(name == "venus") return "ve";
   if(name == "mars") return "ma";
   if(name == "jupiter") return "ju";
   if(name == "saturn") return "sa";
   return name;
}

string DAL_AstroPM_ShortAspect(const string aspect)
{
   if(aspect == "conjunction") return "conj";
   if(aspect == "opposition")  return "opp";
   if(aspect == "square")      return "sq";
   if(aspect == "trine")       return "tri";
   if(aspect == "sextile")     return "sex";
   return "none";
}

string DAL_AstroPM_ShortOrb(const double orb)
{
   if(orb <= 1.0) return "tight";
   if(orb <= 3.0) return "close";
   if(orb <= 6.0) return "wide";
   return "none";
}

string DAL_AstroPM_AppSep(const int applying)
{
   return applying == 1 ? "app" : "sep";
}

bool DAL_AstroPM_IsSoftAspect(const string aspect)
{
   return (aspect == "trine" || aspect == "sextile");
}

bool DAL_AstroPM_IsHardAspect(const string aspect)
{
   return (aspect == "square" || aspect == "opposition" || aspect == "conjunction");
}

bool DAL_AstroPM_GetBody(const DAL_AstroMapRow &row, const string body_name, DAL_AstroBodyState &out)
{
   int idx = DAL_AstroBodyIndexByName(body_name);
   if(idx < 0)
      return false;
   out = row.body[idx];
   return true;
}

bool DAL_AstroPM_GetAspect(const DAL_AstroMapRow &row, const string pair_name, DAL_AstroAspectState &out)
{
   int idx = DAL_AstroAspectIndexByName(pair_name);
   if(idx < 0)
      return false;
   out = row.aspect[idx];
   return true;
}

// Aspect strength is strongest when the orb is tight.
// Applying aspects are slightly stronger because the geometric pressure is still building.
double DAL_AstroPM_AspectStrength(const DAL_AstroAspectState &a, const double max_orb = 6.0)
{
   if(a.aspect == "none" || a.orb > max_orb)
      return 0.0;

   double tightness = DAL_AstroPM_Clamp(1.0 - DAL_AstroPM_SafeDiv(a.orb, max_orb), 0.0, 1.0);
   double motion_mult = a.applying == 1 ? 1.15 : 0.90;
   return DAL_AstroPM_Clamp(100.0 * tightness * motion_mult, 0.0, 100.0);
}

double DAL_AstroPM_SoftAspectScore(const DAL_AstroMapRow &row, const string pair_name, const double weight)
{
   DAL_AstroAspectState a;
   if(!DAL_AstroPM_GetAspect(row, pair_name, a))
      return 0.0;
   if(!DAL_AstroPM_IsSoftAspect(a.aspect))
      return 0.0;
   return weight * DAL_AstroPM_AspectStrength(a, 6.0);
}

double DAL_AstroPM_HardAspectScore(const DAL_AstroMapRow &row, const string pair_name, const double weight)
{
   DAL_AstroAspectState a;
   if(!DAL_AstroPM_GetAspect(row, pair_name, a))
      return 0.0;
   if(!DAL_AstroPM_IsHardAspect(a.aspect))
      return 0.0;

   double base = DAL_AstroPM_AspectStrength(a, 6.0);
   if(a.aspect == "conjunction")
      base *= 0.85; // conjunction is pressure/fusion, but less uniformly conflict-like than square/opposition.
   return weight * base;
}

string DAL_AstroPM_AspectStateText(const DAL_AstroMapRow &row, const string pair_name)
{
   DAL_AstroAspectState a;
   if(!DAL_AstroPM_GetAspect(row, pair_name, a))
      return "missing";

   if(a.aspect == "none" || a.orb > 6.0)
      return "none";

   return DAL_AstroPM_ShortAspect(a.aspect) + "_" + DAL_AstroPM_ShortOrb(a.orb) + "_" + DAL_AstroPM_AppSep(a.applying);
}

// -------------------------
// Body and sky-state helpers
// -------------------------

string DAL_AstroPM_SpeedBucket(const DAL_AstroBodyState &b)
{
   double s = MathAbs(b.speed_lon);
   string n = b.name;

   if(DAL_AstroDF_SpeedState(b) == "station")
      return "station";
   if(b.retro == 1)
      return "retro";

   if(n == "moon")
   {
      if(s < 12.5) return "slow";
      if(s > 13.8) return "fast";
      return "normal";
   }
   if(n == "mercury")
   {
      if(s < 0.70) return "slow";
      if(s > 1.45) return "fast";
      return "normal";
   }
   if(n == "venus")
   {
      if(s < 0.45) return "slow";
      if(s > 1.10) return "fast";
      return "normal";
   }
   if(n == "mars")
   {
      if(s < 0.20) return "slow";
      if(s > 0.55) return "fast";
      return "normal";
   }
   if(n == "jupiter")
   {
      if(s < 0.025) return "slow";
      if(s > 0.11)  return "fast";
      return "normal";
   }
   if(n == "saturn")
   {
      if(s < 0.010) return "slow";
      if(s > 0.075) return "fast";
      return "normal";
   }

   return "normal";
}

double DAL_AstroPM_SpeedScore(const DAL_AstroBodyState &b)
{
   string state = DAL_AstroDF_SpeedState(b);
   string bucket = DAL_AstroPM_SpeedBucket(b);
   if(state == "station") return 5.0;
   if(state == "retro")   return 25.0;
   if(bucket == "fast")   return 100.0;
   if(bucket == "normal") return 65.0;
   if(bucket == "slow")   return 35.0;
   return 50.0;
}

bool DAL_AstroPM_IngressNear(const DAL_AstroBodyState &b, const double orb_deg = 1.0)
{
   return (b.degree <= orb_deg || b.degree >= (30.0 - orb_deg));
}

bool DAL_AstroPM_PhaseBoundaryNear(const double moon_phase_angle, const double orb_deg = 5.0)
{
   double p0 = 0.0;
   double p1 = 90.0;
   double p2 = 180.0;
   double p3 = 270.0;

   double d0 = MathAbs(moon_phase_angle - p0); d0 = MathMin(d0, 360.0 - d0);
   double d1 = MathAbs(moon_phase_angle - p1); d1 = MathMin(d1, 360.0 - d1);
   double d2 = MathAbs(moon_phase_angle - p2); d2 = MathMin(d2, 360.0 - d2);
   double d3 = MathAbs(moon_phase_angle - p3); d3 = MathMin(d3, 360.0 - d3);

   return (d0 <= orb_deg || d1 <= orb_deg || d2 <= orb_deg || d3 <= orb_deg);
}

string DAL_AstroPM_MoonPhaseGroup(const string bucket)
{
   if(bucket == "new") return "new";
   if(bucket == "full") return "full";
   if(StringFind(bucket, "waxing") >= 0 || bucket == "first_quarter") return "waxing";
   if(StringFind(bucket, "waning") >= 0 || bucket == "last_quarter") return "waning";
   return "unknown";
}

string DAL_AstroPM_BodyStateText(const DAL_AstroBodyState &b)
{
   string dir = "D";
   string spd = DAL_AstroPM_SpeedBucket(b);
   if(DAL_AstroDF_SpeedState(b) == "station") dir = "S";
   else if(b.retro == 1) dir = "R";

   string elem = DAL_AstroDF_SignElement(b.sign);
   return dir + "_" + spd + "_" + elem;
}

string DAL_AstroPM_TopBiasFromCounts(const int &counts[], const string &names[])
{
   int best1 = 0;
   int best2 = 1;
   for(int i = 0; i < ArraySize(counts); i++)
   {
      if(counts[i] > counts[best1])
         best1 = i;
   }
   for(int j = 0; j < ArraySize(counts); j++)
   {
      if(j == best1) continue;
      if(counts[j] > counts[best2] || best2 == best1)
         best2 = j;
   }

   if(counts[best1] <= 0)
      return "unknown";
   if(counts[best2] > 0 && counts[best1] == counts[best2])
      return names[best1] + "_" + names[best2];
   return names[best1];
}

string DAL_AstroPM_ElementBias(const DAL_AstroMapRow &row)
{
   int counts[4] = {0,0,0,0};
   string names[4] = {"fire","earth","air","water"};
   string bodies[7] = {"sun","moon","mercury","venus","mars","jupiter","saturn"};

   for(int i = 0; i < 7; i++)
   {
      int idx = DAL_AstroBodyIndexByName(bodies[i]);
      if(idx < 0) continue;
      string e = DAL_AstroDF_SignElement(row.body[idx].sign);
      if(e == "fire") counts[0]++;
      else if(e == "earth") counts[1]++;
      else if(e == "air") counts[2]++;
      else if(e == "water") counts[3]++;
   }
   return DAL_AstroPM_TopBiasFromCounts(counts, names);
}

string DAL_AstroPM_ModalityBias(const DAL_AstroMapRow &row)
{
   int counts[3] = {0,0,0};
   string names[3] = {"cardinal","fixed","mutable"};
   string bodies[7] = {"sun","moon","mercury","venus","mars","jupiter","saturn"};

   for(int i = 0; i < 7; i++)
   {
      int idx = DAL_AstroBodyIndexByName(bodies[i]);
      if(idx < 0) continue;
      string m = DAL_AstroDF_SignModality(row.body[idx].sign);
      if(m == "cardinal") counts[0]++;
      else if(m == "fixed") counts[1]++;
      else if(m == "mutable") counts[2]++;
   }
   return DAL_AstroPM_TopBiasFromCounts(counts, names);
}

// -------------------------
// Raw axis scores
// -------------------------

double DAL_AstroPM_FlowScore(const DAL_AstroMapRow &row)
{
   double total_weight = 0.0;
   double score = 0.0;

   score += DAL_AstroPM_SoftAspectScore(row, "sun_moon",     1.60); total_weight += 1.60;
   score += DAL_AstroPM_SoftAspectScore(row, "venus_mars",   1.50); total_weight += 1.50;
   score += DAL_AstroPM_SoftAspectScore(row, "moon_venus",   1.10); total_weight += 1.10;
   score += DAL_AstroPM_SoftAspectScore(row, "moon_jupiter", 1.10); total_weight += 1.10;
   score += DAL_AstroPM_SoftAspectScore(row, "sun_jupiter",  1.00); total_weight += 1.00;
   score += DAL_AstroPM_SoftAspectScore(row, "jupiter_saturn",0.80); total_weight += 0.80;

   return DAL_AstroPM_Clamp(DAL_AstroPM_SafeDiv(score, total_weight));
}

double DAL_AstroPM_PressureScore(const DAL_AstroMapRow &row)
{
   double total_weight = 0.0;
   double score = 0.0;

   score += DAL_AstroPM_HardAspectScore(row, "mars_saturn",   2.40); total_weight += 2.40;
   score += DAL_AstroPM_HardAspectScore(row, "moon_saturn",   1.60); total_weight += 1.60;
   score += DAL_AstroPM_HardAspectScore(row, "moon_mars",     1.50); total_weight += 1.50;
   score += DAL_AstroPM_HardAspectScore(row, "sun_saturn",    1.30); total_weight += 1.30;
   score += DAL_AstroPM_HardAspectScore(row, "sun_mars",      1.10); total_weight += 1.10;
   score += DAL_AstroPM_HardAspectScore(row, "jupiter_saturn",1.20); total_weight += 1.20;
   score += DAL_AstroPM_HardAspectScore(row, "sun_moon",      0.80); total_weight += 0.80;

   return DAL_AstroPM_Clamp(DAL_AstroPM_SafeDiv(score, total_weight));
}

double DAL_AstroPM_MoonTempoScore(const DAL_AstroMapRow &row)
{
   int idx = DAL_AstroBodyIndexByName("moon");
   if(idx < 0) return 50.0;
   return DAL_AstroPM_SpeedScore(row.body[idx]);
}

double DAL_AstroPM_MercuryDisturbanceScore(const DAL_AstroMapRow &row)
{
   int idx = DAL_AstroBodyIndexByName("mercury");
   if(idx < 0) return 0.0;
   DAL_AstroBodyState m = row.body[idx];

   double score = 0.0;
   if(DAL_AstroDF_SpeedState(m) == "station") score += 55.0;
   else if(m.retro == 1) score += 35.0;

   score += DAL_AstroPM_HardAspectScore(row, "sun_mercury", 0.25);
   score += DAL_AstroPM_HardAspectScore(row, "moon_mercury", 0.35);

   return DAL_AstroPM_Clamp(score);
}

double DAL_AstroPM_SaturnDragScore(const DAL_AstroMapRow &row)
{
   int idx = DAL_AstroBodyIndexByName("saturn");
   if(idx < 0) return 0.0;
   DAL_AstroBodyState s = row.body[idx];

   double score = 0.0;
   string state = DAL_AstroDF_SpeedState(s);
   if(state == "station") score += 35.0;
   else if(s.retro == 1) score += 20.0;
   if(DAL_AstroPM_SpeedBucket(s) == "slow") score += 12.0;

   // Saturn hard aspects represent structural drag, delay, or resistance.
   score += 0.35 * DAL_AstroPM_HardAspectScore(row, "mars_saturn", 1.0);
   score += 0.30 * DAL_AstroPM_HardAspectScore(row, "moon_saturn", 1.0);
   score += 0.25 * DAL_AstroPM_HardAspectScore(row, "sun_saturn", 1.0);
   score += 0.20 * DAL_AstroPM_HardAspectScore(row, "jupiter_saturn", 1.0);

   return DAL_AstroPM_Clamp(score);
}

double DAL_AstroPM_TransitionScore(const DAL_AstroMapRow &row)
{
   double score = 0.0;
   string bodies[7] = {"moon","mercury","venus","mars","jupiter","saturn","sun"};

   for(int i = 0; i < 7; i++)
   {
      int idx = DAL_AstroBodyIndexByName(bodies[i]);
      if(idx < 0) continue;
      DAL_AstroBodyState b = row.body[idx];
      if(DAL_AstroPM_IngressNear(b, bodies[i] == "moon" ? 0.60 : 0.35))
         score += (bodies[i] == "moon" ? 14.0 : 8.0);
      if(DAL_AstroDF_SpeedState(b) == "station")
         score += (bodies[i] == "mercury" || bodies[i] == "mars" || bodies[i] == "saturn" ? 18.0 : 10.0);
   }

   if(DAL_AstroPM_PhaseBoundaryNear(row.moon_phase_angle, 5.0))
      score += 18.0;

   return DAL_AstroPM_Clamp(score);
}

double DAL_AstroPM_ImpulseScore(const DAL_AstroMapRow &row, const string element_bias, const string modality_bias)
{
   int mars = DAL_AstroBodyIndexByName("mars");
   int moon = DAL_AstroBodyIndexByName("moon");
   if(mars < 0 || moon < 0) return 50.0;

   double mars_energy = DAL_AstroPM_SpeedScore(row.body[mars]);
   string mars_element = DAL_AstroDF_SignElement(row.body[mars].sign);
   string mars_modality = DAL_AstroDF_SignModality(row.body[mars].sign);

   double element_impulse = 35.0;
   if(mars_element == "fire") element_impulse = 100.0;
   else if(mars_element == "air") element_impulse = 75.0;
   else if(mars_element == "earth") element_impulse = 45.0;
   else if(mars_element == "water") element_impulse = 50.0;

   double modality_impulse = 50.0;
   if(mars_modality == "cardinal") modality_impulse = 95.0;
   else if(mars_modality == "fixed") modality_impulse = 70.0;
   else if(mars_modality == "mutable") modality_impulse = 55.0;

   double bias_bonus = 0.0;
   if(StringFind(element_bias, "fire") >= 0 || StringFind(element_bias, "air") >= 0) bias_bonus += 8.0;
   if(StringFind(modality_bias, "cardinal") >= 0) bias_bonus += 8.0;

   double moon_tempo = DAL_AstroPM_SpeedScore(row.body[moon]);

   double score = 0.42 * mars_energy + 0.20 * element_impulse + 0.16 * modality_impulse + 0.17 * moon_tempo + bias_bonus;
   return DAL_AstroPM_Clamp(score);
}

double DAL_AstroPM_FrictionScore(
   const DAL_AstroMapRow &row,
   const double pressure_score,
   const double saturn_drag_score,
   const double mercury_disturbance_score,
   const double transition_score
)
{
   double score = 0.38 * saturn_drag_score +
                  0.22 * mercury_disturbance_score +
                  0.20 * pressure_score +
                  0.20 * transition_score;
   return DAL_AstroPM_Clamp(score);
}

// -------------------------
// Composite scores
// -------------------------

string DAL_AstroPM_RegimeFromScores(const DAL_AstroPathMetrics &m)
{
   if(m.clean_path_score >= 70.0 && m.flow_score >= 60.0 && m.friction_score <= 40.0)
      return "clean_flow";

   if(m.clean_impulse_score >= 70.0 && m.impulse_score >= 65.0 && m.friction_score <= 45.0)
      return "clean_impulse";

   if(m.impulse_score >= 70.0 && m.pressure_score >= 65.0 && m.friction_score >= 55.0)
      return "dirty_impulse";

   if(m.friction_score >= 65.0 && m.saturn_drag_score >= 60.0)
      return "drag_chop";

   if(m.transition_score >= 65.0)
      return "transition";

   if(m.flow_score >= 55.0 && m.impulse_score < 45.0)
      return "soft_flow";

   return "neutral";
}

void DAL_AstroPathMetrics_Reset(DAL_AstroPathMetrics &m)
{
   m.valid = false;
   m.broker_time = 0;
   m.utc_time = 0;

   m.flow_score = 0.0;
   m.impulse_score = 0.0;
   m.friction_score = 0.0;
   m.pressure_score = 0.0;
   m.transition_score = 0.0;
   m.moon_tempo_score = 0.0;
   m.saturn_drag_score = 0.0;
   m.mercury_disturbance_score = 0.0;

   m.clean_path_score = 0.0;
   m.clean_impulse_score = 0.0;
   m.smooth_continuation_score = 0.0;
   m.breakout_followthrough_score = 0.0;
   m.pullback_risk_score = 0.0;
   m.chop_risk_score = 0.0;

   m.flow_bucket = "low";
   m.impulse_bucket = "low";
   m.friction_bucket = "low";
   m.pressure_bucket = "low";
   m.transition_bucket = "low";
   m.moon_tempo_bucket = "low";
   m.saturn_drag_bucket = "low";
   m.clean_path_bucket = "low";
   m.pullback_risk_bucket = "low";
   m.chop_risk_bucket = "low";
   m.astro_path_regime = "neutral";

   m.element_bias = "unknown";
   m.modality_bias = "unknown";
   m.moon_phase_group = "unknown";
   m.moon_decl_zone = "unknown";
   m.mars_state = "unknown";
   m.saturn_state = "unknown";
   m.mercury_state = "unknown";
   m.sun_moon_state = "unknown";
   m.moon_mars_state = "unknown";
   m.moon_saturn_state = "unknown";
   m.venus_mars_state = "unknown";
   m.mars_saturn_state = "unknown";
   m.jupiter_saturn_state = "unknown";

   m.astro_path_key = "";
   m.clean_gate_key = "";
   m.diagnostic_key = "";
   m.thesis = "";
   m.warning = "";
}

bool DAL_AstroPathMetrics_Calc(const DAL_AstroMapRow &row, DAL_AstroPathMetrics &m)
{
   DAL_AstroPathMetrics_Reset(m);
   m.valid = true;
   m.broker_time = row.broker_time;
   m.utc_time = row.utc_time;

   int moon = DAL_AstroBodyIndexByName("moon");
   int mars = DAL_AstroBodyIndexByName("mars");
   int saturn = DAL_AstroBodyIndexByName("saturn");
   int mercury = DAL_AstroBodyIndexByName("mercury");
   if(moon < 0 || mars < 0 || saturn < 0 || mercury < 0)
      return false;

   m.element_bias = DAL_AstroPM_ElementBias(row);
   m.modality_bias = DAL_AstroPM_ModalityBias(row);
   m.moon_phase_group = DAL_AstroPM_MoonPhaseGroup(row.moon_phase_bucket);
   m.moon_decl_zone = DAL_AstroDF_DeclinationZone(row.body[moon]);
   m.mars_state = DAL_AstroPM_BodyStateText(row.body[mars]);
   m.saturn_state = DAL_AstroPM_BodyStateText(row.body[saturn]);
   m.mercury_state = DAL_AstroPM_BodyStateText(row.body[mercury]);

   m.sun_moon_state = DAL_AstroPM_AspectStateText(row, "sun_moon");
   m.moon_mars_state = DAL_AstroPM_AspectStateText(row, "moon_mars");
   m.moon_saturn_state = DAL_AstroPM_AspectStateText(row, "moon_saturn");
   m.venus_mars_state = DAL_AstroPM_AspectStateText(row, "venus_mars");
   m.mars_saturn_state = DAL_AstroPM_AspectStateText(row, "mars_saturn");
   m.jupiter_saturn_state = DAL_AstroPM_AspectStateText(row, "jupiter_saturn");

   m.flow_score = DAL_AstroPM_FlowScore(row);
   m.pressure_score = DAL_AstroPM_PressureScore(row);
   m.moon_tempo_score = DAL_AstroPM_MoonTempoScore(row);
   m.mercury_disturbance_score = DAL_AstroPM_MercuryDisturbanceScore(row);
   m.saturn_drag_score = DAL_AstroPM_SaturnDragScore(row);
   m.transition_score = DAL_AstroPM_TransitionScore(row);
   m.impulse_score = DAL_AstroPM_ImpulseScore(row, m.element_bias, m.modality_bias);
   m.friction_score = DAL_AstroPM_FrictionScore(row, m.pressure_score, m.saturn_drag_score, m.mercury_disturbance_score, m.transition_score);

   double low_friction = 100.0 - m.friction_score;
   double low_transition = 100.0 - m.transition_score;
   double low_saturn_drag = 100.0 - m.saturn_drag_score;
   double low_chop = 100.0 - m.chop_risk_score;
   double pressure_balance = DAL_AstroPM_Clamp(100.0 - MathAbs(m.pressure_score - 45.0) * 1.60);

   m.clean_path_score = DAL_AstroPM_Clamp(
      0.30 * m.flow_score +
      0.22 * m.impulse_score +
      0.22 * low_friction +
      0.10 * pressure_balance +
      0.10 * low_transition +
      0.06 * low_saturn_drag
   );

   m.clean_impulse_score = DAL_AstroPM_Clamp(
      0.42 * m.impulse_score +
      0.20 * m.flow_score +
      0.20 * low_friction +
      0.10 * pressure_balance +
      0.08 * low_transition
   );

   m.smooth_continuation_score = DAL_AstroPM_Clamp(
      0.45 * m.flow_score +
      0.20 * m.impulse_score +
      0.20 * low_friction +
      0.10 * low_saturn_drag +
      0.05 * low_transition
   );

   m.breakout_followthrough_score = DAL_AstroPM_Clamp(
      0.45 * m.impulse_score +
      0.18 * m.pressure_score +
      0.17 * m.moon_tempo_score +
      0.20 * low_friction
   );

   m.pullback_risk_score = DAL_AstroPM_Clamp(
      0.34 * m.friction_score +
      0.24 * m.pressure_score +
      0.18 * m.saturn_drag_score +
      0.14 * m.transition_score +
      0.10 * m.mercury_disturbance_score
   );

   m.chop_risk_score = DAL_AstroPM_Clamp(
      0.34 * m.friction_score +
      0.24 * m.transition_score +
      0.20 * m.saturn_drag_score +
      0.22 * (100.0 - m.flow_score)
   );

   m.flow_bucket = DAL_AstroPM_Bucket3(m.flow_score);
   m.impulse_bucket = DAL_AstroPM_Bucket3(m.impulse_score);
   m.friction_bucket = DAL_AstroPM_Bucket3(m.friction_score);
   m.pressure_bucket = DAL_AstroPM_Bucket3(m.pressure_score);
   m.transition_bucket = DAL_AstroPM_Bucket3(m.transition_score);
   m.moon_tempo_bucket = DAL_AstroPM_Bucket3(m.moon_tempo_score);
   m.saturn_drag_bucket = DAL_AstroPM_Bucket3(m.saturn_drag_score);
   m.clean_path_bucket = DAL_AstroPM_Bucket5(m.clean_path_score);
   m.pullback_risk_bucket = DAL_AstroPM_Bucket5(m.pullback_risk_score);
   m.chop_risk_bucket = DAL_AstroPM_Bucket5(m.chop_risk_score);
   m.astro_path_regime = DAL_AstroPM_RegimeFromScores(m);

   m.astro_path_key = "astro_path=" +
      "flow_" + m.flow_bucket +
      "|impulse_" + m.impulse_bucket +
      "|friction_" + m.friction_bucket +
      "|pressure_" + m.pressure_bucket +
      "|transition_" + m.transition_bucket +
      "|moon_" + m.moon_tempo_bucket +
      "|saturn_drag_" + m.saturn_drag_bucket +
      "|regime_" + m.astro_path_regime;

   m.clean_gate_key = "clean_gate=" +
      "clean_" + m.clean_path_bucket +
      "|pb_" + m.pullback_risk_bucket +
      "|chop_" + m.chop_risk_bucket +
      "|ms_" + m.mars_saturn_state +
      "|sm_" + m.sun_moon_state +
      "|elem_" + m.element_bias +
      "|mod_" + m.modality_bias;

   m.diagnostic_key = "astro_diag=" +
      "phase_" + m.moon_phase_group +
      "|moon_decl_" + m.moon_decl_zone +
      "|mars_" + m.mars_state +
      "|saturn_" + m.saturn_state +
      "|mercury_" + m.mercury_state +
      "|moon_mars_" + m.moon_mars_state +
      "|moon_saturn_" + m.moon_saturn_state +
      "|venus_mars_" + m.venus_mars_state +
      "|jupiter_saturn_" + m.jupiter_saturn_state;

   if(m.clean_path_score >= 70.0)
      m.thesis = "PATH THESIS: cleaner-than-normal candidate. Use only as a filter, never as a standalone direction signal.";
   else if(m.pullback_risk_score >= 70.0 || m.chop_risk_score >= 70.0)
      m.thesis = "PATH THESIS: dirty-path risk. Expect deeper pullbacks, chop, or delayed follow-through unless market evidence says otherwise.";
   else
      m.thesis = "PATH THESIS: neutral/mixed. Let Distribution Engineering decide if this state has real lift.";

   m.warning = "No causality claim. Validate with MAE_R, pullback_depth_R, path_efficiency, and out-of-sample sequence lift.";
   return true;
}

// -------------------------
// Display helpers
// -------------------------

string DAL_AstroPM_ScoreLine(const string name, const double score, const string bucket, const string meaning)
{
   return StringFormat("%-15s %6.1f  %-9s  %s", name, score, bucket, meaning);
}

string DAL_AstroPM_BodyLine(const DAL_AstroMapRow &row, const string body_name)
{
   int idx = DAL_AstroBodyIndexByName(body_name);
   if(idx < 0)
      return body_name + ": missing";

   DAL_AstroBodyState b = row.body[idx];
   return StringFormat("%-8s %-11s %5.1f deg  spd=%8.4f  %-8s decl=%7.2f %-10s",
      body_name,
      b.sign,
      b.degree,
      b.speed_lon,
      DAL_AstroPM_BodyStateText(b),
      b.decl,
      DAL_AstroDF_DeclinationZone(b)
   );
}

string DAL_AstroPM_AspectLine(const DAL_AstroMapRow &row, const string pair_name)
{
   int idx = DAL_AstroAspectIndexByName(pair_name);
   if(idx < 0)
      return pair_name + ": missing";

   DAL_AstroAspectState a = row.aspect[idx];
   return StringFormat("%-15s angle=%7.2f  %-11s orb=%5.2f  %-3s  strength=%5.1f",
      pair_name,
      a.angle,
      a.aspect,
      a.orb,
      DAL_AstroPM_AppSep(a.applying),
      DAL_AstroPM_AspectStrength(a, 6.0)
   );
}

string DAL_AstroPM_ToScreenText(const DAL_AstroMapRow &row, const DAL_AstroPathMetrics &m, const bool show_raw = true, const bool show_keys = true)
{
   string t = "";
   t += "EXP0013 ASTRO PATH CLEANLINESS METRICS\n";
   t += "---------------------------------------\n";
   t += "Broker: " + TimeToString(row.broker_time, TIME_DATE | TIME_MINUTES) + "   UTC: " + TimeToString(row.utc_time, TIME_DATE | TIME_MINUTES) + "   JD: " + DoubleToString(row.jd_ut, 5) + "\n";
   t += "Moon phase: " + row.moon_phase_bucket + "  angle=" + DoubleToString(row.moon_phase_angle, 2) + "  illum_proxy=" + DoubleToString(row.moon_illumination_proxy, 3) + "\n";
   t += "Bias: element=" + m.element_bias + "  modality=" + m.modality_bias + "  regime=" + m.astro_path_regime + "\n";
   t += "\n";

   t += "PATH AXES 0..100  [interpretation for clean movement, not direction]\n";
   t += DAL_AstroPM_ScoreLine("Flow",       m.flow_score,       m.flow_bucket,       "soft geometry / smooth continuation potential") + "\n";
   t += DAL_AstroPM_ScoreLine("Impulse",    m.impulse_score,    m.impulse_bucket,    "movement force / breakout energy") + "\n";
   t += DAL_AstroPM_ScoreLine("Friction",   m.friction_score,   m.friction_bucket,   "drag / delay / dirty pullback risk") + "\n";
   t += DAL_AstroPM_ScoreLine("Pressure",   m.pressure_score,   m.pressure_bucket,   "hard geometry / volatility pressure") + "\n";
   t += DAL_AstroPM_ScoreLine("Transition", m.transition_score, m.transition_bucket, "station/ingress/phase-boundary regime change") + "\n";
   t += DAL_AstroPM_ScoreLine("MoonTempo",  m.moon_tempo_score, m.moon_tempo_bucket, "short-term timing speed") + "\n";
   t += DAL_AstroPM_ScoreLine("SaturnDrag", m.saturn_drag_score,m.saturn_drag_bucket,"structural resistance / delay") + "\n";
   t += "\n";

   t += "COMPOSITE PATH SCORES 0..100\n";
   t += DAL_AstroPM_ScoreLine("CleanPath",  m.clean_path_score, DAL_AstroPM_Bucket5(m.clean_path_score), "higher = low-pullback candidate") + "\n";
   t += DAL_AstroPM_ScoreLine("CleanImpulse",m.clean_impulse_score,DAL_AstroPM_Bucket5(m.clean_impulse_score),"higher = impulse with controlled friction") + "\n";
   t += DAL_AstroPM_ScoreLine("SmoothCont", m.smooth_continuation_score,DAL_AstroPM_Bucket5(m.smooth_continuation_score),"higher = smoother continuation candidate") + "\n";
   t += DAL_AstroPM_ScoreLine("BreakoutFT", m.breakout_followthrough_score,DAL_AstroPM_Bucket5(m.breakout_followthrough_score),"higher = breakout follow-through candidate") + "\n";
   t += DAL_AstroPM_ScoreLine("PullbackRisk",m.pullback_risk_score,m.pullback_risk_bucket,"higher = deeper adverse excursion risk") + "\n";
   t += DAL_AstroPM_ScoreLine("ChopRisk",   m.chop_risk_score, m.chop_risk_bucket,  "higher = range/fake-move risk") + "\n";
   t += "\n";

   t += m.thesis + "\n";
   t += m.warning + "\n";

   if(show_raw)
   {
      t += "\nKEY BODIES\n";
      t += DAL_AstroPM_BodyLine(row, "sun") + "\n";
      t += DAL_AstroPM_BodyLine(row, "moon") + "\n";
      t += DAL_AstroPM_BodyLine(row, "mercury") + "\n";
      t += DAL_AstroPM_BodyLine(row, "venus") + "\n";
      t += DAL_AstroPM_BodyLine(row, "mars") + "\n";
      t += DAL_AstroPM_BodyLine(row, "jupiter") + "\n";
      t += DAL_AstroPM_BodyLine(row, "saturn") + "\n";

      t += "\nKEY ASPECTS\n";
      t += DAL_AstroPM_AspectLine(row, "sun_moon") + "\n";
      t += DAL_AstroPM_AspectLine(row, "moon_mars") + "\n";
      t += DAL_AstroPM_AspectLine(row, "moon_saturn") + "\n";
      t += DAL_AstroPM_AspectLine(row, "venus_mars") + "\n";
      t += DAL_AstroPM_AspectLine(row, "mars_saturn") + "\n";
      t += DAL_AstroPM_AspectLine(row, "jupiter_saturn") + "\n";
   }

   if(show_keys)
   {
      t += "\nFEATURE KEYS\n";
      t += m.astro_path_key + "\n";
      t += m.clean_gate_key + "\n";
      t += m.diagnostic_key + "\n";
   }

   return t;
}

void DAL_AstroPM_DeletePanel(const long chart_id, const string prefix)
{
   for(int i = 0; i < DAL_ASTRO_PM_MAX_LINES; i++)
      ObjectDelete(chart_id, prefix + "_ASTRO_PM_LINE_" + IntegerToString(i));
}

void DAL_AstroPM_DrawLine(
   const long chart_id,
   const string name,
   const string text,
   const int x,
   const int y,
   const color clr,
   const int font_size
)
{
   if(ObjectFind(chart_id, name) < 0)
      ObjectCreate(chart_id, name, OBJ_LABEL, 0, 0, 0);

   ObjectSetInteger(chart_id, name, OBJPROP_CORNER, CORNER_LEFT_UPPER);
   ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, font_size);
   ObjectSetString(chart_id, name, OBJPROP_FONT, "Consolas");
   ObjectSetInteger(chart_id, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(chart_id, name, OBJPROP_HIDDEN, true);
   ObjectSetString(chart_id, name, OBJPROP_TEXT, text);
}

void DAL_AstroPM_DrawPanel(
   const long chart_id,
   const string prefix,
   const string text,
   const int x = 10,
   const int y = 20,
   const color clr = clrWhite,
   const int font_size = 8,
   const int line_height = 14,
   const bool clear_old = true
)
{
   if(clear_old)
      DAL_AstroPM_DeletePanel(chart_id, prefix);

   string lines[];
   ushort sep = StringGetCharacter("\n", 0);
   int n = StringSplit(text, sep, lines);
   if(n <= 0)
      return;

   int max_lines = MathMin(n, DAL_ASTRO_PM_MAX_LINES);
   for(int i = 0; i < max_lines; i++)
   {
      color line_clr = clr;
      if(StringFind(lines[i], "PATH THESIS") >= 0) line_clr = clrAqua;
      if(StringFind(lines[i], "WARNING") >= 0 || StringFind(lines[i], "No causality") >= 0) line_clr = clrGold;
      if(StringFind(lines[i], "NOT FOUND") >= 0 || StringFind(lines[i], "MISMATCH") >= 0) line_clr = clrTomato;

      DAL_AstroPM_DrawLine(chart_id, prefix + "_ASTRO_PM_LINE_" + IntegerToString(i), lines[i], x, y + i * line_height, line_clr, font_size);
   }
}

#endif
