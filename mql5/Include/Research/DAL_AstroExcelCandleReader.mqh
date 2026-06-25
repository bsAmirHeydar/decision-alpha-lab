#ifndef __DAL_ASTRO_EXCEL_CANDLE_READER_MQH__
#define __DAL_ASTRO_EXCEL_CANDLE_READER_MQH__

#include <Research/DAL_AstroMapTypes.mqh>

// Decision Alpha Lab - Astro Excel/CSV Candle Reader
// IMPORTANT: MQL5 reads the Excel-compatible CSV mirror, not the binary .xlsx workbook.
// Put the CSV under: <Terminal Data Folder>/MQL5/Files/astro/...

string DAL_AstroCsv_Trim(string value)
{
   StringTrimLeft(value);
   StringTrimRight(value);
   return value;
}

string DAL_AstroCsv_Unquote(string value)
{
   value = DAL_AstroCsv_Trim(value);
   int n = StringLen(value);
   if(n >= 2)
   {
      if(StringSubstr(value, 0, 1) == "\"" && StringSubstr(value, n - 1, 1) == "\"")
         value = StringSubstr(value, 1, n - 2);
   }
   StringReplace(value, "\"\"", "\"");
   return value;
}

datetime DAL_AstroCsv_ParseTime(string value)
{
   value = DAL_AstroCsv_Unquote(value);
   StringReplace(value, "-", ".");
   return StringToTime(value);
}

bool DAL_AstroCsv_SplitLine(const string line, string &cells[])
{
   // Safe for builder output because feature_key and summary avoid commas.
   // If the CSV is manually edited in Excel, keep delimiter comma and do not insert commas in text columns.
   ushort sep = StringGetCharacter(",", 0);
   int n = StringSplit(line, sep, cells);
   return (n > 0);
}

int DAL_AstroCsv_HeaderIndex(const string &headers[], const string name)
{
   for(int i = 0; i < ArraySize(headers); i++)
   {
      if(headers[i] == name)
         return i;
   }
   return -1;
}

string DAL_AstroCsv_GetString(const string &cells[], const int idx, const string fallback = "")
{
   if(idx < 0 || idx >= ArraySize(cells))
      return fallback;
   return DAL_AstroCsv_Unquote(cells[idx]);
}

double DAL_AstroCsv_GetDouble(const string &cells[], const int idx, const double fallback = 0.0)
{
   string v = DAL_AstroCsv_GetString(cells, idx, "");
   if(v == "")
      return fallback;
   return StringToDouble(v);
}

int DAL_AstroCsv_GetInt(const string &cells[], const int idx, const int fallback = 0)
{
   string v = DAL_AstroCsv_GetString(cells, idx, "");
   if(v == "")
      return fallback;
   return (int)StringToInteger(v);
}

long DAL_AstroCsv_GetLong(const string &cells[], const int idx, const long fallback = 0)
{
   string v = DAL_AstroCsv_GetString(cells, idx, "");
   if(v == "")
      return fallback;
   return (long)StringToInteger(v);
}

void DAL_AstroCsv_ReadBody(
   const string &headers[],
   const string &cells[],
   const string body_name,
   DAL_AstroBodyState &b
)
{
   b.name       = body_name;
   b.lon        = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, body_name + "_lon"));
   b.lat        = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, body_name + "_lat"));
   b.dist       = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, body_name + "_dist"));
   b.speed_lon  = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, body_name + "_speed_lon"));
   b.speed_lat  = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, body_name + "_speed_lat"));
   b.speed_dist = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, body_name + "_speed_dist"));
   b.ra         = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, body_name + "_ra"));
   b.decl       = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, body_name + "_decl"));
   b.sign       = DAL_AstroCsv_GetString(cells, DAL_AstroCsv_HeaderIndex(headers, body_name + "_sign"));
   b.sign_index = DAL_AstroCsv_GetInt(cells, DAL_AstroCsv_HeaderIndex(headers, body_name + "_sign_index"), -1);
   b.degree     = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, body_name + "_degree"));
   b.retro      = DAL_AstroCsv_GetInt(cells, DAL_AstroCsv_HeaderIndex(headers, body_name + "_retro"));
}

