#ifndef __FP_NDS_F2_F3_EXIT_MANAGER_MQH__
#define __FP_NDS_F2_F3_EXIT_MANAGER_MQH__
#property strict

#include "FP_NDSF2WaistTradeTypes.mqh"
#include "FP_NDSHookTradeRules.mqh"

// Lightweight, tester-only dynamic-exit registry.
//
// Exit mode FP_NDS_F2_EXIT_F3_FLAG_RETEST keeps the original F2 Leg2 endpoint
// only as the reward/risk reference. No broker TP is attached initially.
// When the exact source F2 confirms, its confirmation node becomes F3 Leg1.
// After price corrects away from that node, the manager arms the position TP at
// the same node. The eventual retest is the executable "F3 flag hit" exit.
//
// The registry is in-memory by design: this dedicated expert is a fast Strategy
// Tester runtime, not a restart-persistent production executor.

FP_NDSF2DynamicExitContext g_fp_nds_f2_exit_contexts[];

void FP_NDSF2ResetDynamicExitContexts()
{
   ArrayResize(g_fp_nds_f2_exit_contexts, 0);
}

int FP_NDSF2FindDynamicContextBySetupHash(const long setup_hash)
{
   for(int i=0; i<ArraySize(g_fp_nds_f2_exit_contexts); i++)
      if(g_fp_nds_f2_exit_contexts[i].active &&
         g_fp_nds_f2_exit_contexts[i].setup_hash == setup_hash)
         return i;
   return -1;
}

int FP_NDSF2FindDynamicContextByOrderTicket(const ulong order_ticket)
{
   if(order_ticket == 0) return -1;
   for(int i=0; i<ArraySize(g_fp_nds_f2_exit_contexts); i++)
      if(g_fp_nds_f2_exit_contexts[i].active &&
         g_fp_nds_f2_exit_contexts[i].order_ticket == order_ticket)
         return i;
   return -1;
}

bool FP_NDSF2RegisterDynamicExitContext(const string symbol,
                                        const ENUM_TIMEFRAMES period,
                                        const FP_NDSF2WaistTradeConfig &cfg,
                                        const FP_NDSF2WaistTradeSetup &setup,
                                        const ulong order_ticket)
{
   if(cfg.exit_mode != FP_NDS_F2_EXIT_F3_FLAG_RETEST) return true;
   if(order_ticket == 0 || setup.setup_hash == 0) return false;

   int existing = FP_NDSF2FindDynamicContextBySetupHash(setup.setup_hash);
   if(existing >= 0)
   {
      g_fp_nds_f2_exit_contexts[existing].order_ticket = order_ticket;
      g_fp_nds_f2_exit_contexts[existing].stage = FP_NDS_F2_DYN_EXIT_PENDING;
      return true;
   }

   FP_NDSF2DynamicExitContext ctx;
   FP_ResetNDSF2DynamicExitContext(ctx);
   ctx.active = true;
   ctx.symbol = symbol;
   ctx.period = period;
   ctx.setup_hash = setup.setup_hash;
   ctx.broker_comment = setup.broker_comment;
   ctx.direction = setup.direction;
   ctx.scale_L = setup.scale_L;
   ctx.f1_waist_time = setup.f1_waist_time;
   ctx.f2_origin_time = setup.f2_origin_time;
   ctx.f2_waist_time = setup.f2_waist_time;
   ctx.initial_f2_leg2_time = setup.f2_leg2_time;
   ctx.initial_f2_leg2_price = setup.rr_reference_target_price;
   ctx.reference_target_price = setup.rr_reference_target_price;
   ctx.order_ticket = order_ticket;
   ctx.stage = FP_NDS_F2_DYN_EXIT_PENDING;

   int n = ArraySize(g_fp_nds_f2_exit_contexts);
   if(ArrayResize(g_fp_nds_f2_exit_contexts, n + 1) != n + 1) return false;
   g_fp_nds_f2_exit_contexts[n] = ctx;
   return true;
}

