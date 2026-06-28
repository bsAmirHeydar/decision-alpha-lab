#ifndef __DAL_STC_PARTIAL_MQH__
#define __DAL_STC_PARTIAL_MQH__
#property strict

#include <IntermarketDivergenceExecution/STC/DAL_STC_Outcome.mqh>

int STC_MEndElapsedForPartial(const STC_MCycle m)
{
   if(m == STC_M1) return 360;
   if(m == STC_M2) return 780;
   if(m == STC_M3) return 1170;
   return -1;
}

int STC_MFinalCheckIndexForPartial(const STC_MCycle m, STC_Config &cfg)
{
   int end_elapsed = STC_MEndElapsedForPartial(m);
   if(end_elapsed < 0 || cfg.check_minutes <= 0) return -1;
   return (end_elapsed / cfg.check_minutes) - 1;
}

int STC_GetPartialMTradeCount(STC_RuntimeState &state, const STC_MCycle m)
{
   if(m == STC_M1) return state.partial_trade_count_m1;
   if(m == STC_M2) return state.partial_trade_count_m2;
   if(m == STC_M3) return state.partial_trade_count_m3;
   return 0;
}

STC_Direction STC_GetPartialMDirectionLock(STC_RuntimeState &state, const STC_MCycle m)
{
   if(m == STC_M1) return state.partial_direction_lock_m1;
   if(m == STC_M2) return state.partial_direction_lock_m2;
   if(m == STC_M3) return state.partial_direction_lock_m3;
   return STC_DIR_NONE;
}

void STC_SetPartialMTradeCount(STC_RuntimeState &state, const STC_MCycle m, const int value)
{
   if(m == STC_M1) state.partial_trade_count_m1 = value;
   else if(m == STC_M2) state.partial_trade_count_m2 = value;
   else if(m == STC_M3) state.partial_trade_count_m3 = value;
}

void STC_SetPartialMDirectionLock(STC_RuntimeState &state, const STC_MCycle m, const STC_Direction direction)
{
   if(m == STC_M1) state.partial_direction_lock_m1 = direction;
   else if(m == STC_M2) state.partial_direction_lock_m2 = direction;
   else if(m == STC_M3) state.partial_direction_lock_m3 = direction;
}

void STC_CopyPartialCountersIntoPaperCounters(STC_RuntimeState &dst)
{
   dst.paper_trade_count_m1 = dst.partial_trade_count_m1;
   dst.paper_trade_count_m2 = dst.partial_trade_count_m2;
   dst.paper_trade_count_m3 = dst.partial_trade_count_m3;
   dst.paper_direction_lock_m1 = dst.partial_direction_lock_m1;
   dst.paper_direction_lock_m2 = dst.partial_direction_lock_m2;
   dst.paper_direction_lock_m3 = dst.partial_direction_lock_m3;
}

void STC_CopyPaperCountersBackToPartialCounters(STC_RuntimeState &src, STC_RuntimeState &dst)
{
   dst.partial_trade_count_m1 = src.paper_trade_count_m1;
   dst.partial_trade_count_m2 = src.paper_trade_count_m2;
   dst.partial_trade_count_m3 = src.paper_trade_count_m3;
   dst.partial_direction_lock_m1 = src.paper_direction_lock_m1;
   dst.partial_direction_lock_m2 = src.paper_direction_lock_m2;
   dst.partial_direction_lock_m3 = src.paper_direction_lock_m3;
}

double STC_CeilVolumeToStep(const double volume, const double step)
{
   if(volume <= 0.0) return 0.0;
   if(step <= 0.0) return volume;
   double units = MathCeil(volume / step);
   return units * step;
}

