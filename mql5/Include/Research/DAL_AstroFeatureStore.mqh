#ifndef __DAL_ASTRO_FEATURE_STORE_MQH__
#define __DAL_ASTRO_FEATURE_STORE_MQH__

#include <Research/DAL_AstroFeatureTypes.mqh>

// Decision Alpha Lab - Astro Feature Store
// Loads Python-generated candle-aligned astrology CSV files into MQL5.
// File path is relative to the MetaTrader terminal MQL5/Files directory.

string DAL_Astro_Trim(string value)
{
   StringTrimLeft(value);
   StringTrimRight(value);
   return value;
}

string DAL_Astro_Unquote(string value)
{
   value = DAL_Astro_Trim(value);
   int n = StringLen(value);
   if(n >= 2)
   {
      if(StringSubstr(value, 0, 1) == "\"" && StringSubstr(value, n - 1, 1) == "\"")
         value = StringSubstr(value, 1, n - 2);
   }
   return value;
}

datetime DAL_Astro_ParseTime(string value)
{
   value = DAL_Astro_Unquote(value);
   StringReplace(value, "-", ".");
   return StringToTime(value);
}

int DAL_Astro_HeaderIndex(const string &headers[], const string name)
{
   int n = ArraySize(headers);
   for(int i = 0; i < n; i++)
   {
      if(headers[i] == name)
         return i;
   }
   return -1;
}

string DAL_Astro_GetString(const string &cells[], const int idx, const string fallback = "")
{
   if(idx < 0 || idx >= ArraySize(cells))
      return fallback;
   return DAL_Astro_Unquote(cells[idx]);
}

double DAL_Astro_GetDouble(const string &cells[], const int idx, const double fallback = 0.0)
{
   if(idx < 0 || idx >= ArraySize(cells))
      return fallback;
   string v = DAL_Astro_Unquote(cells[idx]);
   if(v == "")
      return fallback;
   return StringToDouble(v);
}

int DAL_Astro_GetInt(const string &cells[], const int idx, const int fallback = 0)
{
   if(idx < 0 || idx >= ArraySize(cells))
      return fallback;
   string v = DAL_Astro_Unquote(cells[idx]);
   if(v == "")
      return fallback;
   return (int)StringToInteger(v);
}

bool DAL_Astro_SplitCsvLine(const string line, string &cells[])
{
   // The Python builder intentionally avoids commas inside feature_key and summary.
   // This simple parser is therefore deterministic and fast enough for tester-side loading.
   ushort sep = StringGetCharacter(",", 0);
   int n = StringSplit(line, sep, cells);
   return (n > 0);
}

