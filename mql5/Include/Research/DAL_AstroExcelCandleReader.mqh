#ifndef __DAL_ASTRO_EXCEL_CANDLE_READER_MQH__
#define __DAL_ASTRO_EXCEL_CANDLE_READER_MQH__

#include <Research/DAL_AstroMapTypes.mqh>

#define DAL_ASTRO_DIAG_MAX_LINES 120

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


string DAL_AstroCsv_NormalizeRuntimeFileName(string value)
{
   value = DAL_AstroCsv_Trim(value);
   StringReplace(value, "/", "\\");
   while(StringFind(value, "\\\\") >= 0)
      StringReplace(value, "\\\\", "\\");
   if(StringLen(value) >= 2 && StringSubstr(value, 0, 2) == ".\\")
      value = StringSubstr(value, 2);
   return value;
}

string DAL_AstroCsv_BaseFileName(string value)
{
   value = DAL_AstroCsv_NormalizeRuntimeFileName(value);
   int last = -1;
   int n = StringLen(value);
   for(int i = 0; i < n; i++)
   {
      string ch = StringSubstr(value, i, 1);
      if(ch == "\\" || ch == "/")
         last = i;
   }
   if(last >= 0 && last + 1 < n)
      return StringSubstr(value, last + 1);
   return value;
}

bool DAL_AstroCsv_AddOpenCandidate(string &candidates[], const string candidate)
{
   string c = DAL_AstroCsv_NormalizeRuntimeFileName(candidate);
   if(c == "")
      return false;

   for(int i = 0; i < ArraySize(candidates); i++)
   {
      if(candidates[i] == c)
         return false;
   }

   int n = ArraySize(candidates);
   ArrayResize(candidates, n + 1);
   candidates[n] = c;
   return true;
}

string DAL_AstroCsv_OpenCandidatesText(const string &candidates[])
{
   string out = "";
   for(int i = 0; i < ArraySize(candidates); i++)
   {
      if(i > 0)
         out += " | ";
      out += candidates[i];
   }
   return out;
}

void DAL_AstroCsv_BuildOpenCandidates(const string input_file, string &candidates[])
{
   ArrayResize(candidates, 0);

   string normalized = DAL_AstroCsv_NormalizeRuntimeFileName(input_file);
   string base_name  = DAL_AstroCsv_BaseFileName(normalized);

   // Candidate 1: exactly what user typed in the input.
   DAL_AstroCsv_AddOpenCandidate(candidates, normalized);

   // Candidate 2: root of MQL5\Files. This fixes the common case where the
   // user put the CSV directly in Files instead of Files\astro.
   DAL_AstroCsv_AddOpenCandidate(candidates, base_name);

   // Candidate 3: canonical subfolder used by the research docs.
   DAL_AstroCsv_AddOpenCandidate(candidates, "astro\\" + base_name);
}

int DAL_AstroCsv_FileOpenWithFallback(
   const string input_file,
   string &opened_file,
   string &attempted_files,
   int &last_error
)
{
   string candidates[];
   DAL_AstroCsv_BuildOpenCandidates(input_file, candidates);

   opened_file = "";
   attempted_files = "NORMAL_FILES{" + DAL_AstroCsv_OpenCandidatesText(candidates) + "}";
   attempted_files += " || COMMON_FILES{" + DAL_AstroCsv_OpenCandidatesText(candidates) + "}";
   last_error = 0;

   // Pass 1: normal runtime root.
   // Live chart: <Terminal Data Folder>\MQL5\Files
   // Strategy Tester: <Tester Agent Data Folder>\MQL5\Files
   for(int i = 0; i < ArraySize(candidates); i++)
   {
      ResetLastError();
      int h = FileOpen(candidates[i], FILE_READ | FILE_TXT | FILE_ANSI);
      if(h != INVALID_HANDLE)
      {
         opened_file = candidates[i];
         return h;
      }
      last_error = GetLastError();
   }

   // Pass 2: common terminal root. This is the safest bridge for Strategy Tester
   // because tester agents and live terminals can both access Common\Files when
   // FILE_COMMON is used. Put the CSV under:
   // <MetaQuotes Common Data Folder>\Files\...
   for(int j = 0; j < ArraySize(candidates); j++)
   {
      ResetLastError();
      int h = FileOpen(candidates[j], FILE_READ | FILE_TXT | FILE_ANSI | FILE_COMMON);
      if(h != INVALID_HANDLE)
      {
         opened_file = "COMMON::" + candidates[j];
         return h;
      }
      last_error = GetLastError();
   }

   return INVALID_HANDLE;
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
   const string prefix,
   const string body_name,
   DAL_AstroBodyState &b
)
{
   b.name       = body_name;
   string key = prefix + body_name;
   b.lon        = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, key + "_lon"));
   b.lat        = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, key + "_lat"));
   b.dist       = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, key + "_dist"));
   b.speed_lon  = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, key + "_speed_lon"));
   b.speed_lat  = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, key + "_speed_lat"));
   b.speed_dist = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, key + "_speed_dist"));
   b.ra         = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, key + "_ra"));
   b.decl       = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, key + "_decl"));
   b.sign       = DAL_AstroCsv_GetString(cells, DAL_AstroCsv_HeaderIndex(headers, key + "_sign"));
   b.sign_index = DAL_AstroCsv_GetInt(cells, DAL_AstroCsv_HeaderIndex(headers, key + "_sign_index"), -1);
   b.degree     = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, key + "_degree"));
   b.retro      = DAL_AstroCsv_GetInt(cells, DAL_AstroCsv_HeaderIndex(headers, key + "_retro"));
   b.house      = DAL_AstroCsv_GetInt(cells, DAL_AstroCsv_HeaderIndex(headers, key + "_house"), -1);
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

