#ifndef __DAL_STC_PERSISTENCE_MQH__
#define __DAL_STC_PERSISTENCE_MQH__
#property strict

#include <IntermarketDivergenceExecution/STC/DAL_STC_HardClose.mqh>

int STC_ParseIntDefault(const string value, const int fallback)
{
   if(value == "") return fallback;
   return (int)StringToInteger(value);
}

long STC_ParseLongDefault(const string value, const long fallback)
{
   if(value == "") return fallback;
   return (long)StringToInteger(value);
}

bool STC_ParseBoolDefault(const string value, const bool fallback)
{
   if(value == "true" || value == "TRUE" || value == "1") return true;
   if(value == "false" || value == "FALSE" || value == "0") return false;
   return fallback;
}

STC_Direction STC_ParseDirectionDefault(const string value, const STC_Direction fallback)
{
   int v = STC_ParseIntDefault(value, (int)fallback);
   if(v == (int)STC_DIR_BUY) return STC_DIR_BUY;
   if(v == (int)STC_DIR_SELL) return STC_DIR_SELL;
   return STC_DIR_NONE;
}

bool STC_ReadKeyValueSnapshot(const string file_common, string &keys[], string &values[], int &count)
{
   count = 0;
   ArrayResize(keys, 0);
   ArrayResize(values, 0);
   if(!FileIsExist(file_common, FILE_COMMON))
      return false;

   int h = FileOpen(file_common, FILE_READ | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to read persistence snapshot ", file_common, " err=", GetLastError());
      return false;
   }

   while(!FileIsEnding(h))
   {
      string k = FileReadString(h);
      if(FileIsEnding(h) && k == "")
         break;
      string v = "";
      if(!FileIsEnding(h))
         v = FileReadString(h);
      if(k == "" || k == "field")
         continue;
      int n = count + 1;
      ArrayResize(keys, n);
      ArrayResize(values, n);
      keys[count] = k;
      values[count] = v;
      count = n;
   }
   FileClose(h);
   return (count > 0);
}

bool STC_GetSnapshotValue(string &keys[], string &values[], const int count, const string key, string &value)
{
   for(int i = 0; i < count; i++)
   {
      if(keys[i] == key)
      {
         value = values[i];
         return true;
      }
   }
   value = "";
   return false;
}

string STC_SnapshotValue(string &keys[], string &values[], const int count, const string key, const string fallback)
{
   string v = "";
   if(STC_GetSnapshotValue(keys, values, count, key, v)) return v;
   return fallback;
}

void STC_AppendPersistenceRecoveryCsv(STC_Config &cfg, STC_RuntimeState &state, const string event_type, const string status, const string note)
{
   if(state.persistence_recovery_audit_file_common == "") return;
   bool exists = FileIsExist(state.persistence_recovery_audit_file_common, FILE_COMMON);
   int h = FileOpen(state.persistence_recovery_audit_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append persistence recovery CSV ", state.persistence_recovery_audit_file_common, " err=", GetLastError());
      return;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h,
         "server_write_time", "strategy_id", "run_id", "symbol1", "symbol2", "magic_number",
         "event_type", "status", "stc_day_id", "snapshot_file", "restored", "note",
         "last_check", "last_w", "last_hunt", "last_smt", "last_signal", "last_paper", "last_outcome", "last_partial", "last_hard_close",
         "paper_counts", "paper_locks", "outcome_counts", "outcome_locks", "partial_counts", "partial_locks");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h,
      STC_TimeText(TimeCurrent()), cfg.strategy_id, cfg.run_id, cfg.symbol1, cfg.symbol2, cfg.magic_number,
      event_type, status, state.last_check_audit_stc_day_id, state.persistence_snapshot_file_common, STC_BoolText(state.persistence_restored), note,
      state.last_check_audit_index, state.last_w_level_audit_serial, state.last_hunt_audit_check_index, state.last_smt_audit_check_index, state.last_signal_audit_check_index, state.last_paper_entry_check_index, state.last_paper_outcome_check_index, state.last_partial_audit_check_index, state.last_hard_close_audit_check_index,
      IntegerToString(state.paper_trade_count_m1) + ":" + IntegerToString(state.paper_trade_count_m2) + ":" + IntegerToString(state.paper_trade_count_m3),
      IntegerToString((int)state.paper_direction_lock_m1) + ":" + IntegerToString((int)state.paper_direction_lock_m2) + ":" + IntegerToString((int)state.paper_direction_lock_m3),
      IntegerToString(state.outcome_trade_count_m1) + ":" + IntegerToString(state.outcome_trade_count_m2) + ":" + IntegerToString(state.outcome_trade_count_m3),
      IntegerToString((int)state.outcome_direction_lock_m1) + ":" + IntegerToString((int)state.outcome_direction_lock_m2) + ":" + IntegerToString((int)state.outcome_direction_lock_m3),
      IntegerToString(state.partial_trade_count_m1) + ":" + IntegerToString(state.partial_trade_count_m2) + ":" + IntegerToString(state.partial_trade_count_m3),
      IntegerToString((int)state.partial_direction_lock_m1) + ":" + IntegerToString((int)state.partial_direction_lock_m2) + ":" + IntegerToString((int)state.partial_direction_lock_m3));
   FileClose(h);
}

