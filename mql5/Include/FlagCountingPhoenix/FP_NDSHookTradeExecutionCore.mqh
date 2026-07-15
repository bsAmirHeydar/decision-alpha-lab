#ifndef __FP_NDS_HOOK_TRADE_EXECUTION_CORE_MQH__
#define __FP_NDS_HOOK_TRADE_EXECUTION_CORE_MQH__
#property strict

#include "FP_NDSHookTradeRules.mqh"

// Pure executable workflow shared by the production expert and the lightweight
// Strategy Tester expert. It performs no CSV export and no summary printing.

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

bool FP_NDSHookTradeFixedRProtectionValid(const string symbol,
                                          const int direction,
                                          const double entry_price,
                                          const double stop_price,
                                          const double target_price,
                                          double &risk_distance,
                                          double &reward_distance,
                                          string &reason)
{
   risk_distance = MathAbs(entry_price - stop_price);
   reward_distance = MathAbs(target_price - entry_price);
   reason = "invalid_fixed_r_protection";

   bool geometry_ok = (entry_price > 0.0 && stop_price > 0.0 && target_price > 0.0 &&
                       risk_distance > 0.0 && reward_distance > 0.0);
   if(direction == FP_DIR_BULLISH)
      geometry_ok = (geometry_ok && stop_price < entry_price && entry_price < target_price);
   else if(direction == FP_DIR_BEARISH)
      geometry_ok = (geometry_ok && target_price < entry_price && entry_price < stop_price);
   else
      geometry_ok = false;

   if(!geometry_ok)
   {
      reason = "fixed_r_stop_entry_target_order_invalid";
      return false;
   }

   double tick = FP_NDSHookTradeTickSize(symbol);
   if(tick <= 0.0)
   {
      reason = "fixed_r_tick_size_invalid";
      return false;
   }
   if(reward_distance + tick * 0.1 <
      risk_distance * FP_NDS_HOOK_864_REWARD_R)
   {
      reason = "fixed_r_reward_below_canonical_1R";
      return false;
   }

   reason = "fixed_r_protection_valid";
   return true;
}

