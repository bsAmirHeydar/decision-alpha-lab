#ifndef __DAL_ASTRO_DISTRIBUTION_ADAPTER_MQH__
#define __DAL_ASTRO_DISTRIBUTION_ADAPTER_MQH__

#include <Research/DAL_AstroFeatureStore.mqh>

// Adapter between Astro Feature Store and Distribution Engineering feature keys.
// This file has no trading logic and sends no orders.

string DAL_Astro_KeyAppend(string base_key, const string name, const string value)
{
   if(base_key == "")
      return name + "=" + value;
   return base_key + "|" + name + "=" + value;
}

string DAL_Astro_KeyAppendDoubleBucket(
   string base_key,
   const string name,
   const double value,
   const double low_thr,
   const double high_thr
)
{
   string b = "mid";
   if(value <= low_thr)
      b = "low";
   else if(value >= high_thr)
      b = "high";
   return DAL_Astro_KeyAppend(base_key, name, b);
}

string DAL_Astro_BuildCompactFeatureKey(const DAL_AstroFeatureRow &r)
{
   string key = "";
   key = DAL_Astro_KeyAppend(key, "moon_phase", r.moon_phase_bucket);
   key = DAL_Astro_KeyAppend(key, "sun_sign", r.sun_sign);
   key = DAL_Astro_KeyAppend(key, "moon_sign", r.moon_sign);
   key = DAL_Astro_KeyAppend(key, "mars_sign", r.mars_sign);
   key = DAL_Astro_KeyAppend(key, "saturn_sign", r.saturn_sign);
   key = DAL_Astro_KeyAppend(key, "mercury_retro", IntegerToString(r.mercury_retro));
   key = DAL_Astro_KeyAppend(key, "venus_retro", IntegerToString(r.venus_retro));
   key = DAL_Astro_KeyAppend(key, "mars_retro", IntegerToString(r.mars_retro));
   key = DAL_Astro_KeyAppend(key, "jupiter_retro", IntegerToString(r.jupiter_retro));
   key = DAL_Astro_KeyAppend(key, "saturn_retro", IntegerToString(r.saturn_retro));

   if(r.sun_moon_orb <= 6.0)
      key = DAL_Astro_KeyAppend(key, "sun_moon_asp", r.sun_moon_aspect);
   else
      key = DAL_Astro_KeyAppend(key, "sun_moon_asp", "none");

   if(r.mars_saturn_orb <= 6.0)
      key = DAL_Astro_KeyAppend(key, "mars_saturn_asp", r.mars_saturn_aspect);
   else
      key = DAL_Astro_KeyAppend(key, "mars_saturn_asp", "none");

   if(r.venus_mars_orb <= 6.0)
      key = DAL_Astro_KeyAppend(key, "venus_mars_asp", r.venus_mars_aspect);
   else
      key = DAL_Astro_KeyAppend(key, "venus_mars_asp", "none");

   if(r.jupiter_saturn_orb <= 6.0)
      key = DAL_Astro_KeyAppend(key, "jupiter_saturn_asp", r.jupiter_saturn_aspect);
   else
      key = DAL_Astro_KeyAppend(key, "jupiter_saturn_asp", "none");

   return key;
}

string DAL_Astro_AppendToDistributionKey(
   const string execution_key,
   const DAL_AstroFeatureRow &r,
   const bool use_full_python_key = true
)
{
   string astro_key = r.feature_key;
   if(!use_full_python_key || astro_key == "")
      astro_key = DAL_Astro_BuildCompactFeatureKey(r);

   if(execution_key == "")
      return "astro{" + astro_key + "}";

   return execution_key + "|astro{" + astro_key + "}";
}

#endif
