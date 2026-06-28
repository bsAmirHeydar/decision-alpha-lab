#ifndef __DAL_STC_ALERTS_MQH__
#define __DAL_STC_ALERTS_MQH__
#property strict

#include <IntermarketDivergenceExecution/STC/DAL_STC_Drawing.mqh>

bool STC_AppendPaperLiveAlertCsv(STC_Config &cfg,
                                 STC_RuntimeState &state,
                                 STC_TimeSnapshot &snap,
                                 const string alert_type,
                                 const long previous_count,
                                 const long current_count,
                                 const long delta_count,
                                 const bool transport_allowed,
                                 const bool transport_used,
                                 const string message,
                                 const string rule_note)
{
   if(!cfg.write_alert_audit) return true;
   bool exists = FileIsExist(state.alert_audit_file_common, FILE_COMMON);
   int h = FileOpen(state.alert_audit_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append paper live alert CSV ", state.alert_audit_file_common, " err=", GetLastError());
      return false;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h,
         "server_time", "ny_time", "stc_day_id", "runtime_mode", "run_id", "symbol1", "symbol2", "magic",
         "alert_type", "previous_count", "current_count", "delta_count",
         "transport_allowed", "transport_used", "popup", "push", "sound", "print",
         "check_index", "m_cycle", "w_cycle", "paper_live_baseline_status", "message", "rule_note");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h,
      STC_TimeText(TimeCurrent()),
      STC_TimeText(snap.ny_time),
      snap.stc_day_id,
      STC_RuntimeModeText(cfg.runtime_mode),
      cfg.run_id,
      cfg.symbol1,
      cfg.symbol2,
      IntegerToString(cfg.magic_number),
      alert_type,
      previous_count,
      current_count,
      delta_count,
      STC_BoolText(transport_allowed),
      STC_BoolText(transport_used),
      STC_BoolText(cfg.alert_popup),
      STC_BoolText(cfg.alert_push),
      STC_BoolText(cfg.alert_sound),
      STC_BoolText(cfg.alert_print),
      snap.check_index,
      STC_MCycleText(snap.m_cycle),
      STC_WCycleText(snap.w_cycle),
      state.alert_baseline_status,
      message,
      rule_note);
   FileClose(h);
   state.alert_rows_audited++;
   return true;
}

bool STC_IsPaperLiveAlertTransportMode(STC_Config &cfg)
{
   return (cfg.runtime_mode == STC_MODE_PAPER_LIVE || cfg.runtime_mode == STC_MODE_AUTO_TRADE);
}

void STC_DispatchPaperLiveAlert(STC_Config &cfg,
                                STC_RuntimeState &state,
                                STC_TimeSnapshot &snap,
                                const string alert_type,
                                const long previous_count,
                                const long current_count,
                                const string message,
                                const string rule_note)
{
   long delta_count = current_count - previous_count;
   if(delta_count <= 0) return;

   bool transport_mode = STC_IsPaperLiveAlertTransportMode(cfg);
   bool debounce_ok = true;
   if(cfg.alert_debounce_seconds > 0 && state.last_alert_server_time > 0)
      debounce_ok = (TimeCurrent() - state.last_alert_server_time >= cfg.alert_debounce_seconds);

   bool transport_allowed = cfg.enable_paper_live_alerts && transport_mode && debounce_ok;
   bool transport_used = false;

   string full_message = "DAL STC EXEC001 " + alert_type + " | " + cfg.symbol1 + "/" + cfg.symbol2
      + " | day=" + snap.stc_day_id
      + " | check=" + IntegerToString(snap.check_index)
      + " | M=" + STC_MCycleText(snap.m_cycle)
      + " | W=" + STC_WCycleText(snap.w_cycle)
      + " | delta=" + IntegerToString((int)delta_count)
      + " | no real orders";
   if(message != "") full_message = full_message + " | " + message;

   if(transport_allowed)
   {
      if(cfg.alert_print)
      {
         Print(full_message);
         transport_used = true;
      }
      if(cfg.alert_popup)
      {
         Alert(full_message);
         transport_used = true;
      }
      if(cfg.alert_push)
      {
         SendNotification(full_message);
         transport_used = true;
      }
      if(cfg.alert_sound)
      {
         PlaySound(cfg.alert_sound_file);
         transport_used = true;
      }
      if(transport_used)
         state.last_alert_server_time = TimeCurrent();
   }

   string note = rule_note;
   if(!transport_mode)
      note = note + "; transport suppressed because runtime mode is RESEARCH_BACKTEST";
   if(!debounce_ok)
      note = note + "; transport suppressed by debounce";
   if(!cfg.enable_paper_live_alerts)
      note = note + "; alert layer disabled";

   STC_AppendPaperLiveAlertCsv(cfg, state, snap, alert_type, previous_count, current_count, delta_count, transport_allowed, transport_used, full_message, note);
}