bool DAL_Astro_ReadRowFromCells(const string &headers[], const string &cells[], DAL_AstroFeatureRow &r)
{
   DAL_AstroFeatureRow_Reset(r);

   int i_broker_time = DAL_Astro_HeaderIndex(headers, "broker_time");
   int i_utc_time    = DAL_Astro_HeaderIndex(headers, "utc_time");
   int i_jd_ut       = DAL_Astro_HeaderIndex(headers, "jd_ut");
   int i_key         = DAL_Astro_HeaderIndex(headers, "feature_key");
   int i_summary     = DAL_Astro_HeaderIndex(headers, "summary");

   if(i_broker_time < 0 || i_key < 0)
      return false;

   r.broker_time = DAL_Astro_ParseTime(DAL_Astro_GetString(cells, i_broker_time));
   r.utc_time    = DAL_Astro_ParseTime(DAL_Astro_GetString(cells, i_utc_time));
   r.jd_ut       = DAL_Astro_GetDouble(cells, i_jd_ut);
   r.feature_key = DAL_Astro_GetString(cells, i_key);
   r.summary     = DAL_Astro_GetString(cells, i_summary);

   r.moon_phase_angle = DAL_Astro_GetDouble(cells, DAL_Astro_HeaderIndex(headers, "moon_phase_angle"));
   r.moon_phase_bucket = DAL_Astro_GetString(cells, DAL_Astro_HeaderIndex(headers, "moon_phase_bucket"));
   r.moon_illumination_proxy = DAL_Astro_GetDouble(cells, DAL_Astro_HeaderIndex(headers, "moon_illumination_proxy"));

   r.sun_lon     = DAL_Astro_GetDouble(cells, DAL_Astro_HeaderIndex(headers, "sun_lon"));
   r.moon_lon    = DAL_Astro_GetDouble(cells, DAL_Astro_HeaderIndex(headers, "moon_lon"));
   r.mercury_lon = DAL_Astro_GetDouble(cells, DAL_Astro_HeaderIndex(headers, "mercury_lon"));
   r.venus_lon   = DAL_Astro_GetDouble(cells, DAL_Astro_HeaderIndex(headers, "venus_lon"));
   r.mars_lon    = DAL_Astro_GetDouble(cells, DAL_Astro_HeaderIndex(headers, "mars_lon"));
   r.jupiter_lon = DAL_Astro_GetDouble(cells, DAL_Astro_HeaderIndex(headers, "jupiter_lon"));
   r.saturn_lon  = DAL_Astro_GetDouble(cells, DAL_Astro_HeaderIndex(headers, "saturn_lon"));
   r.uranus_lon  = DAL_Astro_GetDouble(cells, DAL_Astro_HeaderIndex(headers, "uranus_lon"));
   r.neptune_lon = DAL_Astro_GetDouble(cells, DAL_Astro_HeaderIndex(headers, "neptune_lon"));
   r.pluto_lon   = DAL_Astro_GetDouble(cells, DAL_Astro_HeaderIndex(headers, "pluto_lon"));

   r.sun_sign     = DAL_Astro_GetString(cells, DAL_Astro_HeaderIndex(headers, "sun_sign"));
   r.moon_sign    = DAL_Astro_GetString(cells, DAL_Astro_HeaderIndex(headers, "moon_sign"));
   r.mercury_sign = DAL_Astro_GetString(cells, DAL_Astro_HeaderIndex(headers, "mercury_sign"));
   r.venus_sign   = DAL_Astro_GetString(cells, DAL_Astro_HeaderIndex(headers, "venus_sign"));
   r.mars_sign    = DAL_Astro_GetString(cells, DAL_Astro_HeaderIndex(headers, "mars_sign"));
   r.jupiter_sign = DAL_Astro_GetString(cells, DAL_Astro_HeaderIndex(headers, "jupiter_sign"));
   r.saturn_sign  = DAL_Astro_GetString(cells, DAL_Astro_HeaderIndex(headers, "saturn_sign"));

   r.mercury_retro = DAL_Astro_GetInt(cells, DAL_Astro_HeaderIndex(headers, "mercury_retro"));
   r.venus_retro   = DAL_Astro_GetInt(cells, DAL_Astro_HeaderIndex(headers, "venus_retro"));
   r.mars_retro    = DAL_Astro_GetInt(cells, DAL_Astro_HeaderIndex(headers, "mars_retro"));
   r.jupiter_retro = DAL_Astro_GetInt(cells, DAL_Astro_HeaderIndex(headers, "jupiter_retro"));
   r.saturn_retro  = DAL_Astro_GetInt(cells, DAL_Astro_HeaderIndex(headers, "saturn_retro"));

   r.sun_moon_angle = DAL_Astro_GetDouble(cells, DAL_Astro_HeaderIndex(headers, "sun_moon_angle"));
   r.sun_moon_aspect = DAL_Astro_GetString(cells, DAL_Astro_HeaderIndex(headers, "sun_moon_aspect"));
   r.sun_moon_orb = DAL_Astro_GetDouble(cells, DAL_Astro_HeaderIndex(headers, "sun_moon_orb"));
   r.sun_moon_applying = DAL_Astro_GetInt(cells, DAL_Astro_HeaderIndex(headers, "sun_moon_applying"));

   r.mars_saturn_angle = DAL_Astro_GetDouble(cells, DAL_Astro_HeaderIndex(headers, "mars_saturn_angle"));
   r.mars_saturn_aspect = DAL_Astro_GetString(cells, DAL_Astro_HeaderIndex(headers, "mars_saturn_aspect"));
   r.mars_saturn_orb = DAL_Astro_GetDouble(cells, DAL_Astro_HeaderIndex(headers, "mars_saturn_orb"));
   r.mars_saturn_applying = DAL_Astro_GetInt(cells, DAL_Astro_HeaderIndex(headers, "mars_saturn_applying"));

   r.venus_mars_angle = DAL_Astro_GetDouble(cells, DAL_Astro_HeaderIndex(headers, "venus_mars_angle"));
   r.venus_mars_aspect = DAL_Astro_GetString(cells, DAL_Astro_HeaderIndex(headers, "venus_mars_aspect"));
   r.venus_mars_orb = DAL_Astro_GetDouble(cells, DAL_Astro_HeaderIndex(headers, "venus_mars_orb"));
   r.venus_mars_applying = DAL_Astro_GetInt(cells, DAL_Astro_HeaderIndex(headers, "venus_mars_applying"));

   r.jupiter_saturn_angle = DAL_Astro_GetDouble(cells, DAL_Astro_HeaderIndex(headers, "jupiter_saturn_angle"));
   r.jupiter_saturn_aspect = DAL_Astro_GetString(cells, DAL_Astro_HeaderIndex(headers, "jupiter_saturn_aspect"));
   r.jupiter_saturn_orb = DAL_Astro_GetDouble(cells, DAL_Astro_HeaderIndex(headers, "jupiter_saturn_orb"));
   r.jupiter_saturn_applying = DAL_Astro_GetInt(cells, DAL_Astro_HeaderIndex(headers, "jupiter_saturn_applying"));

   return (r.broker_time > 0 && r.feature_key != "");
}