void FP_NDSF2DeactivateDynamicContextByOrderTicket(const ulong order_ticket)
{
   int index = FP_NDSF2FindDynamicContextByOrderTicket(order_ticket);
   if(index < 0) return;
   g_fp_nds_f2_exit_contexts[index].active = false;
   g_fp_nds_f2_exit_contexts[index].stage = FP_NDS_F2_DYN_EXIT_CLOSED;
}

int FP_NDSF2DirectionFromPositionType(const ENUM_POSITION_TYPE type)
{
   if(type == POSITION_TYPE_BUY) return FP_DIR_BULLISH;
   if(type == POSITION_TYPE_SELL) return FP_DIR_BEARISH;
   return FP_DIR_NONE;
}

bool FP_NDSF2FindPositionForDynamicContext(const FP_NDSF2WaistTradeConfig &cfg,
                                           FP_NDSF2DynamicExitContext &ctx)
{
   if(ctx.position_ticket > 0 && PositionSelectByTicket(ctx.position_ticket))
   {
      if((long)PositionGetInteger(POSITION_MAGIC) == cfg.magic &&
         PositionGetString(POSITION_SYMBOL) == ctx.symbol)
         return true;
   }
   ctx.position_ticket = 0;

   long position_identifier = ctx.position_identifier;
   if(position_identifier <= 0 && ctx.order_ticket > 0)
   {
      HistorySelect(0, TimeCurrent());
      if(HistoryOrderSelect(ctx.order_ticket))
         position_identifier = HistoryOrderGetInteger(ctx.order_ticket, ORDER_POSITION_ID);
   }
   if(position_identifier > 0) ctx.position_identifier = position_identifier;

   for(int i=PositionsTotal()-1; i>=0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket)) continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != cfg.magic) continue;
      if(PositionGetString(POSITION_SYMBOL) != ctx.symbol) continue;
      if(FP_NDSF2DirectionFromPositionType(
            (ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE)) != ctx.direction)
         continue;

      long identifier = PositionGetInteger(POSITION_IDENTIFIER);
      string comment = PositionGetString(POSITION_COMMENT);
      bool identifier_match = (position_identifier > 0 && identifier == position_identifier);
      bool comment_match = (ctx.broker_comment != "" && comment == ctx.broker_comment);
      if(!identifier_match && !comment_match) continue;

      ctx.position_ticket = ticket;
      ctx.position_identifier = identifier;
      return true;
   }
   return false;
}

bool FP_NDSF2DynamicReferenceTargetConsumedNow(const FP_NDSF2DynamicExitContext &ctx)
{
   MqlTick tick;
   if(!SymbolInfoTick(ctx.symbol, tick) || tick.bid <= 0.0 || tick.ask <= 0.0)
      return false;

   double trade_tick = FP_NDSHookTradeTickSize(ctx.symbol);
   double eps = (trade_tick > 0.0 ? trade_tick * 0.25 : 0.0);
   if(ctx.direction == FP_DIR_BULLISH)
      return (tick.bid >= ctx.reference_target_price - eps);
   if(ctx.direction == FP_DIR_BEARISH)
      return (tick.ask <= ctx.reference_target_price + eps);
   return false;
}

bool FP_NDSF2DeleteDynamicPending(const FP_NDSF2WaistTradeConfig &cfg,
                                  FP_NDSF2DynamicExitContext &ctx)
{
   if(ctx.order_ticket == 0 || !OrderSelect(ctx.order_ticket)) return false;
   if((long)OrderGetInteger(ORDER_MAGIC) != cfg.magic) return false;

   MqlTradeRequest request;
   MqlTradeResult result;
   ZeroMemory(request);
   ZeroMemory(result);
   request.action = TRADE_ACTION_REMOVE;
   request.order = ctx.order_ticket;
   request.symbol = ctx.symbol;
   request.magic = (ulong)cfg.magic;

   if(!OrderSend(request, result)) return false;
   if(!FP_NDSHookTradeRetcodeAccepted(result.retcode)) return false;

   ctx.active = false;
   ctx.stage = FP_NDS_F2_DYN_EXIT_CLOSED;
   return true;
}

