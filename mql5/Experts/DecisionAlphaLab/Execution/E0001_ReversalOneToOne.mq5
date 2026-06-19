//+------------------------------------------------------------------+
//| Decision Alpha Lab — E0001 H0005 Reversal R1 Executor             |
//| Execution layer: exact H5 reversal R1, six-slot pending grid + touch ledger|
//+------------------------------------------------------------------+
#property strict
#property version   "1.08"
#property description "Execution module for H0005 reversal R1: maintains 3 buy-limit and 3 sell-limit candidates with per-touch one-fill memory."

#include <Trade/Trade.mqh>
#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>
#include <DecisionAlphaLab/M0002/DAL_M0002Engine.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecRisk.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecOrders.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecReversalOneToOne.mqh>

input string InpSymbol = "";
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpBars = 1500;

// Structural research inputs reused from M0001/M0002.
input int InpL = 5;
input double InpZoneRatio = 0.90;
input int InpExitGap = 6;
input ENUM_DALM0001ConsumeMode InpConsumeMode = DAL_M0001_CONSUME_BY_HUNT;
input int InpOutcomeCandleOffsetAfterExit = 0;
input int InpBrokerUtcOffsetHours = 0;
input int InpRegimeLookbackBars = 100;

// Execution policy.
input bool InpTradingEnabled = false;
input long InpMagicNumber = 5001001;
input double InpRiskCash = 100.0;
input double InpCommissionPerLotRoundTurn = 0.0;
input double InpRewardR = 1.0; // H0005 REVERSAL_TRADE_R1 default.
input int InpMaxSimultaneousTrades = -1; // -1 = no global cap; needed for simultaneous 3 buy + 3 sell grid plus open fills.
input bool InpAllowOppositeTrades = true;
input bool InpAllowMinLotIfRiskTooSmall = false;
input int InpOrderExpirationMinutes = 0;
input string InpOrderCommentPrefix = "DALR1"; // Compact managed prefix; comments are capped before send.

// Runtime / speed policy.
enum ENUM_DALExecLogMode
{
   DAL_EXEC_LOG_NONE = 0,
   DAL_EXEC_LOG_ERRORS = 1,
   DAL_EXEC_LOG_ORDERS = 2,
   DAL_EXEC_LOG_VERBOSE = 3
};

input bool InpPlaceOneOrderPerSetup = true; // Exact duplicate guard: one pending/position per setup comment.
input int InpBuyLimitSlots = 3;
input int InpSellLimitSlots = 3;
input bool InpRefreshSetupsOnNewBarOnly = true;
input bool InpManageOrdersEveryTick = true;
input int InpMaxZoneScanNodes = 0; // 0 = scan all active nodes; exact H0005 mode avoids arbitrary candidate pruning.
input bool InpUpdateChartComment = false;
input ENUM_DALExecLogMode InpLogMode = DAL_EXEC_LOG_ERRORS;

// Pending-order sync. This is stable-first: do not chase/replace near-fill orders.
input bool InpSyncManagedPendings = true;
input bool InpCancelStaleManagedPendings = true;
input bool InpCancelManagedPendingsAfterEntry = false; // Multi-touch grid: keep other candidates alive after one fill.
input bool InpUpdateExistingManagedPendings = true;
input bool InpProtectPendingWhenPriceApproaches = true;
input int InpPendingProtectDistancePoints = 20;
input double InpPendingProtectStopFraction = 0.50;

// H5 live touch catch. If price has already arrived inside the zone before a
// limit can be parked, enter at market with the same stop model and true R TP.
input bool InpAllowMarketCatchWhenAlreadyTouching = false; // Limit-only touch execution by default.
input bool InpMarketCatchRequiresPriceBeforeStop = true;
input int InpTouchRevisitResetBufferPoints = 10;

#define DAL_E0001_BUILD "1.08"

CTrade g_trade;
datetime g_last_open_bar_time = 0;
bool g_cache_ready = false;
string g_cache_reason = "not_initialized";
DALExecReversalSetup g_cached_setups[];

struct E0001TouchLock
{
   string comment;
   int direction;
   double entry_price;
   bool locked;
};

E0001TouchLock g_touch_locks[];

string LabSymbol()
{
   if(InpSymbol == "")
      return _Symbol;
   return InpSymbol;
}

ENUM_TIMEFRAMES LabTimeframe()
{
   if(InpTimeframe == PERIOD_CURRENT)
      return (ENUM_TIMEFRAMES)_Period;
   return InpTimeframe;
}

bool LogErrors() { return (InpLogMode >= DAL_EXEC_LOG_ERRORS); }
bool LogOrders() { return (InpLogMode >= DAL_EXEC_LOG_ORDERS); }
bool LogVerbose() { return (InpLogMode >= DAL_EXEC_LOG_VERBOSE); }


