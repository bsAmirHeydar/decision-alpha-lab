#ifndef __DAL_STC_CHECK_CANDLES_MQH__
#define __DAL_STC_CHECK_CANDLES_MQH__
#property strict

#include <IntermarketDivergenceExecution/STC/DAL_STC_Journal.mqh>

void STC_AssignCheckCycleFields(STC_CheckCandleAudit &audit, STC_TimeSnapshot &base_snap)
{
   STC_TimeSnapshot tmp;
   STC_ResetTimeSnapshot(tmp);
   tmp.stc_day_start_ny = base_snap.stc_day_start_ny;
   tmp.elapsed_minutes_from_2000 = audit.check_start_elapsed_minutes;
   STC_AssignMCycle(tmp);

   audit.m_cycle = tmp.m_cycle;
   audit.w_cycle = tmp.w_cycle;
   audit.start_inside_active_m = (tmp.m_cycle != STC_M_NONE);
   audit.close_inside_m = false;
   audit.final_check_of_m = false;
   audit.entry_allowed_at_close = false;
   audit.detection_allowed_for_signal = false;

   if(tmp.m_cycle == STC_M_NONE)
   {
      audit.skip_reason = "check_start_is_not_inside_active_M_gap_no_data_extraction";
      return;
   }

   audit.close_inside_m = (audit.check_end_elapsed_minutes < tmp.m_end_elapsed_minutes);
   audit.final_check_of_m = (audit.check_end_elapsed_minutes >= tmp.m_end_elapsed_minutes);
   audit.entry_allowed_at_close = (audit.start_inside_active_m && audit.close_inside_m && !audit.final_check_of_m);
   audit.detection_allowed_for_signal = audit.entry_allowed_at_close;
   if(audit.final_check_of_m)
      audit.skip_reason = "final_check_of_M_audited_but_no_entry";
   else
      audit.skip_reason = "eligible_for_future_signal_layers_if_pair_data_complete";
}

bool STC_AggregateSymbolM1Bars(const string symbol,
                               const datetime start_server,
                               const datetime end_server,
                               const int expected_m1_bars,
                               STC_SymbolCheckAggregate &agg)
{
   STC_ResetSymbolCheckAggregate(agg);
   agg.symbol = symbol;
   agg.expected_m1_bars = expected_m1_bars;
   agg.selected = SymbolSelect(symbol, true);
   if(!agg.selected)
   {
      agg.status = "symbol_not_selectable";
      return false;
   }

   if(expected_m1_bars <= 0 || start_server <= 0 || end_server <= start_server)
   {
      agg.status = "invalid_interval";
      return false;
   }

   MqlRates rates[];
   ArraySetAsSeries(rates, false);
   ResetLastError();
   datetime copy_stop = (datetime)((long)end_server - 1);
   int copied = CopyRates(symbol, PERIOD_M1, start_server, copy_stop, rates);
   if(copied <= 0)
   {
      agg.actual_m1_bars = 0;
      agg.status = "no_m1_data_err_" + IntegerToString(GetLastError());
      return false;
   }

   agg.actual_m1_bars = copied;
   agg.first_m1_server_time = rates[0].time;
   agg.last_m1_server_time = rates[copied - 1].time;
   agg.open = rates[0].open;
   agg.high = rates[0].high;
   agg.low = rates[0].low;
   agg.close = rates[copied - 1].close;
   agg.tick_volume = 0;
   agg.real_volume = 0;
   agg.spread_max = rates[0].spread;

   for(int i = 0; i < copied; i++)
   {
      if(rates[i].high > agg.high) agg.high = rates[i].high;
      if(rates[i].low < agg.low) agg.low = rates[i].low;
      agg.tick_volume += rates[i].tick_volume;
      agg.real_volume += rates[i].real_volume;
      if(rates[i].spread > agg.spread_max) agg.spread_max = rates[i].spread;
   }

   datetime expected_last = (datetime)((long)start_server + (expected_m1_bars - 1) * 60);
   bool count_ok = (copied == expected_m1_bars);
   bool start_ok = (agg.first_m1_server_time <= start_server);
   bool end_ok = (agg.last_m1_server_time >= expected_last);
   agg.complete = (count_ok && start_ok && end_ok);
   if(agg.complete)
      agg.status = "complete";
   else
      agg.status = "incomplete_count_or_time_coverage";
   return agg.complete;
}

