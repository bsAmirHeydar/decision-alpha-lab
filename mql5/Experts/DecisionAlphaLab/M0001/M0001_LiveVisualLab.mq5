//+------------------------------------------------------------------+
//| Decision Alpha Lab — M0001 MQL-Native Live Visual Lab            |
//| Python-free runtime. MQL5 is the source of truth.                |
//+------------------------------------------------------------------+
#property strict
#property version   "1.56"
#property description "M0001 native MQL5 structural node and RTV visual lab"

#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/Market/DAL_LiveBarStream.mqh>
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001AuditState.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Visual.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001RtvNullComparison.mqh>

input string InpSymbol = "";                 // empty = chart symbol
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpBars = 0;                       // 0 = no cap
input int InpWarmupHistoricalBars = 5000;     // pre-test closed bars used only to seed old nodes

input int InpL = 5;
input double InpZoneRatio = 0.90;
input int InpExitGap = 6;
input ENUM_DALM0001ConsumeMode InpConsumeMode = DAL_M0001_CONSUME_BY_HUNT;

input bool InpShowNodes = true;
input bool InpShowZones = true;
input bool InpShowRevisits = true;
input bool InpShowRTV = false;
input bool InpShowState = true;
input bool InpShowExtremes = false;
input bool InpShowSummary = true;

// Internal defaults kept out of the Inputs panel.
#define DAL_M0001_OBJECT_PREFIX "DAL_MQL_M0001_"
#define DAL_M0001_USE_LIVE_BAR_STREAM true
#define DAL_M0001_START_FROM_NEXT_CLOSED_BAR true
#define DAL_M0001_CLOSED_BARS_ONLY true
#define DAL_M0001_COMPUTE_ON_EVERY_TICK false
#define DAL_M0001_TIMER_MS 100

#define DAL_M0001_DRAW_ONLY_VISIBLE_WINDOW true
#define DAL_M0001_VISIBLE_WINDOW_PADDING_BARS 80
#define DAL_M0001_REDRAW_ON_CHART_CHANGE true
#define DAL_M0001_PURGE_TRACE_LINES true
#define DAL_M0001_PURGE_MAIN_WINDOW_INDICATORS true

#define DAL_M0001_SHOW_NODE_PRICES true
#define DAL_M0001_SHOW_ACTIVE_FROM false
#define DAL_M0001_SHOW_EVENTS false
#define DAL_M0001_SHOW_RTV_LABELS false
#define DAL_M0001_SHOW_NODE_VISIBILITY_DEBUG false
#define DAL_M0001_SHOW_CONSUMED_HISTORY true

#define DAL_M0001_MAX_EVENTS 0
#define DAL_M0001_MIN_RTV 0.0
#define DAL_M0001_PRINT_RUN_STATUS false
#define DAL_M0001_MAX_NODES_TO_DRAW 0
#define DAL_M0001_MAX_EVENTS_TO_DRAW 0
#define DAL_M0001_MAX_AUDIT_STATES_TO_DRAW 0

#define DAL_M0001_NODE_ARROW_WIDTH 2
#define DAL_M0001_HIGH_NODE_PRICE_TEXT_GAP_POINTS 120.0
#define DAL_M0001_LOW_NODE_PRICE_TEXT_GAP_POINTS 120.0
#define DAL_M0001_NODE_PRICE_TEXT_FONT_SIZE 9

datetime g_last_bar_time = 0;
datetime g_last_closed_stream_bar_time = 0;
datetime g_analysis_start_time = 0;
bool g_live_stream_initialized = false;
DALBar g_live_bars[];
int g_live_bars_count = 0;


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

int DAL_M0001StreamMaxBars()
{
   if(InpBars <= 0)
      return 0;

   int warmup_bars = InpWarmupHistoricalBars;
   if(warmup_bars < 0)
      warmup_bars = 0;

   return InpBars + warmup_bars;
}

void BuildConfig(DALM0001Config &config)
{
   DAL_M0001DefaultConfig(config);
   config.L = InpL;
   config.zone_ratio = InpZoneRatio;
   config.exit_gap = InpExitGap;
   config.consume_mode = InpConsumeMode;
   config.consume_on_touch = false;

   if(config.consume_on_touch)
      config.consume_mode = DAL_M0001_CONSUME_BY_TOUCH;

   config.max_events = DAL_M0001_MAX_EVENTS;
   config.min_rtv = DAL_M0001_MIN_RTV;
}

