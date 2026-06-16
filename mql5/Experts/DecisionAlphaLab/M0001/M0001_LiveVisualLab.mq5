//+------------------------------------------------------------------+
//| Decision Alpha Lab — M0001 MQL-Native Live Visual Lab            |
//| Python-free runtime. MQL5 is the source of truth.                |
//+------------------------------------------------------------------+
#property strict
#property version   "1.39"
#property description "M0001 native MQL5 structural node and RTV visual lab"

#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/Market/DAL_LiveBarStream.mqh>
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001AuditState.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Visual.mqh>
#include <DecisionAlphaLab/Research/DAL_ValidationJournal.mqh>

input string InpSymbol = "";                 // empty = chart symbol
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpBars = 0;                      // DATA limit: 0 = all tester/history bars; >0 = cap data/rolling stream
input bool InpUseLiveBarStream = true;        // true = no bulk copy; append each newly closed candle
input int InpWarmupHistoricalBars = 0;        // 0 = start from next closed candle; >0 = optional past context
input bool InpStartFromNextClosedBar = true;  // true = do not process the already closed bar at attach time
input bool InpClosedBarsOnly = true;          // retained for non-stream fallback mode
input bool InpComputeOnEveryTick = false;     // stream mode still processes only newly closed bars
input int InpTimerMilliseconds = 100;

input int InpL = 5;
input double InpZoneRatio = 0.90;
input int InpExitGap = 6;
input ENUM_DALM0001ConsumeMode InpConsumeMode = DAL_M0001_CONSUME_BY_HUNT;
input bool InpConsumeOnTouch = false;        // deprecated alias: true forces TOUCH_ZONE mode
input double InpMinRtv = 0.0;
input int InpMaxEvents = 0;                 // 0 = unlimited computed events

input string InpObjectPrefix = "DAL_MQL_M0001_";
input bool InpDrawOnlyVisibleWindow = true;    // render only current chart viewport to avoid MT5 object overload
input int InpVisibleWindowPaddingBars = 80;    // extra bars around viewport for smooth scroll/zoom
input bool InpRedrawOnChartChange = true;      // redraw viewport objects when chart is scrolled/zoomed
input bool InpPurgeTraceLines = true;          // delete trend/channel trace lines from chart on each redraw
input bool InpPurgeMainWindowIndicators = true; // remove ZigZag/indicator traces from main chart window on init
input bool InpShowNodes = true;
input bool InpShowNodePrices = true;        // true = show node price as local text label, not horizontal line
input bool InpShowNodePriceLines = false;     // deprecated/ignored: M0001 no longer draws full-chart node price lines
input bool InpShowActiveFrom = false;
input bool InpShowEvents = false;
input bool InpShowRtvLabels = false;
input bool InpShowHunts = true;
input bool InpShowExpansionExtremes = true;     // draw node -> expansion extreme audit line
input bool InpShowConsumedExtremeHistory = true; // keep final extreme line after consumption, without extending it
input bool InpShowLiveHuntZones = true;         // draw active live hunt/territory rectangle until consumed/live bar
input bool InpShowInvalidatedHuntZones = false; // deprecated alias
input bool InpShowConsumedHuntZoneHistory = true; // keep consumed zones drawn until consume candle
input bool InpShowConsumedNodeMarkers = true;   // mark the candle where a node is consumed/hunted
input bool InpShowSummary = true;
input bool InpShowNodeVisibilityDebug = true; // summary shows latest computed node and visual caps
input int InpMaxNodesToDraw = 0;            // VISUAL limit: 0 = draw all, >0 = draw latest N nodes
input int InpMaxEventsToDraw = 0;             // VISUAL limit: 0 = draw all, >0 = draw latest N events
input int InpMaxAuditStatesToDraw = 0;        // VISUAL limit: 0 = draw all, >0 = draw latest N audit states
input int InpNodeMarkerStyle = 0;            // deprecated/ignored: strict mode always uses clean arrows
input int InpNodeArrowWidth = 2;
input double InpNodeChevronPoints = 70.0;    // used only when InpNodeMarkerStyle = 1
input double InpNodeChevronBars = 0.28;      // used only when InpNodeMarkerStyle = 1
input int InpNodeChevronWidth = 2;           // used only when InpNodeMarkerStyle = 1
input double InpHighNodePriceTextGapPoints = 120.0;
input double InpLowNodePriceTextGapPoints = 120.0;
input int InpNodePriceTextFontSize = 9;