bool FP_NDSF2DynamicContextF2Matches(const FP_NDSF2DynamicExitContext &ctx,
                                     const FP_FlagEvent &f2)
{
   if(f2.level != FP_LEVEL_F2) return false;
   if(f2.direction != ctx.direction || f2.scale_L != ctx.scale_L) return false;
   if(!f2.has_origin || !f2.has_waist || !f2.has_leg2 || !f2.has_confirm) return false;
   if(f2.status != FP_STATUS_CONFIRMED) return false;
   if(!f2.f2_can_spawn_f3) return false;
   if(f2.origin.time_anchor != ctx.f2_origin_time) return false;
   if(f2.waist.time_anchor != ctx.f2_waist_time) return false;
   if(f2.leg2.time_anchor < ctx.initial_f2_leg2_time) return false;
   if(f2.confirm.time_anchor <= f2.leg2.time_anchor) return false;
   return true;
}

double FP_NDSF2DynamicNormalizeNearest(const string symbol, const double price)
{
   double tick = FP_NDSHookTradeTickSize(symbol);
   int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   if(tick <= 0.0) return NormalizeDouble(price, digits);
   return NormalizeDouble(MathRound(price / tick) * tick, digits);
}

void FP_NDSF2UpdateDynamicExitFromEvents(const FP_NDSF2WaistTradeConfig &cfg,
                                         const FP_FlagEvent &events[],
                                         const int event_count)
{
   if(cfg.exit_mode != FP_NDS_F2_EXIT_F3_FLAG_RETEST) return;

   for(int c=0; c<ArraySize(g_fp_nds_f2_exit_contexts); c++)
   {
      if(!g_fp_nds_f2_exit_contexts[c].active) continue;
      if(g_fp_nds_f2_exit_contexts[c].f2_confirm_captured) continue;
      if(!FP_NDSF2FindPositionForDynamicContext(cfg, g_fp_nds_f2_exit_contexts[c]))
         continue;

      int best = -1;
      for(int i=0; i<event_count; i++)
      {
         if(!FP_NDSF2DynamicContextF2Matches(g_fp_nds_f2_exit_contexts[c], events[i]))
            continue;

         int parent_index = FP_CanonicalFindParentIndex(events, event_count, events[i]);
         if(parent_index < 0 || !events[parent_index].has_waist ||
            events[parent_index].waist.time_anchor !=
               g_fp_nds_f2_exit_contexts[c].f1_waist_time)
            continue;

         if(best < 0 ||
            events[i].leg2.time_anchor > events[best].leg2.time_anchor ||
            (events[i].leg2.time_anchor == events[best].leg2.time_anchor &&
             events[i].confirm.time_anchor < events[best].confirm.time_anchor))
            best = i;
      }
      if(best < 0) continue;

      g_fp_nds_f2_exit_contexts[c].f2_confirm_captured = true;
      g_fp_nds_f2_exit_contexts[c].f2_confirm_event_id = events[best].event_id;
      g_fp_nds_f2_exit_contexts[c].f2_confirm_node_id = events[best].confirm.id;
      g_fp_nds_f2_exit_contexts[c].f2_confirm_time = events[best].confirm.time_anchor;
      g_fp_nds_f2_exit_contexts[c].f2_confirm_price = events[best].confirm.price;
      g_fp_nds_f2_exit_contexts[c].dynamic_target_price =
         FP_NDSF2DynamicNormalizeNearest(g_fp_nds_f2_exit_contexts[c].symbol,
                                 events[best].confirm.price);
      g_fp_nds_f2_exit_contexts[c].stage = FP_NDS_F2_DYN_EXIT_WAIT_CORRECTION;
   }
}

