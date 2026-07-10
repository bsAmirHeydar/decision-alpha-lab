#ifndef __FP_NDS_HOOK_TRADE_ENGINE_MQH__
#define __FP_NDS_HOOK_TRADE_ENGINE_MQH__
#property strict

#include "FP_NDSHookTradeExport.mqh"

bool FP_NDSHookTradeFindManagedPositionForSymbol(const string symbol,
                                                 const FP_NDSHookTradeConfig &cfg,
                                                 ulong &ticket,
                                                 int &direction,
                                                 datetime &open_time)
{
   ticket = 0;
   direction = FP_DIR_NONE;
   open_time = 0;

   for(int i=PositionsTotal()-1; i>=0; i--)
   {
      ulong t = PositionGetTicket(i);
      if(t == 0 || !PositionSelectByTicket(t)) continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol) continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != cfg.magic) continue;

      ENUM_POSITION_TYPE type = (ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);
      direction = (type == POSITION_TYPE_BUY ? FP_DIR_BULLISH :
                   (type == POSITION_TYPE_SELL ? FP_DIR_BEARISH : FP_DIR_NONE));
      ticket = t;
      open_time = (datetime)PositionGetInteger(POSITION_TIME);
      return (direction != FP_DIR_NONE);
   }
   return false;
}