void DAL_AstroCsv_ReadTransitNatalAspect(
   const string &headers[],
   const string &cells[],
   const string pair,
   DAL_AstroAspectState &a
)
{
   DAL_AstroCsv_ReadAspect(headers, cells, pair, a);
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

   r.houses_valid = (DAL_AstroCsv_GetInt(cells, DAL_AstroCsv_HeaderIndex(headers, "houses_valid"), 0) == 1);
   r.house_lat = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, "house_lat"));
   r.house_lon = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, "house_lon"));
   r.house_system = DAL_AstroCsv_GetString(cells, DAL_AstroCsv_HeaderIndex(headers, "house_system"));
   r.asc_lon = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, "asc_lon"));
   r.mc_lon = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, "mc_lon"));
   for(int h = 0; h < 12; h++)
      r.house_cusp[h] = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, "house_" + IntegerToString(h + 1) + "_cusp"));

    r.natal_enabled = (DAL_AstroCsv_GetInt(cells, DAL_AstroCsv_HeaderIndex(headers, "natal_enabled"), 0) == 1);
    r.natal_label = DAL_AstroCsv_GetString(cells, DAL_AstroCsv_HeaderIndex(headers, "natal_label"));
    r.natal_local_time = DAL_AstroCsv_ParseTime(DAL_AstroCsv_GetString(cells, DAL_AstroCsv_HeaderIndex(headers, "natal_local_time")));
    r.natal_utc_time = DAL_AstroCsv_ParseTime(DAL_AstroCsv_GetString(cells, DAL_AstroCsv_HeaderIndex(headers, "natal_utc_time")));
    r.natal_utc_offset_hours = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, "natal_utc_offset_hours"));
    r.natal_houses_valid = (DAL_AstroCsv_GetInt(cells, DAL_AstroCsv_HeaderIndex(headers, "natal_houses_valid"), 0) == 1);
    r.natal_house_lat = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, "natal_house_lat"));
    r.natal_house_lon = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, "natal_house_lon"));
    r.natal_house_system = DAL_AstroCsv_GetString(cells, DAL_AstroCsv_HeaderIndex(headers, "natal_house_system"));
    r.natal_asc_lon = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, "natal_asc_lon"));
    r.natal_mc_lon = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, "natal_mc_lon"));
    for(int h = 0; h < 12; h++)
       r.natal_house_cusp[h] = DAL_AstroCsv_GetDouble(cells, DAL_AstroCsv_HeaderIndex(headers, "natal_house_" + IntegerToString(h + 1) + "_cusp"));

    r.astro_bias_text = DAL_AstroCsv_GetString(cells, DAL_AstroCsv_HeaderIndex(headers, "astro_bias_text"));
    r.astro_path_text = DAL_AstroCsv_GetString(cells, DAL_AstroCsv_HeaderIndex(headers, "astro_path_text"));
    r.astro_signal_text = DAL_AstroCsv_GetString(cells, DAL_AstroCsv_HeaderIndex(headers, "astro_signal_text"));

   for(int i = 0; i < DAL_ASTRO_BODY_COUNT; i++)
      DAL_AstroCsv_ReadBody(headers, cells, "", DAL_AstroBodyName(i), r.body[i]);
   for(int i = 0; i < DAL_ASTRO_BODY_COUNT; i++)
      DAL_AstroCsv_ReadBody(headers, cells, "natal_", DAL_AstroBodyName(i), r.natal_body[i]);

   for(int j = 0; j < DAL_ASTRO_ASPECT_PAIR_COUNT; j++)
      DAL_AstroCsv_ReadAspect(headers, cells, DAL_AstroAspectPairName(j), r.aspect[j]);
   for(int j = 0; j < DAL_ASTRO_TRANSIT_NATAL_ASPECT_COUNT; j++)
      DAL_AstroCsv_ReadTransitNatalAspect(headers, cells, DAL_AstroTransitNatalAspectName(j), r.transit_natal_aspect[j]);
   for(int j = 0; j < DAL_ASTRO_NATAL_CORE_COUNT; j++)
      r.transit_in_natal_house[j] = DAL_AstroCsv_GetInt(cells, DAL_AstroCsv_HeaderIndex(headers, DAL_AstroNatalCoreBodyName(j) + "_in_natal_house"), -1);

   return (r.broker_time > 0 && r.utc_time > 0 && r.feature_key != "");
}