string E0001_ManagedCommentPrefix()
{
   string prefix = InpOrderCommentPrefix;
   if(prefix == "")
      prefix = "DALR1";

   // Keep the managed identity short because many brokers truncate order comments.
   // Local helper avoids compile/runtime dependence on an include version mismatch.
   if(StringLen(prefix) > 10)
      prefix = StringSubstr(prefix, 0, 10);
   return prefix;
}

bool E0001_CheckMarketGeometry(
   const int direction,
   const double sl,
   const double tp,
   string &reason
)
{
   string symbol = LabSymbol();
   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   int stops_level = (int)SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL);
   double min_dist = MathMax(0.0, stops_level * point);

   if(point <= 0.0 || bid <= 0.0 || ask <= 0.0)
   {
      reason = "invalid_market_quote";
      return false;
   }

   if(direction > 0)
   {
      if(!(sl < ask && tp > ask))
      {
         reason = "invalid_buy_market_sl_tp_geometry";
         return false;
      }
      if((ask - sl) < min_dist || (tp - ask) < min_dist)
      {
         reason = "buy_market_sl_tp_too_close";
         return false;
      }
   }
   else if(direction < 0)
   {
      if(!(sl > bid && tp < bid))
      {
         reason = "invalid_sell_market_sl_tp_geometry";
         return false;
      }
      if((sl - bid) < min_dist || (bid - tp) < min_dist)
      {
         reason = "sell_market_sl_tp_too_close";
         return false;
      }
   }
   else
   {
      reason = "zero_direction";
      return false;
   }

   reason = "ok";
   return true;
}

bool E0001_PlaceMarketOrder(
   const int direction,
   const double volume,
   double sl,
   double tp,
   const string comment,
   string &reason
)
{
   string symbol = LabSymbol();
   int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   sl = NormalizeDouble(sl, digits);
   tp = NormalizeDouble(tp, digits);

   if(!E0001_CheckMarketGeometry(direction, sl, tp, reason))
      return false;

   if(volume <= 0.0)
   {
      reason = "volume_zero";
      return false;
   }

   g_trade.SetExpertMagicNumber(InpMagicNumber);

   bool ok = false;
   if(direction > 0)
      ok = g_trade.Buy(volume, symbol, 0.0, sl, tp, comment);
   else
      ok = g_trade.Sell(volume, symbol, 0.0, sl, tp, comment);

   if(!ok)
   {
      reason = "market_send_failed_retcode_" + IntegerToString((int)g_trade.ResultRetcode()) + "_" + g_trade.ResultRetcodeDescription();
      return false;
   }

   reason = "ok_ticket_" + IntegerToString((int)g_trade.ResultOrder());
   return true;
}

double E0001_PriceTolerance()
{
   double point = SymbolInfoDouble(LabSymbol(), SYMBOL_POINT);
   if(point <= 0.0)
      point = 0.00000001;
   return point * 0.5;
}

double E0001_VolumeTolerance()
{
   double step = SymbolInfoDouble(LabSymbol(), SYMBOL_VOLUME_STEP);
   if(step <= 0.0)
      step = 0.00000001;
   return step * 0.5;
}


void BuildM0001Config(DALM0001Config &config)
{
   DAL_M0001DefaultConfig(config);
   config.L = InpL;
   config.zone_ratio = InpZoneRatio;
   config.exit_gap = InpExitGap;
   config.consume_mode = InpConsumeMode;
   config.consume_on_touch = (InpConsumeMode == DAL_M0001_CONSUME_BY_TOUCH);
   config.max_events = 0;
   config.min_rtv = 0.0;
}

void BuildM0002Config(DALM0002Config &config)
{
   DAL_M0002DefaultConfig(config);
   config.measure_mode = DAL_M0002_MEASURE_EVENT_RTV;
   config.outcome_candle_offset_after_exit = MathMax(0, InpOutcomeCandleOffsetAfterExit);
   config.post_outcome_sample_bars = 0;
   config.use_event_length_for_sample = false;
   config.random_samples_per_event = 1;
   config.bootstrap_iterations = 0;
   config.permutation_iterations = 0;
   config.validation_splits = 1;
   config.broker_utc_offset_hours = InpBrokerUtcOffsetHours;
   config.regime_lookback_bars = MathMax(1, InpRegimeLookbackBars);
   config.print_group_session_regime = false;
   config.run_stress_suite = false;
   config.hard_random_candidates = 1;
   config.placebo_shift_bars = 1;
   config.nonoverlap_gap_bars = 0;
   config.block_bootstrap_iterations = 0;
   config.block_bootstrap_block_pairs = 1;
   config.consume_mode = InpConsumeMode;
   config.consume_on_touch = (InpConsumeMode == DAL_M0001_CONSUME_BY_TOUCH);
}

