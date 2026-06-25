#ifndef __DAL_ASTRO_EXECUTION_JOURNAL_MQH__
#define __DAL_ASTRO_EXECUTION_JOURNAL_MQH__

#include <Research/DAL_AstroExecutionStateMachine.mqh>

bool DAL_AstroJournal_EnsureHeader(const string file_name, const bool use_common)
{
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

   FileWriteString(h, "broker_time,utc_time,family_name,doctrine_id,schema_version,phase,action,position_direction,entry_signal,exit_signal,direction_name,regime_name,entry_score,exit_score,long_bias_score,short_bias_score,path_score,friction_score,volatility_score,natal_activation_score,feature_key,astro_trade_key,astro_language,reason,hold_bars\r\n");
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
   string line =
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
      DAL_AstroJournal_Safe(row.feature_key) + "," +
      DAL_AstroJournal_Safe(signal.astro_trade_key) + "," +
      DAL_AstroJournal_Safe(signal.astro_language) + "," +
      DAL_AstroJournal_Safe(state.last_reason) + "," +
      IntegerToString(state.hold_bars) + "\r\n";
   FileWriteString(h, line);
   FileClose(h);
   return true;
}

#endif
