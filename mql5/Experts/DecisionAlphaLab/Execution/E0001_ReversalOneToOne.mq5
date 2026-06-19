//+------------------------------------------------------------------+
//| Decision Alpha Lab — E0001 Reversal One-to-One Executor           |
//| Execution layer: raw reversal 1:R pending-limit executor.          |
//+------------------------------------------------------------------+
#property strict
#property version   "1.00"
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
input int InpBars = 5000;

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

// Safety/debug.
input bool InpPlaceOneOrderPerSetup = true;
input bool InpPrintEveryDecision = true;

#define DAL_E0001_BUILD "1.00"

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
   Comment(
      "Decision Alpha Lab | E0001 Reversal 1:R Executor\n",
      "build=", DAL_E0001_BUILD,
      "  state=", state,
      "  trading=", DAL_BoolToString(InpTradingEnabled), "\n",
      "symbol=", LabSymbol(),
      "  tf=", EnumToString(LabTimeframe()),
      "  riskCash=", DoubleToString(InpRiskCash, 2),
      "  commissionRT/lot=", DoubleToString(InpCommissionPerLotRoundTurn, 2), "\n",
      "rewardR=", DoubleToString(InpRewardR, 2),
      "  maxSimultaneous=", InpMaxSimultaneousTrades,
      "  allowOpposite=", DAL_BoolToString(InpAllowOppositeTrades), "\n",
      "logic: LAST_ONLY reversal regime -> newest untouched structural zone -> limit entry at near edge -> stop at far zone edge -> TP=R multiple"
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

   DALM0002BranchSample all_samples[], rev_samples[], cont_samples[];
   DALM0002Audit audit;
   DAL_M0002CollectBranchSamples(events, events_count, bars, bars_count, 0, m2, all_samples, rev_samples, cont_samples, audit);

   return DAL_ExecBuildReversalOneToOneSetup(
      bars,
      bars_count,
      nodes,
      nodes_count,
      events,
      events_count,
      all_samples,
      ArraySize(all_samples),
      m1.zone_ratio,
      InpRewardR,
      InpOrderCommentPrefix,
      setup
   );
}

void TryPlaceSetup()
{
   DALExecReversalSetup setup;
   bool setup_ok = BuildCurrentSetup(setup);

   if(!setup_ok)
   {
      if(InpPrintEveryDecision)
         Print("DAL_E0001_DECISION *** build=", DAL_E0001_BUILD, "*symbol=", LabSymbol(), "*tf=", EnumToString(LabTimeframe()), "*", DAL_ExecReversalSetupToLog(setup));
      UpdateComment("no_setup_" + setup.reason);
      return;
   }

   if(InpPlaceOneOrderPerSetup && DAL_ExecOrderCommentExists(LabSymbol(), InpMagicNumber, setup.comment))
   {
      if(InpPrintEveryDecision)
         Print("DAL_E0001_DECISION *** build=", DAL_E0001_BUILD, "*symbol=", LabSymbol(), "*tf=", EnumToString(LabTimeframe()), "*duplicate=true*", DAL_ExecReversalSetupToLog(setup));
      UpdateComment("duplicate_setup");
      return;
   }

   string exposure_reason = "";
   if(!DAL_ExecCanOpenDirection(LabSymbol(), InpMagicNumber, setup.direction, InpMaxSimultaneousTrades, InpAllowOppositeTrades, exposure_reason))
   {
      if(InpPrintEveryDecision)
         Print("DAL_E0001_DECISION *** build=", DAL_E0001_BUILD, "*symbol=", LabSymbol(), "*tf=", EnumToString(LabTimeframe()), "*exposureOk=false*exposureReason=", exposure_reason, "*", DAL_ExecReversalSetupToLog(setup));
      UpdateComment("blocked_" + exposure_reason);
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
      Print("DAL_E0001_RISK_REJECT *** build=", DAL_E0001_BUILD, "*symbol=", LabSymbol(), "*tf=", EnumToString(LabTimeframe()), "*", DAL_ExecReversalSetupToLog(setup), "*", DAL_ExecRiskSizingToLog(risk));
      UpdateComment("risk_reject_" + risk.reason);
      return;
   }

   string order_reason = "dry_run";
   bool order_ok = false;
   if(InpTradingEnabled)
   {
      order_ok = DAL_ExecPlaceLimitOrder(
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

   Print(
      "DAL_E0001_ORDER_DECISION *** build=", DAL_E0001_BUILD,
      "*symbol=", LabSymbol(),
      "*tf=", EnumToString(LabTimeframe()),
      "*tradingEnabled=", DAL_BoolToString(InpTradingEnabled),
      "*orderSent=", DAL_BoolToString(order_ok),
      "*orderReason=", order_reason,
      "*", DAL_ExecReversalSetupToLog(setup),
      "*", DAL_ExecRiskSizingToLog(risk)
   );

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

   Print(
      "DAL_E0001_BUILD_SANITY *** build=", DAL_E0001_BUILD,
      "*symbol=", LabSymbol(),
      "*tf=", EnumToString(LabTimeframe()),
      "*module=EXECUTION_REVERSAL_ONE_TO_ONE",
      "*tradingEnabledDefault=false",
      "*regimeSource=LAST_ONLY",
      "*entry=limit_at_next_structural_zone_near_edge",
      "*stop=structural_zone_far_edge",
      "*tp=InpRewardR_multiple",
      "*riskSizing=cash_risk_including_round_turn_commission",
      "*maxSimultaneousInput=", InpMaxSimultaneousTrades,
      "*allowOppositeInput=", DAL_BoolToString(InpAllowOppositeTrades)
   );

   UpdateComment("initialized");
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   Comment("");
}

void OnTick()
{
   if(!HasNewClosedCandle())
      return;

   TryPlaceSetup();
}
