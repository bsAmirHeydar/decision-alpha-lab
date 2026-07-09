#ifndef GARTAL_NEWS_CALENDAR_CLIENT_MQH
#define GARTAL_NEWS_CALENDAR_CLIENT_MQH

string GT_FetchModeText(int mode)
{
   if(mode == GT_FETCH_LOCAL_FILE) return "LOCAL_FILE";
   if(mode == GT_FETCH_WEBREQUEST) return "WEBREQUEST";
   if(mode == GT_FETCH_AUTO)       return "AUTO";
   return "UNKNOWN";
}

string GT_SourceFormatText(int format)
{
   if(format == GT_SOURCE_FORMAT_AUTO) return "AUTO";
   if(format == GT_SOURCE_FORMAT_XML)  return "FF_XML";
   if(format == GT_SOURCE_FORMAT_CSV)  return "FF_CSV";
   if(format == GT_SOURCE_FORMAT_HTML) return "FF_HTML";
   return "UNKNOWN";
}

bool GT_EnsureGartalFolder(string file_name)
{
   int slash = StringFind(file_name, "\\");
   if(slash <= 0)
      return true;

   string folder = StringSubstr(file_name, 0, slash);
   if(GT_IsEmpty(folder))
      return true;

   FolderCreate(folder);
   return true;
}

bool GT_ReadTextFile(string file_name, string &raw, GT_RuntimeState &runtime, bool warn_if_missing=true)
{
   raw = "";
   string clean_file = GT_Trim(file_name);
   if(GT_IsEmpty(clean_file))
      return false;

   ResetLastError();
   int handle = FileOpen(clean_file, FILE_READ|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      int err = GetLastError();
      if(warn_if_missing)
         GT_RuntimeLog(runtime, GT_LOG_WARNING, "Cannot read source file '" + clean_file + "'. err=" + IntegerToString(err));
      runtime.source_last_error = "file read failed err=" + IntegerToString(err);
      runtime.source_last_file = clean_file;
      return false;
   }

   while(!FileIsEnding(handle))
      raw += FileReadString(handle) + "\n";

   FileClose(handle);
   raw = GT_Trim(raw);
   runtime.source_last_file = clean_file;
   runtime.source_raw_bytes = StringLen(raw);
   runtime.source_last_fetch_at = TimeCurrent();

   if(StringLen(raw) <= 0)
   {
      runtime.source_last_error = "file was empty: " + clean_file;
      return false;
   }

   GT_RuntimeLog(runtime, GT_LOG_INFO, "Loaded calendar raw file '" + clean_file + "'. bytes=" + IntegerToString(StringLen(raw)));
   return true;
}

bool GT_WriteTextFile(string file_name, string raw, GT_RuntimeState &runtime)
{
   string clean_file = GT_Trim(file_name);
   if(GT_IsEmpty(clean_file) || StringLen(raw) <= 0)
      return false;

   GT_EnsureGartalFolder(clean_file);
   ResetLastError();
   int handle = FileOpen(clean_file, FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      int err = GetLastError();
      GT_RuntimeLog(runtime, GT_LOG_WARNING, "Cannot write source/cache file '" + clean_file + "'. err=" + IntegerToString(err));
      return false;
   }

   FileWriteString(handle, raw);
   FileClose(handle);
   return true;
}

bool GT_LoadLocalRawFile(GT_Config &config, string &raw, GT_RuntimeState &runtime)
{
   runtime.source_fetch_mode_used = GT_FETCH_LOCAL_FILE;
   return GT_ReadTextFile(config.local_raw_file, raw, runtime, true);
}

bool GT_FetchCalendarByWebRequest(GT_Config &config, string &raw, GT_RuntimeState &runtime)
{
   raw = "";
   runtime.source_fetch_mode_used = GT_FETCH_WEBREQUEST;
   runtime.source_last_url = config.source_url;
   runtime.source_permission_hint = "MT5 indicators normally cannot call WebRequest. Use the downloader EA bridge. If testing anyway, add the URL under Tools > Options > Expert Advisors > Allow WebRequest.";

   if(!config.allow_indicator_webrequest)
   {
      runtime.source_last_error = "indicator WebRequest disabled by config";
      GT_RuntimeLog(runtime, GT_LOG_WARNING, runtime.source_permission_hint);
      return false;
   }

   string headers = "User-Agent: " + config.source_user_agent + "\r\nAccept: text/xml,text/csv,text/html,*/*\r\nCache-Control: no-cache\r\n";
   string result_headers = "";
   char post[];
   char result[];

   ResetLastError();
   int timeout = 10000;
   int status = WebRequest("GET", config.source_url, headers, timeout, post, result, result_headers);
   runtime.source_fetch_status_code = status;
   runtime.source_last_fetch_at = TimeCurrent();

   if(status == -1)
   {
      int err = GetLastError();
      runtime.source_last_error = "WebRequest failed err=" + IntegerToString(err);
      if(err == 4014)
         GT_RuntimeLog(runtime, GT_LOG_WARNING, "WebRequest blocked with 4014. Custom indicators cannot use WebRequest directly; run GartalNewsDownloaderEA or read a local bridge file.");
      else
         GT_RuntimeLog(runtime, GT_LOG_WARNING, "WebRequest failed. err=" + IntegerToString(err) + ". Add URL to MT5 allowed list or use downloader EA bridge.");
      return false;
   }

   raw = CharArrayToString(result, 0, -1, CP_UTF8);
   if(StringLen(raw) == 0)
      raw = CharArrayToString(result, 0, -1, CP_ACP);

   runtime.source_raw_bytes = StringLen(raw);
   if(StringLen(raw) == 0)
   {
      runtime.source_last_error = "WebRequest returned empty body status=" + IntegerToString(status);
      GT_RuntimeLog(runtime, GT_LOG_WARNING, runtime.source_last_error);
      return false;
   }

   GT_RuntimeLog(runtime, GT_LOG_INFO, "Calendar fetched by WebRequest. bytes=" + IntegerToString(StringLen(raw)) + ", status=" + IntegerToString(status));

   if(config.save_raw_after_fetch)
      GT_WriteTextFile(config.local_raw_file, raw, runtime);

   return true;
}

bool GT_FetchCalendarRaw(GT_Config &config, string &raw, GT_RuntimeState &runtime)
{
   raw = "";
   runtime.source_fetch_status_code = 0;
   runtime.source_raw_bytes = 0;
   runtime.source_last_error = "";
   runtime.source_last_url = config.source_url;

   if(config.data_mode != GT_DATA_MODE_DIRECT)
      return false;

   if(config.source_fetch_mode == GT_FETCH_LOCAL_FILE)
      return GT_LoadLocalRawFile(config, raw, runtime);

   if(config.source_fetch_mode == GT_FETCH_WEBREQUEST)
      return GT_FetchCalendarByWebRequest(config, raw, runtime);

   // AUTO mode: first trust the safe local bridge. If unavailable, try WebRequest
   // only when the explicit unsafe diagnostic flag is enabled.
   if(GT_LoadLocalRawFile(config, raw, runtime))
      return true;

   return GT_FetchCalendarByWebRequest(config, raw, runtime);
}

bool GT_SaveCache(GT_Config &config, string raw, GT_RuntimeState &runtime)
{
   if(!config.use_cache)
      return false;

   return GT_WriteTextFile(config.local_cache_file, raw, runtime);
}

bool GT_LoadCache(GT_Config &config, string &raw, GT_RuntimeState &runtime)
{
   if(!config.use_cache)
      return false;

   return GT_ReadTextFile(config.local_cache_file, raw, runtime, true);
}

#endif