void STC_WritePersistenceField(const int h, const string field, const string value)
{
   FileWrite(h, field, value);
}

bool STC_WritePersistenceSnapshot(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap, const string reason)
{
   if(!cfg.write_persistence_snapshot) return false;
   if(state.persistence_snapshot_file_common == "") return false;
   if(snap.stc_day_id == "") return false;

   int h = FileOpen(state.persistence_snapshot_file_common, FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to write persistence snapshot ", state.persistence_snapshot_file_common, " err=", GetLastError());
      STC_AppendPersistenceRecoveryCsv(cfg, state, "SNAPSHOT_WRITE_FAILED", "FAILED", "FileOpen failed for persistence snapshot");
      return false;
   }

   STC_WritePersistenceField(h, "field", "value");
   STC_WritePersistenceField(h, "schema", "DAL_STC_LEVEL12_PERSISTENCE_V1");
   STC_WritePersistenceField(h, "write_reason", reason);
   STC_WritePersistenceField(h, "write_server_time", STC_TimeText(TimeCurrent()));
   STC_WritePersistenceField(h, "strategy_id", cfg.strategy_id);
   STC_WritePersistenceField(h, "run_id", cfg.run_id);
   STC_WritePersistenceField(h, "symbol1", cfg.symbol1);
   STC_WritePersistenceField(h, "symbol2", cfg.symbol2);
   STC_WritePersistenceField(h, "magic_number", IntegerToString(cfg.magic_number));
   STC_WritePersistenceField(h, "check_minutes", IntegerToString(cfg.check_minutes));
   STC_WritePersistenceField(h, "stc_day_id", snap.stc_day_id);
   STC_WritePersistenceField(h, "ny_time", STC_TimeText(snap.ny_time));
   STC_WritePersistenceField(h, "last_check_audit_stc_day_id", state.last_check_audit_stc_day_id);
   STC_WritePersistenceField(h, "last_check_audit_index", IntegerToString(state.last_check_audit_index));
   STC_WritePersistenceField(h, "last_w_level_audit_stc_day_id", state.last_w_level_audit_stc_day_id);
   STC_WritePersistenceField(h, "last_w_level_audit_serial", IntegerToString(state.last_w_level_audit_serial));
   STC_WritePersistenceField(h, "last_hunt_audit_stc_day_id", state.last_hunt_audit_stc_day_id);
   STC_WritePersistenceField(h, "last_hunt_audit_check_index", IntegerToString(state.last_hunt_audit_check_index));
   STC_WritePersistenceField(h, "last_smt_audit_stc_day_id", state.last_smt_audit_stc_day_id);
   STC_WritePersistenceField(h, "last_smt_audit_check_index", IntegerToString(state.last_smt_audit_check_index));
   STC_WritePersistenceField(h, "last_signal_audit_stc_day_id", state.last_signal_audit_stc_day_id);
   STC_WritePersistenceField(h, "last_signal_audit_check_index", IntegerToString(state.last_signal_audit_check_index));
   STC_WritePersistenceField(h, "last_paper_entry_stc_day_id", state.last_paper_entry_stc_day_id);
   STC_WritePersistenceField(h, "last_paper_entry_check_index", IntegerToString(state.last_paper_entry_check_index));
   STC_WritePersistenceField(h, "last_paper_outcome_stc_day_id", state.last_paper_outcome_stc_day_id);
   STC_WritePersistenceField(h, "last_paper_outcome_check_index", IntegerToString(state.last_paper_outcome_check_index));
   STC_WritePersistenceField(h, "last_partial_audit_stc_day_id", state.last_partial_audit_stc_day_id);
   STC_WritePersistenceField(h, "last_partial_audit_check_index", IntegerToString(state.last_partial_audit_check_index));
   STC_WritePersistenceField(h, "last_hard_close_audit_stc_day_id", state.last_hard_close_audit_stc_day_id);
   STC_WritePersistenceField(h, "last_hard_close_audit_check_index", IntegerToString(state.last_hard_close_audit_check_index));
   STC_WritePersistenceField(h, "check_candles_audited", IntegerToString((int)state.check_candles_audited));
   STC_WritePersistenceField(h, "w_levels_audited", IntegerToString((int)state.w_levels_audited));
   STC_WritePersistenceField(h, "hunt_rows_audited", IntegerToString((int)state.hunt_rows_audited));
   STC_WritePersistenceField(h, "smt_candidate_rows_audited", IntegerToString((int)state.smt_candidate_rows_audited));
   STC_WritePersistenceField(h, "signal_rows_audited", IntegerToString((int)state.signal_rows_audited));
   STC_WritePersistenceField(h, "paper_entry_rows_audited", IntegerToString((int)state.paper_entry_rows_audited));
   STC_WritePersistenceField(h, "paper_outcome_rows_audited", IntegerToString((int)state.paper_outcome_rows_audited));
   STC_WritePersistenceField(h, "partial_rows_audited", IntegerToString((int)state.partial_rows_audited));
   STC_WritePersistenceField(h, "hard_close_rows_audited", IntegerToString((int)state.hard_close_rows_audited));
   STC_WritePersistenceField(h, "paper_trade_count_m1", IntegerToString(state.paper_trade_count_m1));
   STC_WritePersistenceField(h, "paper_trade_count_m2", IntegerToString(state.paper_trade_count_m2));
   STC_WritePersistenceField(h, "paper_trade_count_m3", IntegerToString(state.paper_trade_count_m3));
   STC_WritePersistenceField(h, "paper_direction_lock_m1", IntegerToString((int)state.paper_direction_lock_m1));
   STC_WritePersistenceField(h, "paper_direction_lock_m2", IntegerToString((int)state.paper_direction_lock_m2));
   STC_WritePersistenceField(h, "paper_direction_lock_m3", IntegerToString((int)state.paper_direction_lock_m3));
   STC_WritePersistenceField(h, "outcome_trade_count_m1", IntegerToString(state.outcome_trade_count_m1));
   STC_WritePersistenceField(h, "outcome_trade_count_m2", IntegerToString(state.outcome_trade_count_m2));
   STC_WritePersistenceField(h, "outcome_trade_count_m3", IntegerToString(state.outcome_trade_count_m3));
   STC_WritePersistenceField(h, "outcome_direction_lock_m1", IntegerToString((int)state.outcome_direction_lock_m1));
   STC_WritePersistenceField(h, "outcome_direction_lock_m2", IntegerToString((int)state.outcome_direction_lock_m2));
   STC_WritePersistenceField(h, "outcome_direction_lock_m3", IntegerToString((int)state.outcome_direction_lock_m3));
   STC_WritePersistenceField(h, "partial_trade_count_m1", IntegerToString(state.partial_trade_count_m1));
   STC_WritePersistenceField(h, "partial_trade_count_m2", IntegerToString(state.partial_trade_count_m2));
   STC_WritePersistenceField(h, "partial_trade_count_m3", IntegerToString(state.partial_trade_count_m3));
   STC_WritePersistenceField(h, "partial_direction_lock_m1", IntegerToString((int)state.partial_direction_lock_m1));
   STC_WritePersistenceField(h, "partial_direction_lock_m2", IntegerToString((int)state.partial_direction_lock_m2));
   STC_WritePersistenceField(h, "partial_direction_lock_m3", IntegerToString((int)state.partial_direction_lock_m3));
   FileClose(h);

   state.last_persistence_snapshot_server_time = TimeCurrent();
   STC_AppendPersistenceRecoveryCsv(cfg, state, "SNAPSHOT_WRITE", "OK", "reason=" + reason + "; stc_day=" + snap.stc_day_id);
   return true;
}

