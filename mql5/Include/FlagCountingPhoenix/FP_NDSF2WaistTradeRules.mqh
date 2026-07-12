#ifndef __FP_NDS_F2_WAIST_TRADE_RULES_MQH__
#define __FP_NDS_F2_WAIST_TRADE_RULES_MQH__
#property strict

#include <Trade/Trade.mqh>
#include "FP_SequenceEngine.mqh"
#include "FP_NDSHookTradeRules.mqh"
#include "FP_NDSF2WaistTradeTypes.mqh"

CTrade g_fp_nds_f2_waist_trade;

void FP_NDSF2BuildSharedTradeConfig(const FP_NDSF2WaistTradeConfig &src,
                                    FP_NDSHookTradeConfig &dst)
{
   FP_ResetNDSHookTradeConfig(dst);
   dst.enabled = src.enabled;
   dst.send_live_orders = src.send_tester_orders;
   dst.one_attempt_per_hook = src.one_attempt_per_f2;
   dst.reset_used_setups_on_init = src.reset_used_setups_on_init;
   dst.sizing_mode = src.sizing_mode;
   dst.fixed_volume = src.fixed_volume;
   dst.risk_cash = src.risk_cash;
   dst.commission_per_lot_round_turn = src.commission_per_lot_round_turn;
   dst.allow_min_lot_if_risk_too_small = src.allow_min_lot_if_risk_too_small;
   dst.max_deviation_points = src.max_deviation_points;
   dst.entry_lock_timeout_seconds = src.entry_lock_timeout_seconds;
   dst.magic = src.magic;
   dst.comment_prefix = src.comment_prefix;
   dst.export_csv = false;
   dst.print_summary = false;
}

string FP_NDSF2UsedPrefix(const FP_NDSF2WaistTradeConfig &cfg)
{
   return "NDSF2_USED_" + IntegerToString((long)AccountInfoInteger(ACCOUNT_LOGIN)) + "_" +
          IntegerToString(cfg.magic) + "_";
}

string FP_NDSF2UsedName(const FP_NDSF2WaistTradeConfig &cfg,
                        const string setup_key)
{
   return FP_NDSF2UsedPrefix(cfg) + IntegerToString(FP_NDSHookTradeHash(setup_key));
}

bool FP_NDSF2SetupUsed(const FP_NDSF2WaistTradeConfig &cfg,
                       const string setup_key)
{
   if(!cfg.one_attempt_per_f2) return false;
   return GlobalVariableCheck(FP_NDSF2UsedName(cfg, setup_key));
}

bool FP_NDSF2MarkSetupUsed(const FP_NDSF2WaistTradeConfig &cfg,
                           const string setup_key)
{
   if(!cfg.one_attempt_per_f2) return true;
   return (GlobalVariableSet(FP_NDSF2UsedName(cfg, setup_key), (double)TimeCurrent()) > 0);
}

int FP_NDSF2ResetUsedSetups(const FP_NDSF2WaistTradeConfig &cfg)
{
   return GlobalVariablesDeleteAll(FP_NDSF2UsedPrefix(cfg));
}

bool FP_NDSF2IsConfirmed(const FP_FlagEvent &f2,
                         const bool require_visible_main)
{
   if(f2.level != FP_LEVEL_F2) return false;
   if(f2.direction != FP_DIR_BULLISH && f2.direction != FP_DIR_BEARISH) return false;
   if(require_visible_main && !f2.visible_main) return false;
   if(!f2.f2_can_spawn_f3) return false;
   if(f2.f2_lifecycle_status != FP_F2_LC_CONFIRMED) return false;
   if(f2.status != FP_STATUS_CONFIRMED) return false;
   if(!f2.has_waist || !f2.has_leg2 || !f2.has_confirm) return false;
   if(f2.waist.price <= 0.0 || f2.leg2.price <= 0.0) return false;
   return true;
}

int FP_NDSF2SelectLatest(const FP_FlagEvent &events[],
                         const int event_count,
                         const FP_NDSF2WaistTradeConfig &cfg)
{
   int best = -1;
   for(int i=0; i<event_count; i++)
   {
      if(!FP_NDSF2IsConfirmed(events[i], cfg.require_visible_main)) continue;
      if(best < 0)
      {
         best = i;
         continue;
      }

      datetime ti = events[i].confirm.time_anchor;
      datetime tb = events[best].confirm.time_anchor;
      if(ti > tb)
      {
         best = i;
         continue;
      }
      if(ti < tb) continue;

      if(events[i].canonical_rank_final > events[best].canonical_rank_final)
      {
         best = i;
         continue;
      }
      if(events[i].canonical_rank_final < events[best].canonical_rank_final) continue;

      if(events[i].event_id > events[best].event_id) best = i;
   }
   return best;
}