void STC_InitializePaperLiveAlertBaseline(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap, const string reason)
{
   if(cfg.alert_replay_on_init)
   {
      state.signal_rows_alerted = 0;
      state.paper_entry_rows_alerted = 0;
      state.paper_outcome_rows_alerted = 0;
      state.partial_rows_alerted = 0;
      state.hard_close_rows_alerted = 0;
      state.alert_baseline_status = "REPLAY_ON_INIT_ZERO_BASELINE";
   }
   else
   {
      state.signal_rows_alerted = state.signal_rows_audited;
      state.paper_entry_rows_alerted = state.paper_entry_rows_audited;
      state.paper_outcome_rows_alerted = state.paper_outcome_rows_audited;
      state.partial_rows_alerted = state.partial_rows_audited;
      state.hard_close_rows_alerted = state.hard_close_rows_audited;
      state.alert_baseline_status = "BASELINED_TO_CURRENT_COUNTS";
   }

   STC_AppendPaperLiveAlertCsv(cfg, state, snap, "ALERT_BASELINE", 0, 0, 0, false, false,
      "paper live alert baseline initialized; reason=" + reason,
      "prevents alert replay for already audited same-day rows unless alert_replay_on_init=true");
}

void STC_ProcessPaperLiveAlerts(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap)
{
   if(!cfg.enable_paper_live_alerts)
      return;

   if(cfg.alert_on_signal && state.signal_rows_audited > state.signal_rows_alerted)
   {
      long previous = state.signal_rows_alerted;
      STC_DispatchPaperLiveAlert(cfg, state, snap, "SIGNAL_CONFIRMED", previous, state.signal_rows_audited,
         "new Level 07 signal registry row(s); inspect stc_level14_signal_registry.csv",
         "alert-only; signal consumption is handled by the registry; no late entry and no real order");
      state.signal_rows_alerted = state.signal_rows_audited;
   }
   else if(state.signal_rows_audited > state.signal_rows_alerted)
   {
      state.signal_rows_alerted = state.signal_rows_audited;
   }

   if(cfg.alert_on_paper_entry && state.paper_entry_rows_audited > state.paper_entry_rows_alerted)
   {
      long previous = state.paper_entry_rows_alerted;
      STC_DispatchPaperLiveAlert(cfg, state, snap, "PAPER_ENTRY_PLANNED", previous, state.paper_entry_rows_audited,
         "new Level 08 paper entry row(s); inspect stc_level14_paper_entries.csv",
         "alert-only; paper entry uses next check open; no broker order sent");
      state.paper_entry_rows_alerted = state.paper_entry_rows_audited;
   }
   else if(state.paper_entry_rows_audited > state.paper_entry_rows_alerted)
   {
      state.paper_entry_rows_alerted = state.paper_entry_rows_audited;
   }

   bool outcome_alert_enabled = (cfg.alert_on_outcome || cfg.alert_on_ambiguous);
   if(outcome_alert_enabled && state.paper_outcome_rows_audited > state.paper_outcome_rows_alerted)
   {
      long previous = state.paper_outcome_rows_alerted;
      STC_DispatchPaperLiveAlert(cfg, state, snap, "PAPER_OUTCOME_UPDATE", previous, state.paper_outcome_rows_audited,
         "new Level 09 outcome row(s); inspect stc_level14_paper_outcomes.csv for TP/SL/AMBIGUOUS/OPEN_UNRESOLVED",
         "alert-only; ambiguous outcomes are preserved as ambiguous and no path is invented");
      state.paper_outcome_rows_alerted = state.paper_outcome_rows_audited;
   }
   else if(state.paper_outcome_rows_audited > state.paper_outcome_rows_alerted)
   {
      state.paper_outcome_rows_alerted = state.paper_outcome_rows_audited;
   }

   if(cfg.alert_on_partial && state.partial_rows_audited > state.partial_rows_alerted)
   {
      long previous = state.partial_rows_alerted;
      STC_DispatchPaperLiveAlert(cfg, state, snap, "PAPER_PARTIAL_ACTION", previous, state.partial_rows_audited,
         "new Level 10 partial action row(s); inspect stc_level14_partial_actions.csv",
         "alert-only; partial actions are simulated/audited and do not close broker volume");
      state.partial_rows_alerted = state.partial_rows_audited;
   }
   else if(state.partial_rows_audited > state.partial_rows_alerted)
   {
      state.partial_rows_alerted = state.partial_rows_audited;
   }

   if((cfg.alert_on_hard_close || cfg.alert_on_hard_close_due) && state.hard_close_rows_audited > state.hard_close_rows_alerted)
   {
      long previous = state.hard_close_rows_alerted;
      STC_DispatchPaperLiveAlert(cfg, state, snap, "PAPER_HARD_CLOSE_ACTION", previous, state.hard_close_rows_audited,
         "new Level 11 hard-close action row(s); inspect stc_level14_hard_close_actions.csv",
         "alert-only; 15:30 NY hard-close accounting is simulated and no broker position is closed");
      state.hard_close_rows_alerted = state.hard_close_rows_audited;
   }
   else if(state.hard_close_rows_audited > state.hard_close_rows_alerted)
   {
      state.hard_close_rows_alerted = state.hard_close_rows_audited;
   }
}

#endif
