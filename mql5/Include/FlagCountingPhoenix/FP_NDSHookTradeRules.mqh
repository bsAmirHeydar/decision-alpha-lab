#ifndef __FP_NDS_HOOK_TRADE_RULES_MQH__
#define __FP_NDS_HOOK_TRADE_RULES_MQH__
#property strict

#include <Trade/Trade.mqh>
#include "FP_NDSHookTradeTypes.mqh"
#include "FP_HookPhase02Rules.mqh"
#include "FP_NDSHook864CycleR1Rules.mqh"
#include "../Execution/DAL_ExecRisk.mqh"

CTrade g_fp_nds_hook_trade;

string FP_NDSHookTradeBool(const bool v){ return (v ? "true" : "false"); }

string FP_NDSHookTradeActionName(const FP_NDSHookTradeAction a)
{
   if(a == FP_NDS_HOOK_TRADE_ACTION_NONE) return "NONE";
   if(a == FP_NDS_HOOK_TRADE_ACTION_PAPER_LIMIT) return "PAPER_LIMIT";
   if(a == FP_NDS_HOOK_TRADE_ACTION_LIMIT_SENT) return "LIMIT_SENT";
   if(a == FP_NDS_HOOK_TRADE_ACTION_PENDING_HELD) return "PENDING_HELD";
   if(a == FP_NDS_HOOK_TRADE_ACTION_POSITION_HELD) return "POSITION_HELD";
   if(a == FP_NDS_HOOK_TRADE_ACTION_PENDING_CANCELLED) return "PENDING_CANCELLED";
   if(a == FP_NDS_HOOK_TRADE_ACTION_POSITION_CLOSED_F3) return "POSITION_CLOSED_F3";
   if(a == FP_NDS_HOOK_TRADE_ACTION_BLOCKED) return "BLOCKED";
   return "UNKNOWN";
}

string FP_NDSHookTradeDirectionName(const int d)
{
   if(d == FP_DIR_BULLISH) return "BUY";
   if(d == FP_DIR_BEARISH) return "SELL";
   return "NONE";
}

bool FP_NDSHookTradeProfileFromBrokerComment(const FP_NDSHookTradeConfig &cfg,
                                                const string comment,
                                                FP_NDSHookTradeProfile &profile,
                                                string &reason)
{
   profile = FP_NDS_HOOK_TRADE_PROFILE_TERMINAL_F123;
   reason = "unknown_profile_comment";

   string prefix = cfg.comment_prefix + "|";
   if(StringFind(comment, prefix) != 0)
   {
      reason = "comment_prefix_mismatch";
      return false;
   }

   // Phase 52 legacy comments were NDSH|S<sequence>|<family>. They remain
   // authoritative terminal/F123 ownership after restart. The optional TF3
   // token is accepted for forward compatibility with intermediate builds.
   if(StringFind(comment, prefix + "S") == 0 ||
      StringFind(comment, prefix + "TF3|") == 0)
   {
      profile = FP_NDS_HOOK_TRADE_PROFILE_TERMINAL_F123;
      reason = "terminal_f123_profile_comment";
      return true;
   }

   if(StringFind(comment, prefix + "864R1|") == 0)
   {
      profile = FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1;
      reason = "hook_864_cycle_r1_profile_comment";
      return true;
   }

   reason = "unrecognized_managed_profile_comment";
   return false;
}

string FP_NDSHookTradeFamily(const FP_HookPhase02Sequence &seq)
{
   if(seq.valid_after_hook && seq.valid_after_opposing_f3) return "F3H+HH";
   if(seq.valid_after_hook) return "HH";
   if(seq.valid_after_opposing_f3) return "F3H";
   return "NONE";
}

datetime FP_NDSHookTradeSequenceTime(const FP_HookPhase02Sequence &seq)
{
   if(seq.resolve_time > 0) return seq.resolve_time;
   if(seq.last_x_time > 0) return seq.last_x_time;
   return seq.origin_time;
}

bool FP_NDSHookTradeFamilyAllowed(const FP_HookPhase02Sequence &seq,
                                  const FP_NDSHookTradeConfig &cfg)
{
   bool hh = (seq.valid_after_hook && cfg.allow_hook_after_hook);
   bool f3h = (seq.valid_after_opposing_f3 && cfg.allow_hook_after_f3);
   return (hh || f3h);
}

