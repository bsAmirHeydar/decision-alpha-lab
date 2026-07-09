#ifndef GARTAL_NEWS_CALENDAR_CLIENT_MQH
#define GARTAL_NEWS_CALENDAR_CLIENT_MQH

bool GT_FetchCalendarRaw(GT_Config &config, string &raw)
{
   raw = "";

   string headers = "User-Agent: Mozilla/5.0\r\n";
   string result_headers;
   char post[], result[];
   ResetLastError();

   // Production note:
   // User must whitelist the source URL in:
   // MT5 → Tools → Options → Expert Advisors → Allow WebRequest for listed URL.
   int timeout = 10000;
   int status = WebRequest("GET", config.source_url, headers, timeout, post, result, result_headers);

   if(status == -1)
   {
      Print("gartal terminal WebRequest failed. err=", GetLastError());
      return false;
   }

   raw = CharArrayToString(result, 0, -1, CP_UTF8);
   return (StringLen(raw) > 0);
}

bool GT_SaveCache(GT_Config &config, string raw)
{
   if(!config.use_cache)
      return false;

   string folder = "GartalTerminal";
   FolderCreate(folder);
   string file_name = folder + "\\calendar_cache.txt";
   int handle = FileOpen(file_name, FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
      return false;

   FileWriteString(handle, raw);
   FileClose(handle);
   return true;
}

bool GT_LoadCache(GT_Config &config, string &raw)
{
   raw = "";
   string file_name = "GartalTerminal\\calendar_cache.txt";
   int handle = FileOpen(file_name, FILE_READ|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
      return false;

   while(!FileIsEnding(handle))
      raw += FileReadString(handle) + "\n";

   FileClose(handle);
   return (StringLen(raw) > 0);
}

#endif
