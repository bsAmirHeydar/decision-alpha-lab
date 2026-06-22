//+------------------------------------------------------------------+
//| Decision Alpha Lab — E0007 Purple Source Extreme Executor         |
//| Template executor for L=2 purple/source/revisit extreme entries.  |
//+------------------------------------------------------------------+
#property strict
#property version   "1.00"
#property description "E0007: purple/source extreme execution template with L=2 default."

#include <Trade/Trade.mqh>
#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>
#include <DecisionAlphaLab/Execution/E0007/DAL_E0007Modules.mqh>

input string InpSymbol = "";
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpBars = 3500;

// Structural source map. The user examples were L=2.
input int InpSourceL = 2;
input double InpZoneRatio = 0.90;
input int InpExitGap = 6;
input int InpMaxEvents = 2000;

// Source/purple gates.
// 0 = no future/purple oracle; 500 = research mode for zones that already survived 500 bars.
input int InpMinSourceSurvivalBars = 0;
input double InpMinFirstReactionR = 2.0;
input bool InpRequireFirstTouchNotHunted = true;
input bool InpRequireSecondRevisitForEntry = true;
input bool InpAllowFirstTouchResearchEntry = false;
input int InpMaxTouchAgeBars = 2500;

// Entry families to test.
input ENUM_DAL_E0007_ENTRY_MODE InpEntryMode = DAL_E0007_ENTRY_SOURCE_SECOND_REVISIT;
input ENUM_DAL_E0007_STOP_MODE InpStopMode = DAL_E0007_STOP_SECONDARY_NODE;

// Target / exit.
input ENUM_DAL_E0007_TARGET_MODE InpTargetMode = DAL_E0007_TARGET_NTH_OPPOSITE_INTERNAL_NODE;
input double InpFixedRewardR = 0.0;
input int InpOppositeNodeTPCount = 3;

// Asymmetry gate.
input bool InpUseDestinationRFilter = true;
input int InpDestinationLookbackBars = 1500;
input double InpMinPotentialR = 40.0;

// Spread policy.
input double InpBuyEntrySpreadMultiplier = 1.0;
input double InpSellStopSpreadMultiplier = 1.0;

// Exposure / risk.
input long InpMagicNumber = 7007007;
input string InpOrderCommentPrefix = "DALE7";
input double InpRiskCash = 100.0;
input bool InpAllowMinLotIfRiskTooSmall = false;
input double InpCommissionPerLotRoundTurn = 0.0;
input int InpMaxBuyPending = 1;
input int InpMaxSellPending = 1;
input int InpMaxBuyPositions = 1;
input int InpMaxSellPositions = 1;

// Optional coarse HTF gate placeholder. This release keeps it off by default.
input bool InpUseHTFBiasFilter = false;
input ENUM_TIMEFRAMES InpHTFTimeframe = PERIOD_H1;
input int InpHTFL = 2;
input int InpHTFLookbackBars = 1500;

input bool InpTradingEnabled = true;
input bool InpRunOnInit = true;
input int InpUpdateEveryNBars = 1;
input bool InpPrintLogs = true;

#define DAL_E0007_BUILD "1.00"

CTrade g_trade;
datetime g_last_bar_time = 0;
int g_new_bar_counter = 0;

string E0007_Symbol()
{
   return (InpSymbol == "" ? _Symbol : InpSymbol);
}

ENUM_TIMEFRAMES E0007_Timeframe()
{
   return (InpTimeframe == PERIOD_CURRENT ? (ENUM_TIMEFRAMES)_Period : InpTimeframe);
}