void STC_FillPartialBase(STC_Config &cfg,
                         STC_TimeSnapshot &snap,
                         STC_PaperEntryAudit &paper,
                         STC_PartialAudit &partial)
{
   STC_ResetPartialAudit(partial);
   partial.stc_day_id = paper.stc_day_id;
   partial.signal_check_index = paper.check_index;
   partial.entry_check_index = paper.entry_check_index;
   partial.check_minutes = paper.check_minutes;
   partial.signal_check_start_ny = paper.signal_check_start_ny;
   partial.signal_check_end_ny = paper.signal_check_end_ny;
   partial.entry_check_start_ny = paper.entry_check_start_ny;
   partial.entry_check_end_ny = paper.entry_check_end_ny;
   partial.m_cycle = paper.m_cycle;
   partial.current_w_cycle = paper.current_w_cycle;
   partial.paper_status = paper.paper_status;
   partial.signal_id = paper.signal_id;
   partial.paper_trade_id = paper.paper_trade_id;
   partial.is_paper_entry = paper.is_paper_entry;
   partial.partial_enabled = cfg.partial_enabled;
   partial.direction = paper.direction;
   partial.trade_symbol = paper.trade_symbol;
   partial.entry_price = paper.entry_price;
   partial.stop_price = paper.stop_price;
   partial.take_profit_price = paper.take_profit_price;
   partial.paper_order_volume = paper.paper_order_volume;
   partial.broker_volume_step = paper.broker_volume_step;

   int due_index = STC_MFinalCheckIndexForPartial(paper.m_cycle, cfg);
   partial.partial_due_check_index = due_index;
   if(due_index >= 0)
   {
      int due_elapsed = (due_index + 1) * cfg.check_minutes;
      partial.partial_due_ny = (datetime)((long)snap.stc_day_start_ny + due_elapsed * 60);
      partial.partial_due_server = STC_NewYorkToServerUsingSnapshot(cfg, snap, partial.partial_due_ny);
   }
}

void STC_EvaluatePartialFromPaper(STC_Config &cfg,
                                  STC_TimeSnapshot &snap,
                                  STC_PaperEntryAudit &paper,
                                  const int last_closed_index,
                                  STC_PartialAudit &partial)
{
   STC_FillPartialBase(cfg, snap, paper, partial);

   if(!paper.is_paper_entry || !(paper.paper_status == STC_PAPER_PLANNED || paper.paper_status == STC_PAPER_PLANNED_SPLIT_REQUIRED))
   {
      partial.partial_status = STC_PARTIAL_NO_PAPER_ENTRY;
      partial.status = "paper_entry_not_planned_no_partial";
      partial.rule_note = paper.rule_note;
      return;
   }

   if(!cfg.partial_enabled)
   {
      partial.partial_status = STC_PARTIAL_DISABLED;
      partial.status = "partial_switch_off_no_partial_action";
      partial.rule_note = "Locked owner rule: Partial OFF disables partial accounting but does not cancel SL/TP simulation";
      return;
   }

   if(paper.m_cycle == STC_M3)
   {
      partial.partial_status = STC_PARTIAL_SKIPPED_M3_HARD_CLOSE;
      partial.status = "m3_partial_disabled_by_hard_close";
      partial.rule_note = "Locked owner rule: at M3 end 15:30 New York hard close has priority, so partial is meaningless";
      return;
   }

   if(partial.partial_due_check_index < 0 || last_closed_index < partial.partial_due_check_index)
   {
      partial.partial_status = STC_PARTIAL_NOT_DUE_YET;
      partial.status = "w4_end_not_closed_yet_no_partial_action";
      partial.rule_note = "Partial is evaluated exactly at W4/M end and recovered later if missed";
      return;
   }
   partial.partial_due = true;

   STC_PaperOutcomeAudit pre;
   STC_SimulateOutcomeFromPaper(cfg, snap, paper, partial.partial_due_check_index, pre);
   partial.pre_partial_outcome_status = pre.outcome_status;
   partial.last_checked_index = pre.last_checked_index;
   partial.last_checked_close = pre.last_checked_close;
   partial.floating_r_at_partial = pre.floating_r_at_last_check;

   if(pre.outcome_status == STC_OUTCOME_REJECTED_DATA_INCOMPLETE)
   {
      partial.partial_status = STC_PARTIAL_REJECTED_DATA_INCOMPLETE;
      partial.status = "pre_partial_outcome_data_incomplete_no_partial";
      partial.rule_note = pre.rule_note;
      return;
   }

   if(pre.outcome_status != STC_OUTCOME_OPEN_UNRESOLVED)
   {
      partial.partial_status = STC_PARTIAL_NOT_OPEN_AT_W4_END;
      partial.status = "trade_not_open_at_w4_end_no_partial";
      partial.rule_note = "TP, SL, ambiguity, or rejection occurred before the W4 partial checkpoint";
      return;
   }

   partial.open_at_w4_end = true;
   double step = paper.broker_volume_step;
   if(step <= 0.0) step = 0.01;
   double half = paper.paper_order_volume * 0.5;
   double close_volume = STC_CeilVolumeToStep(half, step);
   if(close_volume >= paper.paper_order_volume || paper.paper_order_volume <= step)
   {
      close_volume = paper.paper_order_volume;
      partial.remaining_volume = 0.0;
      partial.full_close_by_small_volume = true;
      partial.partial_status = STC_PARTIAL_FULL_CLOSE_BY_SMALL_VOLUME;
      partial.status = "small_volume_full_close_at_w4_end";
      partial.rule_note = "Locked owner example: volume 0.01 closes fully; half-volume rounded up by broker step would consume the whole trade";
   }
   else
   {
      partial.remaining_volume = paper.paper_order_volume - close_volume;
      partial.partial_status = STC_PARTIAL_PARTIAL_CLOSE;
      partial.status = "partial_close_at_w4_end";
      partial.rule_note = "Locked owner rule: at W4 end close about 50 percent, rounded upward to broker volume step, even if trade is losing";
   }
   partial.close_volume = close_volume;
   if(paper.paper_order_volume > 0.0)
      partial.close_volume_ratio = partial.close_volume / paper.paper_order_volume;
   partial.partial_action_taken = true;
}

