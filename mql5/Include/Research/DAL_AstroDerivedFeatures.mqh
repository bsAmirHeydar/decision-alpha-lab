#ifndef __DAL_ASTRO_DERIVED_FEATURES_MQH__
#define __DAL_ASTRO_DERIVED_FEATURES_MQH__

#include <Research/DAL_AstroExcelCandleReader.mqh>

// Decision Alpha Lab - Astro Derived Features
// Converts raw sky-map fields into explicit, testable Distribution Engineering feature keys.
// No causal claim is made. Every feature is a causal time-state available at candle open.

string DAL_AstroDF_KeyAppend(string base_key, const string name, const string value)
{
   if(base_key == "")
      return name + "=" + value;
   return base_key + "|" + name + "=" + value;
}

string DAL_AstroDF_SignElement(const string sign)
{
   if(sign == "aries" || sign == "leo" || sign == "sagittarius") return "fire";
   if(sign == "taurus" || sign == "virgo" || sign == "capricorn") return "earth";
   if(sign == "gemini" || sign == "libra" || sign == "aquarius") return "air";
   if(sign == "cancer" || sign == "scorpio" || sign == "pisces") return "water";
   return "unknown";
}

string DAL_AstroDF_SignModality(const string sign)
{
   if(sign == "aries" || sign == "cancer" || sign == "libra" || sign == "capricorn") return "cardinal";
   if(sign == "taurus" || sign == "leo" || sign == "scorpio" || sign == "aquarius") return "fixed";
   if(sign == "gemini" || sign == "virgo" || sign == "sagittarius" || sign == "pisces") return "mutable";
   return "unknown";
}

string DAL_AstroDF_DegreeZone(const double degree)
{
   if(degree < 10.0) return "early";
   if(degree < 20.0) return "mid";
   return "late";
}

string DAL_AstroDF_OrbBucket(const double orb)
{
   if(orb <= 1.0) return "tight";
   if(orb <= 3.0) return "close";
   if(orb <= 6.0) return "wide";
   return "none";
}

string DAL_AstroDF_AspectClass(const string aspect)
{
   if(aspect == "conjunction") return "fusion";
   if(aspect == "square" || aspect == "opposition") return "tension";
   if(aspect == "trine" || aspect == "sextile") return "flow";
   return "none";
}

double DAL_AstroDF_StationEpsilon(const string body_name)
{
   if(body_name == "mercury") return 0.08;
   if(body_name == "venus")   return 0.04;
   if(body_name == "mars")    return 0.025;
   if(body_name == "jupiter") return 0.010;
   if(body_name == "saturn")  return 0.006;
   if(body_name == "uranus")  return 0.003;
   if(body_name == "neptune") return 0.002;
   if(body_name == "pluto")   return 0.002;
   return 0.0;
}

string DAL_AstroDF_SpeedState(const DAL_AstroBodyState &b)
{
   double abs_speed = MathAbs(b.speed_lon);
   double eps = DAL_AstroDF_StationEpsilon(b.name);
   if(eps > 0.0 && abs_speed <= eps)
      return "station";
   if(b.retro == 1)
      return "retro";
   return "direct";
}

string DAL_AstroDF_DeclinationZone(const DAL_AstroBodyState &b)
{
   double d = b.decl;
   if(MathAbs(d) >= 23.44)
      return (d > 0.0 ? "north_oob" : "south_oob");
   if(d >= 5.0)
      return "north";
   if(d <= -5.0)
      return "south";
   return "equator";
}

string DAL_AstroDF_PhaseHalf(const string moon_phase_bucket)
{
   if(StringFind(moon_phase_bucket, "waxing") >= 0 || moon_phase_bucket == "first_quarter") return "waxing";
   if(StringFind(moon_phase_bucket, "waning") >= 0 || moon_phase_bucket == "last_quarter") return "waning";
   if(moon_phase_bucket == "new") return "new";
   if(moon_phase_bucket == "full") return "full";
   return "unknown";
}

string DAL_AstroDF_AppendBodyCore(string key, const DAL_AstroMapRow &row, const string body_name)
{
   int idx = DAL_AstroBodyIndexByName(body_name);
   if(idx < 0)
      return key;

   DAL_AstroBodyState b = row.body[idx];
   key = DAL_AstroDF_KeyAppend(key, body_name + "_sign", b.sign);
   key = DAL_AstroDF_KeyAppend(key, body_name + "_element", DAL_AstroDF_SignElement(b.sign));
   key = DAL_AstroDF_KeyAppend(key, body_name + "_modality", DAL_AstroDF_SignModality(b.sign));
   key = DAL_AstroDF_KeyAppend(key, body_name + "_degree_zone", DAL_AstroDF_DegreeZone(b.degree));
   key = DAL_AstroDF_KeyAppend(key, body_name + "_speed_state", DAL_AstroDF_SpeedState(b));
   key = DAL_AstroDF_KeyAppend(key, body_name + "_decl_zone", DAL_AstroDF_DeclinationZone(b));
   return key;
}