void DAL_AstroCsv_ReadAspect(
   const string &headers[],
   const string &cells[],
   const string pair,
   DAL_AstroAspectState &a
)
{
   a.pair     = pair;
   a.angle    = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, pair + "_angle"));
   a.aspect   = DAL_AstroCsv_GetString(cells, DAL_AstroCsv_HeaderIndex(headers, pair + "_aspect"), "none");
   a.orb      = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, pair + "_orb"), 999.0);
   a.applying = DAL_AstroCsv_GetInt(cells, DAL_AstroCsv_HeaderIndex(headers, pair + "_applying"));
}

bool DAL_AstroCsv_ReadMapRow(const string &headers[], const string &cells[], DAL_AstroMapRow &r)
{
   DAL_AstroMapRow_Reset(r);

   int i_broker_time = DAL_AstroCsv_HeaderIndex(headers, "broker_time");
   int i_utc_time    = DAL_AstroCsv_HeaderIndex(headers, "utc_time");
   int i_key         = DAL_AstroCsv_HeaderIndex(headers, "feature_key");

   if(i_broker_time < 0 || i_utc_time < 0 || i_key < 0)
      return false;

   r.broker_time = DAL_AstroCsv_ParseTime(DAL_AstroCsv_GetString(cells, i_broker_time));
   r.utc_time    = DAL_AstroCsv_ParseTime(DAL_AstroCsv_GetString(cells, i_utc_time));
   r.unix_utc    = DAL_AstroCsv_GetLong(cells, DAL_AstroCsv_HeaderIndex(headers, "unix_utc"));
   r.jd_ut       = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, "jd_ut"));
   r.feature_key = DAL_AstroCsv_GetString(cells, i_key);
   r.summary     = DAL_AstroCsv_GetString(cells, DAL_AstroCsv_HeaderIndex(headers, "summary"));

   r.moon_phase_angle = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, "moon_phase_angle"));
   r.moon_phase_bucket = DAL_AstroCsv_GetString(cells, DAL_AstroCsv_HeaderIndex(headers, "moon_phase_bucket"));
   r.moon_illumination_proxy = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, "moon_illumination_proxy"));

   for(int i = 0; i < DAL_ASTRO_BODY_COUNT; i++)
      DAL_AstroCsv_ReadBody(headers, cells, DAL_AstroBodyName(i), r.body[i]);

   for(int j = 0; j < DAL_ASTRO_ASPECT_PAIR_COUNT; j++)
      DAL_AstroCsv_ReadAspect(headers, cells, DAL_AstroAspectPairName(j), r.aspect[j]);

   return (r.broker_time > 0 && r.utc_time > 0 && r.feature_key != "");
}


string DAL_AstroCsv_BaseName(const string path)
{
   string out = path;
   int last = -1;
   int n = StringLen(path);
   for(int i = 0; i < n; i++)
   {
      ushort ch = StringGetCharacter(path, i);
      if(ch == '\\' || ch == '/')
         last = i;
   }
   if(last >= 0 && last + 1 < n)
      out = StringSubstr(path, last + 1);
   return out;
}