bool STC_RestorePersistenceSnapshot(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap)
{
   state.persistence_restored = false;
   state.persistence_restore_status = "NOT_ATTEMPTED";
   state.persistence_restore_note = "";

   if(!cfg.restore_persistence_on_init)
   {
      state.persistence_restore_status = "DISABLED";
      state.persistence_restore_note = "restore disabled by input";
      STC_AppendPersistenceRecoveryCsv(cfg, state, "RESTORE", state.persistence_restore_status, state.persistence_restore_note);
      return false;
   }
   if(snap.stc_day_id == "")
   {
      state.persistence_restore_status = "SKIPPED_NO_STC_DAY";
      state.persistence_restore_note = "current time is outside a restorable STC trading day";
      STC_AppendPersistenceRecoveryCsv(cfg, state, "RESTORE", state.persistence_restore_status, state.persistence_restore_note);
      return false;
   }

   string keys[];
   string values[];
   int count = 0;
   if(!STC_ReadKeyValueSnapshot(state.persistence_snapshot_file_common, keys, values, count))
   {
      state.persistence_restore_status = "SKIPPED_NO_SNAPSHOT";
      state.persistence_restore_note = "no previous level13 run snapshot found";
      STC_AppendPersistenceRecoveryCsv(cfg, state, "RESTORE", state.persistence_restore_status, state.persistence_restore_note);
      return false;
   }

   string stored_schema = STC_SnapshotValue(keys, values, count, "schema", "");
   string stored_strategy = STC_SnapshotValue(keys, values, count, "strategy_id", "");
   string stored_symbol1 = STC_SnapshotValue(keys, values, count, "symbol1", "");
   string stored_symbol2 = STC_SnapshotValue(keys, values, count, "symbol2", "");
   string stored_magic = STC_SnapshotValue(keys, values, count, "magic_number", "");
   string stored_check = STC_SnapshotValue(keys, values, count, "check_minutes", "");
   string stored_day = STC_SnapshotValue(keys, values, count, "stc_day_id", "");

   if(stored_schema != "DAL_STC_LEVEL12_PERSISTENCE_V1")
   {
      state.persistence_restore_status = "SKIPPED_SCHEMA_MISMATCH";
      state.persistence_restore_note = "snapshot schema mismatch: " + stored_schema;
      STC_AppendPersistenceRecoveryCsv(cfg, state, "RESTORE", state.persistence_restore_status, state.persistence_restore_note);
      return false;
   }
   if(stored_strategy != cfg.strategy_id || stored_symbol1 != cfg.symbol1 || stored_symbol2 != cfg.symbol2 || stored_magic != IntegerToString(cfg.magic_number) || stored_check != IntegerToString(cfg.check_minutes))
   {
      state.persistence_restore_status = "SKIPPED_CONFIG_MISMATCH";
      state.persistence_restore_note = "snapshot belongs to different strategy/symbol/magic/check setup";
      STC_AppendPersistenceRecoveryCsv(cfg, state, "RESTORE", state.persistence_restore_status, state.persistence_restore_note);
      return false;
   }
   if(stored_day != snap.stc_day_id)
   {
      state.persistence_restore_status = "SKIPPED_DIFFERENT_STC_DAY";
      state.persistence_restore_note = "stored_day=" + stored_day + "; current_day=" + snap.stc_day_id;
      STC_AppendPersistenceRecoveryCsv(cfg, state, "RESTORE", state.persistence_restore_status, state.persistence_restore_note);
      return false;
   }

   state.last_check_audit_stc_day_id = STC_SnapshotValue(keys, values, count, "last_check_audit_stc_day_id", snap.stc_day_id);
   state.last_check_audit_index = STC_ParseIntDefault(STC_SnapshotValue(keys, values, count, "last_check_audit_index", "-1"), -1);
   state.last_w_level_audit_stc_day_id = STC_SnapshotValue(keys, values, count, "last_w_level_audit_stc_day_id", snap.stc_day_id);
   state.last_w_level_audit_serial = STC_ParseIntDefault(STC_SnapshotValue(keys, values, count, "last_w_level_audit_serial", "-1"), -1);
   state.last_hunt_audit_stc_day_id = STC_SnapshotValue(keys, values, count, "last_hunt_audit_stc_day_id", snap.stc_day_id);
   state.last_hunt_audit_check_index = STC_ParseIntDefault(STC_SnapshotValue(keys, values, count, "last_hunt_audit_check_index", "-1"), -1);
   state.last_smt_audit_stc_day_id = STC_SnapshotValue(keys, values, count, "last_smt_audit_stc_day_id", snap.stc_day_id);
   state.last_smt_audit_check_index = STC_ParseIntDefault(STC_SnapshotValue(keys, values, count, "last_smt_audit_check_index", "-1"), -1);
   state.last_signal_audit_stc_day_id = STC_SnapshotValue(keys, values, count, "last_signal_audit_stc_day_id", snap.stc_day_id);
   state.last_signal_audit_check_index = STC_ParseIntDefault(STC_SnapshotValue(keys, values, count, "last_signal_audit_check_index", "-1"), -1);
   state.last_paper_entry_stc_day_id = STC_SnapshotValue(keys, values, count, "last_paper_entry_stc_day_id", snap.stc_day_id);
   state.last_paper_entry_check_index = STC_ParseIntDefault(STC_SnapshotValue(keys, values, count, "last_paper_entry_check_index", "-1"), -1);
   state.last_paper_outcome_stc_day_id = STC_SnapshotValue(keys, values, count, "last_paper_outcome_stc_day_id", snap.stc_day_id);
   state.last_paper_outcome_check_index = STC_ParseIntDefault(STC_SnapshotValue(keys, values, count, "last_paper_outcome_check_index", "-1"), -1);
   state.last_partial_audit_stc_day_id = STC_SnapshotValue(keys, values, count, "last_partial_audit_stc_day_id", snap.stc_day_id);
   state.last_partial_audit_check_index = STC_ParseIntDefault(STC_SnapshotValue(keys, values, count, "last_partial_audit_check_index", "-1"), -1);
   state.last_hard_close_audit_stc_day_id = STC_SnapshotValue(keys, values, count, "last_hard_close_audit_stc_day_id", snap.stc_day_id);
   state.last_hard_close_audit_check_index = STC_ParseIntDefault(STC_SnapshotValue(keys, values, count, "last_hard_close_audit_check_index", "-1"), -1);

   state.check_candles_audited = STC_ParseLongDefault(STC_SnapshotValue(keys, values, count, "check_candles_audited", "0"), 0);
   state.w_levels_audited = STC_ParseLongDefault(STC_SnapshotValue(keys, values, count, "w_levels_audited", "0"), 0);
   state.hunt_rows_audited = STC_ParseLongDefault(STC_SnapshotValue(keys, values, count, "hunt_rows_audited", "0"), 0);
   state.smt_candidate_rows_audited = STC_ParseLongDefault(STC_SnapshotValue(keys, values, count, "smt_candidate_rows_audited", "0"), 0);
   state.signal_rows_audited = STC_ParseLongDefault(STC_SnapshotValue(keys, values, count, "signal_rows_audited", "0"), 0);
   state.paper_entry_rows_audited = STC_ParseLongDefault(STC_SnapshotValue(keys, values, count, "paper_entry_rows_audited", "0"), 0);
   state.paper_outcome_rows_audited = STC_ParseLongDefault(STC_SnapshotValue(keys, values, count, "paper_outcome_rows_audited", "0"), 0);
   state.partial_rows_audited = STC_ParseLongDefault(STC_SnapshotValue(keys, values, count, "partial_rows_audited", "0"), 0);
   state.hard_close_rows_audited = STC_ParseLongDefault(STC_SnapshotValue(keys, values, count, "hard_close_rows_audited", "0"), 0);

   state.paper_trade_count_m1 = STC_ParseIntDefault(STC_SnapshotValue(keys, values, count, "paper_trade_count_m1", "0"), 0);
   state.paper_trade_count_m2 = STC_ParseIntDefault(STC_SnapshotValue(keys, values, count, "paper_trade_count_m2", "0"), 0);
   state.paper_trade_count_m3 = STC_ParseIntDefault(STC_SnapshotValue(keys, values, count, "paper_trade_count_m3", "0"), 0);
   state.paper_direction_lock_m1 = STC_ParseDirectionDefault(STC_SnapshotValue(keys, values, count, "paper_direction_lock_m1", "0"), STC_DIR_NONE);
   state.paper_direction_lock_m2 = STC_ParseDirectionDefault(STC_SnapshotValue(keys, values, count, "paper_direction_lock_m2", "0"), STC_DIR_NONE);
   state.paper_direction_lock_m3 = STC_ParseDirectionDefault(STC_SnapshotValue(keys, values, count, "paper_direction_lock_m3", "0"), STC_DIR_NONE);

   state.outcome_trade_count_m1 = STC_ParseIntDefault(STC_SnapshotValue(keys, values, count, "outcome_trade_count_m1", "0"), 0);
   state.outcome_trade_count_m2 = STC_ParseIntDefault(STC_SnapshotValue(keys, values, count, "outcome_trade_count_m2", "0"), 0);
   state.outcome_trade_count_m3 = STC_ParseIntDefault(STC_SnapshotValue(keys, values, count, "outcome_trade_count_m3", "0"), 0);
   state.outcome_direction_lock_m1 = STC_ParseDirectionDefault(STC_SnapshotValue(keys, values, count, "outcome_direction_lock_m1", "0"), STC_DIR_NONE);
   state.outcome_direction_lock_m2 = STC_ParseDirectionDefault(STC_SnapshotValue(keys, values, count, "outcome_direction_lock_m2", "0"), STC_DIR_NONE);
   state.outcome_direction_lock_m3 = STC_ParseDirectionDefault(STC_SnapshotValue(keys, values, count, "outcome_direction_lock_m3", "0"), STC_DIR_NONE);

   state.partial_trade_count_m1 = STC_ParseIntDefault(STC_SnapshotValue(keys, values, count, "partial_trade_count_m1", "0"), 0);
   state.partial_trade_count_m2 = STC_ParseIntDefault(STC_SnapshotValue(keys, values, count, "partial_trade_count_m2", "0"), 0);
   state.partial_trade_count_m3 = STC_ParseIntDefault(STC_SnapshotValue(keys, values, count, "partial_trade_count_m3", "0"), 0);
   state.partial_direction_lock_m1 = STC_ParseDirectionDefault(STC_SnapshotValue(keys, values, count, "partial_direction_lock_m1", "0"), STC_DIR_NONE);
   state.partial_direction_lock_m2 = STC_ParseDirectionDefault(STC_SnapshotValue(keys, values, count, "partial_direction_lock_m2", "0"), STC_DIR_NONE);
   state.partial_direction_lock_m3 = STC_ParseDirectionDefault(STC_SnapshotValue(keys, values, count, "partial_direction_lock_m3", "0"), STC_DIR_NONE);

   state.persistence_restored = true;
   state.persistence_restore_status = "RESTORED";
   state.persistence_restore_note = "restored current STC-day cursors, counters, and direction locks from snapshot";
   STC_AppendPersistenceRecoveryCsv(cfg, state, "RESTORE", state.persistence_restore_status, state.persistence_restore_note);
   return true;
}

void STC_MaybeWritePersistenceSnapshot(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap, const string reason, const bool force)
{
   if(!cfg.write_persistence_snapshot) return;
   if(force)
   {
      STC_WritePersistenceSnapshot(cfg, state, snap, reason);
      return;
   }
   int interval = cfg.persistence_snapshot_seconds;
   if(interval < 1) interval = 1;
   datetime now = TimeCurrent();
   if(state.last_persistence_snapshot_server_time <= 0 || now - state.last_persistence_snapshot_server_time >= interval)
      STC_WritePersistenceSnapshot(cfg, state, snap, reason);
}

#endif
