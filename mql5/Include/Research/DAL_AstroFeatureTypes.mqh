#ifndef __DAL_ASTRO_FEATURE_TYPES_MQH__
#define __DAL_ASTRO_FEATURE_TYPES_MQH__

// Decision Alpha Lab - Astro Feature Types
// MQL5 execution-side structures for candle-aligned astrological feature rows.

struct DAL_AstroFeatureRow
{
   datetime broker_time;
   datetime utc_time;
   double   jd_ut;

   string   feature_key;
   string   summary;

   double   moon_phase_angle;
   double   moon_illumination_proxy;
   string   moon_phase_bucket;

   double   sun_lon;
   double   moon_lon;
   double   mercury_lon;
   double   venus_lon;
   double   mars_lon;
   double   jupiter_lon;
   double   saturn_lon;
   double   uranus_lon;
   double   neptune_lon;
   double   pluto_lon;

   string   sun_sign;
   string   moon_sign;
   string   mercury_sign;
   string   venus_sign;
   string   mars_sign;
   string   jupiter_sign;
   string   saturn_sign;

   int      mercury_retro;
   int      venus_retro;
   int      mars_retro;
   int      jupiter_retro;
   int      saturn_retro;

   double   sun_moon_angle;
   string   sun_moon_aspect;
   double   sun_moon_orb;
   int      sun_moon_applying;

   double   mars_saturn_angle;
   string   mars_saturn_aspect;
   double   mars_saturn_orb;
   int      mars_saturn_applying;

   double   venus_mars_angle;
   string   venus_mars_aspect;
   double   venus_mars_orb;
   int      venus_mars_applying;

   double   jupiter_saturn_angle;
   string   jupiter_saturn_aspect;
   double   jupiter_saturn_orb;
   int      jupiter_saturn_applying;
};

struct DAL_AstroFeatureStore
{
   bool     loaded;
   string   source_file;
   int      row_count;
   int      broker_gmt_offset_hours;
   DAL_AstroFeatureRow rows[];
};

void DAL_AstroFeatureRow_Reset(DAL_AstroFeatureRow &r)
{
   r.broker_time = 0;
   r.utc_time = 0;
   r.jd_ut = 0.0;
   r.feature_key = "";
   r.summary = "";
   r.moon_phase_angle = 0.0;
   r.moon_illumination_proxy = 0.0;
   r.moon_phase_bucket = "";

   r.sun_lon = 0.0;
   r.moon_lon = 0.0;
   r.mercury_lon = 0.0;
   r.venus_lon = 0.0;
   r.mars_lon = 0.0;
   r.jupiter_lon = 0.0;
   r.saturn_lon = 0.0;
   r.uranus_lon = 0.0;
   r.neptune_lon = 0.0;
   r.pluto_lon = 0.0;

   r.sun_sign = "";
   r.moon_sign = "";
   r.mercury_sign = "";
   r.venus_sign = "";
   r.mars_sign = "";
   r.jupiter_sign = "";
   r.saturn_sign = "";

   r.mercury_retro = 0;
   r.venus_retro = 0;
   r.mars_retro = 0;
   r.jupiter_retro = 0;
   r.saturn_retro = 0;

   r.sun_moon_angle = 0.0;
   r.sun_moon_aspect = "";
   r.sun_moon_orb = 0.0;
   r.sun_moon_applying = 0;

   r.mars_saturn_angle = 0.0;
   r.mars_saturn_aspect = "";
   r.mars_saturn_orb = 0.0;
   r.mars_saturn_applying = 0;

   r.venus_mars_angle = 0.0;
   r.venus_mars_aspect = "";
   r.venus_mars_orb = 0.0;
   r.venus_mars_applying = 0;

   r.jupiter_saturn_angle = 0.0;
   r.jupiter_saturn_aspect = "";
   r.jupiter_saturn_orb = 0.0;
   r.jupiter_saturn_applying = 0;
}

void DAL_AstroFeatureStore_Reset(DAL_AstroFeatureStore &s)
{
   s.loaded = false;
   s.source_file = "";
   s.row_count = 0;
   s.broker_gmt_offset_hours = 0;
   ArrayResize(s.rows, 0);
}

#endif
