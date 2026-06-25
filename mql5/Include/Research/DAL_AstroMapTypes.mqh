#ifndef __DAL_ASTRO_MAP_TYPES_MQH__
#define __DAL_ASTRO_MAP_TYPES_MQH__

// Decision Alpha Lab - Full Astro Map Types
// Full candle-aligned sky-map structures loaded from Python-generated CSV.
// Runtime rule: MQL5 reads the CSV mirror. The .xlsx workbook is for human inspection.

#define DAL_ASTRO_BODY_COUNT        12
#define DAL_ASTRO_ASPECT_PAIR_COUNT 15

struct DAL_AstroBodyState
{
   string name;
   double lon;
   double lat;
   double dist;
   double speed_lon;
   double speed_lat;
   double speed_dist;
   double ra;
   double decl;
   string sign;
   int    sign_index;
   double degree;
   int    retro;
};

struct DAL_AstroAspectState
{
   string pair;
   double angle;
   string aspect;
   double orb;
   int    applying;
};

struct DAL_AstroMapRow
{
   datetime broker_time;
   datetime utc_time;
   long     unix_utc;
   double   jd_ut;

   string   feature_key;
   string   summary;

   double   moon_phase_angle;
   string   moon_phase_bucket;
   double   moon_illumination_proxy;

   DAL_AstroBodyState   body[DAL_ASTRO_BODY_COUNT];
   DAL_AstroAspectState aspect[DAL_ASTRO_ASPECT_PAIR_COUNT];
};

struct DAL_AstroMapStore
{
   bool     loaded;
   string   source_file;
   int      row_count;
   double   broker_gmt_offset_hours;
   int      timeframe_minutes;
   DAL_AstroMapRow rows[];

   // Runtime diagnostics. These fields make it explicit whether the failure is
   // caused by the file path, an unreadable/empty file, a bad header, bad rows,
   // or a timestamp lookup mismatch after a successful load.
   string   load_stage;
   string   load_error;
   int      file_open_error;
   int      header_columns;
   string   header_line;
   string   first_data_line;
   int      physical_lines;
   int      empty_lines;
   int      split_failed_lines;
   int      parse_failed_lines;
   int      skipped_lines;
   datetime first_broker_time;
   datetime last_broker_time;
   datetime first_utc_time;
   datetime last_utc_time;
};

string DAL_AstroBodyName(const int index)
{
   if(index == 0)  return "sun";
   if(index == 1)  return "moon";
   if(index == 2)  return "mercury";
   if(index == 3)  return "venus";
   if(index == 4)  return "mars";
   if(index == 5)  return "jupiter";
   if(index == 6)  return "saturn";
   if(index == 7)  return "uranus";
   if(index == 8)  return "neptune";
   if(index == 9)  return "pluto";
   if(index == 10) return "true_node";
   if(index == 11) return "mean_node";
   return "unknown";
}

string DAL_AstroAspectPairName(const int index)
{
   if(index == 0)  return "sun_moon";
   if(index == 1)  return "sun_mercury";
   if(index == 2)  return "sun_venus";
   if(index == 3)  return "sun_mars";
   if(index == 4)  return "sun_jupiter";
   if(index == 5)  return "sun_saturn";
   if(index == 6)  return "moon_mercury";
   if(index == 7)  return "moon_venus";
   if(index == 8)  return "moon_mars";
   if(index == 9)  return "moon_jupiter";
   if(index == 10) return "moon_saturn";
   if(index == 11) return "mercury_venus";
   if(index == 12) return "venus_mars";
   if(index == 13) return "mars_saturn";
   if(index == 14) return "jupiter_saturn";
   return "unknown_unknown";
}

int DAL_AstroBodyIndexByName(const string name)
{
   for(int i = 0; i < DAL_ASTRO_BODY_COUNT; i++)
   {
      if(DAL_AstroBodyName(i) == name)
         return i;
   }
   return -1;
}

int DAL_AstroAspectIndexByName(const string pair)
{
   for(int i = 0; i < DAL_ASTRO_ASPECT_PAIR_COUNT; i++)
   {
      if(DAL_AstroAspectPairName(i) == pair)
         return i;
   }
   return -1;
}

void DAL_AstroBodyState_Reset(DAL_AstroBodyState &b, const string name)
{
   b.name = name;
   b.lon = 0.0;
   b.lat = 0.0;
   b.dist = 0.0;
   b.speed_lon = 0.0;
   b.speed_lat = 0.0;
   b.speed_dist = 0.0;
   b.ra = 0.0;
   b.decl = 0.0;
   b.sign = "";
   b.sign_index = -1;
   b.degree = 0.0;
   b.retro = 0;
}

void DAL_AstroAspectState_Reset(DAL_AstroAspectState &a, const string pair)
{
   a.pair = pair;
   a.angle = 0.0;
   a.aspect = "none";
   a.orb = 999.0;
   a.applying = 0;
}

void DAL_AstroMapRow_Reset(DAL_AstroMapRow &r)
{
   r.broker_time = 0;
   r.utc_time = 0;
   r.unix_utc = 0;
   r.jd_ut = 0.0;
   r.feature_key = "";
   r.summary = "";
   r.moon_phase_angle = 0.0;
   r.moon_phase_bucket = "";
   r.moon_illumination_proxy = 0.0;

   for(int i = 0; i < DAL_ASTRO_BODY_COUNT; i++)
      DAL_AstroBodyState_Reset(r.body[i], DAL_AstroBodyName(i));

   for(int j = 0; j < DAL_ASTRO_ASPECT_PAIR_COUNT; j++)
      DAL_AstroAspectState_Reset(r.aspect[j], DAL_AstroAspectPairName(j));
}

void DAL_AstroMapStore_Reset(DAL_AstroMapStore &s)
{
   s.loaded = false;
   s.source_file = "";
   s.row_count = 0;
   s.broker_gmt_offset_hours = 0.0;
   s.timeframe_minutes = 0;
   ArrayResize(s.rows, 0);

   s.load_stage = "RESET";
   s.load_error = "";
   s.file_open_error = 0;
   s.header_columns = 0;
   s.header_line = "";
   s.first_data_line = "";
   s.physical_lines = 0;
   s.empty_lines = 0;
   s.split_failed_lines = 0;
   s.parse_failed_lines = 0;
   s.skipped_lines = 0;
   s.first_broker_time = 0;
   s.last_broker_time = 0;
   s.first_utc_time = 0;
   s.last_utc_time = 0;
}

#endif