bool ResolveChartVisibleTimeWindow(
   datetime &window_from,
   datetime &window_to
)
{
   if(!DAL_M0001_DRAW_ONLY_VISIBLE_WINDOW)
      return false;

   long first_visible = 0;
   long visible_bars = 0;

   if(!ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR, 0, first_visible))
      return false;

   if(!ChartGetInteger(0, CHART_VISIBLE_BARS, 0, visible_bars))
      return false;

   if(first_visible < 0 || visible_bars <= 0)
      return false;

   int padding = DAL_M0001_VISIBLE_WINDOW_PADDING_BARS;
   if(padding < 0)
      padding = 0;

   int left_shift = (int)first_visible + padding;
   int right_shift = (int)first_visible - (int)visible_bars + 1 - padding;

   if(right_shift < 0)
      right_shift = 0;

   datetime left_time = iTime(LabSymbol(), LabTimeframe(), left_shift);
   datetime right_time = iTime(LabSymbol(), LabTimeframe(), right_shift);

   if(left_time <= 0 || right_time <= 0)
      return false;

   if(left_time <= right_time)
   {
      window_from = left_time;
      window_to = right_time;
   }
   else
   {
      window_from = right_time;
      window_to = left_time;
   }

   return (window_from > 0 && window_to > 0 && window_to >= window_from);
}

void BuildVisualConfig(DALM0001VisualConfig &visual)
{
   DAL_M0001DefaultVisualConfig(visual);
   visual.prefix = DAL_M0001_OBJECT_PREFIX;
   visual.show_nodes = InpShowNodes;
   visual.show_node_prices = DAL_M0001_SHOW_NODE_PRICES;
   // Hard-disabled: full-chart node price lines create visual noise.
   // Use DAL_M0001_SHOW_NODE_PRICES for local text labels above/below node markers.
   visual.show_node_price_lines = false;
   visual.show_active_from = DAL_M0001_SHOW_ACTIVE_FROM;
   visual.show_events = DAL_M0001_SHOW_EVENTS;
   visual.show_rtv_labels = InpShowRTV;
   visual.show_revisit_labels = InpShowRevisits;
   visual.show_node_state_labels = InpShowState;
   visual.show_hunts = InpShowState;
   visual.show_node_visibility_debug = DAL_M0001_SHOW_NODE_VISIBILITY_DEBUG;
   visual.show_expansion_extreme_lines = InpShowExtremes;
   visual.show_consumed_extreme_history = DAL_M0001_SHOW_CONSUMED_HISTORY;
   visual.show_live_hunt_zones = InpShowZones;
   visual.show_invalidated_hunt_zones = false;
   visual.show_consumed_hunt_zone_history = DAL_M0001_SHOW_CONSUMED_HISTORY;
   visual.show_consumed_node_markers = InpShowState;
   visual.max_nodes = DAL_M0001_MAX_NODES_TO_DRAW;
   visual.max_events = DAL_M0001_MAX_EVENTS_TO_DRAW;
   visual.max_audit_states = DAL_M0001_MAX_AUDIT_STATES_TO_DRAW;
   // Hard-disabled: chevron mode creates diagonal high/low trace lines.
   visual.node_marker_style = 0;
   visual.node_arrow_width = DAL_M0001_NODE_ARROW_WIDTH;
   visual.chevron_points = 70.0;
   visual.chevron_bars = 0.28;
   visual.chevron_width = 2;
   visual.high_node_price_text_gap_points = DAL_M0001_HIGH_NODE_PRICE_TEXT_GAP_POINTS;
   visual.low_node_price_text_gap_points = DAL_M0001_LOW_NODE_PRICE_TEXT_GAP_POINTS;
   visual.node_price_text_font_size = DAL_M0001_NODE_PRICE_TEXT_FONT_SIZE;

   datetime visible_from = 0;
   datetime visible_to = 0;
   visual.use_time_window = ResolveChartVisibleTimeWindow(visible_from, visible_to);
   visual.time_window_from = visible_from;
   visual.time_window_to = visible_to;
}



