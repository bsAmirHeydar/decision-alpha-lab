#ifndef __DAL_ASTRO_EXECUTION_JOURNAL_MQH__
#define __DAL_ASTRO_EXECUTION_JOURNAL_MQH__

#include <Research/DAL_AstroExecutionStateMachine.mqh>

string DAL_AstroJournal_Header()
{
   return "broker_time,utc_time,family_name,doctrine_id,schema_version,phase,action,position_direction,entry_signal,exit_signal,direction_name,regime_name,entry_score,exit_score,long_bias_score,short_bias_score,path_score,friction_score,volatility_score,natal_activation_score,macro_timing_score,meso_timing_score,micro_timing_score,minute_window_score,minute_exhaustion_score,trigger_state,macro_context,meso_context,micro_context,minute_context,feature_key,astro_trade_key,astro_language,reason,hold_bars\r\n";
}

bool DAL_AstroJournal_EnsureParentFolder(const string file_name, const bool use_common)
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

bool DAL_AstroJournal_EnsureHeader(const string file_name, const bool use_common)
{
   DAL_AstroJournal_EnsureParentFolder(file_name, use_common);

   ResetLastError();
   int flags = FILE_READ | FILE_TXT | FILE_ANSI;
   if(use_common)
      flags |= FILE_COMMON;
   int h = FileOpen(file_name, flags);
   if(h != INVALID_HANDLE)
   {
      FileClose(h);
      return true;
   }

   flags = FILE_WRITE | FILE_TXT | FILE_ANSI;
   if(use_common)
      flags |= FILE_COMMON;
   h = FileOpen(file_name, flags);
   if(h == INVALID_HANDLE)
      return false;

   FileWriteString(h, DAL_AstroJournal_Header());
   FileClose(h);
   return true;
}

string DAL_AstroJournal_Safe(string value)
{
   StringReplace(value, "\"", "'");
   StringReplace(value, ",", ";");
   StringReplace(value, "\r", " ");
   StringReplace(value, "\n", " ");
   return value;
}

string DAL_AstroJournal_Line(
   const DAL_AstroMapRow &row,
   const DAL_AstroPureSignal &signal,
   const DAL_AstroExecState &state
)
{
   return
      TimeToString(row.broker_time, TIME_DATE | TIME_SECONDS) + "," +
      TimeToString(row.utc_time, TIME_DATE | TIME_SECONDS) + "," +
      DAL_AstroJournal_Safe(state.family_name) + "," +
      DAL_AstroJournal_Safe(row.doctrine_id) + "," +
      DAL_AstroJournal_Safe(row.schema_version) + "," +
      state.phase + "," +
      state.action + "," +
      state.position_direction + "," +
      signal.entry_signal + "," +
      signal.exit_signal + "," +
      signal.direction_name + "," +
      signal.regime_name + "," +
      DoubleToString(signal.entry_score, 4) + "," +
      DoubleToString(signal.exit_score, 4) + "," +
      DoubleToString(signal.long_bias_score, 4) + "," +
      DoubleToString(signal.short_bias_score, 4) + "," +
      DoubleToString(signal.path_score, 4) + "," +
      DoubleToString(signal.friction_score, 4) + "," +
      DoubleToString(signal.volatility_score, 4) + "," +
      DoubleToString(signal.natal_activation_score, 4) + "," +
      DoubleToString(signal.macro_timing_score, 4) + "," +
      DoubleToString(signal.meso_timing_score, 4) + "," +
      DoubleToString(signal.micro_timing_score, 4) + "," +
      DoubleToString(signal.minute_window_score, 4) + "," +
      DoubleToString(signal.minute_exhaustion_score, 4) + "," +
      signal.trigger_state + "," +
      DAL_AstroJournal_Safe(signal.macro_context) + "," +
      DAL_AstroJournal_Safe(signal.meso_context) + "," +
      DAL_AstroJournal_Safe(signal.micro_context) + "," +
      DAL_AstroJournal_Safe(signal.minute_context) + "," +
      DAL_AstroJournal_Safe(row.feature_key) + "," +
      DAL_AstroJournal_Safe(signal.astro_trade_key) + "," +
      DAL_AstroJournal_Safe(signal.astro_language) + "," +
      DAL_AstroJournal_Safe(state.last_reason) + "," +
      IntegerToString(state.hold_bars) + "\r\n";
}

bool DAL_AstroJournal_OpenReset(const string file_name, const bool use_common, int &handle)
{
   handle = INVALID_HANDLE;
   DAL_AstroJournal_EnsureParentFolder(file_name, use_common);

   int flags = FILE_WRITE | FILE_TXT | FILE_ANSI;
   if(use_common)
      flags |= FILE_COMMON;
   ResetLastError();
   handle = FileOpen(file_name, flags);
   if(handle == INVALID_HANDLE)
      return false;
   FileWriteString(handle, DAL_AstroJournal_Header());
   return true;
}

bool DAL_AstroJournal_WriteHandle(
   const int handle,
   const DAL_AstroMapRow &row,
   const DAL_AstroPureSignal &signal,
   const DAL_AstroExecState &state
)
{
   if(handle == INVALID_HANDLE)
      return false;
   FileWriteString(handle, DAL_AstroJournal_Line(row, signal, state));
   return true;
}

bool DAL_AstroJournal_ResetFile(const string file_name, const bool use_common)
{
   int h = INVALID_HANDLE;
   if(!DAL_AstroJournal_OpenReset(file_name, use_common, h))
      return false;
   FileClose(h);
   return true;
}

bool DAL_AstroJournal_Append(
   const string file_name,
   const bool use_common,
   const DAL_AstroMapRow &row,
   const DAL_AstroPureSignal &signal,
   const DAL_AstroExecState &state
)
{
   if(!DAL_AstroJournal_EnsureHeader(file_name, use_common))
      return false;

   int flags = FILE_READ | FILE_WRITE | FILE_TXT | FILE_ANSI;
   if(use_common)
      flags |= FILE_COMMON;
   ResetLastError();
   int h = FileOpen(file_name, flags);
   if(h == INVALID_HANDLE)
      return false;

   FileSeek(h, 0, SEEK_END);
   FileWriteString(h, DAL_AstroJournal_Line(row, signal, state));
   FileClose(h);
   return true;
}

#endif