bool HasNewOpenCandle()
{
   datetime current_open = iTime(LabSymbol(), LabTimeframe(), 0);
   if(current_open <= 0)
      return false;

   if(g_last_open_bar_time <= 0)
   {
      g_last_open_bar_time = current_open;
      return true;
   }

   if(current_open == g_last_open_bar_time)
      return false;

   g_last_open_bar_time = current_open;
   return true;
}

void UpdateComment(const string state)
{
   if(!InpUpdateChartComment)
      return;

   Comment(
      "DAL E0001 H5 REV R1 | build=", DAL_E0001_BUILD,
      " | state=", state,
      " | trading=", DAL_BoolToString(InpTradingEnabled), "\n",
      "symbol=", LabSymbol(),
      " tf=", EnumToString(LabTimeframe()),
      " risk=", DoubleToString(InpRiskCash, 2),
      " R=", DoubleToString(InpRewardR, 2),
      " max=", InpMaxSimultaneousTrades,
      " slots=", InpBuyLimitSlots, "/", InpSellLimitSlots,
      " setups=", ArraySize(g_cached_setups)
   );
}

void CopySetupsToCache(const DALExecReversalSetup &setups[], const string reason)
{
   int n = ArraySize(setups);
   ArrayResize(g_cached_setups, n);
   for(int i = 0; i < n; i++)
      g_cached_setups[i] = setups[i];
   g_cache_reason = reason;
   g_cache_ready = true;
}

bool BuildCurrentSetups(DALExecReversalSetup &setups[], string &reason)
{
   ArrayResize(setups, 0);
   reason = "not_built";

   DALBar bars[];
   int bars_count = DAL_LoadBarsChronological(LabSymbol(), LabTimeframe(), InpBars, true, bars);
   if(bars_count <= InpL * 2 + 10)
   {
      reason = "not_enough_bars";
      return false;
   }

   DALM0001Config m1;
   BuildM0001Config(m1);

   DALLRuleNode nodes[];
   int nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, m1.L, nodes);

   DALM0001Event events[];
   int events_count = DAL_M0001ComputeEvents(bars, bars_count, nodes, nodes_count, m1, events);

   DALM0002Config m2;
   BuildM0002Config(m2);

   DALM0002BranchSample last_sample;
   int last_event_index = -1;
   bool has_last_sample = DAL_ExecFindLatestBranchSampleFast(events, events_count, bars, bars_count, 0, m2, last_sample, last_event_index);

   int n = DAL_ExecCollectH5ReversalRSetups(
      LabSymbol(),
      bars,
      bars_count,
      nodes,
      nodes_count,
      events,
      events_count,
      last_sample,
      has_last_sample,
      m1.zone_ratio,
      InpRewardR,
      E0001_ManagedCommentPrefix(),
      InpBuyLimitSlots,
      InpSellLimitSlots,
      InpMaxZoneScanNodes,
      setups,
      reason
   );

   return (n > 0);
}

bool RefreshSetupCacheIfNeeded()
{
   bool refresh = !g_cache_ready;
   if(!refresh)
   {
      if(!InpRefreshSetupsOnNewBarOnly)
         refresh = true;
      else if(HasNewOpenCandle())
         refresh = true;
   }

   if(!refresh)
      return false;

   DALExecReversalSetup setups[];
   string reason = "";
   bool ok = BuildCurrentSetups(setups, reason);
   if(!ok)
      ArrayResize(setups, 0);

   CopySetupsToCache(setups, reason);

   if(LogVerbose())
      Print("DAL_E0001_CACHE *** build=", DAL_E0001_BUILD, "*setups=", ArraySize(g_cached_setups), "*reason=", reason);

   return true;
}

bool SetupCommentInCache(const string comment)
{
   for(int i = 0; i < ArraySize(g_cached_setups); i++)
   {
      if(g_cached_setups[i].valid && g_cached_setups[i].comment == comment)
         return true;
   }
   return false;
}

bool FindSetupInCacheByComment(const string comment, DALExecReversalSetup &setup)
{
   DAL_ExecResetReversalSetup(setup);
   for(int i = 0; i < ArraySize(g_cached_setups); i++)
   {
      if(g_cached_setups[i].valid && g_cached_setups[i].comment == comment)
      {
         setup = g_cached_setups[i];
         return true;
      }
   }
   return false;
}

int E0001_FindTouchLockIndex(const string comment)
{
   for(int i = 0; i < ArraySize(g_touch_locks); i++)
   {
      if(g_touch_locks[i].comment == comment)
         return i;
   }
   return -1;
}

void E0001_SetTouchLock(const string comment, const int direction, const double entry_price)
{
   if(comment == "")
      return;

   int idx = E0001_FindTouchLockIndex(comment);
   if(idx < 0)
   {
      idx = ArraySize(g_touch_locks);
      ArrayResize(g_touch_locks, idx + 1);
      g_touch_locks[idx].comment = comment;
   }

   g_touch_locks[idx].direction = direction;
   g_touch_locks[idx].entry_price = entry_price;
   g_touch_locks[idx].locked = true;
}

