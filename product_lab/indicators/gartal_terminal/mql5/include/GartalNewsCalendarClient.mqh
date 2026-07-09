#ifndef GARTAL_NEWS_CALENDAR_CLIENT_MQH
#define GARTAL_NEWS_CALENDAR_CLIENT_MQH

bool GT_FetchCalendarRaw(GT_Config &config, string &raw, GT_RuntimeState &runtime)
{
   raw = "";

   // Stage 01 contract:
   // Direct WebRequest is intentionally present but not the primary path.
   // The default mode is sample data. Real Forex Factory parsing starts in Stage 08.
   if(config.data_mode != GT_DATA_MODE_DIRECT)
      return false;

   string headers = "User-Agent: Mozilla/5.0\r\nAccept: text/html\r\n";
   string result_headers = "";
   char post[];
   char result[];

   ResetLastError();
   int timeout = 10000;
   int status = WebRequest("GET", config.source_url, headers, timeout, post, result, result_headers);

   if(status == -1)
   {
      GT_RuntimeLog(runtime, GT_LOG_WARNING, "WebRequest failed. err=" + IntegerToString(GetLastError()) + ". Add the URL in MT5 WebRequest allowed list.");
      return false;
   }

   raw = CharArrayToString(result, 0, -1, CP_UTF8);
   if(StringLen(raw) == 0)
   {
      GT_RuntimeLog(runtime, GT_LOG_WARNING, "WebRequest returned empty body. status=" + IntegerToString(status));
      return false;
   }

   GT_RuntimeLog(runtime, GT_LOG_INFO, "Raw calendar fetched. bytes=" + IntegerToString(StringLen(raw)) + ", status=" + IntegerToString(status));
   return true;
}

bool GT_SaveCache(GT_Config &config, string raw, GT_RuntimeState &runtime)
{
   if(!config.use_cache)
      return false;

   string folder = "GartalTerminal";
   FolderCreate(folder);
   string file_name = folder + "\\calendar_cache.txt";
   int handle = FileOpen(file_name, FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      GT_RuntimeLog(runtime, GT_LOG_WARNING, "Cache save failed. err=" + IntegerToString(GetLastError()));
      return false;
   }

   FileWriteString(handle, raw);
   FileClose(handle);
   return true;
}

bool GT_LoadCache(GT_Config &config, string &raw, GT_RuntimeState &runtime)
{
   raw = "";
   string file_name = "GartalTerminal\\calendar_cache.txt";
   int handle = FileOpen(file_name, FILE_READ|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      GT_RuntimeLog(runtime, GT_LOG_WARNING, "No readable cache. err=" + IntegerToString(GetLastError()));
      return false;
   }

   while(!FileIsEnding(handle))
      raw += FileReadString(handle) + "\n";

   FileClose(handle);
   return (StringLen(raw) > 0);
}

#endif