bool FP_NDSF2DynamicCorrectionSeen(const FP_NDSF2WaistTradeConfig &cfg,
                                   const FP_NDSF2DynamicExitContext &ctx,
                                   const MqlTick &market)
{
   double trade_tick = FP_NDSHookTradeTickSize(ctx.symbol);
   if(trade_tick <= 0.0) return false;
   double distance = MathMax(1.0, cfg.f3_exit_correction_ticks) * trade_tick;
   if(ctx.direction == FP_DIR_BULLISH)
      return (market.bid <= ctx.dynamic_target_price - distance);
   if(ctx.direction == FP_DIR_BEARISH)
      return (market.ask >= ctx.dynamic_target_price + distance);
   return false;
}

bool FP_NDSF2DynamicTargetReached(const FP_NDSF2DynamicExitContext &ctx,
                                  const MqlTick &market)
{
   double trade_tick = FP_NDSHookTradeTickSize(ctx.symbol);
   double eps = (trade_tick > 0.0 ? trade_tick * 0.25 : 0.0);
   if(ctx.direction == FP_DIR_BULLISH)
      return (market.bid >= ctx.dynamic_target_price - eps);
   if(ctx.direction == FP_DIR_BEARISH)
      return (market.ask <= ctx.dynamic_target_price + eps);
   return false;
}

bool FP_NDSF2DynamicTPBrokerValid(const FP_NDSF2DynamicExitContext &ctx,
                                  const MqlTick &market)
{
   double point = SymbolInfoDouble(ctx.symbol, SYMBOL_POINT);
   int stops_level = MathMax(0, (int)SymbolInfoInteger(ctx.symbol, SYMBOL_TRADE_STOPS_LEVEL));
   double min_distance = stops_level * point;
   if(ctx.direction == FP_DIR_BULLISH)
      return (ctx.dynamic_target_price > market.bid + min_distance);
   if(ctx.direction == FP_DIR_BEARISH)
      return (ctx.dynamic_target_price < market.ask - min_distance);
   return false;
}

bool FP_NDSF2ArmDynamicPositionTP(const FP_NDSF2WaistTradeConfig &cfg,
                                  FP_NDSF2DynamicExitContext &ctx)
{
   if(ctx.position_ticket == 0 || !PositionSelectByTicket(ctx.position_ticket)) return false;

   double current_sl = PositionGetDouble(POSITION_SL);
   MqlTradeRequest request;
   MqlTradeResult result;
   ZeroMemory(request);
   ZeroMemory(result);
   request.action = TRADE_ACTION_SLTP;
   request.position = ctx.position_ticket;
   request.symbol = ctx.symbol;
   request.magic = (ulong)cfg.magic;
   request.sl = current_sl;
   request.tp = ctx.dynamic_target_price;

   if(!OrderSend(request, result)) return false;
   if(!FP_NDSHookTradeRetcodeAccepted(result.retcode)) return false;
   if(!PositionSelectByTicket(ctx.position_ticket)) return false;

   double actual_tp = PositionGetDouble(POSITION_TP);
   double trade_tick = FP_NDSHookTradeTickSize(ctx.symbol);
   double eps = MathMax(1e-12, trade_tick * 0.25);
   if(MathAbs(actual_tp - ctx.dynamic_target_price) > eps) return false;

   ctx.tp_armed = true;
   ctx.stage = FP_NDS_F2_DYN_EXIT_TP_ARMED;
   return true;
}