bool E0001_TouchLocked(const string comment)
{
   int idx = E0001_FindTouchLockIndex(comment);
   return (idx >= 0 && g_touch_locks[idx].locked);
}

void E0001_UpdateTouchRevisitLocks()
{
   string symbol = LabSymbol();
   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   if(point <= 0.0)
      point = 0.00000001;

   double buffer = MathMax(0.0, (double)InpTouchRevisitResetBufferPoints) * point;

   for(int i = 0; i < ArraySize(g_touch_locks); i++)
   {
      if(!g_touch_locks[i].locked)
         continue;

      DALExecReversalSetup setup;
      bool has_setup = FindSetupInCacheByComment(g_touch_locks[i].comment, setup);
      double entry = has_setup ? setup.entry_price : g_touch_locks[i].entry_price;
      int direction = has_setup ? setup.direction : g_touch_locks[i].direction;

      // A filled touch is allowed to arm again only after price moves away from
      // the touch edge, so the next pending order belongs to a true revisit.
      if(direction > 0 && ask > entry + buffer)
      {
         g_touch_locks[i].locked = false;
         if(LogVerbose())
            Print("DAL_E0001_TOUCH_UNLOCK *** build=", DAL_E0001_BUILD, "*dir=buy*entry=", DoubleToString(entry, _Digits), "*comment=", g_touch_locks[i].comment);
      }
      else if(direction < 0 && bid < entry - buffer)
      {
         g_touch_locks[i].locked = false;
         if(LogVerbose())
            Print("DAL_E0001_TOUCH_UNLOCK *** build=", DAL_E0001_BUILD, "*dir=sell*entry=", DoubleToString(entry, _Digits), "*comment=", g_touch_locks[i].comment);
      }
   }
}

void E0001_PruneTouchLocksToManagedPrefix()
{
   string prefix = E0001_ManagedCommentPrefix();
   for(int i = ArraySize(g_touch_locks) - 1; i >= 0; i--)
   {
      if(!DAL_ExecOrderCommentMatchesPrefix(g_touch_locks[i].comment, prefix))
         continue;

      if(SetupCommentInCache(g_touch_locks[i].comment))
         continue;

      for(int j = i; j < ArraySize(g_touch_locks) - 1; j++)
         g_touch_locks[j] = g_touch_locks[j + 1];
      ArrayResize(g_touch_locks, ArraySize(g_touch_locks) - 1);
   }
}

bool E0001_FindPendingByComment(const string comment, DALExecPendingOrder &pending)
{
   DAL_ExecResetPendingOrder(pending);
   for(int i = 0; i < OrdersTotal(); i++)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0 || !OrderSelect(ticket))
         continue;
      if(OrderGetString(ORDER_SYMBOL) != LabSymbol())
         continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != InpMagicNumber)
         continue;
      if(OrderGetString(ORDER_COMMENT) != comment)
         continue;
      if(!DAL_ExecReadPendingOrder(ticket, pending))
         continue;
      return true;
   }
   return false;
}

bool E0001_PositionExistsByComment(const string comment)
{
   for(int i = 0; i < PositionsTotal(); i++)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != LabSymbol())
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != InpMagicNumber)
         continue;
      if(PositionGetString(POSITION_COMMENT) == comment)
         return true;
   }
   return false;
}

bool E0001_PendingNeedsUpdate(const DALExecPendingOrder &pending, const DALExecReversalSetup &setup, const DALExecRiskSizing &risk, bool &volume_changed)
{
   volume_changed = (MathAbs(pending.volume - risk.volume) > E0001_VolumeTolerance());

   double tol = E0001_PriceTolerance();
   if(MathAbs(pending.price - setup.entry_price) > tol)
      return true;
   if(MathAbs(pending.sl - setup.stop_price) > tol)
      return true;
   if(MathAbs(pending.tp - setup.tp_price) > tol)
      return true;

   return volume_changed;
}

bool E0001_ModifyPendingToSetup(const DALExecPendingOrder &pending, const DALExecReversalSetup &setup, string &reason)
{
   double entry = setup.entry_price;
   double sl = setup.stop_price;
   double tp = setup.tp_price;
   DAL_ExecNormalizePrices(LabSymbol(), entry, sl, tp);

   if(!DAL_ExecCheckLimitGeometry(LabSymbol(), setup.direction, entry, sl, tp, reason))
      return false;

   datetime expiration = 0;
   ENUM_ORDER_TYPE_TIME type_time = ORDER_TIME_GTC;
   if(InpOrderExpirationMinutes > 0)
   {
      type_time = ORDER_TIME_SPECIFIED;
      expiration = TimeCurrent() + InpOrderExpirationMinutes * 60;
   }

   g_trade.SetExpertMagicNumber(InpMagicNumber);
   if(!g_trade.OrderModify(pending.ticket, entry, sl, tp, type_time, expiration, 0.0))
   {
      reason = "modify_failed_retcode_" + IntegerToString((int)g_trade.ResultRetcode()) + "_" + g_trade.ResultRetcodeDescription();
      return false;
   }

   reason = "ok_modified_" + IntegerToString((int)pending.ticket);
   return true;
}

