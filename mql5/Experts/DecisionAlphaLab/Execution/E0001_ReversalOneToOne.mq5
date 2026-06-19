//+------------------------------------------------------------------+
//| Decision Alpha Lab — E0001 Reversal One-to-One Executor           |
//| Execution layer: raw reversal 1:R pending-limit executor.          |
//+------------------------------------------------------------------+
#property strict
#property version   "1.04"
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
input double InpRewardR = 1.0; // H0005 fixed-reward R1 default; change only for intentional variants.
input int InpMaxSimultaneousTrades = 1;
input bool InpAllowOppositeTrades = false;
input bool InpAllowMinLotIfRiskTooSmall = false;
input int InpOrderExpirationMinutes = 0;
input string InpOrderCommentPrefix = "DAL_E0001_H5_REV_R1";

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
input int InpMaxZoneScanNodes = 0; // 0 = scan all active nodes; exact H0005 mode avoids arbitrary candidate pruning.
input bool InpUpdateChartComment = false;
input ENUM_DALExecLogMode InpLogMode = DAL_EXEC_LOG_ERRORS;

// Pending-order update engine.
input bool InpUpdatePendingOrders = true;
input bool InpReplacePendingWithCloserSetup = false;
input bool InpCancelPendingWhenNoSetup = false;
input bool InpCancelExtraManagedPendings = false;
input int InpPendingReplaceMinImprovePoints = 2;
input bool InpProtectPendingWhenPriceApproaches = true;
input int InpPendingProtectDistancePoints = 20;
input double InpPendingProtectStopFraction = 0.50;

#define DAL_E0001_BUILD "1.04"

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
      InpOrderCommentPrefix,
      InpMaxZoneScanNodes,
      setups,
      reason
   );

   return (n > 0);
}

bool BuildCurrentSetup(DALExecReversalSetup &setup)
{
   DALExecReversalSetup setups[];
   string reason = "";
   bool ok = BuildCurrentSetups(setups, reason);
   if(!ok || ArraySize(setups) <= 0)
   {
      DAL_ExecResetReversalSetup(setup);
      setup.reason = reason;
      return false;
   }
   setup = setups[0];
   return true;
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

bool PendingMatchesLiveStrategySide(const DALExecPendingOrder &pending, const DALExecReversalSetup &setup)
{
   if(!pending.found || !setup.valid)
      return false;
   return (pending.direction == setup.direction);
}

bool MultiplePendingSetupsAllowed()
{
   return (InpMaxSimultaneousTrades < 0 || InpMaxSimultaneousTrades > 1);
}

bool PendingIsSameSetupComment(const DALExecPendingOrder &pending, const DALExecReversalSetup &setup)
{
   return (pending.found && setup.valid && pending.comment == setup.comment);
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
   DALExecReversalSetup setups[];
   string setup_reason = "";
   bool has_setups = BuildCurrentSetups(setups, setup_reason);

   if(!has_setups)
   {
      if(LogVerbose())
         Print("DAL_E0001_SKIP *** build=", DAL_E0001_BUILD, "*reason=", setup_reason, "*mode=h5_exact_reversal_r1");
      UpdateComment("no_h5_r1_setup_" + setup_reason);
      return;
   }

   int setup_count = ArraySize(setups);
   int submitted = 0;
   int skipped_existing = 0;
   int skipped_blocked = 0;
   int skipped_risk = 0;

   for(int i = 0; i < setup_count; i++)
   {
      DALExecReversalSetup setup = setups[i];
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
         // Since setups are sorted nearest-first, once max exposure is reached there
         // is no reason to scan/place farther orders on this cycle.
         if(StringFind(exposure_reason, "max_simultaneous", 0) >= 0)
            break;
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
      bool order_ok = PlaceSetupOrder(setup, risk, order_reason);
      if(order_ok)
         submitted++;

      if(LogOrders() || (InpTradingEnabled && !order_ok && LogErrors()))
      {
         Print(
            "DAL_E0001_ORDER *** build=", DAL_E0001_BUILD,
            "*mode=h5_exact_reversal_fixed_r",
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
         "*mode=h5_exact_reversal_r1",
         "*setups=", setup_count,
         "*submitted=", submitted,
         "*skippedExisting=", skipped_existing,
         "*skippedBlocked=", skipped_blocked,
         "*skippedRisk=", skipped_risk);
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

   if(LogErrors())
   {
      Print(
         "DAL_E0001_BUILD_SANITY *** build=", DAL_E0001_BUILD,
         "*symbol=", LabSymbol(),
         "*tf=", EnumToString(LabTimeframe()),
         "*module=EXECUTION_H0005_REVERSAL_FIXED_R1_EXACT_CANDIDATES",
         "*bars=", InpBars,
         "*maxZoneScanNodes=", InpMaxZoneScanNodes,
         "*h5Exact=LAST_ONLY_REVERSAL_NEXT_STRUCTURAL_ZONE_TOUCH",
         "*rewardR=", DoubleToString(InpRewardR, 4),
         "*entryModel=limit_at_touch_edge",
         "*researchEntryModel=touch_bar_close_in_M0005_report",
         "*stopModel=zone_edge",
         "*maxSimultaneousTrades=", InpMaxSimultaneousTrades,
         "*maxZoneScanNodes=", InpMaxZoneScanNodes,
         "*placeOneOrderPerSetup=", DAL_BoolToString(InpPlaceOneOrderPerSetup),
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