bool FP_NDSF2CloseDynamicPosition(const FP_NDSF2WaistTradeConfig &cfg,
                                  FP_NDSF2DynamicExitContext &ctx)
{
   if(ctx.position_ticket == 0 || !PositionSelectByTicket(ctx.position_ticket)) return false;

   g_fp_nds_hook_trade.SetAsyncMode(false);
   g_fp_nds_hook_trade.SetExpertMagicNumber((ulong)cfg.magic);
   g_fp_nds_hook_trade.SetDeviationInPoints((ulong)MathMax(0, cfg.max_deviation_points));
   g_fp_nds_hook_trade.SetTypeFillingBySymbol(ctx.symbol);
   bool ok = g_fp_nds_hook_trade.PositionClose(ctx.position_ticket,
                                               (ulong)MathMax(0, cfg.max_deviation_points));
   uint retcode = g_fp_nds_hook_trade.ResultRetcode();
   if(!ok || !FP_NDSHookTradeRetcodeAccepted(retcode)) return false;
   if(PositionSelectByTicket(ctx.position_ticket)) return false;

   ctx.active = false;
   ctx.stage = FP_NDS_F2_DYN_EXIT_CLOSED;
   return true;
}

void FP_NDSF2ManageOneDynamicContextOnTick(const FP_NDSF2WaistTradeConfig &cfg,
                                            const MqlTick &market,
                                            FP_NDSF2DynamicExitContext &ctx)
{
   bool order_active = (ctx.order_ticket > 0 && OrderSelect(ctx.order_ticket));
   bool position_active = FP_NDSF2FindPositionForDynamicContext(cfg, ctx);

   if(order_active && !position_active)
   {
      ctx.stage = FP_NDS_F2_DYN_EXIT_PENDING;
      if(cfg.cancel_pending_if_target_touched_before_fill &&
         FP_NDSF2DynamicReferenceTargetConsumedNow(ctx))
         FP_NDSF2DeleteDynamicPending(cfg, ctx);
      return;
   }

   if(position_active)
   {
      if(ctx.stage == FP_NDS_F2_DYN_EXIT_PENDING)
         ctx.stage = FP_NDS_F2_DYN_EXIT_WAIT_F2_CONFIRM;

      if(!ctx.f2_confirm_captured) return;

      if(!ctx.correction_seen && FP_NDSF2DynamicCorrectionSeen(cfg, ctx, market))
      {
         ctx.correction_seen = true;
         ctx.stage = FP_NDS_F2_DYN_EXIT_WAIT_RETEST;
      }
      if(!ctx.correction_seen || ctx.tp_armed) return;

      if(FP_NDSF2DynamicTargetReached(ctx, market))
      {
         if(cfg.close_at_market_if_f3_target_already_reached)
            FP_NDSF2CloseDynamicPosition(cfg, ctx);
         return;
      }

      if(FP_NDSF2DynamicTPBrokerValid(ctx, market))
         FP_NDSF2ArmDynamicPositionTP(cfg, ctx);
      return;
   }

   // A just-filled pending order may already have a position identifier while
   // the position list is not yet refreshed in this event. Keep the context for
   // the next tick instead of deactivating it prematurely.
   if(ctx.position_identifier > 0)
   {
      ctx.stage = FP_NDS_F2_DYN_EXIT_WAIT_F2_CONFIRM;
      return;
   }

   // Neither the original pending order nor its position is active.
   ctx.active = false;
   ctx.stage = FP_NDS_F2_DYN_EXIT_CLOSED;
}

void FP_NDSF2ManageDynamicExitOnTick(const string symbol,
                                     const ENUM_TIMEFRAMES period,
                                     const FP_NDSF2WaistTradeConfig &cfg)
{
   if(cfg.exit_mode != FP_NDS_F2_EXIT_F3_FLAG_RETEST) return;

   MqlTick market;
   if(!SymbolInfoTick(symbol, market) || market.bid <= 0.0 || market.ask <= 0.0)
      return;

   for(int i=0; i<ArraySize(g_fp_nds_f2_exit_contexts); i++)
   {
      if(!g_fp_nds_f2_exit_contexts[i].active) continue;
      if(g_fp_nds_f2_exit_contexts[i].symbol != symbol ||
         g_fp_nds_f2_exit_contexts[i].period != period)
         continue;
      FP_NDSF2ManageOneDynamicContextOnTick(cfg, market,
                                            g_fp_nds_f2_exit_contexts[i]);
   }
}

#endif // __FP_NDS_F2_F3_EXIT_MANAGER_MQH__