bool PendingIsProtectedNearMarket(const DALExecPendingOrder &pending)
{
   if(!pending.found || !InpProtectPendingWhenPriceApproaches)
      return false;

   double point = SymbolInfoDouble(LabSymbol(), SYMBOL_POINT);
   if(point <= 0.0)
      point = 0.00000001;

   double stop_distance = MathAbs(pending.price - pending.sl);
   double protect_distance = MathMax(0.0, (double)InpPendingProtectDistancePoints) * point;
   if(stop_distance > 0.0 && InpPendingProtectStopFraction > 0.0)
      protect_distance = MathMax(protect_distance, stop_distance * InpPendingProtectStopFraction);

   if(protect_distance <= 0.0)
      return false;

   double market_distance = DAL_ExecPendingDistanceToMarket(LabSymbol(), pending.direction, pending.price);
   return (market_distance <= protect_distance);
}

bool HasManagedPosition()
{
   string managed_prefix = E0001_ManagedCommentPrefix();
   int total = PositionsTotal();
   for(int i = 0; i < total; i++)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != LabSymbol())
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != InpMagicNumber)
         continue;
      if(!DAL_ExecOrderCommentMatchesPrefix(PositionGetString(POSITION_COMMENT), managed_prefix))
         continue;
      return true;
   }
   return false;
}

void SyncStaleManagedPendings()
{
   if(!InpSyncManagedPendings || !InpCancelStaleManagedPendings)
      return;

   string managed_prefix = E0001_ManagedCommentPrefix();
   bool managed_position_open = (InpCancelManagedPendingsAfterEntry && HasManagedPosition());
   bool no_current_reversal_setups = (ArraySize(g_cached_setups) <= 0);
   int deleted = 0;

   for(int i = OrdersTotal() - 1; i >= 0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0 || !OrderSelect(ticket))
         continue;
      if(OrderGetString(ORDER_SYMBOL) != LabSymbol())
         continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != InpMagicNumber)
         continue;

      ENUM_ORDER_TYPE type = (ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE);
      if(!DAL_ExecOrderIsPendingLimit(type))
         continue;

      string comment = OrderGetString(ORDER_COMMENT);
      if(!DAL_ExecOrderCommentMatchesPrefix(comment, managed_prefix))
         continue;

      if(!managed_position_open && SetupCommentInCache(comment))
         continue;

      DALExecPendingOrder pending;
      if(!DAL_ExecReadPendingOrder(ticket, pending))
         continue;

      // In continuation/non-reversal regime everything must be removed. Protection
      // is only for active reversal setups that are close to being filled.
      if(!managed_position_open && !no_current_reversal_setups && PendingIsProtectedNearMarket(pending))
         continue;

      string delete_reason = "";
      string sync_reason = managed_position_open ? "managed_position_open_cancel_unused_candidate" : "stale_or_non_reversal_regime";
      if(DAL_ExecDeletePendingOrder(ticket, g_trade, delete_reason))
      {
         deleted++;
         if(LogOrders())
            Print("DAL_E0001_PENDING_DELETE *** build=", DAL_E0001_BUILD, "*ticket=", (long)ticket, "*reason=", sync_reason, "*comment=", comment);
      }
      else if(LogErrors())
      {
         Print("DAL_E0001_PENDING_DELETE_FAIL *** build=", DAL_E0001_BUILD, "*ticket=", (long)ticket, "*reason=", delete_reason, "*comment=", comment);
      }
   }

   if(no_current_reversal_setups)
      E0001_PruneTouchLocksToManagedPrefix();

   if(deleted > 0 && LogVerbose())
      Print("DAL_E0001_PENDING_SYNC *** build=", DAL_E0001_BUILD, "*deleted=", deleted);
}

bool MarketIsAlreadyTouchingSetup(const DALExecReversalSetup &setup, double &market_entry)
{
   market_entry = 0.0;
   double bid = SymbolInfoDouble(LabSymbol(), SYMBOL_BID);
   double ask = SymbolInfoDouble(LabSymbol(), SYMBOL_ASK);
   if(bid <= 0.0 || ask <= 0.0 || !setup.valid)
      return false;

   if(setup.direction > 0)
   {
      market_entry = ask;
      if(!(ask <= setup.entry_price))
         return false;
      if(InpMarketCatchRequiresPriceBeforeStop && !(ask > setup.stop_price))
         return false;
      return true;
   }

   if(setup.direction < 0)
   {
      market_entry = bid;
      if(!(bid >= setup.entry_price))
         return false;
      if(InpMarketCatchRequiresPriceBeforeStop && !(bid < setup.stop_price))
         return false;
      return true;
   }

   return false;
}