bool FP_NDSHookTradeSequenceEligible(const FP_HookPhase02Sequence &seq,
                                     const FP_NDSHookTradeConfig &cfg)
{
   if(!seq.valid || seq.hook_failed || !seq.valid_hook_family)
      return false;
   if(!FP_NDSHookTradeFamilyAllowed(seq, cfg))
      return false;
   if(cfg.require_closed_hook && !FP_HookP02SequenceCycleClosed(seq))
      return false;
   if(seq.resolve_price <= 0.0 || seq.origin_price <= 0.0)
      return false;
   if(seq.direction != FP_HOOK_P02_DIRECTION_POSITIVE &&
      seq.direction != FP_HOOK_P02_DIRECTION_NEGATIVE)
      return false;

   if(cfg.profile == FP_NDS_HOOK_TRADE_PROFILE_TERMINAL_F123)
      return true;

   if(cfg.profile == FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1)
   {
      string profile_reason;
      return FP_NDSHook864CycleR1SequenceEligible(seq, cfg, profile_reason);
   }

   return false;
}

bool FP_NDSHookTradeSelectLatest(const string symbol,
                                 const ENUM_TIMEFRAMES period,
                                 const FP_HookPhase02Sequence &sequences[],
                                 const FP_NDSHookTradeConfig &cfg,
                                 FP_HookPhase02Sequence &selected)
{
   bool found = false;
   datetime best_time = 0;
   int best_id = -1;

   for(int i=0; i<ArraySize(sequences); i++)
   {
      bool eligible = false;
      if(cfg.profile == FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1)
      {
         FP_NDSHook864CycleR1Evidence evidence;
         string reason;
         eligible = FP_NDSHook864CycleR1RuntimeEligible(symbol, period,
                                                        sequences[i], cfg,
                                                        evidence, reason);
      }
      else
      {
         eligible = FP_NDSHookTradeSequenceEligible(sequences[i], cfg);
      }
      if(!eligible)
         continue;

      datetime t = FP_NDSHookTradeSequenceTime(sequences[i]);
      if(!found || t > best_time || (t == best_time && sequences[i].sequence_id > best_id))
      {
         selected = sequences[i];
         best_time = t;
         best_id = sequences[i].sequence_id;
         found = true;
      }
   }

   return found;
}

long FP_NDSHookTradeHash(const string value)
{
   long h = 5381;
   int n = StringLen(value);
   for(int i=0; i<n; i++)
   {
      int c = StringGetCharacter(value, i);
      h = (h * 33 + c) % 2147483629;
   }
   if(h < 0) h = -h;
   return h;
}

string FP_NDSHookTradeUsedPrefix(const FP_NDSHookTradeConfig &cfg)
{
   return "DAL_NDS_USED_" + IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN)) +
          "_" + IntegerToString(cfg.magic) + "_";
}

string FP_NDSHookTradeUsedName(const FP_NDSHookTradeConfig &cfg,
                               const string setup_key)
{
   return FP_NDSHookTradeUsedPrefix(cfg) + IntegerToString(FP_NDSHookTradeHash(setup_key));
}

bool FP_NDSHookTradeSetupUsed(const FP_NDSHookTradeConfig &cfg,
                              const string setup_key)
{
   if(!cfg.one_attempt_per_hook)
      return false;
   return GlobalVariableCheck(FP_NDSHookTradeUsedName(cfg, setup_key));
}

bool FP_NDSHookTradeMarkSetupUsed(const FP_NDSHookTradeConfig &cfg,
                                  const string setup_key)
{
   if(!cfg.one_attempt_per_hook)
      return true;
   if(setup_key == "")
      return false;
   if(GlobalVariableSet(FP_NDSHookTradeUsedName(cfg, setup_key),
                        (double)TimeCurrent()) == 0)
      return false;
   GlobalVariablesFlush();
   return true;
}

int FP_NDSHookTradeResetUsedSetups(const FP_NDSHookTradeConfig &cfg)
{
   return GlobalVariablesDeleteAll(FP_NDSHookTradeUsedPrefix(cfg));
}

double FP_NDSHookTradeTickSize(const string symbol)
{
   double tick = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE);
   if(tick <= 0.0) tick = SymbolInfoDouble(symbol, SYMBOL_POINT);
   return tick;
}

double FP_NDSHookTradeNormalizePrice(const string symbol,
                                     const double price,
                                     const bool round_up)
{
   double tick = FP_NDSHookTradeTickSize(symbol);
   int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   if(tick <= 0.0)
      return NormalizeDouble(price, digits);
   double units = price / tick;
   double rounded = (round_up ? MathCeil(units - 1e-10) : MathFloor(units + 1e-10));
   return NormalizeDouble(rounded * tick, digits);
}

double FP_NDSHookTradeNormalizeFixedVolume(const string symbol,
                                           const double requested)
{
   if(requested <= 0.0)
      return 0.0;

   double vmin = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN);
   double vmax = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX);
   double step = SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP);
   if(vmin <= 0.0 || vmax <= 0.0 || step <= 0.0)
      return 0.0;

   double v = MathMax(vmin, MathMin(vmax, requested));
   v = MathFloor(v / step + 1e-10) * step;
   if(v < vmin) v = vmin;
   return NormalizeDouble(v, DAL_ExecVolumeDigitsFromStep(step));
}

