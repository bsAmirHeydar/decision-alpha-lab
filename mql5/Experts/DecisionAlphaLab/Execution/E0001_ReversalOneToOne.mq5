//+------------------------------------------------------------------+
//| Decision Alpha Lab — E0001 Reversal One-to-One Executor           |
//| Execution layer: raw reversal 1:R pending-limit executor.          |
//+------------------------------------------------------------------+
#property strict
#property version   "1.02"
#property description "Execution module for H0005 reversal regime: limit entry at structural zone touch, zone-edge stop, fixed R take-profit."

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
input double InpRewardR = 1.0;
input int InpMaxSimultaneousTrades = 1;
input bool InpAllowOppositeTrades = false;
input bool InpAllowMinLotIfRiskTooSmall = false;
input int InpOrderExpirationMinutes = 0;
input string InpOrderCommentPrefix = "DAL_E0001_REV_1R";

// Runtime / speed policy.
enum ENUM_DALExecLogMode
{
   DAL_EXEC_LOG_NONE = 0,
   DAL_EXEC_LOG_ERRORS = 1,
   DAL_EXEC_LOG_ORDERS = 2,
   DAL_EXEC_LOG_VERBOSE = 3
};

input bool InpPlaceOneOrderPerSetup = true;
input bool InpEvaluateOnNewBarOnly = true;
input int InpMaxZoneScanNodes = 300;
input bool InpUpdateChartComment = false;
input ENUM_DALExecLogMode InpLogMode = DAL_EXEC_LOG_ERRORS;

// Pending-order update engine.
input bool InpUpdatePendingOrders = true;
input bool InpReplacePendingWithCloserSetup = true;
input bool InpCancelPendingWhenNoSetup = true;
input bool InpCancelExtraManagedPendings = true;
input int InpPendingReplaceMinImprovePoints = 2;

#define DAL_E0001_BUILD "1.02"

CTrade g_trade;
datetime g_last_open_bar_time = 0;

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

bool HasNewClosedCandle()
{
   datetime current_open = iTime(LabSymbol(), LabTimeframe(), 0);
   if(current_open <= 0)
      return false;

   if(g_last_open_bar_time <= 0)
   {
      g_last_open_bar_time = current_open;
      return false;
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
      "DAL E0001 Reversal 1:R | build=", DAL_E0001_BUILD,
      " | state=", state,
      " | trading=", DAL_BoolToString(InpTradingEnabled), "\n",
      "symbol=", LabSymbol(),
      " tf=", EnumToString(LabTimeframe()),
      " risk=", DoubleToString(InpRiskCash, 2),
      " R=", DoubleToString(InpRewardR, 2),
      " max=", InpMaxSimultaneousTrades
   );
}