bool PlaceSetupLimitOrder(const DALExecReversalSetup &setup, const DALExecRiskSizing &risk, string &order_reason)
{
   order_reason = "dry_run";
   if(!InpTradingEnabled)
      return false;

   return DAL_ExecPlaceLimitOrder(
      LabSymbol(),
      InpMagicNumber,
      setup.direction,
      risk.volume,
      setup.entry_price,
      setup.stop_price,
      setup.tp_price,
      setup.comment,
      InpOrderExpirationMinutes,
      g_trade,
      order_reason
   );
}

bool PlaceSetupMarketCatch(const DALExecReversalSetup &setup, const double market_entry, string &order_reason, DALExecRiskSizing &risk)
{
   order_reason = "market_catch_disabled";
   DAL_ExecResetRiskSizing(risk);

   if(!InpAllowMarketCatchWhenAlreadyTouching)
      return false;

   double stop_distance = MathAbs(market_entry - setup.stop_price);
   if(stop_distance <= 0.0)
   {
      order_reason = "market_catch_zero_stop_distance";
      return false;
   }

   double tp = market_entry + setup.direction * stop_distance * setup.reward_r;
   bool risk_ok = DAL_ExecCalculateRiskVolume(
      LabSymbol(),
      market_entry,
      setup.stop_price,
      InpRiskCash,
      InpCommissionPerLotRoundTurn,
      InpAllowMinLotIfRiskTooSmall,
      risk
   );
   if(!risk_ok)
   {
      order_reason = "market_catch_risk_reject_" + risk.reason;
      return false;
   }

   order_reason = "dry_run_market_catch";
   if(!InpTradingEnabled)
      return false;

   return E0001_PlaceMarketOrder(
      setup.direction,
      risk.volume,
      setup.stop_price,
      tp,
      setup.comment,
      order_reason
   );
}