void FP_RunNDSHookTradeExecutionCore(const string symbol,
                                     const ENUM_TIMEFRAMES period,
                                     const FP_FlagEvent &events[],
                                     const int event_count,
                                     const FP_NDSHookTradeConfig &cfg,
                                     FP_NDSHookTradeReport &report)
{
   FP_ResetNDSHookTradeReport(report);
   report.schema_version = FP_NDSHookTradeSchemaName(cfg.profile);
   report.symbol = symbol;
   report.period = period;
   report.attempted = cfg.enabled;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "NDS_HOOK_TRADE_DISABLED";
      report.reason = "InpNDSHookTradeEnabled_false";
      FP_NDSHookTradeFinalizeReport(report);
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
         return;
      }

      report.position_ticket = position_ticket;

      if(!PositionSelectByTicket(position_ticket))
      {
         report.ok = false;
         report.action = FP_NDS_HOOK_TRADE_ACTION_BLOCKED;
         report.status = "BLOCKED_MANAGED_POSITION_NOT_SELECTABLE";
         report.reason = "managed_position_disappeared_before_profile_recovery";
         FP_NDSHookTradeFinalizeReport(report);
         return;
      }

      FP_NDSHookTradeProfile position_profile;
      string position_profile_reason;
      string position_comment = PositionGetString(POSITION_COMMENT);
      if(!FP_NDSHookTradeProfileFromBrokerComment(cfg, position_comment,
                                                  position_profile,
                                                  position_profile_reason))
      {
         report.ok = false;
         report.action = FP_NDS_HOOK_TRADE_ACTION_BLOCKED;
         report.status = "BLOCKED_MANAGED_POSITION_PROFILE_UNKNOWN";
         report.reason = position_profile_reason;
         FP_NDSHookTradeFinalizeReport(report);
         return;
      }

      bool position_profile_recovered = (position_profile != cfg.profile);
      report.setup.profile_label = FP_NDSHookTradeProfileName(position_profile);
      report.schema_version = FP_NDSHookTradeSchemaName(position_profile);

      if(position_profile == FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1)
      {
         // The broker-attached SL/TP owns the fixed-1R lifecycle. The F123 exit
         // detector remains untouched and is not consulted for this profile.
         if(!PositionSelectByTicket(position_ticket))
         {
            report.ok = false;
            report.action = FP_NDS_HOOK_TRADE_ACTION_BLOCKED;
            report.status = "BLOCKED_FIXED_R_POSITION_NOT_SELECTABLE";
            report.reason = "managed_position_disappeared_during_protection_check";
         }
         else
         {
            double open_price = PositionGetDouble(POSITION_PRICE_OPEN);
            double stop_price = PositionGetDouble(POSITION_SL);
            double target_price = PositionGetDouble(POSITION_TP);
            double risk_distance = 0.0;
            double reward_distance = 0.0;
            string protection_reason;
            report.ok = FP_NDSHookTradeFixedRProtectionValid(symbol,
                                                              position_direction,
                                                              open_price,
                                                              stop_price,
                                                              target_price,
                                                              risk_distance,
                                                              reward_distance,
                                                              protection_reason);
            report.setup.direction = position_direction;
            report.setup.direction_label = FP_NDSHookTradeDirectionName(position_direction);
            report.setup.entry_price = open_price;
            report.setup.stop_price = stop_price;
            report.setup.target_price = target_price;
            report.setup.risk_distance = risk_distance;
            report.setup.reward_distance = reward_distance;
            report.setup.reward_r = (risk_distance > 0.0 ?
                                     reward_distance / risk_distance : 0.0);
            report.action = (report.ok ? FP_NDS_HOOK_TRADE_ACTION_POSITION_HELD :
                                         FP_NDS_HOOK_TRADE_ACTION_BLOCKED);
            report.status = (report.ok ? "POSITION_HELD_BY_FIXED_R1_PROTECTION" :
                                         "BLOCKED_FIXED_R_POSITION_PROTECTION");
            report.reason = (report.ok ? "broker_sl_tp_own_exit_no_f123_close" :
                                         protection_reason);
            if(position_profile_recovered)
               report.reason += ";position_profile_recovered_from_broker_comment";
         }

         FP_NDSHookTradeFinalizeReport(report);
         return;
      }

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

      if(position_profile_recovered)
         report.reason += ";position_profile_recovered_from_broker_comment";
      FP_NDSHookTradeFinalizeReport(report);
      return;
   }

   if(cancelled_dead > 0)
   {
      report.ok = true;
      report.action = FP_NDS_HOOK_TRADE_ACTION_PENDING_CANCELLED;
      report.status = "PENDING_CANCELLED_AFTER_HOOK_DEATH";
      report.reason = cancel_reason;
      FP_NDSHookTradeFinalizeReport(report);
      return;
   }

   if(report.managed_pending_count > 0)
   {
      FP_NDSHookTradeProfile pending_profile;
      string pending_profile_reason;
      bool pending_selected = (report.order_ticket > 0 && OrderSelect(report.order_ticket));
      string pending_comment = (pending_selected ? OrderGetString(ORDER_COMMENT) : "");
      if(!pending_selected ||
         !FP_NDSHookTradeProfileFromBrokerComment(cfg, pending_comment,
                                                  pending_profile,
                                                  pending_profile_reason))
      {
         report.ok = false;
         report.action = FP_NDS_HOOK_TRADE_ACTION_BLOCKED;
         report.status = "BLOCKED_MANAGED_PENDING_PROFILE_UNKNOWN";
         report.reason = (pending_selected ? pending_profile_reason :
                                             "managed_pending_not_selectable");
         FP_NDSHookTradeFinalizeReport(report);
         return;
      }

      bool pending_profile_recovered = (pending_profile != cfg.profile);
      report.setup.profile_label = FP_NDSHookTradeProfileName(pending_profile);
      report.schema_version = FP_NDSHookTradeSchemaName(pending_profile);

      if(pending_profile == FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1)
      {
         ENUM_ORDER_TYPE pending_type = (ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE);
         int pending_direction = (pending_type == ORDER_TYPE_BUY_LIMIT ? FP_DIR_BULLISH :
                                  (pending_type == ORDER_TYPE_SELL_LIMIT ? FP_DIR_BEARISH : FP_DIR_NONE));
         double pending_entry = OrderGetDouble(ORDER_PRICE_OPEN);
         double pending_stop = OrderGetDouble(ORDER_SL);
         double pending_target = OrderGetDouble(ORDER_TP);
         double pending_risk = 0.0;
         double pending_reward = 0.0;
         string pending_protection_reason;
         bool pending_protection_ok = FP_NDSHookTradeFixedRProtectionValid(symbol,
                                                                           pending_direction,
                                                                           pending_entry,
                                                                           pending_stop,
                                                                           pending_target,
                                                                           pending_risk,
                                                                           pending_reward,
                                                                           pending_protection_reason);
         report.setup.direction = pending_direction;
         report.setup.direction_label = FP_NDSHookTradeDirectionName(pending_direction);
         report.setup.entry_price = pending_entry;
         report.setup.stop_price = pending_stop;
         report.setup.target_price = pending_target;
         report.setup.risk_distance = pending_risk;
         report.setup.reward_distance = pending_reward;
         report.setup.reward_r = (pending_risk > 0.0 ? pending_reward / pending_risk : 0.0);
         report.setup.broker_comment = pending_comment;

         if(!pending_protection_ok)
         {
            g_fp_nds_hook_trade.SetAsyncMode(false);
            g_fp_nds_hook_trade.SetExpertMagicNumber((ulong)cfg.magic);
            bool deleted = g_fp_nds_hook_trade.OrderDelete(report.order_ticket);
            uint delete_retcode = g_fp_nds_hook_trade.ResultRetcode();
            report.ok = deleted && FP_NDSHookTradeRetcodeAccepted(delete_retcode);
            report.action = (report.ok ? FP_NDS_HOOK_TRADE_ACTION_PENDING_CANCELLED :
                                         FP_NDS_HOOK_TRADE_ACTION_BLOCKED);
            report.status = (report.ok ? "PENDING_CANCELLED_INVALID_FIXED_R_PROTECTION" :
                                         "BLOCKED_INVALID_FIXED_R_PENDING_PROTECTION");
            report.reason = pending_protection_reason;
            if(report.ok)
               report.managed_pending_count = 0;
            else
               report.reason += ";delete_failed_" + IntegerToString((int)delete_retcode);
            FP_NDSHookTradeFinalizeReport(report);
            return;
         }
      }

      report.ok = true;
      report.action = FP_NDS_HOOK_TRADE_ACTION_PENDING_HELD;
      report.status = (pending_profile_recovered ?
                       "SINGLE_PENDING_LIMIT_HELD_PROFILE_RECOVERED" :
                       "SINGLE_PENDING_LIMIT_HELD");
      report.reason = (pending_profile_recovered ?
                       "single_exposure_lock;pending_profile_recovered_from_broker_comment" :
                       "single_exposure_lock_blocks_new_setups");
      FP_NDSHookTradeFinalizeReport(report);
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
      return;
   }

   if(!FP_NDSStructureSnapshotMatches(symbol, period))
   {
      report.ok = false;
      report.action = FP_NDS_HOOK_TRADE_ACTION_BLOCKED;
      report.status = "BLOCKED_NO_HOOK_SNAPSHOT";
      report.reason = "phase02_snapshot_not_ready_for_symbol_timeframe";
      FP_NDSHookTradeFinalizeReport(report);
      return;
   }

   FP_HookPhase02Sequence sequences[];
   FP_NDSCopyStructureSnapshot(sequences);
   FP_HookPhase02Sequence selected;
   if(!FP_NDSHookTradeSelectLatest(sequences, cfg, selected))
   {
      report.ok = true;
      report.action = FP_NDS_HOOK_TRADE_ACTION_NONE;
      report.status = (cfg.profile == FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1 ?
                       "NO_ELIGIBLE_HOOK_864_CYCLE_R1_SETUP" :
                       "NO_VALID_H3F_OR_HH_SETUP");
      report.reason = (cfg.profile == FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1 ?
                       "no_closed_valid_family_with_x3_or_x4_before_864" :
                       "latest_snapshot_has_no_eligible_valid_family");
      FP_NDSHookTradeFinalizeReport(report);
      return;
   }

   if(!FP_NDSHookTradeBuildSetup(symbol, period, selected, cfg, report.setup))
   {
      report.ok = true;
      report.action = FP_NDS_HOOK_TRADE_ACTION_BLOCKED;
      report.status = report.setup.status;
      report.reason = report.setup.reason;
      FP_NDSHookTradeFinalizeReport(report);
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
      return;
   }

   if(!cfg.send_live_orders)
   {
      bool paper_registry_ok = FP_NDSHookTradeMarkSetupUsed(cfg, report.setup.setup_key);
      FP_NDSHookTradeReleaseEntryLock(cfg, entry_lock_token);
      report.ok = paper_registry_ok;
      report.action = FP_NDS_HOOK_TRADE_ACTION_PAPER_LIMIT;
      report.status = (paper_registry_ok ?
                       (cfg.profile == FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1 ?
                        "PAPER_LIMIT_AT_HOOK_864_CYCLE_R1" :
                        "PAPER_LIMIT_AT_HOOK_TERMINAL") :
                       "PAPER_LIMIT_REGISTRY_FAILED");
      report.reason = (paper_registry_ok ? "send_live_orders_false" :
                                          "paper_decision_not_persisted");
      FP_NDSHookTradeFinalizeReport(report);
      return;
   }

   string send_reason;
   ulong order_ticket = 0;
   if(FP_NDSHookTradeSendLimit(symbol, cfg, report.setup, order_ticket, send_reason))
   {
      bool registry_ok = FP_NDSHookTradeMarkSetupUsed(cfg, report.setup.setup_key);
      report.ok = true;
      report.action = FP_NDS_HOOK_TRADE_ACTION_LIMIT_SENT;
      report.status = (registry_ok ?
                       (cfg.profile == FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1 ?
                        "LIMIT_SENT_AT_VALID_HOOK_864_CYCLE_R1" :
                        "LIMIT_SENT_AT_VALID_HOOK_TERMINAL") :
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
}

// Backward-compatible Phase 52 core API. Existing direct callers retain the
// same behavior because TERMINAL_F123 remains the default profile.
void FP_RunNDSHookLimitF123ExecutionCore(const string symbol,
                                         const ENUM_TIMEFRAMES period,
                                         const FP_FlagEvent &events[],
                                         const int event_count,
                                         const FP_NDSHookTradeConfig &cfg,
                                         FP_NDSHookTradeReport &report)
{
   FP_RunNDSHookTradeExecutionCore(symbol, period,
                                   events, event_count,
                                   cfg, report);
}

#endif // __FP_NDS_HOOK_TRADE_EXECUTION_CORE_MQH__