input bool InpWriteValidationJournal = false;
input string InpJournalPrefix = "DecisionAlphaLab\\M0001\\";

datetime g_last_bar_time = 0;
datetime g_last_closed_stream_bar_time = 0;
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

void BuildConfig(DALM0001Config &config)
{
   DAL_M0001DefaultConfig(config);
   config.L = InpL;
   config.zone_ratio = InpZoneRatio;
   config.exit_gap = InpExitGap;
   config.consume_mode = InpConsumeMode;
   config.consume_on_touch = InpConsumeOnTouch;

   if(config.consume_on_touch)
      config.consume_mode = DAL_M0001_CONSUME_BY_TOUCH;

   config.max_events = InpMaxEvents;
   config.min_rtv = InpMinRtv;
}

bool ResolveChartVisibleTimeWindow(
   datetime &window_from,
   datetime &window_to
)
{
   if(!InpDrawOnlyVisibleWindow)
      return false;

   long first_visible = 0;
   long visible_bars = 0;

   if(!ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR, 0, first_visible))
      return false;

   if(!ChartGetInteger(0, CHART_VISIBLE_BARS, 0, visible_bars))
      return false;

   if(first_visible < 0 || visible_bars <= 0)
      return false;

   int padding = InpVisibleWindowPaddingBars;
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
   visual.prefix = InpObjectPrefix;
   visual.show_nodes = InpShowNodes;
   visual.show_node_prices = InpShowNodePrices;
   // Hard-disabled: full-chart node price lines create visual noise.
   // Use InpShowNodePrices for local text labels above/below node markers.
   visual.show_node_price_lines = false;
   visual.show_active_from = InpShowActiveFrom;
   visual.show_events = InpShowEvents;
   visual.show_rtv_labels = InpShowRtvLabels;
   visual.show_hunts = InpShowHunts;
   visual.show_node_visibility_debug = InpShowNodeVisibilityDebug;
   visual.show_expansion_extreme_lines = InpShowExpansionExtremes;
   visual.show_consumed_extreme_history = InpShowConsumedExtremeHistory;
   visual.show_live_hunt_zones = InpShowLiveHuntZones;
   visual.show_invalidated_hunt_zones = InpShowInvalidatedHuntZones;
   visual.show_consumed_hunt_zone_history = InpShowConsumedHuntZoneHistory;
   visual.show_consumed_node_markers = InpShowConsumedNodeMarkers;
   visual.max_nodes = InpMaxNodesToDraw;
   visual.max_events = InpMaxEventsToDraw;
   visual.max_audit_states = InpMaxAuditStatesToDraw;
   // Hard-disabled: chevron mode creates diagonal high/low trace lines.
   visual.node_marker_style = 0;
   visual.node_arrow_width = InpNodeArrowWidth;
   visual.chevron_points = InpNodeChevronPoints;
   visual.chevron_bars = InpNodeChevronBars;
   visual.chevron_width = InpNodeChevronWidth;
   visual.high_node_price_text_gap_points = InpHighNodePriceTextGapPoints;
   visual.low_node_price_text_gap_points = InpLowNodePriceTextGapPoints;
   visual.node_price_text_font_size = InpNodePriceTextFontSize;

   datetime visible_from = 0;
   datetime visible_to = 0;
   visual.use_time_window = ResolveChartVisibleTimeWindow(visible_from, visible_to);
   visual.time_window_from = visible_from;
   visual.time_window_to = visible_to;
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

   DALM0001VisualConfig visual;
   BuildVisualConfig(visual);

   if(InpPurgeTraceLines)
      DAL_DeleteTraceLineObjects();

   DAL_DeleteM0001VisualArtifacts(InpObjectPrefix);
   DAL_M0001DrawNodes(nodes, nodes_count, visual, LabTimeframe());
   DAL_M0001DrawAuditStates(audit_states, audit_states_count, visual);
   DAL_M0001DrawEvents(events, events_count, visual);

   if(InpShowSummary)
      DAL_M0001DrawSummary(InpObjectPrefix, bars_count, nodes_count, events_count, audit_states_count, config, visual, nodes);

   if(InpWriteValidationJournal)
   {
      string node_file = InpJournalPrefix + LabSymbol() + "_M0001_nodes.csv";
      string audit_file = InpJournalPrefix + LabSymbol() + "_M0001_node_audit_states.csv";
      string event_file = InpJournalPrefix + LabSymbol() + "_M0001_events.csv";
      DAL_WriteM0001NodeJournal(node_file, nodes, nodes_count);
      DAL_WriteM0001NodeAuditStateJournal(audit_file, audit_states, audit_states_count);
      DAL_WriteM0001EventJournal(event_file, events, events_count);
   }

   ChartRedraw(0);

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