void TryPlaceCachedSetups()
{
   E0001_UpdateTouchRevisitLocks();
   SyncStaleManagedPendings();

   int setup_count = ArraySize(g_cached_setups);
   if(setup_count <= 0)
   {
      if(LogVerbose())
         Print("DAL_E0001_SKIP *** build=", DAL_E0001_BUILD, "*reason=", g_cache_reason, "*mode=h5_reversal_r1_six_slot_cache");
      UpdateComment("no_h5_r1_setup_" + g_cache_reason);
      return;
   }

   int submitted = 0;
   int modified = 0;
   int skipped_existing = 0;
   int skipped_touch_lock = 0;
   int skipped_blocked = 0;
   int skipped_risk = 0;
   int skipped_market_catch = 0;
   int skipped_update = 0;

   for(int i = 0; i < setup_count; i++)
   {
      DALExecReversalSetup setup = g_cached_setups[i];
      if(!setup.valid)
         continue;

      if(E0001_PositionExistsByComment(setup.comment))
      {
         E0001_SetTouchLock(setup.comment, setup.direction, setup.entry_price);
         skipped_existing++;
         continue;
      }

      if(E0001_TouchLocked(setup.comment))
      {
         skipped_touch_lock++;
         if(LogVerbose())
            Print("DAL_E0001_SKIP *** build=", DAL_E0001_BUILD, "*reason=touch_locked_wait_revisit*comment=", setup.comment);
         continue;
      }

      DALExecRiskSizing risk;
      bool risk_ok = DAL_ExecCalculateRiskVolume(
         LabSymbol(),
         setup.entry_price,
         setup.stop_price,
         InpRiskCash,
         InpCommissionPerLotRoundTurn,
         InpAllowMinLotIfRiskTooSmall,
         risk
      );

      if(!risk_ok)
      {
         skipped_risk++;
         if(LogErrors())
            Print("DAL_E0001_RISK_REJECT *** build=", DAL_E0001_BUILD, "*reason=", risk.reason, "*entry=", DoubleToString(setup.entry_price, _Digits), "*stop=", DoubleToString(setup.stop_price, _Digits), "*comment=", setup.comment);
         continue;
      }

      DALExecPendingOrder pending;
      if(E0001_FindPendingByComment(setup.comment, pending))
      {
         bool volume_changed = false;
         bool needs_update = E0001_PendingNeedsUpdate(pending, setup, risk, volume_changed);
         if(!needs_update || !InpUpdateExistingManagedPendings)
         {
            skipped_existing++;
            continue;
         }

         if(PendingIsProtectedNearMarket(pending))
         {
            skipped_update++;
            if(LogVerbose())
               Print("DAL_E0001_PENDING_UPDATE_SKIP *** build=", DAL_E0001_BUILD, "*reason=protected_near_market*comment=", setup.comment);
            continue;
         }

         string update_reason = "";
         bool update_ok = false;
         if(volume_changed)
         {
            if(DAL_ExecDeletePendingOrder(pending.ticket, g_trade, update_reason))
            {
               string order_reason = "";
               update_ok = PlaceSetupLimitOrder(setup, risk, order_reason);
               update_reason = update_reason + "+" + order_reason;
               if(update_ok)
                  modified++;
            }
         }
         else
         {
            update_ok = E0001_ModifyPendingToSetup(pending, setup, update_reason);
            if(update_ok)
               modified++;
         }

         if(LogOrders() || (InpTradingEnabled && !update_ok && LogErrors()))
         {
            Print(
               "DAL_E0001_PENDING_UPDATE *** build=", DAL_E0001_BUILD,
               "*ok=", DAL_BoolToString(update_ok),
               "*reason=", update_reason,
               "*volumeChanged=", DAL_BoolToString(volume_changed),
               "*dir=", setup.direction,
               "*entry=", DoubleToString(setup.entry_price, _Digits),
               "*sl=", DoubleToString(setup.stop_price, _Digits),
               "*tp=", DoubleToString(setup.tp_price, _Digits),
               "*comment=", setup.comment
            );
         }

         if(!update_ok)
            skipped_update++;
         continue;
      }

      string exposure_reason = "";
      if(!DAL_ExecCanOpenDirection(LabSymbol(), InpMagicNumber, setup.direction, InpMaxSimultaneousTrades, InpAllowOppositeTrades, exposure_reason))
      {
         skipped_blocked++;
         if(LogVerbose())
            Print("DAL_E0001_SKIP *** build=", DAL_E0001_BUILD, "*reason=", exposure_reason, "*direction=", setup.direction, "*comment=", setup.comment);
         if(StringFind(exposure_reason, "max_simultaneous", 0) >= 0)
            break;
         continue;
      }

      double market_entry = 0.0;
      bool already_touching = MarketIsAlreadyTouchingSetup(setup, market_entry);
      if(already_touching)
      {
         DALExecRiskSizing market_risk;
         string market_reason = "";
         bool market_ok = PlaceSetupMarketCatch(setup, market_entry, market_reason, market_risk);
         if(market_ok)
         {
            E0001_SetTouchLock(setup.comment, setup.direction, setup.entry_price);
            submitted++;
         }
         else
            skipped_market_catch++;

         if(LogOrders() || (InpTradingEnabled && !market_ok && LogErrors()))
         {
            Print(
               "DAL_E0001_MARKET_CATCH *** build=", DAL_E0001_BUILD,
               "*sent=", DAL_BoolToString(market_ok),
               "*reason=", market_reason,
               "*dir=", setup.direction,
               "*entry=", DoubleToString(market_entry, _Digits),
               "*sl=", DoubleToString(setup.stop_price, _Digits),
               "*rewardR=", DoubleToString(setup.reward_r, 4),
               "*vol=", DoubleToString(market_risk.volume, 4),
               "*comment=", setup.comment
            );
         }
         continue;
      }

      string order_reason = "";
      bool order_ok = PlaceSetupLimitOrder(setup, risk, order_reason);
      if(order_ok)
         submitted++;

      if(LogOrders() || (InpTradingEnabled && !order_ok && LogErrors()))
      {
         Print(
            "DAL_E0001_LIMIT_ORDER *** build=", DAL_E0001_BUILD,
            "*sent=", DAL_BoolToString(order_ok),
            "*reason=", order_reason,
            "*dir=", setup.direction,
            "*vol=", DoubleToString(risk.volume, 4),
            "*entry=", DoubleToString(setup.entry_price, _Digits),
            "*sl=", DoubleToString(setup.stop_price, _Digits),
            "*tp=", DoubleToString(setup.tp_price, _Digits),
            "*rewardR=", DoubleToString(setup.reward_r, 4),
            "*risk=", DoubleToString(risk.estimated_total_risk_cash, 2),
            "*nodeId=", setup.node_id,
            "*lastBranchSampleId=", setup.last_branch_sample_id,
            "*comment=", setup.comment
         );
      }
   }

   if(LogVerbose())
   {
      Print("DAL_E0001_CYCLE *** build=", DAL_E0001_BUILD,
         "*mode=h5_reversal_r1_six_slot_touch_ledger",
         "*setups=", setup_count,
         "*submitted=", submitted,
         "*modified=", modified,
         "*skippedExisting=", skipped_existing,
         "*skippedTouchLock=", skipped_touch_lock,
         "*skippedBlocked=", skipped_blocked,
         "*skippedRisk=", skipped_risk,
         "*skippedMarketCatch=", skipped_market_catch,
         "*skippedUpdate=", skipped_update);
   }

   UpdateComment("h5_r1_setups_" + IntegerToString(setup_count) + "_new_" + IntegerToString(submitted) + "_upd_" + IntegerToString(modified));
}