bool DAL_AstroMapStore_LoadCsvCandidate(
   DAL_AstroMapStore &store,
   const string candidate_file,
   const double broker_gmt_offset_hours,
   const int timeframe_minutes,
   const bool use_common_files
)
{
   DAL_AstroMapStore_Reset(store);
   store.source_file = use_common_files ? ("COMMON:" + candidate_file) : candidate_file;
   store.broker_gmt_offset_hours = broker_gmt_offset_hours;
   store.timeframe_minutes = timeframe_minutes;

   int flags = FILE_READ | FILE_TXT | FILE_ANSI;
   if(use_common_files)
      flags |= FILE_COMMON;

   ResetLastError();
   int h = FileOpen(candidate_file, flags);
   if(h == INVALID_HANDLE)
   {
      Print("DAL_AstroMapStore candidate failed: file=", candidate_file,
            " common=", (use_common_files ? "true" : "false"),
            " err=", GetLastError());
      return false;
   }

   if(FileIsEnding(h))
   {
      FileClose(h);
      Print("DAL_AstroMapStore candidate empty: file=", candidate_file,
            " common=", (use_common_files ? "true" : "false"));
      return false;
   }

   string header_line = FileReadString(h);
   string headers[];
   if(!DAL_AstroCsv_SplitLine(header_line, headers))
   {
      FileClose(h);
      Print("DAL_AstroMapStore bad header split: file=", candidate_file,
            " common=", (use_common_files ? "true" : "false"));
      return false;
   }

   for(int i = 0; i < ArraySize(headers); i++)
      headers[i] = DAL_AstroCsv_Unquote(headers[i]);

   int i_broker = DAL_AstroCsv_HeaderIndex(headers, "broker_time");
   int i_utc    = DAL_AstroCsv_HeaderIndex(headers, "utc_time");
   int i_key    = DAL_AstroCsv_HeaderIndex(headers, "feature_key");
   if(i_broker < 0 || i_utc < 0 || i_key < 0)
   {
      FileClose(h);
      Print("DAL_AstroMapStore missing required header: file=", candidate_file,
            " need broker_time,utc_time,feature_key");
      return false;
   }

   int capacity = 4096;
   ArrayResize(store.rows, capacity);
   int count = 0;

   while(!FileIsEnding(h))
   {
      string line = FileReadString(h);
      if(line == "")
         continue;

      string cells[];
      if(!DAL_AstroCsv_SplitLine(line, cells))
         continue;

      DAL_AstroMapRow row;
      if(!DAL_AstroCsv_ReadMapRow(headers, cells, row))
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

   if(store.loaded)
   {
      Print("DAL Astro Map Store loaded: rows=", count,
            " file=", candidate_file,
            " common=", (use_common_files ? "true" : "false"));
      return true;
   }

   Print("DAL_AstroMapStore no valid rows: file=", candidate_file,
         " common=", (use_common_files ? "true" : "false"));
   return false;
}

bool DAL_AstroMapStore_LoadExcelCsv(
   DAL_AstroMapStore &store,
   const string csv_file_name,
   const double broker_gmt_offset_hours,
   const int timeframe_minutes = 1
)
{
   // Runtime file resolution contract:
   // 1. Try exactly what the input says under normal MQL5\\Files.
   // 2. Try the basename directly under MQL5\\Files.
   // 3. Try astro\\basename under MQL5\\Files.
   // 4. Repeat the same three attempts under MetaQuotes Common\\Files.
   // This makes the same code work in live charts, Visual Tester agents,
   // root Files layout, and Files\\astro layout.
   string base = DAL_AstroCsv_BaseName(csv_file_name);
   string c0 = csv_file_name;
   string c1 = base;
   string c2 = "astro\\" + base;

   if(DAL_AstroMapStore_LoadCsvCandidate(store, c0, broker_gmt_offset_hours, timeframe_minutes, false)) return true;
   if(c1 != c0 && DAL_AstroMapStore_LoadCsvCandidate(store, c1, broker_gmt_offset_hours, timeframe_minutes, false)) return true;
   if(c2 != c0 && c2 != c1 && DAL_AstroMapStore_LoadCsvCandidate(store, c2, broker_gmt_offset_hours, timeframe_minutes, false)) return true;

   if(DAL_AstroMapStore_LoadCsvCandidate(store, c0, broker_gmt_offset_hours, timeframe_minutes, true)) return true;
   if(c1 != c0 && DAL_AstroMapStore_LoadCsvCandidate(store, c1, broker_gmt_offset_hours, timeframe_minutes, true)) return true;
   if(c2 != c0 && c2 != c1 && DAL_AstroMapStore_LoadCsvCandidate(store, c2, broker_gmt_offset_hours, timeframe_minutes, true)) return true;

   DAL_AstroMapStore_Reset(store);
   store.source_file = csv_file_name;
   store.broker_gmt_offset_hours = broker_gmt_offset_hours;
   store.timeframe_minutes = timeframe_minutes;
   Print("DAL_AstroMapStore_LoadExcelCsv failed all candidates. input=", csv_file_name,
         " basename=", base,
         " normal roots=MQL5\\Files, common root=Terminal\\Common\\Files");
   return false;
}

bool DAL_AstroMapStore_FindByBrokerTime(
   const DAL_AstroMapStore &store,
   const datetime broker_time,
   DAL_AstroMapRow &out_row,
   const bool exact = true
)
{
   DAL_AstroMapRow_Reset(out_row);
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

bool DAL_AstroMapStore_FindForCandleOpen(
   const DAL_AstroMapStore &store,
   const datetime candle_open_broker_time,
   DAL_AstroMapRow &out_row,
   const bool require_exact = true
)
{
   return DAL_AstroMapStore_FindByBrokerTime(store, candle_open_broker_time, out_row, require_exact);
}

bool DAL_AstroMapRow_ValidateUtcOffset(
   const DAL_AstroMapRow &row,
   const double broker_gmt_offset_hours,
   const int max_abs_seconds = 2
)
{
   int offset_seconds = (int)MathRound(broker_gmt_offset_hours * 3600.0);
   datetime expected_utc = row.broker_time - offset_seconds;
   int diff = (int)MathAbs((double)(expected_utc - row.utc_time));
   return (diff <= max_abs_seconds);
}

string DAL_AstroMapRow_ToMultilineText(const DAL_AstroMapRow &r)
{
   int sun = DAL_AstroBodyIndexByName("sun");
   int moon = DAL_AstroBodyIndexByName("moon");
   int mars = DAL_AstroBodyIndexByName("mars");
   int saturn = DAL_AstroBodyIndexByName("saturn");
   int ms = DAL_AstroAspectIndexByName("mars_saturn");
   int sm = DAL_AstroAspectIndexByName("sun_moon");

   string txt = "ASTRO MAP / CANDLE\n";
   txt += "broker=" + TimeToString(r.broker_time, TIME_DATE | TIME_MINUTES) + " utc=" + TimeToString(r.utc_time, TIME_DATE | TIME_MINUTES) + "\n";
   txt += "moon_phase=" + r.moon_phase_bucket + " angle=" + DoubleToString(r.moon_phase_angle, 2) + " illum=" + DoubleToString(r.moon_illumination_proxy, 3) + "\n";
   txt += "sun=" + r.body[sun].sign + ":" + DoubleToString(r.body[sun].degree, 1)
       + " moon=" + r.body[moon].sign + ":" + DoubleToString(r.body[moon].degree, 1) + "\n";
   txt += "mars=" + r.body[mars].sign + ":" + DoubleToString(r.body[mars].degree, 1)
       + " saturn=" + r.body[saturn].sign + ":" + DoubleToString(r.body[saturn].degree, 1) + "\n";
   txt += "sun_moon=" + r.aspect[sm].aspect + " orb=" + DoubleToString(r.aspect[sm].orb, 2)
       + " mars_saturn=" + r.aspect[ms].aspect + " orb=" + DoubleToString(r.aspect[ms].orb, 2) + "\n";
   txt += "key=" + r.feature_key;
   return txt;
}

void DAL_AstroMap_DrawPanel(
   const long chart_id,
   const string prefix,
   const DAL_AstroMapRow &r,
   const int x = 10,
   const int y = 20,
   const color text_color = clrWhite
)
{
   string name = prefix + "_ASTRO_MAP_PANEL";
   if(ObjectFind(chart_id, name) < 0)
      ObjectCreate(chart_id, name, OBJ_LABEL, 0, 0, 0);

   ObjectSetInteger(chart_id, name, OBJPROP_CORNER, CORNER_LEFT_UPPER);
   ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, 9);
   ObjectSetString(chart_id, name, OBJPROP_FONT, "Consolas");
   ObjectSetInteger(chart_id, name, OBJPROP_COLOR, text_color);
   ObjectSetString(chart_id, name, OBJPROP_TEXT, DAL_AstroMapRow_ToMultilineText(r));
}

void DAL_AstroMap_DrawStatus(
   const long chart_id,
   const string prefix,
   const string status,
   const int x = 10,
   const int y = 20,
   const color text_color = clrYellow
)
{
   string name = prefix + "_ASTRO_MAP_PANEL";
   if(ObjectFind(chart_id, name) < 0)
      ObjectCreate(chart_id, name, OBJ_LABEL, 0, 0, 0);

   ObjectSetInteger(chart_id, name, OBJPROP_CORNER, CORNER_LEFT_UPPER);
   ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, 9);
   ObjectSetString(chart_id, name, OBJPROP_FONT, "Consolas");
   ObjectSetInteger(chart_id, name, OBJPROP_COLOR, text_color);
   ObjectSetString(chart_id, name, OBJPROP_TEXT, status);
}

#endif