void InitializeLiveBarStream()
{
   if(g_live_stream_initialized)
      return;

   ArrayResize(g_live_bars, 0);
   g_live_bars_count = 0;
   g_last_closed_stream_bar_time = 0;

   if(InpWarmupHistoricalBars > 0)
   {
      DAL_WarmupClosedBarsByShift(
         LabSymbol(),
         LabTimeframe(),
         InpWarmupHistoricalBars,
         InpBars,
         g_live_bars,
         g_live_bars_count
      );

      if(g_live_bars_count > 0)
         g_last_closed_stream_bar_time = g_live_bars[g_live_bars_count - 1].time;
   }
   else if(InpStartFromNextClosedBar)
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

   return DAL_AppendLatestClosedBarIfNew(
      LabSymbol(),
      LabTimeframe(),
      InpBars,
      g_live_bars,
      g_live_bars_count,
      g_last_closed_stream_bar_time
   );
}

void RunM0001()
{
   if(InpUseLiveBarStream)
   {
      InitializeLiveBarStream();
      RunM0001FromBars(g_live_bars, g_live_bars_count, "live_stream");
      return;
   }

   DALBar bars[];
   int bars_count = DAL_LoadBarsChronological(LabSymbol(), LabTimeframe(), InpBars, InpClosedBarsOnly, bars);
   RunM0001FromBars(bars, bars_count, "fallback_copyrates");
}

int OnInit()
{
   if(InpPurgeMainWindowIndicators)
      DAL_DeleteMainWindowIndicators();

   if(InpUseLiveBarStream)
   {
      InitializeLiveBarStream();
      if(g_live_bars_count > 0)
         RunM0001FromBars(g_live_bars, g_live_bars_count, "live_stream_init");
      else
         Print("DAL M0001 MQL-NATIVE | live stream initialized empty; waiting for next closed candle");
   }
   else
   {
      RunM0001();
   }

   if(InpTimerMilliseconds > 0)
      EventSetMillisecondTimer(InpTimerMilliseconds);

   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   DAL_DeleteM0001VisualArtifacts(InpObjectPrefix);
}

void OnTick()
{
   if(InpUseLiveBarStream)
   {
      if(UpdateLiveBarStream())
         RunM0001FromBars(g_live_bars, g_live_bars_count, "live_stream_new_bar");
      return;
   }

   datetime current_bar = iTime(LabSymbol(), LabTimeframe(), 0);
   if(InpComputeOnEveryTick || current_bar != g_last_bar_time)
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
   if(!InpRedrawOnChartChange)
      return;

   if(id == CHARTEVENT_CHART_CHANGE)
      RunM0001();
}

void OnTimer()
{
   if(InpUseLiveBarStream)
   {
      if(UpdateLiveBarStream())
         RunM0001FromBars(g_live_bars, g_live_bars_count, "live_stream_timer_new_bar");
      return;
   }

   if(InpComputeOnEveryTick)
      return;

   datetime current_bar = iTime(LabSymbol(), LabTimeframe(), 0);
   if(current_bar != g_last_bar_time)
   {
      g_last_bar_time = current_bar;
      RunM0001();
   }
}