void DAL_M0001UpdateRuntimeComment(
   const int bars_count,
   const int nodes_count,
   const int events_count,
   const int audit_states_count,
   const string source_mode
)
{
   string start_text = g_analysis_start_time > 0 ? TimeToString(g_analysis_start_time, TIME_DATE | TIME_MINUTES) : "pending";

   Comment(
      "Decision Alpha Lab | M0001 Runtime\n",
      "source=", source_mode,
      "  symbol=", LabSymbol(),
      "  tf=", EnumToString(LabTimeframe()), "\n",
      "bars=", bars_count,
      "  nodes=", nodes_count,
      "  events=", events_count,
      "  audit_states=", audit_states_count, "\n",
      "warmup_bars=", InpWarmupHistoricalBars,
      "  analysis_start=", start_text, "\n",
      "final node/random logRTV report prints once on deinit"
   );
}


void RunM0001FromBars(
   const DALBar &bars[],
   const int bars_count,
   const string source_mode
)
{
   if(bars_count <= 0)
      return;

   DALM0001Config config;
   BuildConfig(config);

   DALLRuleNode nodes[];
   int nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, config.L, nodes);

   DALM0001Event events[];
   int events_count = DAL_M0001ComputeEvents(bars, bars_count, nodes, nodes_count, config, events);

   DALM0001NodeAuditState audit_states[];
   int audit_states_count = DAL_M0001ComputeNodeAuditStates(bars, bars_count, nodes, nodes_count, config, audit_states);

   DAL_M0001UpdateRuntimeComment(bars_count, nodes_count, events_count, audit_states_count, source_mode);

   DALM0001VisualConfig visual;
   BuildVisualConfig(visual);

   if(DAL_M0001_PURGE_TRACE_LINES)
      DAL_DeleteTraceLineObjects();

   DAL_DeleteM0001VisualArtifacts(DAL_M0001_OBJECT_PREFIX);
   DAL_M0001DrawNodes(nodes, nodes_count, visual, LabTimeframe());
   DAL_M0001DrawAuditStates(audit_states, audit_states_count, visual, config);
   DAL_M0001DrawEvents(events, events_count, visual, config);

   if(InpShowSummary)
      DAL_M0001DrawSummary(DAL_M0001_OBJECT_PREFIX, bars_count, nodes_count, events_count, audit_states_count, config, visual, nodes);

   ChartRedraw(0);

   if(DAL_M0001_PRINT_RUN_STATUS)
   {
      Print(
         "DAL M0001 MQL-NATIVE | source=", source_mode,
         " bars=", bars_count,
         " nodes=", nodes_count,
         " events=", events_count,
         " L=", config.L,
         " zone=", DoubleToString(config.zone_ratio, 2),
         " gap=", config.exit_gap,
         " consume=", DAL_M0001ConsumeModeToString(config.consume_mode)
      );
   }
}

void InitializeLiveBarStream()
{
   if(g_live_stream_initialized)
      return;

   ArrayResize(g_live_bars, 0);
   g_live_bars_count = 0;
   g_last_closed_stream_bar_time = 0;

   int warmup_bars = InpWarmupHistoricalBars;
   if(warmup_bars < 0)
      warmup_bars = 0;

   if(warmup_bars > 0)
   {
      DAL_WarmupClosedBarsByShift(
         LabSymbol(),
         LabTimeframe(),
         warmup_bars,
         0,
         g_live_bars,
         g_live_bars_count
      );

      if(g_live_bars_count > 0)
         g_last_closed_stream_bar_time = g_live_bars[g_live_bars_count - 1].time;
   }
   else if(DAL_M0001_START_FROM_NEXT_CLOSED_BAR)
   {
      // Critical live-safe behavior:
      // Do not copy/process history at attach time. Start only when the next bar closes.
      g_last_closed_stream_bar_time = DAL_LastClosedBarTime(LabSymbol(), LabTimeframe());
   }

   g_live_stream_initialized = true;
}

bool UpdateLiveBarStream()
{
   InitializeLiveBarStream();

   int before_count = g_live_bars_count;

   bool appended = DAL_AppendLatestClosedBarIfNew(
      LabSymbol(),
      LabTimeframe(),
      DAL_M0001StreamMaxBars(),
      g_live_bars,
      g_live_bars_count,
      g_last_closed_stream_bar_time
   );

   if(appended && g_analysis_start_time <= 0 && g_live_bars_count > before_count)
      g_analysis_start_time = g_live_bars[g_live_bars_count - 1].time;

   return appended;
}