bool FP_NDSHookTradeComputeVolume(const string symbol,
                                  const FP_NDSHookTradeConfig &cfg,
                                  const double entry,
                                  const double stop,
                                  double &volume,
                                  string &reason)
{
   volume = 0.0;
   reason = "not_calculated";

   if(cfg.sizing_mode == FP_NDS_HOOK_TRADE_SIZE_FIXED_VOLUME)
   {
      volume = FP_NDSHookTradeNormalizeFixedVolume(symbol, cfg.fixed_volume);
      if(volume <= 0.0)
      {
         reason = "fixed_volume_invalid_for_symbol";
         return false;
      }
      reason = "fixed_volume_ok";
      return true;
   }

   DALExecRiskSizing risk;
   if(!DAL_ExecCalculateRiskVolume(symbol,
                                   entry,
                                   stop,
                                   cfg.risk_cash,
                                   cfg.commission_per_lot_round_turn,
                                   cfg.allow_min_lot_if_risk_too_small,
                                   risk))
   {
      reason = "risk_sizing_" + risk.reason;
      return false;
   }

   volume = risk.volume;
   reason = "risk_cash_ok";
   return true;
}

string FP_NDSHookTradeBuildSetupKey(const string symbol,
                                    const ENUM_TIMEFRAMES period,
                                    const FP_HookPhase02Sequence &seq,
                                    const FP_NDSHookTradeConfig &cfg)
{
   string key = symbol;
   key += "|TF=" + EnumToString(period);
   key += "|SEQ=" + IntegerToString(seq.sequence_id);
   key += "|DIR=" + IntegerToString((int)seq.direction);
   key += "|O=" + IntegerToString((long)seq.origin_time);
   key += "|F=" + FP_NDSHookTradeFamily(seq);
   key += "|P=" + FP_NDSHookTradeProfileCode(cfg.profile);
   if(cfg.profile == FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1)
   {
      // Stable one-attempt identity belongs to the Hook sequence, not to the
      // current x3/x4 terminal. A later x4 extension must not create or reprice
      // a second order for the same Hook.
      key += "|R=" + DoubleToString(cfg.hook_entry_ratio, 6);
   }
   else
   {
      // Preserve the Phase 52 terminal-entry identity exactly.
      key += "|T=" + IntegerToString((long)seq.resolve_time);
   }
   return key;
}

string FP_NDSHookTradeBuildComment(const FP_NDSHookTradeConfig &cfg,
                                   const FP_HookPhase02Sequence &seq)
{
   string code = FP_NDSHookTradeFamily(seq);
   string comment;
   if(cfg.profile == FP_NDS_HOOK_TRADE_PROFILE_TERMINAL_F123)
   {
      // Preserve the exact Phase 52 broker-comment shape for compatibility
      // with existing pending orders, positions, exports and recovery tooling.
      comment = cfg.comment_prefix + "|S" + IntegerToString(seq.sequence_id) + "|" + code;
   }
   else
   {
      comment = cfg.comment_prefix + "|" + FP_NDSHookTradeProfileCode(cfg.profile) +
                "|S" + IntegerToString(seq.sequence_id) + "|" + code;
   }
   if(StringLen(comment) > 31)
      comment = StringSubstr(comment, 0, 31);
   return comment;
}