string DAL_AstroDiag_DateTime(const datetime t)
{
   if(t <= 0)
      return "n/a";
   return TimeToString(t, TIME_DATE | TIME_SECONDS);
}

string DAL_AstroDiag_RuntimeFilePath(const string relative_file_name)
{
   string root = TerminalInfoString(TERMINAL_DATA_PATH);
   if(root == "")
      root = "<MT5 Data Folder>";
   return root + "\\MQL5\\Files\\" + relative_file_name;
}

string DAL_AstroDiag_CommonFilePath(const string relative_file_name)
{
   string root = TerminalInfoString(TERMINAL_COMMONDATA_PATH);
   if(root == "")
      root = "<MT5 Common Data Folder>";
   return root + "\\Files\\" + relative_file_name;
}

string DAL_AstroMapStore_LoadDiagnosticText(const DAL_AstroMapStore &store)
{
   string txt = "ASTRO CSV LOAD DIAGNOSTIC\n";
   txt += "stage: " + store.load_stage + "\n";
   txt += "file input: " + store.source_file + "\n";
   txt += "runtime path: " + DAL_AstroDiag_RuntimeFilePath(store.source_file) + "\n";
   txt += "common path:  " + DAL_AstroDiag_CommonFilePath(DAL_AstroCsv_BaseFileName(store.source_file)) + "\n";
   txt += "fallback rule: normal Files first, then Common\\Files; each tries input path, root filename, and astro\\filename.\n";
   txt += "xlsx note: MQL runtime reads .csv only. .xlsx is review-only.\n";
   txt += "loaded: " + (store.loaded ? "true" : "false") + "\n";
   txt += "rows parsed: " + IntegerToString(store.row_count) + "\n";
   txt += "physical lines: " + IntegerToString(store.physical_lines) + "\n";
   txt += "header columns: " + IntegerToString(store.header_columns) + "\n";
   txt += "empty lines: " + IntegerToString(store.empty_lines) + "\n";
   txt += "split failed lines: " + IntegerToString(store.split_failed_lines) + "\n";
   txt += "parse failed rows: " + IntegerToString(store.parse_failed_lines) + "\n";
   txt += "skipped lines: " + IntegerToString(store.skipped_lines) + "\n";
   txt += "file open error: " + IntegerToString(store.file_open_error) + "\n";
   if(store.load_error != "")
      txt += "error: " + store.load_error + "\n";
   txt += "csv range broker: " + DAL_AstroDiag_DateTime(store.first_broker_time) + " -> " + DAL_AstroDiag_DateTime(store.last_broker_time) + "\n";
   txt += "csv range utc: " + DAL_AstroDiag_DateTime(store.first_utc_time) + " -> " + DAL_AstroDiag_DateTime(store.last_utc_time) + "\n";
   if(store.header_line != "")
      txt += "header: " + StringSubstr(store.header_line, 0, 220) + "\n";
   if(store.first_data_line != "")
      txt += "first data: " + StringSubstr(store.first_data_line, 0, 220) + "\n";

   if(!store.loaded)
   {
      txt += "\nDIAGNOSIS:\n";
      if(store.load_stage == "FILE_OPEN_FAILED")
      {
         txt += "Problem is FILE ADDRESS / runtime file access.\n";
         txt += "In Strategy Tester, <Terminal>\\MQL5\\Files is NOT the same as the agent runtime Files folder.\n";
         txt += "Put CSV either under <MT5 Data Folder>\\MQL5\\Files or, safer, under <Common Data Folder>\\Files.\n";
      }
      else if(store.load_stage == "EMPTY_FILE" || store.load_stage == "HEADER_READ_FAILED")
      {
         txt += "Problem is file content: file exists but is empty/unreadable.\n";
      }
      else if(store.load_stage == "BAD_HEADER")
      {
         txt += "Problem is CSV header: required columns are missing.\n";
         txt += "Required columns: broker_time, utc_time, feature_key.\n";
      }
      else if(store.load_stage == "NO_VALID_ROWS")
      {
         txt += "Problem is inside the CSV: header exists but no rows could be parsed.\n";
         txt += "Check date format, delimiter, and required columns.\n";
      }
   }

   return txt;
}