bool DAL_AstroFeatureStore_LoadCsv(
   DAL_AstroFeatureStore &store,
   const string file_name,
   const int broker_gmt_offset_hours = 0
)
{
   DAL_AstroFeatureStore_Reset(store);
   store.source_file = file_name;
   store.broker_gmt_offset_hours = broker_gmt_offset_hours;

   int h = FileOpen(file_name, FILE_READ | FILE_TXT | FILE_ANSI);
   if(h == INVALID_HANDLE)
   {
      Print("DAL_AstroFeatureStore_LoadCsv failed: file=", file_name, " err=", GetLastError());
      return false;
   }

   if(FileIsEnding(h))
   {
      FileClose(h);
      return false;
   }

   string header_line = FileReadString(h);
   string headers[];
   if(!DAL_Astro_SplitCsvLine(header_line, headers))
   {
      FileClose(h);
      return false;
   }
   for(int i = 0; i < ArraySize(headers); i++)
      headers[i] = DAL_Astro_Unquote(headers[i]);

   int capacity = 4096;
   ArrayResize(store.rows, capacity);
   int count = 0;

   while(!FileIsEnding(h))
   {
      string line = FileReadString(h);
      if(line == "")
         continue;

      string cells[];
      if(!DAL_Astro_SplitCsvLine(line, cells))
         continue;

      DAL_AstroFeatureRow row;
      if(!DAL_Astro_ReadRowFromCells(headers, cells, row))
         continue;

      if(count >= capacity)
      {
         capacity *= 2;
         ArrayResize(store.rows, capacity);
      }
      store.rows[count] = row;
      count++;
   }

   FileClose(h);
   ArrayResize(store.rows, count);
   store.row_count = count;
   store.loaded = (count > 0);
   Print("DAL Astro Feature Store loaded: rows=", count, " file=", file_name);
   return store.loaded;
}

bool DAL_AstroFeatureStore_FindByBrokerTime(
   const DAL_AstroFeatureStore &store,
   const datetime broker_time,
   DAL_AstroFeatureRow &out_row,
   const bool exact = true
)
{
   DAL_AstroFeatureRow_Reset(out_row);
   if(!store.loaded || store.row_count <= 0)
      return false;

   int lo = 0;
   int hi = store.row_count - 1;
   int best = -1;

   while(lo <= hi)
   {
      int mid = (lo + hi) / 2;
      datetime t = store.rows[mid].broker_time;
      if(t == broker_time)
      {
         out_row = store.rows[mid];
         return true;
      }
      if(t < broker_time)
      {
         best = mid;
         lo = mid + 1;
      }
      else
      {
         hi = mid - 1;
      }
   }

   if(!exact && best >= 0)
   {
      out_row = store.rows[best];
      return true;
   }

   return false;
}

string DAL_AstroFeatureRow_ToMultilineText(const DAL_AstroFeatureRow &r)
{
   string txt = "ASTRO FEATURE STORE\n";
   txt += "broker=" + TimeToString(r.broker_time, TIME_DATE | TIME_MINUTES) + " utc=" + TimeToString(r.utc_time, TIME_DATE | TIME_MINUTES) + "\n";
   txt += "moon_phase=" + r.moon_phase_bucket + " angle=" + DoubleToString(r.moon_phase_angle, 2) + " illum=" + DoubleToString(r.moon_illumination_proxy, 3) + "\n";
   txt += "sun=" + r.sun_sign + " moon=" + r.moon_sign + " mars=" + r.mars_sign + " saturn=" + r.saturn_sign + "\n";
   txt += "mars_saturn=" + r.mars_saturn_aspect + " orb=" + DoubleToString(r.mars_saturn_orb, 2) + " app=" + IntegerToString(r.mars_saturn_applying) + "\n";
   txt += "key=" + r.feature_key;
   return txt;
}

void DAL_Astro_DrawPanel(
   const long chart_id,
   const string prefix,
   const DAL_AstroFeatureRow &r,
   const int x = 10,
   const int y = 20
)
{
   string name = prefix + "_ASTRO_PANEL";
   if(ObjectFind(chart_id, name) < 0)
      ObjectCreate(chart_id, name, OBJ_LABEL, 0, 0, 0);

   ObjectSetInteger(chart_id, name, OBJPROP_CORNER, CORNER_LEFT_UPPER);
   ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, 9);
   ObjectSetString(chart_id, name, OBJPROP_FONT, "Consolas");
   ObjectSetInteger(chart_id, name, OBJPROP_COLOR, clrWhite);
   ObjectSetString(chart_id, name, OBJPROP_TEXT, DAL_AstroFeatureRow_ToMultilineText(r));
}

void DAL_Astro_DrawStatus(
   const long chart_id,
   const string prefix,
   const string status,
   const int x = 10,
   const int y = 20
)
{
   string name = prefix + "_ASTRO_PANEL";
   if(ObjectFind(chart_id, name) < 0)
      ObjectCreate(chart_id, name, OBJ_LABEL, 0, 0, 0);

   ObjectSetInteger(chart_id, name, OBJPROP_CORNER, CORNER_LEFT_UPPER);
   ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, 9);
   ObjectSetString(chart_id, name, OBJPROP_FONT, "Consolas");
   ObjectSetInteger(chart_id, name, OBJPROP_COLOR, clrYellow);
   ObjectSetString(chart_id, name, OBJPROP_TEXT, status);
}

#endif