bool FP_NDSHookTradeBuildSetup(const string symbol,
                               const ENUM_TIMEFRAMES period,
                               const FP_HookPhase02Sequence &seq,
                               const FP_NDSHookTradeConfig &cfg,
                               FP_NDSHookTradeSetup &setup)
{
   FP_ResetNDSHookTradeSetup(setup);
   setup.available = true;
   setup.sequence_id = seq.sequence_id;
   setup.direction = (seq.direction == FP_HOOK_P02_DIRECTION_POSITIVE ? FP_DIR_BULLISH : FP_DIR_BEARISH);
   setup.direction_label = FP_NDSHookTradeDirectionName(setup.direction);
   setup.family = FP_NDSHookTradeFamily(seq);
   setup.profile_label = FP_NDSHookTradeProfileName(cfg.profile);
   setup.valid_after_hook = seq.valid_after_hook;
   setup.valid_after_f3 = seq.valid_after_opposing_f3;
   setup.structure_time = FP_NDSHookTradeSequenceTime(seq);
   setup.x_count = seq.x_count;
   setup.origin_price = seq.origin_price;
   setup.crown_price = seq.cycle_crown_price;
   setup.terminal_price = seq.resolve_price;
   setup.terminal_retracement_ratio = seq.retracement_ratio;
   setup.entry_ratio = (cfg.profile == FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1 ?
                        cfg.hook_entry_ratio : 0.0);
   setup.entry_level_untouched = (cfg.profile == FP_NDS_HOOK_TRADE_PROFILE_TERMINAL_F123);
   setup.setup_key = FP_NDSHookTradeBuildSetupKey(symbol, period, seq, cfg);
   setup.broker_comment = FP_NDSHookTradeBuildComment(cfg, seq);
   setup.already_used = FP_NDSHookTradeSetupUsed(cfg, setup.setup_key);

   if(cfg.profile != FP_NDS_HOOK_TRADE_PROFILE_TERMINAL_F123 &&
      cfg.profile != FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1)
   {
      setup.status = "BLOCKED_PROFILE";
      setup.reason = "unknown_hook_trade_profile";
      return false;
   }

   if(cfg.profile == FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1)
   {
      FP_NDSHook864CycleR1Evidence evidence;
      string profile_reason;
      if(!FP_NDSHook864CycleR1RuntimeEligible(symbol, period, seq, cfg,
                                               evidence, profile_reason))
      {
         setup.status = "BLOCKED_HOOK_864_PROFILE";
         setup.reason = profile_reason;
         return false;
      }
      setup.phase04_evidence_found = true;
      setup.phase04_x_closed = evidence.x_closed;
      setup.x_closure_time = evidence.x_closure_time;
      setup.x_closure_price = evidence.x_closure_price;
      setup.x_closure_threshold_price = evidence.x_closure_threshold_price;
      setup.cycle_dead_after_terminal = evidence.origin_return_penetrated;
      setup.first_864_touch_found = evidence.level_touched_after_closure;
      setup.first_864_touch_time = evidence.first_touch_time;
      setup.first_864_touch_price = evidence.first_touch_price;
      setup.entry_level_untouched = !evidence.level_touched_after_closure;
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

   double raw_entry = seq.resolve_price;
   if(cfg.profile == FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1)
      raw_entry = FP_NDSHook864CycleR1RawEntry(seq, cfg.hook_entry_ratio);

   double death = (seq.death_boundary_price > 0.0 ? seq.death_boundary_price : seq.origin_price);
   double spread = MathMax(0.0, ask - bid);
   double buffer = MathMax(0, cfg.stop_buffer_points) * point +
                   MathMax(0.0, cfg.stop_spread_multiplier) * spread;
   int stops_level = MathMax(0, (int)SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL));
   int freeze_level = MathMax(0, (int)SymbolInfoInteger(symbol, SYMBOL_TRADE_FREEZE_LEVEL));
   double stop_min_dist = stops_level * point;
   double entry_min_dist = MathMax(stops_level, freeze_level) * point;

   if(setup.direction == FP_DIR_BULLISH)
   {
      setup.entry_price = FP_NDSHookTradeNormalizePrice(symbol, raw_entry, false);
      setup.death_price = FP_NDSHookTradeNormalizePrice(symbol, death, false);
      setup.stop_price = FP_NDSHookTradeNormalizePrice(symbol, death - buffer, false);
      if(setup.entry_price - setup.stop_price < stop_min_dist)
         setup.stop_price = FP_NDSHookTradeNormalizePrice(symbol, setup.entry_price - stop_min_dist, false);

      if(!(setup.death_price < setup.entry_price))
      {
         setup.status = "BLOCKED_HOOK_GEOMETRY";
         setup.reason = "bullish_death_must_be_below_limit_entry";
         return false;
      }
      if(!(setup.entry_price < ask - entry_min_dist))
      {
         setup.status = "BLOCKED_LIMIT_GEOMETRY";
         setup.reason = "buy_limit_entry_not_below_current_ask";
         return false;
      }
   }
   else if(setup.direction == FP_DIR_BEARISH)
   {
      setup.entry_price = FP_NDSHookTradeNormalizePrice(symbol, raw_entry, true);
      setup.death_price = FP_NDSHookTradeNormalizePrice(symbol, death, true);
      setup.stop_price = FP_NDSHookTradeNormalizePrice(symbol, death + buffer, true);
      if(setup.stop_price - setup.entry_price < stop_min_dist)
         setup.stop_price = FP_NDSHookTradeNormalizePrice(symbol, setup.entry_price + stop_min_dist, true);

      if(!(setup.death_price > setup.entry_price))
      {
         setup.status = "BLOCKED_HOOK_GEOMETRY";
         setup.reason = "bearish_death_must_be_above_limit_entry";
         return false;
      }
      if(!(setup.entry_price > bid + entry_min_dist))
      {
         setup.status = "BLOCKED_LIMIT_GEOMETRY";
         setup.reason = "sell_limit_entry_not_above_current_bid";
         return false;
      }
   }
   else
   {
      setup.status = "BLOCKED_DIRECTION";
      setup.reason = "hook_direction_none";
      return false;
   }

   setup.risk_distance = MathAbs(setup.entry_price - setup.stop_price);
   if(setup.risk_distance <= 0.0)
   {
      setup.status = "BLOCKED_RISK_GEOMETRY";
      setup.reason = "entry_stop_distance_not_positive";
      return false;
   }

   if(cfg.profile == FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1)
   {
      setup.reward_r = cfg.fixed_reward_r;
      double raw_target = (setup.direction == FP_DIR_BULLISH ?
                           setup.entry_price + setup.risk_distance * setup.reward_r :
                           setup.entry_price - setup.risk_distance * setup.reward_r);
      setup.target_price = FP_NDSHookTradeNormalizePrice(symbol, raw_target,
                                                         setup.direction == FP_DIR_BULLISH);
      setup.reward_distance = MathAbs(setup.target_price - setup.entry_price);

      if(setup.direction == FP_DIR_BULLISH && !(setup.stop_price < setup.entry_price &&
                                                setup.entry_price < setup.target_price))
      {
         setup.status = "BLOCKED_FIXED_R_GEOMETRY";
         setup.reason = "bullish_stop_entry_target_order_invalid";
         return false;
      }
      if(setup.direction == FP_DIR_BEARISH && !(setup.target_price < setup.entry_price &&
                                                setup.entry_price < setup.stop_price))
      {
         setup.status = "BLOCKED_FIXED_R_GEOMETRY";
         setup.reason = "bearish_target_entry_stop_order_invalid";
         return false;
      }
      if(setup.reward_distance + point * 0.1 < setup.risk_distance * cfg.fixed_reward_r)
      {
         setup.status = "BLOCKED_FIXED_R_GEOMETRY";
         setup.reason = "normalized_target_below_requested_reward_r";
         return false;
      }
   }

   if(setup.already_used)
   {
      setup.status = "BLOCKED_ALREADY_USED";
      setup.reason = "one_attempt_per_hook_registry";
      return false;
   }

   string volume_reason;
   if(!FP_NDSHookTradeComputeVolume(symbol, cfg, setup.entry_price, setup.stop_price,
                                    setup.volume, volume_reason))
   {
      setup.status = "BLOCKED_VOLUME";
      setup.reason = volume_reason;
      return false;
   }

   setup.eligible = true;
   setup.status = (cfg.profile == FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1 ?
                   "READY_LIMIT_AT_HOOK_864_CYCLE_R1" :
                   "READY_LIMIT_AT_HOOK_TERMINAL");
   setup.reason = "none";
   return true;
}