void E0007_FillPolicies(
   DALE0007SourcePolicy &source,
   DALE0007PricingPolicy &pricing,
   DALE0007ExposurePolicy &exposure
)
{
   DAL_E0007_DefaultSourcePolicy(source);
   source.L = MathMax(1, InpSourceL);
   source.zone_ratio = MathMax(0.0, MathMin(0.9999, InpZoneRatio));
   source.exit_gap = MathMax(1, InpExitGap);
   source.max_events = MathMax(1, InpMaxEvents);
   source.min_source_survival_bars = MathMax(0, InpMinSourceSurvivalBars);
   source.min_first_reaction_r = MathMax(0.0, InpMinFirstReactionR);
   source.require_first_touch_not_hunted = InpRequireFirstTouchNotHunted;
   source.require_second_revisit_for_entry = InpRequireSecondRevisitForEntry;
   source.allow_first_touch_research_entry = InpAllowFirstTouchResearchEntry;
   source.max_touch_age_bars = MathMax(0, InpMaxTouchAgeBars);
   source.use_destination_r_filter = InpUseDestinationRFilter;
   source.destination_lookback_bars = MathMax(10, InpDestinationLookbackBars);
   source.min_potential_r = MathMax(0.0, InpMinPotentialR);
   source.use_htf_bias_filter = InpUseHTFBiasFilter;
   source.htf_timeframe = InpHTFTimeframe;
   source.htf_L = MathMax(1, InpHTFL);
   source.htf_lookback_bars = MathMax(100, InpHTFLookbackBars);

   DAL_E0007_DefaultPricingPolicy(pricing);
   pricing.entry_mode = InpEntryMode;
   pricing.stop_mode = InpStopMode;
   pricing.target_mode = InpTargetMode;
   pricing.buy_entry_spread_mult = MathMax(0.0, InpBuyEntrySpreadMultiplier);
   pricing.sell_stop_spread_mult = MathMax(0.0, InpSellStopSpreadMultiplier);
   pricing.fixed_reward_r = MathMax(0.0, InpFixedRewardR);
   pricing.opposite_node_count = MathMax(1, InpOppositeNodeTPCount);

   DAL_E0007_DefaultExposurePolicy(exposure);
   exposure.max_buy_pending = MathMax(0, InpMaxBuyPending);
   exposure.max_sell_pending = MathMax(0, InpMaxSellPending);
   exposure.max_buy_positions = MathMax(0, InpMaxBuyPositions);
   exposure.max_sell_positions = MathMax(0, InpMaxSellPositions);
}

bool E0007_LoadMap(
   const string symbol,
   const ENUM_TIMEFRAMES tf,
   const int bars_requested,
   const int L,
   const double zone_ratio,
   const int exit_gap,
   const int max_events,
   DALBar &bars[],
   int &bars_count,
   DALLRuleNode &nodes[],
   int &nodes_count,
   DALM0001Event &events[],
   int &events_count,
   string &reason
)
{
   bars_count = DAL_LoadBarsChronological(symbol, tf, bars_requested, true, bars);
   if(bars_count <= 0)
   {
      reason = "bars_load_failed";
      return false;
   }

   nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, MathMax(1, L), nodes);
   if(nodes_count <= 0)
   {
      reason = "no_nodes";
      return false;
   }

   DALM0001Config cfg;
   DAL_M0001DefaultConfig(cfg);
   cfg.L = MathMax(1, L);
   cfg.zone_ratio = MathMax(0.0, MathMin(0.9999, zone_ratio));
   cfg.exit_gap = MathMax(1, exit_gap);
   cfg.consume_mode = DAL_M0001_CONSUME_BY_HUNT;
   cfg.consume_on_touch = false;
   cfg.max_events = MathMax(1, max_events);
   cfg.min_rtv = 0.0;

   events_count = DAL_M0001ComputeEvents(bars, bars_count, nodes, nodes_count, cfg, events);
   if(events_count <= 0)
   {
      reason = "no_m0001_events";
      return false;
   }

   reason = "ok";
   return true;
}

