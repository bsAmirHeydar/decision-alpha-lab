#ifndef __DAL_ASTRO_SIGNAL_WINDOWS_MQH__
#define __DAL_ASTRO_SIGNAL_WINDOWS_MQH__

#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroPureAstrologySignals.mqh>

struct DAL_AstroSignalWindow
{
   bool     valid;
   int      start_index;
   int      end_index;
   int      bars;
   datetime start_broker_time;
   datetime end_broker_time;
   datetime end_exclusive_broker_time;
   string   key;
   string   direction_name;
   string   entry_signal;
   string   exit_signal;
   string   regime_name;
   string   trigger_state;
   double   avg_entry_score;
   double   avg_exit_score;
   double   avg_path_score;
   double   avg_friction_score;
   double   avg_natal_activation_score;
};

void DAL_AstroSignalWindow_Reset(DAL_AstroSignalWindow &w)
{
   w.valid = false;
   w.start_index = -1;
   w.end_index = -1;
   w.bars = 0;
   w.start_broker_time = 0;
   w.end_broker_time = 0;
   w.end_exclusive_broker_time = 0;
   w.key = "";
   w.direction_name = "flat";
   w.entry_signal = "wait";
   w.exit_signal = "hold";
   w.regime_name = "neutral";
   w.trigger_state = "standby";
   w.avg_entry_score = 0.0;
   w.avg_exit_score = 0.0;
   w.avg_path_score = 0.0;
   w.avg_friction_score = 0.0;
   w.avg_natal_activation_score = 0.0;
}


bool DAL_AstroSW_EnsureParentFolder(const string file_name, const bool use_common)
{
   int last_slash = -1;
   string normalized = file_name;
   StringReplace(normalized, "/", "\\");
   for(int i = 0; i < StringLen(normalized); i++)
   {
      if(StringSubstr(normalized, i, 1) == "\\")
         last_slash = i;
   }
   if(last_slash <= 0)
      return true;

   string folder = StringSubstr(normalized, 0, last_slash);
   int flags = use_common ? FILE_COMMON : 0;
   string acc = "";
   for(int j = 0; j < StringLen(folder); j++)
   {
      string ch = StringSubstr(folder, j, 1);
      if(ch == "\\")
      {
         if(acc != "")
            FolderCreate(acc, flags);
      }
      acc += ch;
   }
   if(acc != "")
      FolderCreate(acc, flags);
   return true;
}



string DAL_AstroSW_TimeText(const datetime t)
{
   if(t <= 0)
      return "n/a";
   return TimeToString(t, TIME_DATE | TIME_MINUTES);
}

string DAL_AstroSW_Safe(string value)
{
   StringReplace(value, "\"", "'");
   StringReplace(value, ",", ";");
   StringReplace(value, "\r", " ");
   StringReplace(value, "\n", " ");
   return value;
}

string DAL_AstroSW_Key(const DAL_AstroPureSignal &s)
{
   return "dir=" + s.direction_name +
          "|entry=" + s.entry_signal +
          "|exit=" + s.exit_signal +
          "|regime=" + s.regime_name +
          "|state=" + s.trigger_state;
}

int DAL_AstroSW_TimeframeSeconds(const DAL_AstroMapStore &store)
{
   if(store.timeframe_minutes > 0)
      return store.timeframe_minutes * 60;
   if(store.row_count >= 2)
   {
      int sec = (int)(store.rows[1].broker_time - store.rows[0].broker_time);
      if(sec > 0)
         return sec;
   }
   return 60;
}

bool DAL_AstroSW_CalcAt(const DAL_AstroMapStore &store, const int index, DAL_AstroPureSignal &s, string &key)
{
   key = "";
   if(index < 0 || index >= store.row_count)
      return false;
   if(!DAL_AstroPureSignal_Calc(store.rows[index], s) || !s.valid)
      return false;
   key = DAL_AstroSW_Key(s);
   return true;
}