int FP_NDSHookTradeCountManagedOrders(const FP_NDSHookTradeConfig &cfg,
                                      ulong &first_ticket)
{
   first_ticket = 0;
   int count = 0;
   for(int i=OrdersTotal()-1; i>=0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0) continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != cfg.magic) continue;
      count++;
      if(first_ticket == 0) first_ticket = ticket;
   }
   return count;
}

int FP_NDSHookTradeCountManagedPositions(const FP_NDSHookTradeConfig &cfg,
                                         ulong &first_ticket)
{
   first_ticket = 0;
   int count = 0;
   for(int i=PositionsTotal()-1; i>=0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket)) continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != cfg.magic) continue;
      count++;
      if(first_ticket == 0) first_ticket = ticket;
   }
   return count;
}

int FP_NDSHookTradeCountForeignPositionsOnSymbol(const string symbol,
                                                 const FP_NDSHookTradeConfig &cfg)
{
   int count = 0;
   for(int i=PositionsTotal()-1; i>=0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket)) continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol) continue;
      long magic = (long)PositionGetInteger(POSITION_MAGIC);
      if(magic == cfg.magic) continue;
      count++;
   }
   return count;
}

bool FP_NDSHookTradeRetcodeAccepted(const uint retcode)
{
   return (retcode == TRADE_RETCODE_DONE ||
           retcode == TRADE_RETCODE_PLACED ||
           retcode == TRADE_RETCODE_DONE_PARTIAL);
}

