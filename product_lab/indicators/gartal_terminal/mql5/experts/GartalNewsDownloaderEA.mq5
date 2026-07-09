//+------------------------------------------------------------------+
//| GartalNewsDownloaderEA.mq5                                       |
//| Stage 08 helper EA: downloads Forex Factory/Fair Economy XML      |
//| and writes a local bridge file for the gartal terminal indicator. |
//+------------------------------------------------------------------+
#property strict
#property version "0.8.0"
#property description "Helper EA for gartal terminal Stage 08 local file bridge"

input string InpSourceUrl       = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml";
input string InpOutputFile      = "GartalTerminal\\ff_calendar_thisweek.xml";
input int    InpRefreshMinutes  = 15;
input bool   InpDownloadOnInit  = true;
input bool   InpPrintRawBytes   = true;
input string InpUserAgent       = "Mozilla/5.0 gartal-terminal-downloader/0.8";

int GTD_ClampInt(int v, int lo, int hi)
{
   if(v < lo) return lo;
   if(v > hi) return hi;
   return v;
}

string GTD_Trim(string value)
{
   string s = value;
   StringTrimLeft(s);
   StringTrimRight(s);
   return s;
}

bool GTD_EnsureFolder(string file_name)
{
   int slash = StringFind(file_name, "\\");
   if(slash <= 0)
      return true;
   string folder = StringSubstr(file_name, 0, slash);
   if(StringLen(folder) > 0)
      FolderCreate(folder);
   return true;
}

bool GTD_WriteTextFile(string file_name, string raw)
{
   string clean = GTD_Trim(file_name);
   if(StringLen(clean) <= 0)
      return false;

   GTD_EnsureFolder(clean);
   ResetLastError();
   int handle = FileOpen(clean, FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      Print("gartal downloader ERROR | FileOpen failed: ", clean, " err=", GetLastError());
      return false;
   }

   FileWriteString(handle, raw);
   FileClose(handle);
   return true;
}

bool GTD_Download()
{
   string url = GTD_Trim(InpSourceUrl);
   if(StringLen(url) <= 0)
   {
      Print("gartal downloader ERROR | Source URL is empty.");
      return false;
   }

   string headers = "User-Agent: " + InpUserAgent + "\r\nAccept: text/xml,text/csv,text/html,*/*\r\nCache-Control: no-cache\r\n";
   string result_headers = "";
   char post[];
   char result[];

   ResetLastError();
   int status = WebRequest("GET", url, headers, 10000, post, result, result_headers);
   if(status == -1)
   {
      int err = GetLastError();
      Print("gartal downloader ERROR | WebRequest failed err=", err, ". Add URL under Tools > Options > Expert Advisors > Allow WebRequest.");
      return false;
   }

   string raw = CharArrayToString(result, 0, -1, CP_UTF8);
   if(StringLen(raw) == 0)
      raw = CharArrayToString(result, 0, -1, CP_ACP);

   if(StringLen(raw) <= 0)
   {
      Print("gartal downloader WARNING | Empty body. status=", status);
      return false;
   }

   if(!GTD_WriteTextFile(InpOutputFile, raw))
      return false;

   if(InpPrintRawBytes)
      Print("gartal downloader INFO | downloaded bytes=", StringLen(raw), " status=", status, " file=", InpOutputFile);

   return true;
}

int OnInit()
{
   int seconds = GTD_ClampInt(InpRefreshMinutes, 5, 240) * 60;
   EventSetTimer(seconds);

   if(InpDownloadOnInit)
      GTD_Download();

   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   EventKillTimer();
}

void OnTimer()
{
   GTD_Download();
}