string FP_NDSF2BuildSetupKey(const string symbol,
                             const ENUM_TIMEFRAMES period,
                             const FP_FlagEvent &f2)
{
   string key = symbol;
   key += "|TF=" + EnumToString(period);
   key += "|F2=" + IntegerToString(f2.event_id);
   key += "|SEQ=" + IntegerToString(f2.sequence_id);
   key += "|DIR=" + IntegerToString(f2.direction);
   key += "|C=" + IntegerToString((long)f2.confirm.time_anchor);
   key += "|W=" + IntegerToString((long)f2.waist.time_anchor);
   key += "|L2=" + IntegerToString((long)f2.leg2.time_anchor);
   return key;
}

string FP_NDSF2BuildComment(const FP_NDSF2WaistTradeConfig &cfg,
                            const FP_FlagEvent &f2)
{
   string comment = cfg.comment_prefix + "|F2|S" + IntegerToString(f2.sequence_id);
   if(StringLen(comment) > 31) comment = StringSubstr(comment, 0, 31);
   return comment;
}

bool FP_NDSF2BuildSetup(const string symbol,
                        const ENUM_TIMEFRAMES period,
                        const FP_FlagEvent &events[],
                        const int event_count,
                        const int f2_index,
                        const FP_NDSF2WaistTradeConfig &cfg,
                        FP_NDSF2WaistTradeSetup &setup)
{
   FP_ResetNDSF2WaistTradeSetup(setup);
   if(f2_index < 0 || f2_index >= event_count)
   {
      setup.status = "BLOCKED_NO_CONFIRMED_F2";
      setup.reason = "no_eligible_f2_index";
      return false;
   }

   FP_FlagEvent f2 = events[f2_index];
   int f1_index = FP_CanonicalFindParentIndex(events, event_count, f2);
   if(f1_index < 0)
   {
      setup.status = "BLOCKED_PARENT_F1";
      setup.reason = "canonical_parent_f1_not_found";
      return false;
   }
   FP_FlagEvent f1 = events[f1_index];
   if(f1.level != FP_LEVEL_F1 || f1.direction != f2.direction || !f1.has_waist || f1.waist.price <= 0.0)
   {
      setup.status = "BLOCKED_PARENT_F1";
      setup.reason = "parent_f1_waist_unavailable_or_direction_mismatch";
      return false;
   }

   setup.available = true;
   setup.f1_event_id = f1.event_id;
   setup.f2_event_id = f2.event_id;
   setup.sequence_id = f2.sequence_id;
   setup.direction = f2.direction;
   setup.scale_L = f2.scale_L;
   setup.f2_confirm_time = f2.confirm.time_anchor;
   setup.f1_waist_price = f1.waist.price;
   setup.f2_waist_price = f2.waist.price;
   setup.f2_leg2_price = f2.leg2.price;
   setup.setup_key = FP_NDSF2BuildSetupKey(symbol, period, f2);
   setup.broker_comment = FP_NDSF2BuildComment(cfg, f2);
   setup.already_used = FP_NDSF2SetupUsed(cfg, setup.setup_key);

   int confirm_shift = iBarShift(symbol, period, f2.confirm.time_anchor, true);
   if(confirm_shift < 0)
   {
      setup.status = "BLOCKED_F2_AGE";
      setup.reason = "f2_confirm_bar_not_resolved_on_chart";
      return false;
   }
   if(cfg.max_setup_age_bars >= 0 && confirm_shift > cfg.max_setup_age_bars)
   {
      setup.status = "BLOCKED_F2_AGE";
      setup.reason = "confirmed_f2_older_than_allowed_setup_window";
      return false;
   }

   if(setup.already_used)
   {
      setup.status = "BLOCKED_ALREADY_USED";
      setup.reason = "one_attempt_per_f2_registry";
      return false;
   }

   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   if(point <= 0.0 || bid <= 0.0 || ask <= 0.0)
   {
      setup.status = "BLOCKED_QUOTES";
      setup.reason = "invalid_bid_ask_or_point";
      return false;
   }

   double offset = MathMax(0.0, cfg.entry_offset_points) * point;
   int stops_level = MathMax(0, (int)SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL));
   int freeze_level = MathMax(0, (int)SymbolInfoInteger(symbol, SYMBOL_TRADE_FREEZE_LEVEL));
   double stop_min_dist = stops_level * point;
   double entry_min_dist = MathMax(stops_level, freeze_level) * point;

   if(setup.direction == FP_DIR_BULLISH)
   {
      setup.entry_price = FP_NDSHookTradeNormalizePrice(symbol, f2.waist.price - offset, false);
      setup.stop_price = FP_NDSHookTradeNormalizePrice(symbol, f1.waist.price, false);
      setup.target_price = FP_NDSHookTradeNormalizePrice(symbol, f2.leg2.price, false);

      if(!(setup.stop_price < setup.entry_price && setup.entry_price < setup.target_price))
      {
         setup.status = "BLOCKED_PRICE_GEOMETRY";
         setup.reason = "bullish_requires_f1_waist_below_entry_below_f2_leg2";
         return false;
      }
      if(!(setup.entry_price < ask - entry_min_dist))
      {
         setup.status = "BLOCKED_LIMIT_GEOMETRY";
         setup.reason = "buy_limit_below_f2_waist_not_below_current_ask";
         return false;
      }
      if(setup.entry_price - setup.stop_price < stop_min_dist ||
         setup.target_price - setup.entry_price < stop_min_dist)
      {
         setup.status = "BLOCKED_BROKER_DISTANCE";
         setup.reason = "exact_f1_waist_stop_or_f2_leg2_target_violates_stops_level";
         return false;
      }
   }
   else if(setup.direction == FP_DIR_BEARISH)
   {
      setup.entry_price = FP_NDSHookTradeNormalizePrice(symbol, f2.waist.price + offset, true);
      setup.stop_price = FP_NDSHookTradeNormalizePrice(symbol, f1.waist.price, true);
      setup.target_price = FP_NDSHookTradeNormalizePrice(symbol, f2.leg2.price, true);

      if(!(setup.target_price < setup.entry_price && setup.entry_price < setup.stop_price))
      {
         setup.status = "BLOCKED_PRICE_GEOMETRY";
         setup.reason = "bearish_requires_f2_leg2_below_entry_below_f1_waist";
         return false;
      }
      if(!(setup.entry_price > bid + entry_min_dist))
      {
         setup.status = "BLOCKED_LIMIT_GEOMETRY";
         setup.reason = "sell_limit_above_f2_waist_not_above_current_bid";
         return false;
      }
      if(setup.stop_price - setup.entry_price < stop_min_dist ||
         setup.entry_price - setup.target_price < stop_min_dist)
      {
         setup.status = "BLOCKED_BROKER_DISTANCE";
         setup.reason = "exact_f1_waist_stop_or_f2_leg2_target_violates_stops_level";
         return false;
      }
   }
   else
   {
      setup.status = "BLOCKED_DIRECTION";
      setup.reason = "f2_direction_none";
      return false;
   }

   FP_NDSHookTradeConfig shared_cfg;
   FP_NDSF2BuildSharedTradeConfig(cfg, shared_cfg);
   string volume_reason;
   if(!FP_NDSHookTradeComputeVolume(symbol, shared_cfg,
                                    setup.entry_price, setup.stop_price,
                                    setup.volume, volume_reason))
   {
      setup.status = "BLOCKED_VOLUME";
      setup.reason = volume_reason;
      return false;
   }

   setup.eligible = true;
   setup.status = "READY_F2_WAIST_LIMIT";
   setup.reason = "confirmed_f2_exact_f1_waist_stop_exact_f2_leg2_target";
   return true;
}

