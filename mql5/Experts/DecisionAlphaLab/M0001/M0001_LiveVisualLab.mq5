//+------------------------------------------------------------------+
//| Decision Alpha Lab — M0001 MQL-Native Live Visual Lab            |
//| Python-free runtime. MQL5 is the source of truth.                |
//+------------------------------------------------------------------+
#property strict
#property version   "1.10"
#property description "M0001 native MQL5 structural node and RTV visual lab"

#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/Market/DAL_LiveBarStream.mqh>
#include <DecisionAlphaLab/StructuralNodes/LRule/DAL_LRuleDetector.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Visual.mqh>
#include <DecisionAlphaLab/Research/DAL_ValidationJournal.mqh>

input string InpSymbol = "";                 // empty = chart symbol
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpBars = 800;                    // max rolling stream size
input bool InpUseLiveBarStream = true;        // true = no bulk copy; append each newly closed candle
input int InpWarmupHistoricalBars = 0;        // 0 = start from next closed candle; >0 = optional past context
input bool InpStartFromNextClosedBar = true;  // true = do not process the already closed bar at attach time
input bool InpClosedBarsOnly = true;          // retained for non-stream fallback mode
input bool InpComputeOnEveryTick = false;     // stream mode still processes only newly closed bars
input int InpTimerMilliseconds = 100;

input int InpL = 5;
input double InpZoneRatio = 0.90;
input int InpExitGap = 6;
input bool InpConsumeOnTouch = false;
input double InpMinRtv = 0.0;
input int InpMaxEvents = 300;

input string InpObjectPrefix = "DAL_MQL_M0001_";
input bool InpShowNodes = true;
input bool InpShowNodePrices = false;       // true = show node price as local text label, not horizontal line
input bool InpShowNodePriceLines = false;     // optional old behavior: horizontal full-chart price lines
input bool InpShowActiveFrom = false;
input bool InpShowEvents = false;
input bool InpShowRtvLabels = false;
input bool InpShowHunts = true;
input bool InpShowSummary = true;
input int InpMaxNodesToDraw = 120;
input int InpMaxEventsToDraw = 80;
input double InpNodeChevronPoints = 70.0;
input double InpNodeChevronBars = 0.28;
input int InpNodeChevronWidth = 2;
input double InpNodePriceTextGapPoints = 35.0;
input int InpNodePriceTextFontSize = 8;

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
   config.consume_on_touch = InpConsumeOnTouch;
   config.max_events = InpMaxEvents;
   config.min_rtv = InpMinRtv;
}

void BuildVisualConfig(DALM0001VisualConfig &visual)
{
   DAL_M0001DefaultVisualConfig(visual);
   visual.prefix = InpObjectPrefix;
   visual.show_nodes = InpShowNodes;
   visual.show_node_prices = InpShowNodePrices;
   visual.show_node_price_lines = InpShowNodePriceLines;
   visual.show_active_from = InpShowActiveFrom;
   visual.show_events = InpShowEvents;
   visual.show_rtv_labels = InpShowRtvLabels;
   visual.show_hunts = InpShowHunts;
   visual.max_nodes = InpMaxNodesToDraw;
   visual.max_events = InpMaxEventsToDraw;
   visual.chevron_points = InpNodeChevronPoints;
   visual.chevron_bars = InpNodeChevronBars;
   visual.chevron_width = InpNodeChevronWidth;
   visual.node_price_text_gap_points = InpNodePriceTextGapPoints;
   visual.node_price_text_font_size = InpNodePriceTextFontSize;
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
   int nodes_count = DAL_DetectLRuleNodes(bars, bars_count, config.L, nodes);

   DALM0001Event events[];
   int events_count = DAL_M0001ComputeEvents(bars, bars_count, nodes, nodes_count, config, events);

   DALM0001VisualConfig visual;
   BuildVisualConfig(visual);

   DAL_DeleteByPrefix(InpObjectPrefix);
   DAL_M0001DrawNodes(nodes, nodes_count, visual, LabTimeframe());
   DAL_M0001DrawEvents(events, events_count, visual);

   if(InpShowSummary)
      DAL_M0001DrawSummary(InpObjectPrefix, bars_count, nodes_count, events_count, config);

   if(InpWriteValidationJournal)
   {
      string node_file = InpJournalPrefix + LabSymbol() + "_M0001_nodes.csv";
      string event_file = InpJournalPrefix + LabSymbol() + "_M0001_events.csv";
      DAL_WriteM0001NodeJournal(node_file, nodes, nodes_count);
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
      " gap=", config.exit_gap
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
   DAL_DeleteByPrefix(InpObjectPrefix);
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