bool DAL_AstroSW_FindWindowByIndex(const DAL_AstroMapStore &store, const int index, DAL_AstroSignalWindow &w)
{
   DAL_AstroSignalWindow_Reset(w);
   if(!store.loaded || index < 0 || index >= store.row_count)
      return false;

   DAL_AstroPureSignal s0;
   string key0 = "";
   if(!DAL_AstroSW_CalcAt(store, index, s0, key0))
      return false;

   int first = index;
   for(int i = index - 1; i >= 0; i--)
   {
      DAL_AstroPureSignal sp;
      string kp = "";
      if(!DAL_AstroSW_CalcAt(store, i, sp, kp) || kp != key0)
         break;
      first = i;
   }

   int last = index;
   for(int j = index + 1; j < store.row_count; j++)
   {
      DAL_AstroPureSignal sn;
      string kn = "";
      if(!DAL_AstroSW_CalcAt(store, j, sn, kn) || kn != key0)
         break;
      last = j;
   }

   double entry_sum = 0.0;
   double exit_sum = 0.0;
   double path_sum = 0.0;
   double friction_sum = 0.0;
   double natal_sum = 0.0;
   int n = 0;
   for(int k = first; k <= last; k++)
   {
      DAL_AstroPureSignal sx;
      string kx = "";
      if(!DAL_AstroSW_CalcAt(store, k, sx, kx))
         continue;
      entry_sum += sx.entry_score;
      exit_sum += sx.exit_score;
      path_sum += sx.path_score;
      friction_sum += sx.friction_score;
      natal_sum += sx.natal_activation_score;
      n++;
   }
   if(n <= 0)
      return false;

   w.valid = true;
   w.start_index = first;
   w.end_index = last;
   w.bars = last - first + 1;
   w.start_broker_time = store.rows[first].broker_time;
   w.end_broker_time = store.rows[last].broker_time;
   if(last + 1 < store.row_count)
      w.end_exclusive_broker_time = store.rows[last + 1].broker_time;
   else
      w.end_exclusive_broker_time = store.rows[last].broker_time + DAL_AstroSW_TimeframeSeconds(store);
   w.key = key0;
   w.direction_name = s0.direction_name;
   w.entry_signal = s0.entry_signal;
   w.exit_signal = s0.exit_signal;
   w.regime_name = s0.regime_name;
   w.trigger_state = s0.trigger_state;
   w.avg_entry_score = entry_sum / n;
   w.avg_exit_score = exit_sum / n;
   w.avg_path_score = path_sum / n;
   w.avg_friction_score = friction_sum / n;
   w.avg_natal_activation_score = natal_sum / n;
   return true;
}

bool DAL_AstroSW_FindWindowByBrokerTime(const DAL_AstroMapStore &store, const datetime broker_time, const bool require_exact, DAL_AstroSignalWindow &w)
{
   int idx = DAL_AstroMapStore_FindIndexByBrokerTime(store, broker_time, require_exact);
   if(idx < 0)
   {
      DAL_AstroSignalWindow_Reset(w);
      return false;
   }
   return DAL_AstroSW_FindWindowByIndex(store, idx, w);
}

string DAL_AstroSW_WindowLabel(const DAL_AstroSignalWindow &w)
{
   if(!w.valid)
      return "window n/a";
   return DAL_AstroSW_TimeText(w.start_broker_time) + " -> " + DAL_AstroSW_TimeText(w.end_exclusive_broker_time) + " excl";
}

bool DAL_AstroSW_ExportPureWindows(const string file_name, const bool use_common, const DAL_AstroMapStore &store)
{
   if(!store.loaded || store.row_count <= 0)
      return false;

   DAL_AstroSW_EnsureParentFolder(file_name, use_common);

   int flags = FILE_WRITE | FILE_TXT | FILE_ANSI;
   if(use_common)
      flags |= FILE_COMMON;
   ResetLastError();
   int h = FileOpen(file_name, flags);
   if(h == INVALID_HANDLE)
      return false;

   FileWriteString(h, "window_start_broker,window_end_broker,window_end_exclusive_broker,bars,direction,entry,exit,regime,state,avg_entry_score,avg_exit_score,avg_path_score,avg_friction_score,avg_natal_activation_score,key\r\n");

   int i = 0;
   while(i < store.row_count)
   {
      DAL_AstroSignalWindow w;
      if(!DAL_AstroSW_FindWindowByIndex(store, i, w) || !w.valid)
      {
         i++;
         continue;
      }

      string line =
         TimeToString(w.start_broker_time, TIME_DATE | TIME_SECONDS) + "," +
         TimeToString(w.end_broker_time, TIME_DATE | TIME_SECONDS) + "," +
         TimeToString(w.end_exclusive_broker_time, TIME_DATE | TIME_SECONDS) + "," +
         IntegerToString(w.bars) + "," +
         w.direction_name + "," +
         w.entry_signal + "," +
         w.exit_signal + "," +
         w.regime_name + "," +
         w.trigger_state + "," +
         DoubleToString(w.avg_entry_score, 4) + "," +
         DoubleToString(w.avg_exit_score, 4) + "," +
         DoubleToString(w.avg_path_score, 4) + "," +
         DoubleToString(w.avg_friction_score, 4) + "," +
         DoubleToString(w.avg_natal_activation_score, 4) + "," +
         DAL_AstroSW_Safe(w.key) + "\r\n";
      FileWriteString(h, line);
      i = w.end_index + 1;
   }

   FileClose(h);
   return true;
}

#endif