bool BuildCurrentSetup(DALExecReversalSetup &setup)
{
   DALBar bars[];
   int bars_count = DAL_LoadBarsChronological(LabSymbol(), LabTimeframe(), InpBars, true, bars);
   if(bars_count <= InpL * 2 + 10)
   {
      DAL_ExecResetReversalSetup(setup);
      setup.reason = "not_enough_bars";
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

   return DAL_ExecBuildReversalOneToOneSetup(
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
      InpOrderCommentPrefix,
      InpMaxZoneScanNodes,
      setup
   );
}

bool SetupPricesAlmostSame(const DALExecReversalSetup &setup, const DALExecPendingOrder &pending)
{
   double point = SymbolInfoDouble(LabSymbol(), SYMBOL_POINT);
   if(point <= 0.0)
      point = 0.00000001;
   double tol = MathMax(point * 0.5, point * MathMax(1, InpPendingReplaceMinImprovePoints));

   return (pending.found
      && pending.direction == setup.direction
      && MathAbs(pending.price - setup.entry_price) <= tol
      && MathAbs(pending.sl - setup.stop_price) <= tol
      && MathAbs(pending.tp - setup.tp_price) <= tol);
}

bool NewSetupIsCloserThanPending(const DALExecReversalSetup &setup, const DALExecPendingOrder &pending)
{
   if(!pending.found)
      return true;

   double point = SymbolInfoDouble(LabSymbol(), SYMBOL_POINT);
   if(point <= 0.0)
      point = 0.00000001;

   double old_distance = DAL_ExecPendingDistanceToMarket(LabSymbol(), pending.direction, pending.price);
   double new_distance = DAL_ExecPendingDistanceToMarket(LabSymbol(), setup.direction, setup.entry_price);
   double min_improve = MathMax(0, InpPendingReplaceMinImprovePoints) * point;

   if(pending.direction != setup.direction)
      return (new_distance + min_improve < old_distance);

   return (new_distance + min_improve < old_distance);
}

bool PlaceSetupOrder(const DALExecReversalSetup &setup, const DALExecRiskSizing &risk, string &order_reason)
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

void TryPlaceSetup()
{
   string cleanup_reason = "";
   DALExecPendingOrder pending;
   bool has_pending = DAL_ExecFindManagedPendingLimit(
      LabSymbol(),
      InpMagicNumber,
      InpOrderCommentPrefix,
      pending
   );

   if(InpCancelExtraManagedPendings && has_pending && InpTradingEnabled)
   {
      int deleted_extra = 0;
      DAL_ExecDeleteManagedPendingLimitsExcept(
         LabSymbol(),
         InpMagicNumber,
         InpOrderCommentPrefix,
         pending.ticket,
         g_trade,
         deleted_extra,
         cleanup_reason
      );
      if(deleted_extra > 0 && LogOrders())
         Print("DAL_E0001_PENDING_CLEANUP *** build=", DAL_E0001_BUILD, "*deletedExtra=", deleted_extra, "*reason=", cleanup_reason);
   }

   DALExecReversalSetup setup;
   bool setup_ok = BuildCurrentSetup(setup);

   if(!setup_ok)
   {
      if(has_pending && InpUpdatePendingOrders && InpCancelPendingWhenNoSetup && InpTradingEnabled)
      {
         string delete_reason = "";
         bool deleted = DAL_ExecDeletePendingOrder(pending.ticket, g_trade, delete_reason);
         if(LogOrders() || (LogErrors() && !deleted))
            Print("DAL_E0001_PENDING_DELETE *** build=", DAL_E0001_BUILD, "*sent=", DAL_BoolToString(deleted), "*reason=", delete_reason, "*cause=no_valid_setup", "*ticket=", pending.ticket);
      }
      else if(LogVerbose())
         Print("DAL_E0001_SKIP *** build=", DAL_E0001_BUILD, "*reason=", setup.reason, "*hasPending=", DAL_BoolToString(has_pending));

      UpdateComment("no_setup_" + setup.reason);
      return;
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
      if(LogErrors())
         Print("DAL_E0001_RISK_REJECT *** build=", DAL_E0001_BUILD, "*reason=", risk.reason, "*entry=", DoubleToString(setup.entry_price, _Digits), "*stop=", DoubleToString(setup.stop_price, _Digits));
      UpdateComment("risk_reject_" + risk.reason);
      return;
   }

   if(has_pending && InpUpdatePendingOrders)
   {
      if(SetupPricesAlmostSame(setup, pending))
      {
         if(LogVerbose())
            Print("DAL_E0001_PENDING_KEEP *** build=", DAL_E0001_BUILD, "*reason=same_setup_or_prices*ticket=", pending.ticket, "*comment=", pending.comment);
         UpdateComment("pending_current");
         return;
      }

      if(InpReplacePendingWithCloserSetup && NewSetupIsCloserThanPending(setup, pending))
      {
         string delete_reason = "";
         bool deleted = true;
         if(InpTradingEnabled)
            deleted = DAL_ExecDeletePendingOrder(pending.ticket, g_trade, delete_reason);
         else
            delete_reason = "dry_run_delete_old_pending";

         if(!deleted)
         {
            if(LogErrors())
               Print("DAL_E0001_PENDING_REPLACE_FAIL *** build=", DAL_E0001_BUILD, "*stage=delete_old*reason=", delete_reason, "*ticket=", pending.ticket);
            UpdateComment("replace_delete_failed");
            return;
         }

         if(LogOrders())
            Print("DAL_E0001_PENDING_REPLACE *** build=", DAL_E0001_BUILD,
               "*oldTicket=", pending.ticket,
               "*oldDir=", pending.direction,
               "*newDir=", setup.direction,
               "*oldEntry=", DoubleToString(pending.price, _Digits),
               "*newEntry=", DoubleToString(setup.entry_price, _Digits),
               "*oldDistance=", DoubleToString(DAL_ExecPendingDistanceToMarket(LabSymbol(), pending.direction, pending.price), _Digits),
               "*newDistance=", DoubleToString(DAL_ExecPendingDistanceToMarket(LabSymbol(), setup.direction, setup.entry_price), _Digits),
               "*deleteReason=", delete_reason);

         has_pending = false;
      }
      else
      {
         if(LogVerbose())
            Print("DAL_E0001_PENDING_KEEP *** build=", DAL_E0001_BUILD, "*reason=existing_is_closer_or_replace_disabled*ticket=", pending.ticket);
         UpdateComment("pending_kept");
         return;
      }
   }

   string exposure_reason = "";
   if(!DAL_ExecCanOpenDirection(LabSymbol(), InpMagicNumber, setup.direction, InpMaxSimultaneousTrades, InpAllowOppositeTrades, exposure_reason))
   {
      if(LogVerbose())
         Print("DAL_E0001_SKIP *** build=", DAL_E0001_BUILD, "*reason=", exposure_reason, "*direction=", setup.direction);
      UpdateComment("blocked_" + exposure_reason);
      return;
   }

   if(InpPlaceOneOrderPerSetup && DAL_ExecOrderCommentExists(LabSymbol(), InpMagicNumber, setup.comment))
   {
      if(LogVerbose())
         Print("DAL_E0001_SKIP *** build=", DAL_E0001_BUILD, "*reason=duplicate_setup*comment=", setup.comment);
      UpdateComment("duplicate_setup");
      return;
   }

   string order_reason = "";
   bool order_ok = PlaceSetupOrder(setup, risk, order_reason);

   if(LogOrders() || (InpTradingEnabled && !order_ok && LogErrors()))
   {
      Print(
         "DAL_E0001_ORDER *** build=", DAL_E0001_BUILD,
         "*sent=", DAL_BoolToString(order_ok),
         "*reason=", order_reason,
         "*dir=", setup.direction,
         "*vol=", DoubleToString(risk.volume, 4),
         "*entry=", DoubleToString(setup.entry_price, _Digits),
         "*sl=", DoubleToString(setup.stop_price, _Digits),
         "*tp=", DoubleToString(setup.tp_price, _Digits),
         "*risk=", DoubleToString(risk.estimated_total_risk_cash, 2),
         "*comment=", setup.comment
      );
   }

   UpdateComment(InpTradingEnabled ? (order_ok ? "order_sent" : "order_rejected") : "dry_run_setup_ready");
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

   if(LogErrors())
   {
      Print(
         "DAL_E0001_BUILD_SANITY *** build=", DAL_E0001_BUILD,
         "*symbol=", LabSymbol(),
         "*tf=", EnumToString(LabTimeframe()),
         "*module=EXECUTION_REVERSAL_ONE_TO_ONE_FAST_UPDATE_ENGINE",
         "*bars=", InpBars,
         "*maxZoneScanNodes=", InpMaxZoneScanNodes,
         "*updatePending=", DAL_BoolToString(InpUpdatePendingOrders),
         "*replaceCloser=", DAL_BoolToString(InpReplacePendingWithCloserSetup),
         "*replaceMinImprovePoints=", InpPendingReplaceMinImprovePoints,
         "*logMode=", EnumToString(InpLogMode)
      );
   }

   UpdateComment("initialized");
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   Comment("");
}

void OnTick()
{
   if(InpEvaluateOnNewBarOnly && !HasNewClosedCandle())
      return;

   TryPlaceSetup();
}