void FP_RunNDSHookLimitF123Execution(const string symbol,
                                     const ENUM_TIMEFRAMES period,
                                     const FP_FlagEvent &events[],
                                     const int event_count,
                                     const FP_NDSHookTradeConfig &cfg,
                                     FP_NDSHookTradeReport &report)
{
   FP_ResetNDSHookTradeReport(report);
   report.symbol = symbol;
   report.period = period;
   report.attempted = cfg.enabled;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "NDS_HOOK_TRADE_DISABLED";
      report.reason = "InpNDSHookTradeEnabled_false";
      FP_NDSHookTradeFinalizeReport(report);
      FP_NDSHookTradeExportReport(cfg, report);
      return;
   }

   string cancel_reason;
   int cancelled_dead = FP_NDSHookTradeCancelDeadPending(symbol, cfg, cancel_reason);

   ulong first_order = 0;
   ulong first_position = 0;
   report.managed_pending_count = FP_NDSHookTradeCountManagedOrders(cfg, first_order);
   report.managed_position_count = FP_NDSHookTradeCountManagedPositions(cfg, first_position);
   report.foreign_symbol_position_count = FP_NDSHookTradeCountForeignPositionsOnSymbol(symbol, cfg);
   report.order_ticket = first_order;
   report.position_ticket = first_position;

   if(report.managed_position_count > 1)
   {
      string delete_reason;
      if(report.managed_pending_count > 0)
         FP_NDSHookTradeDeleteAllManagedPending(cfg, delete_reason);
      report.ok = false;
      report.action = FP_NDS_HOOK_TRADE_ACTION_BLOCKED;
      report.status = "INVARIANT_MULTIPLE_MANAGED_POSITIONS";
      report.reason = "manual_operator_reconciliation_required";
      FP_NDSHookTradeFinalizeReport(report);
      FP_NDSHookTradeExportReport(cfg, report);
      return;
   }

   if(report.managed_position_count == 0 && report.managed_pending_count > 1)
   {
      ulong kept_ticket = 0;
      string reconcile_reason;
      FP_NDSHookTradeReconcileDuplicatePending(cfg, kept_ticket, reconcile_reason);
      report.managed_pending_count = FP_NDSHookTradeCountManagedOrders(cfg, first_order);
      report.order_ticket = (kept_ticket > 0 ? kept_ticket : first_order);
      if(report.managed_pending_count > 1)
      {
         report.ok = false;
         report.action = FP_NDS_HOOK_TRADE_ACTION_BLOCKED;
         report.status = "INVARIANT_MULTIPLE_PENDING_ORDERS";
         report.reason = "duplicate_pending_reconciliation_failed";
         FP_NDSHookTradeFinalizeReport(report);
         FP_NDSHookTradeExportReport(cfg, report);
         return;
      }
   }

   // Hard current contract: one managed exposure globally for this magic. A
   // filled position owns the strategy until its same-direction F1-F2-F3 exit.
   if(report.managed_position_count > 0)
   {
      string pending_delete_reason;
      if(report.managed_pending_count > 0)
         FP_NDSHookTradeDeleteAllManagedPending(cfg, pending_delete_reason);

      ulong position_ticket = 0;
      int position_direction = FP_DIR_NONE;
      datetime position_open_time = 0;
      if(!FP_NDSHookTradeFindManagedPositionForSymbol(symbol, cfg,
                                                      position_ticket,
                                                      position_direction,
                                                      position_open_time))
      {
         report.ok = true;
         report.action = FP_NDS_HOOK_TRADE_ACTION_POSITION_HELD;
         report.status = "SINGLE_EXPOSURE_HELD_ON_OTHER_SYMBOL";
         report.reason = "managed_position_exists_globally_for_magic";
         FP_NDSHookTradeFinalizeReport(report);
         FP_NDSHookTradeExportReport(cfg, report);
         return;
      }

      report.position_ticket = position_ticket;
      if(FP_NDSHookTradeFindExitF3(events, event_count,
                                   position_direction,
                                   position_open_time,
                                   cfg,
                                   report.exit_signal))
      {
         if(!cfg.send_live_orders)
         {
            report.ok = true;
            report.action = FP_NDS_HOOK_TRADE_ACTION_POSITION_HELD;
            report.status = "PAPER_EXIT_SIGNAL_READY";
            report.reason = "same_direction_f123_completed_but_live_send_disabled";
         }
         else
         {
            string close_reason;
            if(FP_NDSHookTradeClosePositionOnF3(position_ticket, cfg, close_reason))
            {
               report.ok = true;
               report.action = FP_NDS_HOOK_TRADE_ACTION_POSITION_CLOSED_F3;
               report.status = "POSITION_CLOSED_ON_SAME_DIRECTION_F3";
               report.reason = close_reason;
               report.close_ticket = position_ticket;
            }
            else
            {
               report.ok = false;
               report.action = FP_NDS_HOOK_TRADE_ACTION_BLOCKED;
               report.status = "POSITION_CLOSE_FAILED";
               report.reason = close_reason;
            }
         }
      }
      else
      {
         report.ok = true;
         report.action = FP_NDS_HOOK_TRADE_ACTION_POSITION_HELD;
         report.status = "POSITION_WAITING_FOR_SAME_DIRECTION_F123";
         report.reason = "no_completed_post_entry_same_direction_f3";
      }

      FP_NDSHookTradeFinalizeReport(report);
      FP_NDSHookTradeExportReport(cfg, report);
      return;
   }

   if(cancelled_dead > 0)
   {
      report.ok = true;
      report.action = FP_NDS_HOOK_TRADE_ACTION_PENDING_CANCELLED;
      report.status = "PENDING_CANCELLED_AFTER_HOOK_DEATH";
      report.reason = cancel_reason;
      FP_NDSHookTradeFinalizeReport(report);
      FP_NDSHookTradeExportReport(cfg, report);
      return;
   }

   if(report.managed_pending_count > 0)
   {
      report.ok = true;
      report.action = FP_NDS_HOOK_TRADE_ACTION_PENDING_HELD;
      report.status = "SINGLE_PENDING_LIMIT_HELD";
      report.reason = "single_exposure_lock_blocks_new_setups";
      FP_NDSHookTradeFinalizeReport(report);
      FP_NDSHookTradeExportReport(cfg, report);
      return;
   }

   // Netting/foreign-position guard: do not merge NDS exposure into a position
   // that this module does not own.
   if(report.foreign_symbol_position_count > 0)
   {
      report.ok = true;
      report.action = FP_NDS_HOOK_TRADE_ACTION_BLOCKED;
      report.status = "BLOCKED_FOREIGN_POSITION_ON_SYMBOL";
      report.reason = "existing_symbol_position_not_owned_by_nds_hook_trade";
      FP_NDSHookTradeFinalizeReport(report);
      FP_NDSHookTradeExportReport(cfg, report);
      return;
   }

   if(!FP_NDSStructureSnapshotMatches(symbol, period))
   {
      report.ok = false;
      report.action = FP_NDS_HOOK_TRADE_ACTION_BLOCKED;
      report.status = "BLOCKED_NO_HOOK_SNAPSHOT";
      report.reason = "phase02_snapshot_not_ready_for_symbol_timeframe";
      FP_NDSHookTradeFinalizeReport(report);
      FP_NDSHookTradeExportReport(cfg, report);
      return;
   }

   FP_HookPhase02Sequence sequences[];
   FP_NDSCopyStructureSnapshot(sequences);
   FP_HookPhase02Sequence selected;
   if(!FP_NDSHookTradeSelectLatest(sequences, cfg, selected))
   {
      report.ok = true;
      report.action = FP_NDS_HOOK_TRADE_ACTION_NONE;
      report.status = "NO_VALID_H3F_OR_HH_SETUP";
      report.reason = "latest_snapshot_has_no_eligible_valid_family";
      FP_NDSHookTradeFinalizeReport(report);
      FP_NDSHookTradeExportReport(cfg, report);
      return;
   }

   if(!FP_NDSHookTradeBuildSetup(symbol, period, selected, cfg, report.setup))
   {
      report.ok = true;
      report.action = FP_NDS_HOOK_TRADE_ACTION_BLOCKED;
      report.status = report.setup.status;
      report.reason = report.setup.reason;
      FP_NDSHookTradeFinalizeReport(report);
      FP_NDSHookTradeExportReport(cfg, report);
      return;
   }

   double entry_lock_token = 0.0;
   string entry_lock_reason;
   if(!FP_NDSHookTradeAcquireEntryLock(cfg, entry_lock_token, entry_lock_reason))
   {
      report.ok = true;
      report.action = FP_NDS_HOOK_TRADE_ACTION_BLOCKED;
      report.status = "BLOCKED_GLOBAL_ENTRY_LOCK";
      report.reason = entry_lock_reason;
      FP_NDSHookTradeFinalizeReport(report);
      FP_NDSHookTradeExportReport(cfg, report);
      return;
   }

   // Re-check broker state while holding the terminal-wide compare-and-swap
   // lock. This closes the multi-chart race between exposure scan and send.
   ulong locked_order = 0;
   ulong locked_position = 0;
   int locked_pending_count = FP_NDSHookTradeCountManagedOrders(cfg, locked_order);
   int locked_position_count = FP_NDSHookTradeCountManagedPositions(cfg, locked_position);
   int locked_foreign_count = FP_NDSHookTradeCountForeignPositionsOnSymbol(symbol, cfg);
   if(locked_pending_count > 0 || locked_position_count > 0 || locked_foreign_count > 0)
   {
      FP_NDSHookTradeReleaseEntryLock(cfg, entry_lock_token);
      report.ok = true;
      report.action = FP_NDS_HOOK_TRADE_ACTION_BLOCKED;
      report.status = "BLOCKED_EXPOSURE_CHANGED_DURING_ENTRY";
      report.reason = "single_exposure_recheck_failed";
      report.managed_pending_count = locked_pending_count;
      report.managed_position_count = locked_position_count;
      report.foreign_symbol_position_count = locked_foreign_count;
      report.order_ticket = locked_order;
      report.position_ticket = locked_position;
      FP_NDSHookTradeFinalizeReport(report);
      FP_NDSHookTradeExportReport(cfg, report);
      return;
   }

   if(!cfg.send_live_orders)
   {
      bool paper_registry_ok = FP_NDSHookTradeMarkSetupUsed(cfg, report.setup.setup_key);
      FP_NDSHookTradeReleaseEntryLock(cfg, entry_lock_token);
      report.ok = paper_registry_ok;
      report.action = FP_NDS_HOOK_TRADE_ACTION_PAPER_LIMIT;
      report.status = (paper_registry_ok ? "PAPER_LIMIT_AT_HOOK_TERMINAL" :
                                          "PAPER_LIMIT_REGISTRY_FAILED");
      report.reason = (paper_registry_ok ? "send_live_orders_false" :
                                          "paper_decision_not_persisted");
      FP_NDSHookTradeFinalizeReport(report);
      FP_NDSHookTradeExportReport(cfg, report);
      return;
   }

   string send_reason;
   ulong order_ticket = 0;
   if(FP_NDSHookTradeSendLimit(symbol, cfg, report.setup, order_ticket, send_reason))
   {
      bool registry_ok = FP_NDSHookTradeMarkSetupUsed(cfg, report.setup.setup_key);
      report.ok = true;
      report.action = FP_NDS_HOOK_TRADE_ACTION_LIMIT_SENT;
      report.status = (registry_ok ? "LIMIT_SENT_AT_VALID_HOOK_TERMINAL" :
                                     "LIMIT_SENT_REGISTRY_WARNING");
      report.reason = (registry_ok ? send_reason :
                                     send_reason + ";one_attempt_registry_write_failed");
      report.order_ticket = order_ticket;
   }
   else
   {
      report.ok = false;
      report.action = FP_NDS_HOOK_TRADE_ACTION_BLOCKED;
      report.status = "LIMIT_SEND_FAILED";
      report.reason = send_reason;
   }

   FP_NDSHookTradeReleaseEntryLock(cfg, entry_lock_token);
   FP_NDSHookTradeFinalizeReport(report);
   FP_NDSHookTradeExportReport(cfg, report);
}

void FP_PrintNDSHookTradeReport(const string tag,
                                const FP_NDSHookTradeReport &report)
{
   Print(tag,
         " attempted=", FP_NDSHookTradeBool(report.attempted),
         " ok=", FP_NDSHookTradeBool(report.ok),
         " action=", report.action_label,
         " status=", report.status,
         " reason=", report.reason,
         " pending=", report.managed_pending_count,
         " positions=", report.managed_position_count,
         " seq=", report.setup.sequence_id,
         " family=", report.setup.family,
         " entry=", DoubleToString(report.setup.entry_price, _Digits),
         " stop=", DoubleToString(report.setup.stop_price, _Digits),
         " exit_f3=", report.exit_signal.event_id);
}

#endif // __FP_NDS_HOOK_TRADE_ENGINE_MQH__