void STC_AppendPartialSkipRow(STC_Config &cfg,
                              STC_RuntimeState &state,
                              STC_TimeSnapshot &snap,
                              const int check_index,
                              const STC_PartialStatus status,
                              const string status_text,
                              const string rule_note)
{
   STC_CheckCandleAudit check_audit;
   STC_BuildCheckCandleAudit(cfg, snap, check_index, check_audit);

   STC_PartialAudit row;
   STC_ResetPartialAudit(row);
   row.stc_day_id = check_audit.stc_day_id;
   row.signal_check_index = check_audit.check_index;
   row.entry_check_index = check_audit.check_index + 1;
   row.check_minutes = check_audit.check_minutes;
   row.signal_check_start_ny = check_audit.check_start_ny;
   row.signal_check_end_ny = check_audit.check_end_ny;
   row.m_cycle = check_audit.m_cycle;
   row.current_w_cycle = check_audit.w_cycle;
   row.partial_status = status;
   row.partial_enabled = cfg.partial_enabled;
   row.signal_id = cfg.strategy_id + "|" + row.stc_day_id + "|CHK" + IntegerToString(row.signal_check_index) + "|PARTIAL_SKIP";
   row.paper_trade_id = row.signal_id;
   row.status = status_text;
   row.rule_note = rule_note;
   STC_AppendPartialAuditCsv(cfg, state, row);
   state.partial_rows_audited++;
}

void STC_ProcessPartialCandidate(STC_Config &cfg,
                                 STC_RuntimeState &state,
                                 STC_TimeSnapshot &snap,
                                 STC_SMTCandidateAudit &candidate,
                                 const int last_closed_index)
{
   STC_RuntimeState calc_state = state;
   STC_CopyPartialCountersIntoPaperCounters(calc_state);

   STC_SignalAudit signal;
   STC_FinalizeSignalFromCandidate(cfg, calc_state, candidate, signal);

   STC_PaperEntryAudit paper;
   STC_FillPaperFromSignal(cfg, calc_state, snap, signal, paper);
   STC_CopyPaperCountersBackToPartialCounters(calc_state, state);

   STC_PartialAudit partial;
   STC_EvaluatePartialFromPaper(cfg, snap, paper, last_closed_index, partial);
   STC_AppendPartialAuditCsv(cfg, state, partial);
   state.partial_rows_audited++;
}

