#ifndef __FP_NDS_F2_WAIST_TRADE_ENGINE_MQH__
#define __FP_NDS_F2_WAIST_TRADE_ENGINE_MQH__
#property strict

#include "FP_NDSF2WaistTradeRules.mqh"

void FP_RunNDSF2WaistTradeCore(const string symbol,
                               const ENUM_TIMEFRAMES period,
                               const FP_FlagEvent &events[],
                               const int event_count,
                               const FP_NDSF2WaistTradeConfig &cfg,
                               FP_NDSF2WaistTradeReport &report)
{
   FP_ResetNDSF2WaistTradeReport(report);
   report.symbol = symbol;
   report.period = period;
   report.attempted = cfg.enabled;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "NDS_F2_WAIST_TRADE_DISABLED";
      report.reason = "trade_enabled_false";
      return;
   }

   FP_NDSHookTradeConfig shared_cfg;
   FP_NDSF2BuildSharedTradeConfig(cfg, shared_cfg);

   ulong first_order = 0;
   ulong first_position = 0;
   report.managed_pending_count = FP_NDSHookTradeCountManagedOrders(shared_cfg, first_order);
   report.managed_position_count = FP_NDSHookTradeCountManagedPositions(shared_cfg, first_position);
   report.foreign_symbol_position_count = FP_NDSHookTradeCountForeignPositionsOnSymbol(symbol, shared_cfg);
   report.order_ticket = first_order;
   report.position_ticket = first_position;

   if(report.managed_position_count > 1)
   {
      report.ok = false;
      report.action = FP_NDS_F2_ACTION_BLOCKED;
      report.status = "INVARIANT_MULTIPLE_MANAGED_POSITIONS";
      report.reason = "manual_reconciliation_required";
      return;
   }

   if(report.managed_position_count == 0 && report.managed_pending_count > 1)
   {
      ulong kept_ticket = 0;
      string reconcile_reason;
      FP_NDSHookTradeReconcileDuplicatePending(shared_cfg, kept_ticket, reconcile_reason);
      report.managed_pending_count = FP_NDSHookTradeCountManagedOrders(shared_cfg, first_order);
      report.order_ticket = (kept_ticket > 0 ? kept_ticket : first_order);
      if(report.managed_pending_count > 1)
      {
         report.ok = false;
         report.action = FP_NDS_F2_ACTION_BLOCKED;
         report.status = "INVARIANT_MULTIPLE_PENDING_ORDERS";
         report.reason = "duplicate_pending_reconciliation_failed";
         return;
      }
   }

   if(report.managed_position_count > 0)
   {
      string pending_delete_reason;
      if(report.managed_pending_count > 0)
         FP_NDSHookTradeDeleteAllManagedPending(shared_cfg, pending_delete_reason);
      report.ok = true;
      report.action = FP_NDS_F2_ACTION_POSITION_HELD;
      report.status = "POSITION_HELD_BROKER_SL_TP";
      report.reason = "single_position_owns_strategy_until_exact_sl_or_tp";
      return;
   }

   if(report.managed_pending_count > 0)
   {
      report.ok = true;
      report.action = FP_NDS_F2_ACTION_PENDING_HELD;
      report.status = "SINGLE_F2_LIMIT_PENDING";
      report.reason = "single_exposure_lock_blocks_new_f2_setups";
      return;
   }

   if(report.foreign_symbol_position_count > 0)
   {
      report.ok = true;
      report.action = FP_NDS_F2_ACTION_BLOCKED;
      report.status = "BLOCKED_FOREIGN_POSITION_ON_SYMBOL";
      report.reason = "prevent_netting_merge_with_foreign_position";
      return;
   }

   int f2_index = FP_NDSF2SelectLatest(events, event_count, cfg);
   if(f2_index < 0)
   {
      report.ok = true;
      report.action = FP_NDS_F2_ACTION_NONE;
      report.status = "NO_CONFIRMED_F2";
      report.reason = "no_visible_confirmed_f2_can_spawn_f3";
      return;
   }

   if(!FP_NDSF2BuildSetup(symbol, period, events, event_count, f2_index, cfg, report.setup))
   {
      report.ok = true;
      report.action = FP_NDS_F2_ACTION_BLOCKED;
      report.status = report.setup.status;
      report.reason = report.setup.reason;
      return;
   }

   double lock_token = 0.0;
   string lock_reason;
   if(!FP_NDSHookTradeAcquireEntryLock(shared_cfg, lock_token, lock_reason))
   {
      report.ok = true;
      report.action = FP_NDS_F2_ACTION_BLOCKED;
      report.status = "BLOCKED_GLOBAL_ENTRY_LOCK";
      report.reason = lock_reason;
      return;
   }

   ulong locked_order = 0;
   ulong locked_position = 0;
   int locked_pending = FP_NDSHookTradeCountManagedOrders(shared_cfg, locked_order);
   int locked_positions = FP_NDSHookTradeCountManagedPositions(shared_cfg, locked_position);
   int locked_foreign = FP_NDSHookTradeCountForeignPositionsOnSymbol(symbol, shared_cfg);
   if(locked_pending > 0 || locked_positions > 0 || locked_foreign > 0)
   {
      FP_NDSHookTradeReleaseEntryLock(shared_cfg, lock_token);
      report.ok = true;
      report.action = FP_NDS_F2_ACTION_BLOCKED;
      report.status = "BLOCKED_EXPOSURE_CHANGED_DURING_ENTRY";
      report.reason = "single_exposure_recheck_failed";
      return;
   }

   if(!cfg.send_tester_orders)
   {
      bool registry_ok = FP_NDSF2MarkSetupUsed(cfg, report.setup.setup_key);
      FP_NDSHookTradeReleaseEntryLock(shared_cfg, lock_token);
      report.ok = registry_ok;
      report.action = FP_NDS_F2_ACTION_PAPER_LIMIT;
      report.status = (registry_ok ? "PAPER_F2_WAIST_LIMIT" : "PAPER_REGISTRY_FAILED");
      report.reason = (registry_ok ? "send_tester_orders_false" : "setup_registry_write_failed");
      return;
   }

   ulong order_ticket = 0;
   string send_reason;
   if(FP_NDSF2SendLimit(symbol, cfg, report.setup, order_ticket, send_reason))
   {
      bool registry_ok = FP_NDSF2MarkSetupUsed(cfg, report.setup.setup_key);
      report.ok = true;
      report.action = FP_NDS_F2_ACTION_LIMIT_SENT;
      report.status = (registry_ok ? "F2_WAIST_LIMIT_SENT" : "F2_WAIST_LIMIT_SENT_REGISTRY_WARNING");
      report.reason = (registry_ok ? send_reason : send_reason + ";registry_write_failed");
      report.order_ticket = order_ticket;
   }
   else
   {
      report.ok = false;
      report.action = FP_NDS_F2_ACTION_BLOCKED;
      report.status = "F2_WAIST_LIMIT_SEND_FAILED";
      report.reason = send_reason;
   }

   FP_NDSHookTradeReleaseEntryLock(shared_cfg, lock_token);
}

#endif // __FP_NDS_F2_WAIST_TRADE_ENGINE_MQH__