bool DAL_AstroMapStore_NearestIndices(
   const DAL_AstroMapStore &store,
   const datetime broker_time,
   int &before_index,
   int &after_index
)
{
   before_index = -1;
   after_index = -1;
   if(!store.loaded || store.row_count <= 0)
      return false;

   int lo = 0;
   int hi = store.row_count - 1;
   while(lo <= hi)
   {
      int mid = (lo + hi) / 2;
      datetime t = store.rows[mid].broker_time;
      if(t == broker_time)
      {
         before_index = mid;
         after_index = mid;
         return true;
      }
      if(t < broker_time)
      {
         before_index = mid;
         lo = mid + 1;
      }
      else
      {
         after_index = mid;
         hi = mid - 1;
      }
   }
   return true;
}

string DAL_AstroMapStore_LookupDiagnosticText(
   const DAL_AstroMapStore &store,
   const datetime requested_broker_time,
   const bool require_exact,
   const double broker_gmt_offset_hours
)
{
   string txt = "ASTRO CSV LOOKUP DIAGNOSTIC\n";
   txt += "file input: " + store.source_file + "\n";
   txt += "runtime path: " + DAL_AstroDiag_RuntimeFilePath(store.source_file) + "\n";
   txt += "common path:  " + DAL_AstroDiag_CommonFilePath(DAL_AstroCsv_BaseFileName(store.source_file)) + "\n";
   txt += "fallback rule: normal Files first, then Common\\Files; each tries input path, root filename, and astro\\filename.\n";
   txt += "load stage: " + store.load_stage + "\n";
   txt += "loaded: " + (store.loaded ? "true" : "false") + " rows=" + IntegerToString(store.row_count) + "\n";
   txt += "requested broker time: " + DAL_AstroDiag_DateTime(requested_broker_time) + "\n";
   int offset_seconds = (int)MathRound(broker_gmt_offset_hours * 3600.0);
   txt += "requested utc by input offset: " + DAL_AstroDiag_DateTime(requested_broker_time - offset_seconds) + "\n";
   txt += "input broker GMT offset: " + DoubleToString(broker_gmt_offset_hours, 2) + "\n";
   txt += "require exact: " + (require_exact ? "true" : "false") + "\n";
   txt += "csv broker range: " + DAL_AstroDiag_DateTime(store.first_broker_time) + " -> " + DAL_AstroDiag_DateTime(store.last_broker_time) + "\n";
   txt += "csv utc range: " + DAL_AstroDiag_DateTime(store.first_utc_time) + " -> " + DAL_AstroDiag_DateTime(store.last_utc_time) + "\n";

   if(!store.loaded)
   {
      txt += "\nDIAGNOSIS: not a lookup problem. CSV was not loaded. See load diagnostic above.\n";
      return txt;
   }

   int before_i = -1;
   int after_i = -1;
   DAL_AstroMapStore_NearestIndices(store, requested_broker_time, before_i, after_i);

   if(before_i >= 0)
   {
      int delta_before = (int)(requested_broker_time - store.rows[before_i].broker_time);
      txt += "nearest before/equal: " + DAL_AstroDiag_DateTime(store.rows[before_i].broker_time)
          + " delta_sec=" + IntegerToString(delta_before) + "\n";
   }
   else
      txt += "nearest before/equal: none\n";

   if(after_i >= 0)
   {
      int delta_after = (int)(store.rows[after_i].broker_time - requested_broker_time);
      txt += "nearest after/equal: " + DAL_AstroDiag_DateTime(store.rows[after_i].broker_time)
          + " delta_sec=" + IntegerToString(delta_after) + "\n";
   }
   else
      txt += "nearest after/equal: none\n";

   txt += "\nDIAGNOSIS:\n";
   if(requested_broker_time < store.first_broker_time || requested_broker_time > store.last_broker_time)
   {
      txt += "Problem is CSV DATE RANGE. File is loaded, but requested candle is outside CSV range.\n";
      txt += "Regenerate CSV for this tester/live date range.\n";
   }
   else if(require_exact)
   {
      txt += "Problem is TIMESTAMP EXACT MATCH. File is loaded and date is inside range, but exact candle time was not found.\n";
      txt += "Check timeframe, broker GMT offset, seconds alignment, and broker candle open time.\n";
      txt += "For visual debugging, set InpRequireExactBarTime=false. For final research, fix alignment and turn exact back on.\n";
   }
   else
   {
      txt += "File and range are OK. Non-exact lookup should use nearest previous row. If still missing, row array may be unsorted.\n";
   }

   return txt;
}

