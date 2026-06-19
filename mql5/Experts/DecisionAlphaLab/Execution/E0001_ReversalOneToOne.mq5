//+------------------------------------------------------------------+
//| Decision Alpha Lab — E0001 H0005 Reversal R1 Executor             |
//| Execution layer: exact H5 reversal R1, stable pending sync + touch catch|
//+------------------------------------------------------------------+
#property strict
#property version   "1.06"
#property description "Execution module for H0005 reversal R1: stable limit orders at structural zone touch, optional market catch if price is already touching."

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
input int InpMaxSimultaneousTrades = 1;
input bool InpAllowOppositeTrades = false;
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

input bool InpPlaceOneOrderPerSetup = true;
input bool InpRefreshSetupsOnNewBarOnly = true;
input bool InpManageOrdersEveryTick = true;
input int InpMaxZoneScanNodes = 0; // 0 = scan all active nodes; exact H0005 mode avoids arbitrary candidate pruning.
input bool InpUpdateChartComment = false;
input ENUM_DALExecLogMode InpLogMode = DAL_EXEC_LOG_ERRORS;

// Pending-order sync. This is stable-first: do not chase/replace near-fill orders.
input bool InpSyncManagedPendings = true;
input bool InpCancelStaleManagedPendings = true;
input bool InpCancelManagedPendingsAfterEntry = true; // H5 path has one actual next-touch entry; cancel unused candidate orders after a fill.
input bool InpProtectPendingWhenPriceApproaches = true;
input int InpPendingProtectDistancePoints = 20;
input double InpPendingProtectStopFraction = 0.50;

// H5 live touch catch. If price has already arrived inside the zone before a
// limit can be parked, enter at market with the same stop model and true R TP.
input bool InpAllowMarketCatchWhenAlreadyTouching = true;
input bool InpMarketCatchRequiresPriceBeforeStop = true;

#define DAL_E0001_BUILD "1.06"

CTrade g_trade;
datetime g_last_open_bar_time = 0;
bool g_cache_ready = false;
string g_cache_reason = "not_initialized";
DALExecReversalSetup g_cached_setups[];

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
      DAL_ExecManagedCommentPrefix(InpOrderCommentPrefix),
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

bool PendingIsProtectedNearMarket(const DALExecPendingOrder &pending)
{
   if(!pending.found || !InpProtectPendingWhenPriceApproaches)
      return false;

   double point = SymbolInfoDouble(LabSymbol(), SYMBOL_POINT);
   if(point <= 0.0)
      point = 0.00000001;

   double stop_distance = MathAbs(pending.price - pending.sl);
   double protect_distance = MathMax(0, InpPendingProtectDistancePoints) * point;
   if(stop_distance > 0.0 && InpPendingProtectStopFraction > 0.0)
      protect_distance = MathMax(protect_distance, stop_distance * InpPendingProtectStopFraction);

   if(protect_distance <= 0.0)
      return false;

   double market_distance = DAL_ExecPendingDistanceToMarket(LabSymbol(), pending.direction, pending.price);
   return (market_distance <= protect_distance);
}

bool HasManagedPosition()
{
   string managed_prefix = DAL_ExecManagedCommentPrefix(InpOrderCommentPrefix);
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

   string managed_prefix = DAL_ExecManagedCommentPrefix(InpOrderCommentPrefix);
   bool managed_position_open = (InpCancelManagedPendingsAfterEntry && HasManagedPosition());
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

      if(!managed_position_open && PendingIsProtectedNearMarket(pending))
         continue;

      string delete_reason = "";
      string sync_reason = managed_position_open ? "managed_position_open_cancel_unused_candidate" : "stale_not_in_current_h5_setup";
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

   return DAL_ExecPlaceMarketOrder(
      LabSymbol(),
      InpMagicNumber,
      setup.direction,
      risk.volume,
      setup.stop_price,
      tp,
      setup.comment,
      g_trade,
      order_reason
   );
}

void TryPlaceCachedSetups()
{
   SyncStaleManagedPendings();

   int setup_count = ArraySize(g_cached_setups);
   if(setup_count <= 0)
   {
      if(LogVerbose())
         Print("DAL_E0001_SKIP *** build=", DAL_E0001_BUILD, "*reason=", g_cache_reason, "*mode=h5_reversal_r1_cache");
      UpdateComment("no_h5_r1_setup_" + g_cache_reason);
      return;
   }

   int submitted = 0;
   int skipped_existing = 0;
   int skipped_blocked = 0;
   int skipped_risk = 0;
   int skipped_market_catch = 0;

   for(int i = 0; i < setup_count; i++)
   {
      DALExecReversalSetup setup = g_cached_setups[i];
      if(!setup.valid)
         continue;

      if(InpPlaceOneOrderPerSetup && DAL_ExecOrderCommentExists(LabSymbol(), InpMagicNumber, setup.comment))
      {
         skipped_existing++;
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
            submitted++;
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
         "*mode=h5_reversal_r1_stateful_execution",
         "*setups=", setup_count,
         "*submitted=", submitted,
         "*skippedExisting=", skipped_existing,
         "*skippedBlocked=", skipped_blocked,
         "*skippedRisk=", skipped_risk,
         "*skippedMarketCatch=", skipped_market_catch);
   }

   UpdateComment("h5_r1_setups_" + IntegerToString(setup_count) + "_submitted_" + IntegerToString(submitted));
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
   g_cache_ready = false;

   if(LogErrors())
   {
      Print(
         "DAL_E0001_BUILD_SANITY *** build=", DAL_E0001_BUILD,
         "*symbol=", LabSymbol(),
         "*tf=", EnumToString(LabTimeframe()),
         "*module=EXECUTION_H0005_REVERSAL_R1_STATEFUL",
         "*bars=", InpBars,
         "*h5Exact=LAST_ONLY_REVERSAL_NEXT_STRUCTURAL_ZONE_TOUCH",
         "*rewardR=", DoubleToString(InpRewardR, 4),
         "*entryModel=limit_at_touch_edge_or_market_catch_if_already_touching",
         "*researchEntryModel=touch_bar_close_in_M0005_report",
         "*stopModel=zone_edge",
         "*maxSimultaneousTrades=", InpMaxSimultaneousTrades,
         "*orderCommentPrefix=", DAL_ExecManagedCommentPrefix(InpOrderCommentPrefix),
         "*manageEveryTick=", DAL_BoolToString(InpManageOrdersEveryTick),
         "*marketCatch=", DAL_BoolToString(InpAllowMarketCatchWhenAlreadyTouching),
         "*cancelStale=", DAL_BoolToString(InpCancelStaleManagedPendings),
         "*cancelAfterEntry=", DAL_BoolToString(InpCancelManagedPendingsAfterEntry),
         "*logMode=", EnumToString(InpLogMode)
      );
   }

   RefreshSetupCacheIfNeeded();
   UpdateComment("initialized");
   return INIT_SUCCEEDED;
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