bool FP_NDSHookTradeCanSend(const string symbol,
                                const int direction,
                                const bool require_take_profit,
                                string &reason)
{
   if(symbol == "")
   {
      reason = "empty_symbol";
      return false;
   }
   if(direction != FP_DIR_BULLISH && direction != FP_DIR_BEARISH)
   {
      reason = "invalid_trade_direction";
      return false;
   }
   if(!TerminalInfoInteger(TERMINAL_TRADE_ALLOWED))
   {
      reason = "terminal_trade_not_allowed";
      return false;
   }
   if(!MQLInfoInteger(MQL_TRADE_ALLOWED))
   {
      reason = "mql_trade_not_allowed";
      return false;
   }
   if(!AccountInfoInteger(ACCOUNT_TRADE_ALLOWED))
   {
      reason = "account_trade_not_allowed";
      return false;
   }
   ENUM_SYMBOL_TRADE_MODE mode = (ENUM_SYMBOL_TRADE_MODE)SymbolInfoInteger(symbol, SYMBOL_TRADE_MODE);
   if(mode == SYMBOL_TRADE_MODE_DISABLED || mode == SYMBOL_TRADE_MODE_CLOSEONLY)
   {
      reason = "symbol_trade_mode_blocks_new_orders";
      return false;
   }
   if(direction == FP_DIR_BULLISH && mode == SYMBOL_TRADE_MODE_SHORTONLY)
   {
      reason = "symbol_short_only_blocks_buy_limit";
      return false;
   }
   if(direction == FP_DIR_BEARISH && mode == SYMBOL_TRADE_MODE_LONGONLY)
   {
      reason = "symbol_long_only_blocks_sell_limit";
      return false;
   }

   long order_mode = SymbolInfoInteger(symbol, SYMBOL_ORDER_MODE);
   if((order_mode & SYMBOL_ORDER_LIMIT) == 0)
   {
      reason = "symbol_limit_orders_not_supported";
      return false;
   }
   if((order_mode & SYMBOL_ORDER_SL) == 0)
   {
      reason = "symbol_stop_loss_not_supported";
      return false;
   }
   if(require_take_profit && (order_mode & SYMBOL_ORDER_TP) == 0)
   {
      reason = "symbol_take_profit_not_supported";
      return false;
   }

   reason = "ok";
   return true;
}

bool FP_NDSHookTradeSendLimit(const string symbol,
                              const FP_NDSHookTradeConfig &cfg,
                              const FP_NDSHookTradeSetup &setup,
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

   string trade_reason;
   bool require_take_profit = (setup.target_price > 0.0);
   if(!FP_NDSHookTradeCanSend(symbol, setup.direction, require_take_profit, trade_reason))
   {
      reason = trade_reason;
      return false;
   }

   g_fp_nds_hook_trade.SetAsyncMode(false);
   g_fp_nds_hook_trade.SetExpertMagicNumber((ulong)cfg.magic);
   g_fp_nds_hook_trade.SetDeviationInPoints((ulong)MathMax(0, cfg.max_deviation_points));
   g_fp_nds_hook_trade.SetTypeFillingBySymbol(symbol);

   bool ok = false;
   if(setup.direction == FP_DIR_BULLISH)
      ok = g_fp_nds_hook_trade.BuyLimit(setup.volume, setup.entry_price, symbol,
                                       setup.stop_price, setup.target_price,
                                       ORDER_TIME_GTC, 0, setup.broker_comment);
   else if(setup.direction == FP_DIR_BEARISH)
      ok = g_fp_nds_hook_trade.SellLimit(setup.volume, setup.entry_price, symbol,
                                        setup.stop_price, setup.target_price,
                                        ORDER_TIME_GTC, 0, setup.broker_comment);

   uint retcode = g_fp_nds_hook_trade.ResultRetcode();
   if(!ok || !FP_NDSHookTradeRetcodeAccepted(retcode))
   {
      reason = "send_failed_" + IntegerToString((int)retcode) + "_" +
               g_fp_nds_hook_trade.ResultRetcodeDescription();
      return false;
   }

   ticket = g_fp_nds_hook_trade.ResultOrder();
   if(ticket == 0)
   {
      reason = "limit_accepted_without_order_ticket";
      return false;
   }
   reason = "limit_accepted";
   return true;
}

datetime FP_NDSHookTradeF3TerminalTime(const FP_FlagEvent &e)
{
   datetime t = 0;
   if(e.has_leg2) t = e.leg2.time_anchor;
   if(e.has_extension && e.extension_end.time_anchor > t) t = e.extension_end.time_anchor;
   if(e.has_confirm && e.confirm.time_anchor > t) t = e.confirm.time_anchor;
   return t;
}

double FP_NDSHookTradeF3TerminalPrice(const FP_FlagEvent &e)
{
   if(e.has_extension) return e.extension_end.price;
   if(e.has_leg2) return e.leg2.price;
   return 0.0;
}

bool FP_NDSHookTradeFindF123Evidence(const FP_FlagEvent &events[],
                                         const int event_count,
                                         const int sequence_id,
                                         const int direction,
                                         const datetime f3_completion_time,
                                         datetime &f1_start,
                                         datetime &f2_start)
{
   f1_start = 0;
   f2_start = 0;
   int n = MathMin(event_count, ArraySize(events));

   for(int i=0; i<n; i++)
   {
      if(events[i].sequence_id != sequence_id) continue;
      if(events[i].direction != direction) continue;
      if(!events[i].visible_main) continue;
      if(events[i].status == FP_STATUS_INVALIDATED) continue;
      if(!events[i].has_origin) continue;

      datetime t = events[i].origin.time_anchor;
      if(t <= 0 || t > f3_completion_time) continue;

      if(events[i].level == FP_LEVEL_F1)
      {
         if(!events[i].lifecycle_can_spawn_f2) continue;
         if(f1_start == 0 || t < f1_start) f1_start = t;
      }
      else if(events[i].level == FP_LEVEL_F2)
      {
         if(!events[i].f2_parent_ready || !events[i].f2_can_spawn_f3) continue;
         if(f2_start == 0 || t < f2_start) f2_start = t;
      }
   }

   if(f1_start <= 0 || f2_start <= 0) return false;
   if(f1_start > f2_start || f2_start > f3_completion_time) return false;
   return true;
}