bool DAL_AstroMapStore_LoadExcelCsv(
   DAL_AstroMapStore &store,
   const string csv_file_name,
   const double broker_gmt_offset_hours,
   const int timeframe_minutes = 1
)
{
   DAL_AstroMapStore_Reset(store);
   store.source_file = csv_file_name;
   store.broker_gmt_offset_hours = broker_gmt_offset_hours;
   store.timeframe_minutes = timeframe_minutes;
   store.load_stage = "START";

   string opened_file = "";
   string attempted_files = "";
   int open_last_error = 0;

   int h = DAL_AstroCsv_FileOpenWithFallback(
      csv_file_name,
      opened_file,
      attempted_files,
      open_last_error
   );

   if(h == INVALID_HANDLE)
   {
      store.file_open_error = open_last_error;
      store.load_stage = "FILE_OPEN_FAILED";
      store.load_error = "FileOpen failed after fallback attempts. Tried: " + attempted_files + ". This is a path/runtime access problem, not a CSV parsing problem.";
      Print(DAL_AstroMapStore_LoadDiagnosticText(store));
      return false;
   }

   // From this point onward source_file is the actual file successfully opened.
   // This makes the on-chart diagnostic match what MQL really read.
   store.source_file = opened_file;
   store.load_stage = "FILE_OPEN_OK";

   if(FileIsEnding(h))
   {
      FileClose(h);
      store.load_stage = "EMPTY_FILE";
      store.load_error = "FileOpen succeeded, but file is empty.";
      Print(DAL_AstroMapStore_LoadDiagnosticText(store));
      return false;
   }

   string header_line = FileReadString(h);
   store.physical_lines = 1;
   store.header_line = header_line;

   if(header_line == "")
   {
      FileClose(h);
      store.load_stage = "HEADER_READ_FAILED";
      store.load_error = "FileOpen succeeded, but header line is empty.";
      Print(DAL_AstroMapStore_LoadDiagnosticText(store));
      return false;
   }

   string headers[];
   if(!DAL_AstroCsv_SplitLine(header_line, headers))
   {
      FileClose(h);
      store.load_stage = "HEADER_SPLIT_FAILED";
      store.load_error = "Header line could not be split as CSV.";
      Print(DAL_AstroMapStore_LoadDiagnosticText(store));
      return false;
   }

   for(int i = 0; i < ArraySize(headers); i++)
      headers[i] = DAL_AstroCsv_Unquote(headers[i]);

   store.header_columns = ArraySize(headers);

   int i_broker_time = DAL_AstroCsv_HeaderIndex(headers, "broker_time");
   int i_utc_time    = DAL_AstroCsv_HeaderIndex(headers, "utc_time");
   int i_feature_key = DAL_AstroCsv_HeaderIndex(headers, "feature_key");

   if(i_broker_time < 0 || i_utc_time < 0 || i_feature_key < 0)
   {
      FileClose(h);
      store.load_stage = "BAD_HEADER";
      store.load_error = "Required header missing. Required: broker_time, utc_time, feature_key.";
      Print(DAL_AstroMapStore_LoadDiagnosticText(store));
      return false;
   }

   int capacity = 4096;
   ArrayResize(store.rows, capacity);
   int count = 0;

   while(!FileIsEnding(h))
   {
      string line = FileReadString(h);
      store.physical_lines++;

      if(line == "")
      {
         store.empty_lines++;
         continue;
      }

      if(store.first_data_line == "")
         store.first_data_line = line;

      string cells[];
      if(!DAL_AstroCsv_SplitLine(line, cells))
      {
         store.split_failed_lines++;
         store.skipped_lines++;
         continue;
      }

      DAL_AstroMapRow row;
      if(!DAL_AstroCsv_ReadMapRow(headers, cells, row))
      {
         store.parse_failed_lines++;
         store.skipped_lines++;
         continue;
      }

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

   if(count > 0)
   {
      store.first_broker_time = store.rows[0].broker_time;
      store.last_broker_time  = store.rows[count - 1].broker_time;
      store.first_utc_time    = store.rows[0].utc_time;
      store.last_utc_time     = store.rows[count - 1].utc_time;
      store.load_stage = "LOAD_OK";
      store.load_error = "";
   }
   else
   {
      store.load_stage = "NO_VALID_ROWS";
      store.load_error = "Header was readable, but no valid astro rows were parsed.";
   }

   Print(DAL_AstroMapStore_LoadDiagnosticText(store));
   return store.loaded;
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

string DAL_AstroDiag_TruncateLine(const string line, const int max_chars = 185)
{
   if(max_chars <= 0)
      return line;
   if(StringLen(line) <= max_chars)
      return line;
   return StringSubstr(line, 0, max_chars - 3) + "...";
}

void DAL_AstroDiag_DeletePanel(const long chart_id, const string prefix)
{
   ObjectDelete(chart_id, prefix + "_ASTRO_MAP_PANEL");
   for(int i = 0; i < DAL_ASTRO_DIAG_MAX_LINES; i++)
      ObjectDelete(chart_id, prefix + "_ASTRO_DIAG_LINE_" + IntegerToString(i));
}

void DAL_AstroDiag_DrawLine(
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
   ObjectSetString(chart_id, name, OBJPROP_TEXT, DAL_AstroDiag_TruncateLine(text));
}

void DAL_AstroDiag_DrawPanel(
   const long chart_id,
   const string prefix,
   const string text,
   const int x = 10,
   const int y = 90,
   const color clr = clrWhite,
   const int font_size = 8,
   const int line_height = 16,
   const bool clear_old = true
)
{
   if(clear_old)
      DAL_AstroDiag_DeletePanel(chart_id, prefix);

   string lines[];
   ushort sep = StringGetCharacter("\n", 0);
   int n = StringSplit(text, sep, lines);
   if(n <= 0)
      return;

   int max_lines = MathMin(n, DAL_ASTRO_DIAG_MAX_LINES);
   for(int i = 0; i < max_lines; i++)
   {
      color line_clr = clr;
      if(StringFind(lines[i], "FILE_OPEN_FAILED") >= 0 || StringFind(lines[i], "CSV NOT LOADED") >= 0)
         line_clr = clrTomato;
      else if(StringFind(lines[i], "DIAGNOSIS") >= 0)
         line_clr = clrGold;
      else if(StringFind(lines[i], "runtime path") >= 0 || StringFind(lines[i], "file input") >= 0)
         line_clr = clrAqua;

      DAL_AstroDiag_DrawLine(chart_id, prefix + "_ASTRO_DIAG_LINE_" + IntegerToString(i), lines[i], x, y + i * line_height, line_clr, font_size);
   }

   if(n > max_lines)
      DAL_AstroDiag_DrawLine(chart_id, prefix + "_ASTRO_DIAG_LINE_" + IntegerToString(max_lines), "... truncated lines=" + IntegerToString(n - max_lines), x, y + max_lines * line_height, clrGold, font_size);

   ChartRedraw(chart_id);
}

void DAL_AstroMap_DrawPanel(
   const long chart_id,
   const string prefix,
   const DAL_AstroMapRow &r,
   const int x = 10,
   const int y = 90,
   const color text_color = clrWhite
)
{
   DAL_AstroDiag_DrawPanel(chart_id, prefix, DAL_AstroMapRow_ToMultilineText(r), x, y, text_color, 8, 16, true);
}

void DAL_AstroMap_DrawStatus(
   const long chart_id,
   const string prefix,
   const string status,
   const int x = 10,
   const int y = 90,
   const color text_color = clrYellow
)
{
   DAL_AstroDiag_DrawPanel(chart_id, prefix, status, x, y, text_color, 8, 16, true);
}

#endif