bool FP_NDSF2CanSend(const string symbol,
                     const int direction,
                     string &reason)
{
   if(!FP_NDSHookTradeCanSend(symbol, direction, reason)) return false;
   long order_mode = SymbolInfoInteger(symbol, SYMBOL_ORDER_MODE);
   if((order_mode & SYMBOL_ORDER_TP) == 0)
   {
      reason = "symbol_take_profit_not_supported";
      return false;
   }
   reason = "ok";
   return true;
}

bool FP_NDSF2SendLimit(const string symbol,
                       const FP_NDSF2WaistTradeConfig &cfg,
                       const FP_NDSF2WaistTradeSetup &setup,
                       ulong &ticket,
                       string &reason)
{
   ticket = 0;
   reason = "not_sent";
   if(cfg.magic <= 0)
   {
      reason = "magic_must_be_positive";
      return false;
   }
   if(!FP_NDSF2CanSend(symbol, setup.direction, reason)) return false;

   g_fp_nds_f2_waist_trade.SetAsyncMode(false);
   g_fp_nds_f2_waist_trade.SetExpertMagicNumber((ulong)cfg.magic);
   g_fp_nds_f2_waist_trade.SetDeviationInPoints((ulong)MathMax(0, cfg.max_deviation_points));
   g_fp_nds_f2_waist_trade.SetTypeFillingBySymbol(symbol);

   bool ok = false;
   if(setup.direction == FP_DIR_BULLISH)
      ok = g_fp_nds_f2_waist_trade.BuyLimit(setup.volume, setup.entry_price, symbol,
                                            setup.stop_price, setup.target_price,
                                            ORDER_TIME_GTC, 0, setup.broker_comment);
   else if(setup.direction == FP_DIR_BEARISH)
      ok = g_fp_nds_f2_waist_trade.SellLimit(setup.volume, setup.entry_price, symbol,
                                             setup.stop_price, setup.target_price,
                                             ORDER_TIME_GTC, 0, setup.broker_comment);

   uint retcode = g_fp_nds_f2_waist_trade.ResultRetcode();
   if(!ok || !FP_NDSHookTradeRetcodeAccepted(retcode))
   {
      reason = "send_failed_" + IntegerToString((int)retcode) + "_" +
               g_fp_nds_f2_waist_trade.ResultRetcodeDescription();
      return false;
   }

   ticket = g_fp_nds_f2_waist_trade.ResultOrder();
   if(ticket == 0)
   {
      reason = "limit_accepted_without_order_ticket";
      return false;
   }
   reason = "limit_with_exact_f1_waist_sl_and_f2_leg2_tp_accepted";
   return true;
}

#endif // __FP_NDS_F2_WAIST_TRADE_RULES_MQH__