bool FP_NDSHookTradeFindExitF3(const FP_FlagEvent &events[],
                               const int event_count,
                               const int position_direction,
                               const datetime position_open_time,
                               const FP_NDSHookTradeConfig &cfg,
                               FP_NDSHookTradeExitSignal &signal)
{
   FP_ResetNDSHookTradeExitSignal(signal);
   int n = MathMin(event_count, ArraySize(events));
   datetime best_terminal = 0;

   for(int i=0; i<n; i++)
   {
      FP_FlagEvent e = events[i];
      if(e.level != FP_LEVEL_F3) continue;
      if(e.direction != position_direction) continue;
      if(!e.visible_main) continue;
      if(!e.f3_terminal_complete) continue;
      if(e.status != FP_STATUS_COMPLETED && e.status != FP_STATUS_LOCKED) continue;

      datetime terminal_time = FP_NDSHookTradeF3TerminalTime(e);
      if(terminal_time <= position_open_time) continue;

      datetime f1_start = 0;
      datetime f2_start = 0;
      if(!FP_NDSHookTradeFindF123Evidence(events, n, e.sequence_id, e.direction,
                                          terminal_time, f1_start, f2_start))
         continue;
      if(cfg.require_full_f123_after_entry &&
         (f1_start <= position_open_time || f2_start <= position_open_time))
         continue;

      if(!signal.found || terminal_time < best_terminal)
      {
         signal.found = true;
         signal.event_id = e.event_id;
         signal.sequence_id = e.sequence_id;
         signal.direction = e.direction;
         signal.f1_start_time = f1_start;
         signal.f2_start_time = f2_start;
         signal.f3_terminal_time = terminal_time;
         signal.f3_terminal_price = FP_NDSHookTradeF3TerminalPrice(e);
         signal.reason = "completed_same_direction_f123_after_entry";
         best_terminal = terminal_time;
      }
   }

   return signal.found;
}

bool FP_NDSHookTradeClosePositionOnF3(const ulong position_ticket,
                                      const FP_NDSHookTradeConfig &cfg,
                                      string &reason)
{
   reason = "not_closed";
   if(position_ticket == 0 || !PositionSelectByTicket(position_ticket))
   {
      reason = "position_ticket_not_found";
      return false;
   }

   g_fp_nds_hook_trade.SetAsyncMode(false);
   g_fp_nds_hook_trade.SetExpertMagicNumber((ulong)cfg.magic);
   g_fp_nds_hook_trade.SetDeviationInPoints((ulong)MathMax(0, cfg.max_deviation_points));
   bool ok = g_fp_nds_hook_trade.PositionClose(position_ticket,
                                               (ulong)MathMax(0, cfg.max_deviation_points));
   uint retcode = g_fp_nds_hook_trade.ResultRetcode();
   if(!ok || !FP_NDSHookTradeRetcodeAccepted(retcode))
   {
      reason = "close_failed_" + IntegerToString((int)retcode) + "_" +
               g_fp_nds_hook_trade.ResultRetcodeDescription();
      return false;
   }

   if(PositionSelectByTicket(position_ticket))
   {
      reason = "close_request_accepted_but_position_still_open";
      return false;
   }

   reason = "closed_on_same_direction_f3";
   return true;
}

int FP_NDSHookTradeDeleteAllManagedPending(const FP_NDSHookTradeConfig &cfg,
                                           string &last_reason)
{
   int deleted = 0;
   last_reason = "none";
   g_fp_nds_hook_trade.SetAsyncMode(false);
   g_fp_nds_hook_trade.SetExpertMagicNumber((ulong)cfg.magic);

   for(int i=OrdersTotal()-1; i>=0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0) continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != cfg.magic) continue;

      if(g_fp_nds_hook_trade.OrderDelete(ticket))
      {
         deleted++;
         last_reason = "managed_pending_deleted";
      }
      else
      {
         last_reason = "delete_failed_" + IntegerToString((int)g_fp_nds_hook_trade.ResultRetcode());
      }
   }
   return deleted;
}