bool STC_BuildCheckCandleAudit(STC_Config &cfg,
                               STC_TimeSnapshot &base_snap,
                               const int check_index,
                               STC_CheckCandleAudit &audit)
{
   STC_ResetCheckCandleAudit(audit);
   if(check_index < 0 || cfg.check_minutes <= 0)
   {
      audit.skip_reason = "invalid_check_index_or_minutes";
      return false;
   }

   audit.stc_day_id = base_snap.stc_day_id;
   audit.check_index = check_index;
   audit.check_minutes = cfg.check_minutes;
   audit.check_start_elapsed_minutes = check_index * cfg.check_minutes;
   audit.check_end_elapsed_minutes = audit.check_start_elapsed_minutes + cfg.check_minutes;
   audit.check_start_ny = (datetime)((long)base_snap.stc_day_start_ny + audit.check_start_elapsed_minutes * 60);
   audit.check_end_ny = (datetime)((long)base_snap.stc_day_start_ny + audit.check_end_elapsed_minutes * 60);
   audit.check_start_server = STC_NewYorkToServerUsingSnapshot(cfg, base_snap, audit.check_start_ny);
   audit.check_end_server = STC_NewYorkToServerUsingSnapshot(cfg, base_snap, audit.check_end_ny);

   if(audit.check_start_elapsed_minutes < 0 || audit.check_start_elapsed_minutes >= STC_DAY_ACTIVE_MINUTES)
   {
      audit.skip_reason = "outside_stc_active_day_no_data_extraction";
      return false;
   }

   STC_AssignCheckCycleFields(audit, base_snap);
   if(!audit.start_inside_active_m)
      return true;

   bool s1 = STC_AggregateSymbolM1Bars(cfg.symbol1, audit.check_start_server, audit.check_end_server, cfg.check_minutes, audit.symbol1);
   bool s2 = STC_AggregateSymbolM1Bars(cfg.symbol2, audit.check_start_server, audit.check_end_server, cfg.check_minutes, audit.symbol2);
   audit.pair_data_complete = (s1 && s2);
   if(!audit.pair_data_complete)
      audit.skip_reason = "pair_data_incomplete_no_future_signal_allowed";
   else if(audit.final_check_of_m)
      audit.skip_reason = "final_check_of_M_audited_but_no_entry";
   else
      audit.skip_reason = "pair_data_complete_and_check_eligible_for_future_signal_layers";

   return true;
}

void STC_ProcessClosedCheckCandles(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap)
{
   if(!cfg.write_check_candle_audit)
      return;
   if(snap.stc_day_id == "" || snap.elapsed_seconds_from_2000 <= 0)
      return;

   int closed_index = STC_LastClosedCheckIndex(snap);
   if(closed_index < 0)
      return;

   int max_allowed_index = (STC_DAY_ACTIVE_MINUTES / cfg.check_minutes) - 1;
   if(closed_index > max_allowed_index)
      closed_index = max_allowed_index;

   if(state.last_check_audit_stc_day_id != snap.stc_day_id)
   {
      state.last_check_audit_stc_day_id = snap.stc_day_id;
      int backfill = cfg.max_check_backfill_on_init;
      if(backfill < 0) backfill = 0;
      state.last_check_audit_index = closed_index - backfill;
      if(state.last_check_audit_index < -1) state.last_check_audit_index = -1;
      STC_AppendRuntimeEventCsv(cfg, state, "CHECK_DAY_RESET", "stc_day=" + snap.stc_day_id + "; closed_index=" + IntegerToString(closed_index));
   }

   int start_index = state.last_check_audit_index + 1;
   if(start_index < 0) start_index = 0;
   if(start_index > closed_index)
      return;

   int catchup = cfg.max_check_catchup_per_pulse;
   if(catchup < 1) catchup = 1;
   int end_index = closed_index;
   if(end_index - start_index + 1 > catchup)
      end_index = start_index + catchup - 1;

   for(int idx = start_index; idx <= end_index; idx++)
   {
      STC_CheckCandleAudit audit;
      STC_BuildCheckCandleAudit(cfg, snap, idx, audit);
      STC_AppendCheckCandleAuditCsv(cfg, state, audit);
      state.last_check_audit_index = idx;
      state.check_candles_audited++;
   }
}

#endif