void DAL_M0001PrintFinalReportsFromBars(
   const DALBar &bars[],
   const int bars_count,
   const string source_mode
)
{
   if(bars_count <= 0)
      return;

   DALM0001Config config;
   BuildConfig(config);

   DALLRuleNode nodes[];
   int nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, config.L, nodes);

   DALM0001Event events[];
   int events_count = DAL_M0001ComputeEvents(bars, bars_count, nodes, nodes_count, config, events);

   DAL_M0001PrintFinalNodeRandomReports(
      events,
      events_count,
      bars,
      bars_count,
      LabSymbol(),
      EnumToString(LabTimeframe()),
      source_mode,
      g_analysis_start_time
   );
}

void DAL_M0001PrintFinalReports()
{
   if(DAL_M0001_USE_LIVE_BAR_STREAM)
   {
      DAL_M0001PrintFinalReportsFromBars(g_live_bars, g_live_bars_count, "final_live_stream");
      return;
   }

   DALBar bars[];
   int bars_count = DAL_LoadBarsChronological(LabSymbol(), LabTimeframe(), InpBars, DAL_M0001_CLOSED_BARS_ONLY, bars);
   DAL_M0001PrintFinalReportsFromBars(bars, bars_count, "final_copyrates");
}

void RunM0001()
{
   if(DAL_M0001_USE_LIVE_BAR_STREAM)
   {
      InitializeLiveBarStream();
      RunM0001FromBars(g_live_bars, g_live_bars_count, "live_stream");
      return;
   }

   DALBar bars[];
   int bars_count = DAL_LoadBarsChronological(LabSymbol(), LabTimeframe(), InpBars, DAL_M0001_CLOSED_BARS_ONLY, bars);
   RunM0001FromBars(bars, bars_count, "fallback_copyrates");
}

int OnInit()
{
   if(DAL_M0001_PURGE_MAIN_WINDOW_INDICATORS)
      DAL_DeleteMainWindowIndicators();

   if(DAL_M0001_USE_LIVE_BAR_STREAM)
   {
      InitializeLiveBarStream();
      DAL_M0001UpdateRuntimeComment(g_live_bars_count, 0, 0, 0, "live_stream_warmup_ready");
   }
   else
   {
      RunM0001();
   }

   if(DAL_M0001_TIMER_MS > 0)
      EventSetMillisecondTimer(DAL_M0001_TIMER_MS);

   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   DAL_M0001PrintFinalReports();

   EventKillTimer();
   Comment("");
   DAL_DeleteM0001VisualArtifacts(DAL_M0001_OBJECT_PREFIX);
}

void OnTick()
{
   if(DAL_M0001_USE_LIVE_BAR_STREAM)
   {
      if(UpdateLiveBarStream())
         RunM0001FromBars(g_live_bars, g_live_bars_count, "live_stream_new_bar");
      return;
   }

   datetime current_bar = iTime(LabSymbol(), LabTimeframe(), 0);
   if(DAL_M0001_COMPUTE_ON_EVERY_TICK || current_bar != g_last_bar_time)
   {
      g_last_bar_time = current_bar;
      RunM0001();
   }
}

void OnChartEvent(
   const int id,
   const long &lparam,
   const double &dparam,
   const string &sparam
)
{
   if(!DAL_M0001_REDRAW_ON_CHART_CHANGE)
      return;

   if(id == CHARTEVENT_CHART_CHANGE)
      RunM0001();
}

void OnTimer()
{
   if(DAL_M0001_USE_LIVE_BAR_STREAM)
   {
      if(UpdateLiveBarStream())
         RunM0001FromBars(g_live_bars, g_live_bars_count, "live_stream_timer_new_bar");
      return;
   }

   if(DAL_M0001_COMPUTE_ON_EVERY_TICK)
      return;

   datetime current_bar = iTime(LabSymbol(), LabTimeframe(), 0);
   if(current_bar != g_last_bar_time)
   {
      g_last_bar_time = current_bar;
      RunM0001();
   }
}