string DAL_AstroDF_AppendAspectCore(string key, const DAL_AstroMapRow &row, const string pair_name, const double max_orb = 6.0)
{
   int idx = DAL_AstroAspectIndexByName(pair_name);
   if(idx < 0)
      return key;

   DAL_AstroAspectState a = row.aspect[idx];
   if(a.orb > max_orb)
   {
      key = DAL_AstroDF_KeyAppend(key, pair_name + "_aspect", "none");
      return key;
   }

   key = DAL_AstroDF_KeyAppend(key, pair_name + "_aspect", a.aspect);
   key = DAL_AstroDF_KeyAppend(key, pair_name + "_aspect_class", DAL_AstroDF_AspectClass(a.aspect));
   key = DAL_AstroDF_KeyAppend(key, pair_name + "_orb", DAL_AstroDF_OrbBucket(a.orb));
   key = DAL_AstroDF_KeyAppend(key, pair_name + "_motion", (a.applying == 1 ? "applying" : "separating"));
   return key;
}

string DAL_AstroDF_BuildResearchKey(const DAL_AstroMapRow &row)
{
   string key = "";

   key = DAL_AstroDF_KeyAppend(key, "moon_phase", row.moon_phase_bucket);
   key = DAL_AstroDF_KeyAppend(key, "moon_phase_half", DAL_AstroDF_PhaseHalf(row.moon_phase_bucket));

   key = DAL_AstroDF_AppendBodyCore(key, row, "sun");
   key = DAL_AstroDF_AppendBodyCore(key, row, "moon");
   key = DAL_AstroDF_AppendBodyCore(key, row, "mercury");
   key = DAL_AstroDF_AppendBodyCore(key, row, "venus");
   key = DAL_AstroDF_AppendBodyCore(key, row, "mars");
   key = DAL_AstroDF_AppendBodyCore(key, row, "jupiter");
   key = DAL_AstroDF_AppendBodyCore(key, row, "saturn");

   key = DAL_AstroDF_AppendAspectCore(key, row, "sun_moon", 6.0);
   key = DAL_AstroDF_AppendAspectCore(key, row, "moon_mars", 6.0);
   key = DAL_AstroDF_AppendAspectCore(key, row, "venus_mars", 6.0);
   key = DAL_AstroDF_AppendAspectCore(key, row, "mars_saturn", 6.0);
   key = DAL_AstroDF_AppendAspectCore(key, row, "jupiter_saturn", 6.0);

   return key;
}

string DAL_AstroDF_BuildCompactExecutionKey(const DAL_AstroMapRow &row)
{
   // Smaller key for live filters so sample size does not collapse too quickly.
   string key = "";
   int mars = DAL_AstroBodyIndexByName("mars");
   int saturn = DAL_AstroBodyIndexByName("saturn");
   int moon = DAL_AstroBodyIndexByName("moon");

   key = DAL_AstroDF_KeyAppend(key, "moon_phase_half", DAL_AstroDF_PhaseHalf(row.moon_phase_bucket));
   key = DAL_AstroDF_KeyAppend(key, "moon_element", DAL_AstroDF_SignElement(row.body[moon].sign));
   key = DAL_AstroDF_KeyAppend(key, "mars_speed_state", DAL_AstroDF_SpeedState(row.body[mars]));
   key = DAL_AstroDF_KeyAppend(key, "saturn_speed_state", DAL_AstroDF_SpeedState(row.body[saturn]));
   key = DAL_AstroDF_AppendAspectCore(key, row, "mars_saturn", 6.0);
   key = DAL_AstroDF_AppendAspectCore(key, row, "sun_moon", 6.0);
   return key;
}

string DAL_AstroDF_AppendToDistributionKey(const string execution_key, const DAL_AstroMapRow &row, const bool compact = true)
{
   string astro_key = compact ? DAL_AstroDF_BuildCompactExecutionKey(row) : DAL_AstroDF_BuildResearchKey(row);
   if(execution_key == "")
      return "astro{" + astro_key + "}";
   return execution_key + "|astro{" + astro_key + "}";
}

#endif