int FP_NDSHookTradeCancelDeadPending(const string symbol,
                                     const FP_NDSHookTradeConfig &cfg,
                                     string &last_reason)
{
   last_reason = "none";
   if(!cfg.cancel_pending_on_death)
      return 0;

   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   if(bid <= 0.0 || ask <= 0.0)
   {
      last_reason = "invalid_quotes";
      return 0;
   }

   int deleted = 0;
   g_fp_nds_hook_trade.SetAsyncMode(false);
   g_fp_nds_hook_trade.SetExpertMagicNumber((ulong)cfg.magic);

   for(int i=OrdersTotal()-1; i>=0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0) continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != cfg.magic) continue;
      if(OrderGetString(ORDER_SYMBOL) != symbol) continue;

      ENUM_ORDER_TYPE type = (ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE);
      double sl = OrderGetDouble(ORDER_SL);
      bool dead = false;
      if(type == ORDER_TYPE_BUY_LIMIT && sl > 0.0 && bid <= sl) dead = true;
      if(type == ORDER_TYPE_SELL_LIMIT && sl > 0.0 && ask >= sl) dead = true;
      if(!dead) continue;

      if(g_fp_nds_hook_trade.OrderDelete(ticket))
      {
         deleted++;
         last_reason = "pending_cancelled_after_death_boundary";
      }
      else
      {
         last_reason = "death_cancel_failed_" + IntegerToString((int)g_fp_nds_hook_trade.ResultRetcode());
      }
   }

   return deleted;
}

string FP_NDSHookTradeEntryLockName(const FP_NDSHookTradeConfig &cfg)
{
   return "DAL_NDS_ENTRY_LOCK_" + IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN)) +
          "_" + IntegerToString(cfg.magic);
}

bool FP_NDSHookTradeAcquireEntryLock(const FP_NDSHookTradeConfig &cfg,
                                     double &token,
                                     string &reason)
{
   token = (double)GetTickCount64() + 1.0;
   string name = FP_NDSHookTradeEntryLockName(cfg);
   if(!GlobalVariableCheck(name) && !GlobalVariableTemp(name))
   {
      reason = "entry_lock_create_failed_" + IntegerToString(GetLastError());
      return false;
   }

   double observed = 0.0;
   if(!GlobalVariableGet(name, observed))
   {
      reason = "entry_lock_read_failed_" + IntegerToString(GetLastError());
      return false;
   }
   double timeout_ms = (double)MathMax(1, cfg.entry_lock_timeout_seconds) * 1000.0;
   if(observed > 0.0 && token >= observed && token - observed <= timeout_ms)
   {
      reason = "entry_lock_busy";
      return false;
   }

   if(!GlobalVariableSetOnCondition(name, token, observed))
   {
      reason = "entry_lock_race_lost";
      return false;
   }

   reason = "entry_lock_acquired";
   return true;
}

void FP_NDSHookTradeReleaseEntryLock(const FP_NDSHookTradeConfig &cfg,
                                     const double token)
{
   if(token <= 0.0) return;
   string name = FP_NDSHookTradeEntryLockName(cfg);
   if(!GlobalVariableCheck(name)) return;
   GlobalVariableSetOnCondition(name, 0.0, token);
}

int FP_NDSHookTradeReconcileDuplicatePending(const FP_NDSHookTradeConfig &cfg,
                                             ulong &kept_ticket,
                                             string &reason)
{
   kept_ticket = 0;
   datetime kept_time = 0;
   int managed = 0;

   for(int i=OrdersTotal()-1; i>=0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0) continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != cfg.magic) continue;
      managed++;
      datetime setup_time = (datetime)OrderGetInteger(ORDER_TIME_SETUP);
      if(kept_ticket == 0 || setup_time < kept_time ||
         (setup_time == kept_time && ticket < kept_ticket))
      {
         kept_ticket = ticket;
         kept_time = setup_time;
      }
   }

   if(managed <= 1)
   {
      reason = (managed == 1 ? "single_pending_invariant_ok" : "no_pending");
      return 0;
   }

   g_fp_nds_hook_trade.SetAsyncMode(false);
   g_fp_nds_hook_trade.SetExpertMagicNumber((ulong)cfg.magic);
   int deleted = 0;
   for(int i=OrdersTotal()-1; i>=0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0 || ticket == kept_ticket) continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != cfg.magic) continue;
      if(g_fp_nds_hook_trade.OrderDelete(ticket))
         deleted++;
   }

   reason = "duplicate_pending_reconciled_keep_oldest";
   return deleted;
}

void FP_NDSHookTradeFinalizeReport(FP_NDSHookTradeReport &report)
{
   report.action_label = FP_NDSHookTradeActionName(report.action);
   report.state_key = report.symbol;
   report.state_key += "|TF=" + EnumToString(report.period);
   report.state_key += "|ACTION=" + report.action_label;
   report.state_key += "|STATUS=" + report.status;
   report.state_key += "|PEND=" + IntegerToString(report.managed_pending_count);
   report.state_key += "|POS=" + IntegerToString(report.managed_position_count);
   report.state_key += "|SETUP=" + report.setup.setup_key;
}

#endif // __FP_NDS_HOOK_TRADE_RULES_MQH__