void STC_ProcessOnePartialCheck(STC_Config &cfg,
                                STC_RuntimeState &state,
                                STC_TimeSnapshot &snap,
                                const int check_index,
                                const int last_closed_index)
{
   STC_SMTCandidateAudit candidate;
   string status_text = "";
   string rule_note = "";
   if(!STC_FindOutcomeCandidateForCheck(cfg, state, snap, check_index, candidate, status_text, rule_note))
   {
      STC_AppendPartialSkipRow(cfg, state, snap, check_index, STC_PARTIAL_NO_PAPER_ENTRY, status_text, rule_note);
      return;
   }
   STC_ProcessPartialCandidate(cfg, state, snap, candidate, last_closed_index);
}

int STC_MaxSignalIndexWithPartialDue(STC_Config &cfg, STC_TimeSnapshot &snap, const int last_closed_index)
{
   int max_allowed_index = (STC_DAY_ACTIVE_MINUTES / cfg.check_minutes) - 2;
   int max_due = -1;
   for(int idx = 0; idx <= max_allowed_index; idx++)
   {
      STC_CheckCandleAudit check;
      STC_BuildCheckCandleAudit(cfg, snap, idx, check);
      if(check.m_cycle == STC_M_NONE)
      {
         if(idx <= last_closed_index) max_due = idx;
         continue;
      }
      int due_index = STC_MFinalCheckIndexForPartial(check.m_cycle, cfg);
      if(due_index >= 0 && due_index <= last_closed_index)
         max_due = idx;
      else if(idx > last_closed_index)
         break;
   }
   return max_due;
}

void STC_ProcessClosedPartials(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap)
{
   if(!cfg.write_partial_audit)
      return;
   if(snap.stc_day_id == "" || snap.elapsed_seconds_from_2000 <= 0)
      return;

   int closed_index = STC_LastClosedCheckIndex(snap);
   if(closed_index < 0)
      return;

   int max_signal_index_with_partial_due = STC_MaxSignalIndexWithPartialDue(cfg, snap, closed_index);
   if(max_signal_index_with_partial_due < 0)
      return;

   if(state.last_partial_audit_stc_day_id != snap.stc_day_id)
   {
      state.last_partial_audit_stc_day_id = snap.stc_day_id;
      state.partial_trade_count_m1 = 0;
      state.partial_trade_count_m2 = 0;
      state.partial_trade_count_m3 = 0;
      state.partial_direction_lock_m1 = STC_DIR_NONE;
      state.partial_direction_lock_m2 = STC_DIR_NONE;
      state.partial_direction_lock_m3 = STC_DIR_NONE;
      int backfill = cfg.max_partial_backfill_on_init;
      if(backfill < 0) backfill = 0;
      state.last_partial_audit_check_index = max_signal_index_with_partial_due - backfill;
      if(state.last_partial_audit_check_index < -1) state.last_partial_audit_check_index = -1;
      STC_AppendRuntimeEventCsv(cfg, state, "PARTIAL_DAY_RESET", "stc_day=" + snap.stc_day_id + "; max_signal_index_with_partial_due=" + IntegerToString(max_signal_index_with_partial_due));
   }

   int start_index = state.last_partial_audit_check_index + 1;
   if(start_index < 0) start_index = 0;
   if(start_index > max_signal_index_with_partial_due)
      return;

   int catchup = cfg.max_partial_catchup_per_pulse;
   if(catchup < 1) catchup = 1;
   int end_index = max_signal_index_with_partial_due;
   if(end_index - start_index + 1 > catchup)
      end_index = start_index + catchup - 1;

   for(int idx = start_index; idx <= end_index; idx++)
   {
      STC_ProcessOnePartialCheck(cfg, state, snap, idx, closed_index);
      state.last_partial_audit_check_index = idx;
   }
}

#endif
