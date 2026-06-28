#ifndef __DAL_STC_W_LEVELS_MQH__
#define __DAL_STC_W_LEVELS_MQH__
#property strict

#include <IntermarketDivergenceExecution/STC/DAL_STC_CheckCandles.mqh>

int STC_WLevel_MStartElapsed(const STC_MCycle m)
{
   if(m == STC_M1) return 0;
   if(m == STC_M2) return 420;
   if(m == STC_M3) return 810;
   return -1;
}

bool STC_WLevel_FromSerial(const int serial, STC_MCycle &m, STC_WCycle &w)
{
   m = STC_M_NONE;
   w = STC_W_NONE;
   if(serial < 0 || serial > 11) return false;
   int mi = serial / 4;
   int wi = serial % 4;
   m = (STC_MCycle)(mi + 1);
   w = (STC_WCycle)(wi + 1);
   return true;
}

int STC_WLevel_Serial(const STC_MCycle m, const STC_WCycle w)
{
   if(m == STC_M_NONE || w == STC_W_NONE) return -1;
   return (((int)m) - 1) * 4 + (((int)w) - 1);
}

int STC_WLevel_StartElapsed(const STC_MCycle m, const STC_WCycle w)
{
   int ms = STC_WLevel_MStartElapsed(m);
   if(ms < 0 || w == STC_W_NONE) return -1;
   return ms + (((int)w) - 1) * 90;
}

int STC_WLevel_EndElapsed(const STC_MCycle m, const STC_WCycle w)
{
   int s = STC_WLevel_StartElapsed(m, w);
   if(s < 0) return -1;
   return s + 90;
}

string STC_WLevel_SignalReferenceSet(const STC_WCycle w)
{
   if(w == STC_W1) return "NONE_W1_HAS_NO_SIGNAL";
   if(w == STC_W2) return "W1";
   if(w == STC_W3) return "W2|W1";
   if(w == STC_W4) return "W3|W2|W1";
   return "NONE";
}

string STC_WLevel_FutureReferenceRole(const STC_WCycle w)
{
   if(w == STC_W1) return "reference_for_W2_W3_W4";
   if(w == STC_W2) return "reference_for_W3_W4";
   if(w == STC_W3) return "reference_for_W4";
   if(w == STC_W4) return "audit_only_no_later_W_in_same_M";
   return "none";
}

int STC_LastClosedWSerial(STC_TimeSnapshot &snap)
{
   if(snap.stc_day_id == "" || snap.elapsed_seconds_from_2000 < 0)
      return -1;

   int last = -1;
   for(int serial = 0; serial < 12; serial++)
   {
      STC_MCycle m;
      STC_WCycle w;
      if(!STC_WLevel_FromSerial(serial, m, w)) continue;
      int end_elapsed = STC_WLevel_EndElapsed(m, w);
      if(end_elapsed < 0) continue;
      if(snap.elapsed_seconds_from_2000 >= end_elapsed * 60)
         last = serial;
   }
   return last;
}

bool STC_BuildWLevelAudit(STC_Config &cfg,
                          STC_TimeSnapshot &base_snap,
                          const int w_serial,
                          STC_WLevelAudit &audit)
{
   STC_ResetWLevelAudit(audit);
   audit.stc_day_id = base_snap.stc_day_id;
   audit.w_serial = w_serial;

   STC_MCycle m;
   STC_WCycle w;
   if(!STC_WLevel_FromSerial(w_serial, m, w))
   {
      audit.status = "invalid_w_serial";
      return false;
   }

   audit.m_cycle = m;
   audit.w_cycle = w;
   audit.w_start_elapsed_minutes = STC_WLevel_StartElapsed(m, w);
   audit.w_end_elapsed_minutes = STC_WLevel_EndElapsed(m, w);
   audit.w_start_ny = (datetime)((long)base_snap.stc_day_start_ny + audit.w_start_elapsed_minutes * 60);
   audit.w_end_ny = (datetime)((long)base_snap.stc_day_start_ny + audit.w_end_elapsed_minutes * 60);
   audit.w_start_server = STC_NewYorkToServerUsingSnapshot(cfg, base_snap, audit.w_start_ny);
   audit.w_end_server = STC_NewYorkToServerUsingSnapshot(cfg, base_snap, audit.w_end_ny);
   audit.w_closed = (base_snap.elapsed_seconds_from_2000 >= audit.w_end_elapsed_minutes * 60);
   audit.w1_no_signal = (w == STC_W1);
   audit.future_reference_candidate = (w != STC_W4);
   audit.signal_reference_set_for_this_w = STC_WLevel_SignalReferenceSet(w);
   audit.future_reference_role = STC_WLevel_FutureReferenceRole(w);

   if(!audit.w_closed)
   {
      audit.status = "w_not_closed_yet";
      return true;
   }

   bool s1 = STC_AggregateSymbolM1Bars(cfg.symbol1, audit.w_start_server, audit.w_end_server, 90, audit.symbol1);
   bool s2 = STC_AggregateSymbolM1Bars(cfg.symbol2, audit.w_start_server, audit.w_end_server, 90, audit.symbol2);
   audit.pair_data_complete = (s1 && s2);
   if(audit.pair_data_complete)
      audit.status = "complete_90m_w_level_ready_for_future_reference_layers";
   else
      audit.status = "incomplete_w_level_not_usable_as_reference";
   return audit.pair_data_complete;
}

void STC_ProcessClosedWLevels(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap)
{
   if(!cfg.write_w_level_audit)
      return;
   if(snap.stc_day_id == "" || snap.elapsed_seconds_from_2000 < 0)
      return;

   int closed_serial = STC_LastClosedWSerial(snap);
   if(closed_serial < 0)
      return;

   if(state.last_w_level_audit_stc_day_id != snap.stc_day_id)
   {
      state.last_w_level_audit_stc_day_id = snap.stc_day_id;
      int backfill = cfg.max_w_level_backfill_on_init;
      if(backfill < 0) backfill = 0;
      if(backfill > 12) backfill = 12;
      state.last_w_level_audit_serial = closed_serial - backfill;
      if(state.last_w_level_audit_serial < -1) state.last_w_level_audit_serial = -1;
      STC_AppendRuntimeEventCsv(cfg, state, "W_LEVEL_DAY_RESET", "stc_day=" + snap.stc_day_id + "; closed_w_serial=" + IntegerToString(closed_serial));
   }

   int start_serial = state.last_w_level_audit_serial + 1;
   if(start_serial < 0) start_serial = 0;
   if(start_serial > closed_serial)
      return;

   int catchup = cfg.max_w_level_catchup_per_pulse;
   if(catchup < 1) catchup = 1;
   if(catchup > 12) catchup = 12;
   int end_serial = closed_serial;
   if(end_serial - start_serial + 1 > catchup)
      end_serial = start_serial + catchup - 1;

   for(int serial = start_serial; serial <= end_serial; serial++)
   {
      STC_WLevelAudit audit;
      STC_BuildWLevelAudit(cfg, snap, serial, audit);
      STC_AppendWLevelAuditCsv(cfg, state, audit);
      state.last_w_level_audit_serial = serial;
      state.w_levels_audited++;
   }
}

#endif