int OnInit()
{
   if(!SymbolSelect(LabSymbol(), true))
   {
      Print("DAL_E0001_INIT_FAIL *** reason=symbol_select_failed*symbol=", LabSymbol());
      return INIT_FAILED;
   }

   g_trade.SetExpertMagicNumber(InpMagicNumber);
   g_last_open_bar_time = iTime(LabSymbol(), LabTimeframe(), 0);
   ArrayResize(g_cached_setups, 0);
   ArrayResize(g_touch_locks, 0);
   g_cache_ready = false;

   if(LogErrors())
   {
      Print(
         "DAL_E0001_BUILD_SANITY *** build=", DAL_E0001_BUILD,
         "*symbol=", LabSymbol(),
         "*tf=", EnumToString(LabTimeframe()),
         "*module=EXECUTION_H0005_REVERSAL_R1_SIX_SLOT_TOUCH_LEDGER",
         "*bars=", InpBars,
         "*h5Exact=LAST_ONLY_REVERSAL_NEXT_STRUCTURAL_ZONE_TOUCH",
         "*rewardR=", DoubleToString(InpRewardR, 4),
         "*entryModel=three_buy_limits_three_sell_limits_revisit_locked",
         "*researchEntryModel=touch_bar_close_in_M0005_report",
         "*stopModel=zone_edge",
         "*maxSimultaneousTrades=", InpMaxSimultaneousTrades,
         "*buySlots=", InpBuyLimitSlots,
         "*sellSlots=", InpSellLimitSlots,
         "*allowOpposite=", DAL_BoolToString(InpAllowOppositeTrades),
         "*orderCommentPrefix=", E0001_ManagedCommentPrefix(),
         "*manageEveryTick=", DAL_BoolToString(InpManageOrdersEveryTick),
         "*marketCatch=", DAL_BoolToString(InpAllowMarketCatchWhenAlreadyTouching),
         "*cancelStale=", DAL_BoolToString(InpCancelStaleManagedPendings),
         "*cancelAfterEntry=", DAL_BoolToString(InpCancelManagedPendingsAfterEntry),
         "*updatePendings=", DAL_BoolToString(InpUpdateExistingManagedPendings),
         "*touchRevisitBufferPoints=", InpTouchRevisitResetBufferPoints,
         "*logMode=", EnumToString(InpLogMode)
      );
   }

   RefreshSetupCacheIfNeeded();
   UpdateComment("initialized");
   return INIT_SUCCEEDED;
}


void OnTradeTransaction(const MqlTradeTransaction &trans, const MqlTradeRequest &request, const MqlTradeResult &result)
{
   if(trans.type != TRADE_TRANSACTION_DEAL_ADD)
      return;
   if(trans.deal == 0 || !HistoryDealSelect(trans.deal))
      return;
   if(HistoryDealGetString(trans.deal, DEAL_SYMBOL) != LabSymbol())
      return;
   if((long)HistoryDealGetInteger(trans.deal, DEAL_MAGIC) != InpMagicNumber)
      return;

   long entry_type = HistoryDealGetInteger(trans.deal, DEAL_ENTRY);
   if(entry_type != DEAL_ENTRY_IN && entry_type != DEAL_ENTRY_INOUT)
      return;

   string comment = HistoryDealGetString(trans.deal, DEAL_COMMENT);
   if(!DAL_ExecOrderCommentMatchesPrefix(comment, E0001_ManagedCommentPrefix()))
      return;

   int direction = 0;
   long deal_type = HistoryDealGetInteger(trans.deal, DEAL_TYPE);
   if(deal_type == DEAL_TYPE_BUY)
      direction = +1;
   else if(deal_type == DEAL_TYPE_SELL)
      direction = -1;

   double entry_price = HistoryDealGetDouble(trans.deal, DEAL_PRICE);
   DALExecReversalSetup setup;
   if(FindSetupInCacheByComment(comment, setup))
   {
      direction = setup.direction;
      entry_price = setup.entry_price;
   }

   E0001_SetTouchLock(comment, direction, entry_price);

   if(LogOrders())
      Print("DAL_E0001_TOUCH_LOCK *** build=", DAL_E0001_BUILD, "*deal=", (long)trans.deal, "*dir=", direction, "*entry=", DoubleToString(entry_price, _Digits), "*comment=", comment);
}

void OnDeinit(const int reason)
{
   Comment("");
}

void OnTick()
{
   bool refreshed = RefreshSetupCacheIfNeeded();

   if(!InpManageOrdersEveryTick && !refreshed)
      return;

   TryPlaceCachedSetups();
}