void E0007_Process(const string run_mode)
{
   string symbol = E0007_Symbol();
   ENUM_TIMEFRAMES tf = E0007_Timeframe();

   DALE0007SourcePolicy source;
   DALE0007PricingPolicy pricing;
   DALE0007ExposurePolicy exposure;
   E0007_FillPolicies(source, pricing, exposure);

   DALBar bars[];
   DALLRuleNode nodes[];
   DALM0001Event events[];
   int bars_count = 0, nodes_count = 0, events_count = 0;
   string load_reason = "";

   if(!E0007_LoadMap(symbol, tf, InpBars, source.L, source.zone_ratio, source.exit_gap, source.max_events,
                    bars, bars_count, nodes, nodes_count, events, events_count, load_reason))
   {
      if(InpPrintLogs)
         Print("DAL_E0007_SKIP *** build=", DAL_E0007_BUILD, "*runMode=", run_mode, "*reason=", load_reason);
      return;
   }

   int tp_checked=0, tp_modified=0, tp_waiting=0, tp_rejected=0;
   if(InpTargetMode == DAL_E0007_TARGET_NTH_OPPOSITE_INTERNAL_NODE)
      DAL_E0007SyncOppositeNodeTP(symbol, InpMagicNumber, InpOrderCommentPrefix, nodes, nodes_count, pricing.opposite_node_count,
                                  g_trade, tp_checked, tp_modified, tp_waiting, tp_rejected);

   DALE0007Candidate candidates[];
   int candidates_count = DAL_E0007BuildCandidates(symbol, bars, bars_count, nodes, nodes_count, events, events_count,
                                                   source, pricing, candidates);

   int sent = 0, rejected = 0, scanned = 0;
   for(int i = 0; i < candidates_count; i++)
   {
      scanned++;
      string send_reason = "";
      bool ok = false;
      if(InpTradingEnabled)
         ok = DAL_E0007SendCandidateLimit(symbol, InpMagicNumber, InpRiskCash, InpCommissionPerLotRoundTurn,
                                          InpAllowMinLotIfRiskTooSmall, exposure, InpOrderCommentPrefix,
                                          candidates[i], g_trade, send_reason);
      else
      {
         ok = true;
         send_reason = "trading_disabled_plan_only";
      }

      if(ok)
      {
         sent++;
         if(InpPrintLogs)
            Print("DAL_E0007_PLAN *** build=", DAL_E0007_BUILD,
               "*mode=", DAL_E0007EntryModeName(candidates[i].entry_mode),
               "*role=", DAL_E0007RoleName(candidates[i].role),
               "*dir=", candidates[i].direction,
               "*originNode=", candidates[i].origin_node_id,
               "*event=", candidates[i].source_event_id,
               "*entry=", DoubleToString(candidates[i].entry, _Digits),
               "*sl=", DoubleToString(candidates[i].sl, _Digits),
               "*tp=", DoubleToString(candidates[i].tp, _Digits),
               "*risk=", DoubleToString(candidates[i].risk_distance, _Digits),
               "*firstReactionR=", DoubleToString(candidates[i].first_reaction_r, 2),
               "*potentialR=", DoubleToString(candidates[i].potential_r, 2),
               "*destination=", DoubleToString(candidates[i].destination_price, _Digits),
               "*secondary=", DAL_BoolToString(candidates[i].has_secondary_node),
               "*reason=", send_reason);
      }
      else
      {
         rejected++;
         if(InpPrintLogs)
            Print("DAL_E0007_REJECT *** build=", DAL_E0007_BUILD,
               "*candidateReason=", candidates[i].reason,
               "*sendReason=", send_reason);
      }
   }

   if(InpPrintLogs)
   {
      Print("DAL_E0007_AUDIT *** build=", DAL_E0007_BUILD,
         "*runMode=", run_mode,
         "*symbol=", symbol,
         "*tf=", EnumToString(tf),
         "*L=", source.L,
         "*bars=", bars_count,
         "*nodes=", nodes_count,
         "*events=", events_count,
         "*entryMode=", DAL_E0007EntryModeName(pricing.entry_mode),
         "*stopMode=", DAL_E0007StopModeName(pricing.stop_mode),
         "*survivalBars=", source.min_source_survival_bars,
         "*minFirstReactionR=", DoubleToString(source.min_first_reaction_r, 2),
         "*minPotentialR=", DoubleToString(source.min_potential_r, 2),
         "*candidates=", candidates_count,
         "*scanned=", scanned,
         "*sentOrPlanned=", sent,
         "*rejected=", rejected,
         "*tpChecked=", tp_checked,
         "*tpModified=", tp_modified,
         "*tpWaiting=", tp_waiting,
         "*tpRejected=", tp_rejected);
   }
}

int OnInit()
{
   g_trade.SetExpertMagicNumber(InpMagicNumber);

   Print("DAL_E0007_BUILD_SANITY *** build=", DAL_E0007_BUILD,
      "*module=E0007_PURPLE_SOURCE_EXTREME_EXECUTOR",
      "*defaultL=2",
      "*entryMode=", DAL_E0007EntryModeName(InpEntryMode),
      "*stopMode=", DAL_E0007StopModeName(InpStopMode),
      "*targetMode=", IntegerToString((int)InpTargetMode),
      "*minPotentialR=", DoubleToString(InpMinPotentialR, 2),
      "*note=purple_is_context_not_signal");

   if(InpRunOnInit)
      E0007_Process("INIT");

   return INIT_SUCCEEDED;
}

void OnTick()
{
   string symbol = E0007_Symbol();
   ENUM_TIMEFRAMES tf = E0007_Timeframe();

   datetime open_time = iTime(symbol, tf, 0);
   if(open_time <= 0)
      return;
   if(open_time == g_last_bar_time)
      return;

   g_last_bar_time = open_time;
   g_new_bar_counter++;

   int every = MathMax(1, InpUpdateEveryNBars);
   if((g_new_bar_counter % every) != 0)
      return;

   E0007_Process("NEW_BAR");
}
