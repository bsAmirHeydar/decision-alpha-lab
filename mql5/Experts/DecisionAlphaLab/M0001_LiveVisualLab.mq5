
//+------------------------------------------------------------------+
//| Decision Alpha Lab — M0001 Python-Brain Visual Lab               |
//| MQL is visual only. The Python M0001 engine is the single source  |
//| of truth for backtest, validation, export and live visual output. |
//+------------------------------------------------------------------+
#property strict
#property version   "6.20"
#property description "Python-brain M0001 visual lab: MQL draws the Python visual contract only"

input string InpFileName          = "DecisionAlphaLab\\M0001\\GOLD_M15_visual.csv";
input bool   InpAutoBuildFileName  = true;  // true: file is built from Python brain symbol/timeframe inputs
input string InpPythonConfigFile   = "DecisionAlphaLab\\M0001\\m0001_runtime_config.ini";
input bool   InpWritePythonConfig  = true;
input bool   InpUseCommonFiles     = true;  // true = use MetaQuotes Common\Files so Python and Strategy Tester see the same files

// Python brain parameters. MQL writes these into InpPythonConfigFile.
// The Python watcher reads this file and regenerates the visual contract.
// This keeps the metric brain in Python while still letting you change research
// parameters from the MT5 Expert inputs.
input string InpBrainSymbol        = "";     // empty = chart symbol
input string InpBrainTimeframe     = "";     // empty = chart timeframe
input int    InpBrainBars          = 1200;
input int    InpBrainL             = 5;
input double InpBrainZoneRatio     = 0.90;
input int    InpBrainExitGap       = 6;
input bool   InpBrainConsumeOnTouch= false;  // false = hunt mode, true = touch mode
input bool   InpBrainRandom        = false;
input int    InpBrainRandomCount   = 0;      // 0 = same count as actual references
input int    InpBrainRandomSeed    = 42;
input int    InpBrainRefreshMs     = 2000;   // Python watcher cadence hint

// Event bridge: MQL streams chart candles to Python on each new bar or tick.
// Python is still the brain; MQL only exports observed market data and draws results.
input bool   InpBridgeExportChartCandles = true;
input bool   InpBridgeOnEveryTick        = false; // false = new-bar event; true = every tick
input bool   InpBridgeClosedBarsOnly     = true;  // true = no forming candle; false = include current candle
input int    InpBridgeLookbackBars       = 0;     // 0 = InpBrainBars
input string InpBridgeCandlesFile        = "";    // empty = auto <symbol>_<tf>_candles.csv
input string InpBridgeStatusFile         = "";    // empty = auto <symbol>_<tf>_status.ini
input string InpBridgeParquetDir         = "";    // empty = auto DecisionAlphaLab\M0001\parquet\<symbol>_<tf>
input bool   InpShowBridgeStatusPanel    = true;

input string InpObjectPrefix      = "DAL_M0001_PY_";
input bool   InpDeleteOldObjects  = true;
input int    InpAutoReloadSeconds = 2;
input int    InpMaxObjects        = 2500;

// Package selector. Visual inputs below are all false by default.
// 0 Custom manual toggles
// 1 Structural Node Audit
// 2 Territory Construction Audit
// 3 Event Entry Exit Audit
// 4 Baseline vs Inside Sample Audit
// 5 RTV Formula Audit
// 6 Hunt Validation Audit
// 7 Live/Open Event Audit
// 8 Candle Classification Audit
// 9 State Machine Audit
// 10 Focused Event Inspector
// 11 Multi Event Overview
// 12 Full Research Lab
input int    InpViewPreset        = 0;

// Focus and filters
input int    InpFocusNodeId       = -1;
input int    InpFocusRevisitId    = -1;
input bool   InpOnlyActual        = true;
input bool   InpShowRandom        = false;
input bool   InpOnlyHunted        = false;
input bool   InpOnlyStrongRtv     = false;
input double InpStrongRtvLevel    = 1.25;
input double InpMinRtv            = 0.0; // 0 disables
input double InpMaxRtv            = 0.0; // 0 disables

// Visual toggles — all false by default for clean package-by-package inspection.
input bool   InpShowNodes                 = false;
input bool   InpShowNodePriceLines        = false;
input bool   InpShowActiveFromLines       = false;
input bool   InpShowConfirmationWindows   = false;
input bool   InpShowExpansionExtremes     = false;
input bool   InpShowTerritories           = false;
input bool   InpShowEventWindows          = false;
input bool   InpShowEntryExitMarkers      = false;
input bool   InpShowBeforeSamples         = false;
input bool   InpShowInsideSamples         = false;
input bool   InpShowOutsideActiveSamples  = false;
input bool   InpShowRtvLabels             = false;
input bool   InpShowRtvFormula            = false;
input bool   InpShowHunts                 = false;
input bool   InpShowEventInfo             = false;
input bool   InpShowCandleClassification  = false;
input bool   InpShowStateLabels           = false;
input bool   InpShowSummaryPanel          = false;

// Performance controls
input int    InpMaxNodesToDraw            = 150;
input int    InpMaxEventsToDraw           = 80;
input int    InpMaxSampleCandlesToDraw    = 300;
input bool   InpLightMode                 = true;

int g_drawn = 0;
int g_events_seen = 0;
int g_nodes_seen = 0;
int g_hunts_seen = 0;
double g_rtv_sum = 0.0;
int g_rtv_count = 0;
datetime g_last_bridge_bar_time = 0;
uint g_last_request_tick = 0;

//+------------------------------------------------------------------+
int OnInit()
{
   if(InpWritePythonConfig || InpBridgeExportChartCandles)
      BridgePulse("init");

   if(InpDeleteOldObjects)
      DeleteLabObjects();

   DrawFromCsv();

   if(InpAutoReloadSeconds > 0)
      EventSetTimer(InpAutoReloadSeconds);

   return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   EventKillTimer();
}

//+------------------------------------------------------------------+
void OnTick()
{
   if(!InpBridgeExportChartCandles)
      return;

   datetime current_bar_time = iTime(BrainSymbol(), BrainPeriod(), 0);
   if(InpBridgeOnEveryTick || current_bar_time != g_last_bridge_bar_time)
   {
      g_last_bridge_bar_time = current_bar_time;
      BridgePulse(InpBridgeOnEveryTick ? "tick" : "new_bar");
   }
}

//+------------------------------------------------------------------+
void OnTimer()
{
   if(InpBridgeExportChartCandles)
   {
      // Timer is used as a safety pulse. OnTick remains the true event trigger.
      if(InpBridgeOnEveryTick)
         BridgePulse("timer_tick_mode");
      else if(InpWritePythonConfig)
         WritePythonBrainConfig("timer_config");
   }
   else if(InpWritePythonConfig)
      WritePythonBrainConfig("timer_config");

   DeleteLabObjects();
   DrawFromCsv();
}

//+------------------------------------------------------------------+
void DrawFromCsv()
{
   g_drawn = 0;
   g_events_seen = 0;
   g_nodes_seen = 0;
   g_hunts_seen = 0;
   g_rtv_sum = 0.0;
   g_rtv_count = 0;

   string visualFile = VisualFileName();
   int handle = OpenTextRead(visualFile, '\n');
   if(handle == INVALID_HANDLE)
   {
      Print("Decision Alpha Lab: cannot open Python visual file: ", visualFile, " error=", GetLastError());
      DrawMessage("NO_PYTHON_FILE", "Waiting for Python visual contract:\n" + visualFile + "\nRoot: " + FileRootMode() + "\nRun Python event bridge with -EventBridge", clrTomato, 12, 18);
      if(InpShowBridgeStatusPanel)
         DrawBridgeStatusPanel();
      return;
   }

   bool header = true;
   int nodes_drawn = 0;
   int events_drawn = 0;
   int samples_drawn = 0;

   while(!FileIsEnding(handle) && g_drawn < InpMaxObjects)
   {
      string line = FileReadString(handle);
      StringTrimLeft(line);
      StringTrimRight(line);
      if(line == "")
         continue;

      if(header)
      {
         header = false;
         continue;
      }

      string f[];
      int n = StringSplit(line, ',', f);
      if(n < 13)
         continue;

      string kind       = Field(f, n, 0);
      string baseline   = Field(f, n, 1);
      string id         = Field(f, n, 2);
      string startStr   = Field(f, n, 3);
      string endStr     = Field(f, n, 4);
      string anchorStr  = Field(f, n, 5);
      double price      = ToDouble(Field(f, n, 6));
      double lower      = ToDouble(Field(f, n, 7));
      double upper      = ToDouble(Field(f, n, 8));
      string label      = Field(f, n, 9);
      string nodeType   = Field(f, n, 10);
      double rtv        = ToDouble(Field(f, n, 11));
      bool hunted       = ToBool(Field(f, n, 12));
      int nodeId        = ToInt(Field(f, n, 13));
      int revisitId     = ToInt(Field(f, n, 14));
      int entryIndex    = ToInt(Field(f, n, 15));
      int exitIndex     = ToInt(Field(f, n, 16));
      int candleIndex   = ToInt(Field(f, n, 17));
      double value1     = ToDouble(Field(f, n, 18));
      double value2     = ToDouble(Field(f, n, 19));
      string note       = Field(f, n, 20);

      UpdateStats(kind, rtv, hunted);

      if(!RowPassesFilters(kind, baseline, nodeId, revisitId, rtv, hunted))
         continue;

      if(kind == "NODE" && nodes_drawn >= InpMaxNodesToDraw)
         continue;
      if(IsEventKind(kind) && events_drawn >= InpMaxEventsToDraw)
         continue;
      if(IsSampleKind(kind) && samples_drawn >= InpMaxSampleCandlesToDraw)
         continue;
      if(!KindVisible(kind))
         continue;

      DrawRow(kind, baseline, id, startStr, endStr, anchorStr, price, lower, upper, label, nodeType, rtv, hunted, nodeId, revisitId, entryIndex, exitIndex, candleIndex, value1, value2, note);

      if(kind == "NODE") nodes_drawn++;
      if(IsEventKind(kind)) events_drawn++;
      if(IsSampleKind(kind)) samples_drawn++;
   }

   FileClose(handle);

   if(FlagSummaryPanel())
      DrawSummaryPanel();

   if(InpShowBridgeStatusPanel)
      DrawBridgeStatusPanel();

   ChartRedraw(0);
   Print("DAL M0001 PYTHON-BRAIN VISUAL | rows_drawn=", g_drawn, " events=", g_events_seen, " nodes=", g_nodes_seen, " file=", VisualFileName(), " config=", InpPythonConfigFile);
}

//+------------------------------------------------------------------+
void DrawRow(
   const string kind,
   const string baseline,
   const string id,
   const string startStr,
   const string endStr,
   const string anchorStr,
   const double price,
   const double lower,
   const double upper,
   const string label,
   const string nodeType,
   const double rtv,
   const bool hunted,
   const int nodeId,
   const int revisitId,
   const int entryIndex,
   const int exitIndex,
   const int candleIndex,
   const double value1,
   const double value2,
   const string note
)
{
   datetime startTime = ToTime(startStr);
   datetime endTime = ToTime(endStr);
   datetime anchorTime = ToTime(anchorStr);
   if(anchorTime == 0 && startTime != 0)
      anchorTime = startTime;

   if(kind == "NODE")
      DrawNode(id, anchorTime, price, nodeType, label, nodeId);
   else if(kind == "NODE_PRICE")
      DrawHLine(id, price, NodeColor(nodeType), "node price | " + label);
   else if(kind == "ACTIVE_FROM")
      DrawVLine(id, anchorTime, clrSilver, label);
   else if(kind == "CONFIRMATION_WINDOW")
      DrawConfirmation(id, startTime, endTime, lower, label);
   else if(kind == "EXPANSION_EXTREME")
      DrawHLine(id, price, clrOrange, label);
   else if(kind == "TERRITORY")
      DrawRect(id, startTime, endTime, upper, lower, clrDarkSlateGray, true, "territory | " + label);
   else if(kind == "EVENT")
      DrawRect(id, startTime, endTime, upper, lower, RtvColor(rtv), false, "event | RTV=" + DoubleToString(rtv, 4));
   else if(kind == "RTV_LABEL")
      DrawText(id, anchorTime, price, label, RtvColor(rtv), 8, note);
   else if(kind == "RTV_FORMULA")
      DrawText(id, anchorTime, price, label, clrWhite, 8, note);
   else if(kind == "ENTRY")
      DrawMarker(id, anchorTime, price, 233, clrLime, "ENTRY | " + note);
   else if(kind == "EXIT")
      DrawMarker(id, anchorTime, price, 234, clrGold, "EXIT | " + note);
   else if(kind == "HUNT")
      DrawMarker(id, anchorTime, price, 251, clrRed, "HUNT | " + note);
   else if(kind == "EVENT_INFO")
      DrawText(id, anchorTime, price, label, clrAqua, 8, note);
   else if(kind == "BEFORE_SAMPLE")
      DrawSample(id, anchorTime, lower, upper, clrViolet, "BEFORE log_move=" + DoubleToString(value1, 4));
   else if(kind == "INSIDE_SAMPLE")
      DrawSample(id, anchorTime, lower, upper, clrAqua, "INSIDE log_move=" + DoubleToString(value1, 4));
   else if(kind == "OUTSIDE_ACTIVE")
      DrawSample(id, anchorTime, lower, upper, clrOrange, "OUTSIDE-ACTIVE log_move=" + DoubleToString(value1, 4));

   g_drawn++;
}

//+------------------------------------------------------------------+
bool KindVisible(const string kind)
{
   if(kind == "NODE") return FlagNodes();
   if(kind == "NODE_PRICE") return FlagNodePriceLines();
   if(kind == "ACTIVE_FROM") return FlagActiveFromLines();
   if(kind == "CONFIRMATION_WINDOW") return FlagConfirmationWindows();
   if(kind == "EXPANSION_EXTREME") return FlagExpansionExtremes();
   if(kind == "TERRITORY") return FlagTerritories();
   if(kind == "EVENT") return FlagEventWindows();
   if(kind == "ENTRY" || kind == "EXIT") return FlagEntryExitMarkers();
   if(kind == "BEFORE_SAMPLE") return FlagBeforeSamples();
   if(kind == "INSIDE_SAMPLE") return FlagInsideSamples();
   if(kind == "OUTSIDE_ACTIVE") return FlagOutsideActiveSamples();
   if(kind == "RTV_LABEL") return FlagRtvLabels();
   if(kind == "RTV_FORMULA") return FlagRtvFormula();
   if(kind == "HUNT") return FlagHunts();
   if(kind == "EVENT_INFO") return FlagEventInfo();
   return false;
}

bool FlagNodes()                { return InpShowNodes                || InpViewPreset==1 || InpViewPreset==10 || InpViewPreset==11 || InpViewPreset==12; }
bool FlagNodePriceLines()       { return InpShowNodePriceLines       || InpViewPreset==1 || InpViewPreset==2  || InpViewPreset==6  || InpViewPreset==10 || InpViewPreset==12; }
bool FlagActiveFromLines()      { return InpShowActiveFromLines      || InpViewPreset==1 || InpViewPreset==12; }
bool FlagConfirmationWindows()  { return InpShowConfirmationWindows  || InpViewPreset==1 || InpViewPreset==12; }
bool FlagExpansionExtremes()    { return InpShowExpansionExtremes    || InpViewPreset==2 || InpViewPreset==10 || InpViewPreset==12; }
bool FlagTerritories()          { return InpShowTerritories          || InpViewPreset==2 || InpViewPreset==10 || InpViewPreset==12; }
bool FlagEventWindows()         { return InpShowEventWindows         || InpViewPreset==3 || InpViewPreset==10 || InpViewPreset==11 || InpViewPreset==12; }
bool FlagEntryExitMarkers()     { return InpShowEntryExitMarkers     || InpViewPreset==3 || InpViewPreset==10 || InpViewPreset==12; }
bool FlagBeforeSamples()        { return InpShowBeforeSamples        || InpViewPreset==4 || InpViewPreset==8  || InpViewPreset==10 || InpViewPreset==12; }
bool FlagInsideSamples()        { return InpShowInsideSamples        || InpViewPreset==4 || InpViewPreset==8  || InpViewPreset==10 || InpViewPreset==12; }
bool FlagOutsideActiveSamples() { return InpShowOutsideActiveSamples || InpViewPreset==4 || InpViewPreset==8  || InpViewPreset==12; }
bool FlagRtvLabels()            { return InpShowRtvLabels            || InpViewPreset==5 || InpViewPreset==10 || InpViewPreset==11 || InpViewPreset==12; }
bool FlagRtvFormula()           { return InpShowRtvFormula           || InpViewPreset==5 || InpViewPreset==10 || InpViewPreset==12; }
bool FlagHunts()                { return InpShowHunts                || InpViewPreset==6 || InpViewPreset==10 || InpViewPreset==11 || InpViewPreset==12; }
bool FlagEventInfo()            { return InpShowEventInfo            || InpViewPreset==5 || InpViewPreset==8  || InpViewPreset==9  || InpViewPreset==10 || InpViewPreset==12; }
bool FlagSummaryPanel()         { return InpShowSummaryPanel         || InpViewPreset==11 || InpViewPreset==12; }

//+------------------------------------------------------------------+
bool RowPassesFilters(const string kind, const string baseline, const int nodeId, const int revisitId, const double rtv, const bool hunted)
{
   if(InpOnlyActual && baseline != "actual")
      return false;
   if(!InpShowRandom && baseline == "random")
      return false;
   if(InpFocusNodeId >= 0 && nodeId != InpFocusNodeId)
      return false;
   if(InpFocusRevisitId >= 0 && revisitId != InpFocusRevisitId)
      return false;
   if(InpOnlyHunted && !hunted)
      return false;
   if(InpOnlyStrongRtv && rtv < InpStrongRtvLevel)
      return false;
   if(InpMinRtv > 0.0 && rtv > 0.0 && rtv < InpMinRtv)
      return false;
   if(InpMaxRtv > 0.0 && rtv > InpMaxRtv)
      return false;
   return true;
}

bool IsEventKind(const string kind)
{
   return (kind == "EVENT" || kind == "TERRITORY" || kind == "RTV_LABEL" || kind == "RTV_FORMULA" || kind == "HUNT" || kind == "ENTRY" || kind == "EXIT" || kind == "EVENT_INFO");
}

bool IsSampleKind(const string kind)
{
   return (kind == "BEFORE_SAMPLE" || kind == "INSIDE_SAMPLE" || kind == "OUTSIDE_ACTIVE");
}

void UpdateStats(const string kind, const double rtv, const bool hunted)
{
   if(kind == "NODE")
      g_nodes_seen++;
   if(kind == "EVENT")
      g_events_seen++;
   if(kind == "HUNT")
      g_hunts_seen++;
   if(kind == "RTV_LABEL" && rtv > 0.0)
   {
      g_rtv_sum += rtv;
      g_rtv_count++;
   }
}

//+------------------------------------------------------------------+
void DrawNode(const string id, const datetime t, const double price, const string nodeType, const string label, const int nodeId)
{
   string name = ObjName(id);
   int code = (nodeType == "LOW" ? 233 : 234);
   ObjectCreate(0, name, OBJ_ARROW, 0, t, price);
   ObjectSetInteger(0, name, OBJPROP_ARROWCODE, code);
   ObjectSetInteger(0, name, OBJPROP_COLOR, NodeColor(nodeType));
   ObjectSetInteger(0, name, OBJPROP_WIDTH, 1);
   ObjectSetString(0, name, OBJPROP_TOOLTIP, label);
}

void DrawHLine(const string id, const double price, const color c, const string tip)
{
   string name = ObjName(id);
   ObjectCreate(0, name, OBJ_HLINE, 0, 0, price);
   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_DOT);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, 1);
   ObjectSetString(0, name, OBJPROP_TOOLTIP, tip);
}

void DrawVLine(const string id, const datetime t, const color c, const string tip)
{
   string name = ObjName(id);
   ObjectCreate(0, name, OBJ_VLINE, 0, t, 0);
   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_DOT);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, 1);
   ObjectSetString(0, name, OBJPROP_TOOLTIP, tip);
}

void DrawConfirmation(const string id, const datetime startTime, const datetime endTime, const double price, const string tip)
{
   if(startTime == 0 || endTime == 0)
      return;
   DrawVLine(id + "_START", startTime, clrDimGray, "confirmation starts | " + tip);
   DrawVLine(id + "_ACTIVE", endTime, clrSilver, "active_from | " + tip);
}

void DrawRect(const string id, const datetime t1, const datetime t2, const double upper, const double lower, const color c, const bool fill, const string tip)
{
   if(t1 == 0 || t2 == 0 || upper == 0.0 || lower == 0.0)
      return;
   string name = ObjName(id);
   ObjectCreate(0, name, OBJ_RECTANGLE, 0, t1, upper, t2, lower);
   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_STYLE, fill ? STYLE_SOLID : STYLE_DASH);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, fill ? 1 : 2);
   ObjectSetInteger(0, name, OBJPROP_BACK, fill);
   ObjectSetInteger(0, name, OBJPROP_FILL, fill);
   ObjectSetString(0, name, OBJPROP_TOOLTIP, tip);
}

void DrawSample(const string id, const datetime t, const double low, const double high, const color c, const string tip)
{
   if(t == 0)
      return;
   datetime t2 = t + PeriodSeconds(_Period);
   string name = ObjName(id);
   ObjectCreate(0, name, OBJ_RECTANGLE, 0, t, high, t2, low);
   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, 1);
   ObjectSetInteger(0, name, OBJPROP_BACK, true);
   ObjectSetInteger(0, name, OBJPROP_FILL, false);
   ObjectSetString(0, name, OBJPROP_TOOLTIP, tip);
}

void DrawText(const string id, const datetime t, const double price, const string text, const color c, const int size, const string tip)
{
   if(t == 0 || price == 0.0)
      return;
   string name = ObjName(id);
   ObjectCreate(0, name, OBJ_TEXT, 0, t, price);
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, size);
   ObjectSetString(0, name, OBJPROP_FONT, "Consolas");
   ObjectSetString(0, name, OBJPROP_TOOLTIP, tip);
}

void DrawMarker(const string id, const datetime t, const double price, const int code, const color c, const string tip)
{
   if(t == 0 || price == 0.0)
      return;
   string name = ObjName(id);
   ObjectCreate(0, name, OBJ_ARROW, 0, t, price);
   ObjectSetInteger(0, name, OBJPROP_ARROWCODE, code);
   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, 2);
   ObjectSetString(0, name, OBJPROP_TOOLTIP, tip);
}

void DrawBridgeStatusPanel()
{
   string statusFile = StatusFileName();
   int handle = OpenTextRead(statusFile, '\n');
   if(handle == INVALID_HANDLE)
   {
      DrawMessage("BRIDGE_STATUS", "Python bridge status: waiting\n" + statusFile, clrDarkOrange, 12, 120);
      return;
   }

   string text = "Python bridge status";
   int lines = 0;
   while(!FileIsEnding(handle) && lines < 10)
   {
      string line = FileReadString(handle);
      StringTrimLeft(line);
      StringTrimRight(line);
      if(line != "")
      {
         text += "\n" + line;
         lines++;
      }
   }
   FileClose(handle);
   text += "\nArtifacts: " + ParquetArtifactDir();
   text += "\nFile root: " + FileRootMode();
   text += "\nNote: Parquet is Python-side source; CSV is only MQL render adapter.";
   DrawMessage("BRIDGE_STATUS", text, clrLightSteelBlue, 12, 120);
}

void DrawSummaryPanel()
{
   double mean_rtv = (g_rtv_count > 0 ? g_rtv_sum / g_rtv_count : 0.0);
   string text = "Decision Alpha Lab | M0001 Python Brain"
               + "\nMQL mode: VISUAL ONLY"
               + "\nFile: " + VisualFileName()
               + "\nPython params: " + BrainSymbol() + " " + BrainTimeframe() + " bars=" + IntegerToString(InpBrainBars)
               + " L=" + IntegerToString(InpBrainL) + " zone=" + DoubleToString(InpBrainZoneRatio, 2)
               + " gap=" + IntegerToString(InpBrainExitGap) + " mode=" + BrainMode()
               + "\nNodes: " + IntegerToString(g_nodes_seen)
               + " | Events: " + IntegerToString(g_events_seen)
               + " | Hunts: " + IntegerToString(g_hunts_seen)
               + "\nMean RTV: " + DoubleToString(mean_rtv, 3)
               + "\nPreset: " + IntegerToString(InpViewPreset)
               + "\nBridge: " + (InpBridgeExportChartCandles ? "MQL candles -> Python" : "config only")
               + " | trigger=" + (InpBridgeOnEveryTick ? "tick" : "new_bar")
               + "\nPython artifacts: Parquet | MQL adapter: CSV"
               + "\nFile root: " + FileRootMode();
   DrawMessage("SUMMARY", text, clrAqua, 12, 18);
}

void DrawMessage(const string id, const string text, const color c, const int x, const int y)
{
   string name = ObjName(id);
   ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0);
   ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_LEFT_UPPER);
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(0, name, OBJPROP_COLOR, c);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 9);
   ObjectSetString(0, name, OBJPROP_FONT, "Consolas");
   ObjectSetString(0, name, OBJPROP_TEXT, text);
}



//+------------------------------------------------------------------+
int OpenTextRead(const string file_name, const ushort delimiter)
{
   int flags = FILE_READ | FILE_TXT | FILE_ANSI;
   if(InpUseCommonFiles)
      flags |= FILE_COMMON;
   return FileOpen(file_name, flags, delimiter);
}

int OpenTextWrite(const string file_name)
{
   int flags = FILE_WRITE | FILE_TXT | FILE_ANSI;
   if(InpUseCommonFiles)
      flags |= FILE_COMMON;
   return FileOpen(file_name, flags);
}

int OpenCsvWrite(const string file_name, const ushort delimiter)
{
   int flags = FILE_WRITE | FILE_CSV | FILE_ANSI;
   if(InpUseCommonFiles)
      flags |= FILE_COMMON;
   return FileOpen(file_name, flags, delimiter);
}

string FileRootMode()
{
   return InpUseCommonFiles ? "COMMON\\Files" : "TERMINAL\\MQL5\\Files";
}

//+------------------------------------------------------------------+
void BridgePulse(const string reason)
{
   if(InpBridgeExportChartCandles)
      WriteChartCandlesForPython(reason);

   if(InpWritePythonConfig)
      WritePythonBrainConfig(reason);
}

void WritePythonBrainConfig(const string reason)
{
   int handle = OpenTextWrite(InpPythonConfigFile);
   if(handle == INVALID_HANDLE)
   {
      Print("Decision Alpha Lab: cannot write Python config file: ", InpPythonConfigFile, " error=", GetLastError());
      return;
   }

   string visualFile = VisualFileName();
   string candlesFile = CandlesFileName();
   string statusFile = StatusFileName();
   string requestId = RequestId(reason);
   g_last_request_tick = GetTickCount();

   FileWrite(handle, "request_id=" + requestId);
   FileWrite(handle, "trigger=" + reason);
   FileWrite(handle, "data_source=" + (InpBridgeExportChartCandles ? "mql_candles" : "cache"));
   FileWrite(handle, "symbol=" + BrainSymbol());
   FileWrite(handle, "timeframe=" + BrainTimeframe());
   FileWrite(handle, "bars=" + IntegerToString(InpBridgeBars()));
   FileWrite(handle, "L=" + IntegerToString(InpBrainL));
   FileWrite(handle, "zone_ratio=" + DoubleToString(InpBrainZoneRatio, 8));
   FileWrite(handle, "exit_gap=" + IntegerToString(InpBrainExitGap));
   FileWrite(handle, "mode=" + BrainMode());
   FileWrite(handle, "random=" + (InpBrainRandom ? "1" : "0"));
   FileWrite(handle, "random_count=" + IntegerToString(InpBrainRandomCount));
   FileWrite(handle, "seed=" + IntegerToString(InpBrainRandomSeed));
   FileWrite(handle, "refresh_ms=" + IntegerToString(InpBrainRefreshMs));
   FileWrite(handle, "closed_bars_only=" + (InpBridgeClosedBarsOnly ? "1" : "0"));
   FileWrite(handle, "on_every_tick=" + (InpBridgeOnEveryTick ? "1" : "0"));
   FileWrite(handle, "candles_file=" + candlesFile);
   FileWrite(handle, "output=" + visualFile);
   FileWrite(handle, "status_file=" + statusFile);
   FileWrite(handle, "artifact_dir=" + ParquetArtifactDir());
   FileWrite(handle, "artifact_format=parquet");
   FileWrite(handle, "mql_visual_adapter=csv");
   FileWrite(handle, "chart_symbol=" + _Symbol);
   FileWrite(handle, "chart_timeframe=" + PeriodToText(_Period));
   FileWrite(handle, "source=MQL_EVENT_BRIDGE");
   FileClose(handle);
}

void WriteChartCandlesForPython(const string reason)
{
   string symbol = BrainSymbol();
   ENUM_TIMEFRAMES tf = BrainPeriod();
   int bars = InpBridgeBars();
   int start_pos = InpBridgeClosedBarsOnly ? 1 : 0;

   MqlRates rates[];
   int copied = CopyRates(symbol, tf, start_pos, bars, rates);
   if(copied <= 0)
   {
      Print("Decision Alpha Lab: CopyRates failed for bridge candles symbol=", symbol, " tf=", BrainTimeframe(), " error=", GetLastError());
      return;
   }
   ArraySetAsSeries(rates, false);

   string candlesFile = CandlesFileName();
   int handle = OpenCsvWrite(candlesFile, ',');
   if(handle == INVALID_HANDLE)
   {
      Print("Decision Alpha Lab: cannot write bridge candles file: ", candlesFile, " error=", GetLastError());
      return;
   }

   FileWrite(handle, "time", "open", "high", "low", "close", "tick_volume", "spread", "real_volume", "is_closed", "request_reason");
   for(int i=0; i<copied; i++)
   {
      bool is_closed = true;
      if(!InpBridgeClosedBarsOnly && i == copied - 1)
         is_closed = false;

      FileWrite(
         handle,
         TimeToString(rates[i].time, TIME_DATE | TIME_SECONDS),
         DoubleToString(rates[i].open, _Digits),
         DoubleToString(rates[i].high, _Digits),
         DoubleToString(rates[i].low, _Digits),
         DoubleToString(rates[i].close, _Digits),
         (long)rates[i].tick_volume,
         (int)rates[i].spread,
         (long)rates[i].real_volume,
         is_closed ? 1 : 0,
         reason
      );
   }
   FileClose(handle);
}

string RequestId(const string reason)
{
   return TimeToString(TimeLocal(), TIME_DATE | TIME_SECONDS) + "_" + IntegerToString((int)GetTickCount()) + "_" + reason;
}

int InpBridgeBars()
{
   if(InpBridgeLookbackBars > 0)
      return InpBridgeLookbackBars;
   return InpBrainBars;
}

string ParquetArtifactDir()
{
   string value = InpBridgeParquetDir;
   StringTrimLeft(value);
   StringTrimRight(value);
   if(value != "")
      return value;
   return "DecisionAlphaLab\\M0001\\parquet\\" + Sanitize(BrainSymbol()) + "_" + Sanitize(BrainTimeframe());
}

string CandlesFileName()
{
   string value = InpBridgeCandlesFile;
   StringTrimLeft(value);
   StringTrimRight(value);
   if(value != "")
      return value;
   return "DecisionAlphaLab\\M0001\\" + Sanitize(BrainSymbol()) + "_" + Sanitize(BrainTimeframe()) + "_candles.csv";
}

string StatusFileName()
{
   string value = InpBridgeStatusFile;
   StringTrimLeft(value);
   StringTrimRight(value);
   if(value != "")
      return value;
   return "DecisionAlphaLab\\M0001\\" + Sanitize(BrainSymbol()) + "_" + Sanitize(BrainTimeframe()) + "_status.ini";
}

string VisualFileName()
{
   if(!InpAutoBuildFileName)
      return InpFileName;

   return "DecisionAlphaLab\\M0001\\" + Sanitize(BrainSymbol()) + "_" + Sanitize(BrainTimeframe()) + "_visual.csv";
}

string BrainSymbol()
{
   string value = InpBrainSymbol;
   StringTrimLeft(value);
   StringTrimRight(value);
   if(value == "")
      return _Symbol;
   return value;
}

string BrainTimeframe()
{
   string value = InpBrainTimeframe;
   StringTrimLeft(value);
   StringTrimRight(value);
   if(value == "")
      return PeriodToText(_Period);
   return value;
}

string BrainMode()
{
   return InpBrainConsumeOnTouch ? "touch" : "hunt";
}

ENUM_TIMEFRAMES BrainPeriod()
{
   string tf = BrainTimeframe();
   if(tf == "M1") return PERIOD_M1;
   if(tf == "M2") return PERIOD_M2;
   if(tf == "M3") return PERIOD_M3;
   if(tf == "M4") return PERIOD_M4;
   if(tf == "M5") return PERIOD_M5;
   if(tf == "M6") return PERIOD_M6;
   if(tf == "M10") return PERIOD_M10;
   if(tf == "M12") return PERIOD_M12;
   if(tf == "M15") return PERIOD_M15;
   if(tf == "M20") return PERIOD_M20;
   if(tf == "M30") return PERIOD_M30;
   if(tf == "H1") return PERIOD_H1;
   if(tf == "H2") return PERIOD_H2;
   if(tf == "H3") return PERIOD_H3;
   if(tf == "H4") return PERIOD_H4;
   if(tf == "H6") return PERIOD_H6;
   if(tf == "H8") return PERIOD_H8;
   if(tf == "H12") return PERIOD_H12;
   if(tf == "D1") return PERIOD_D1;
   if(tf == "W1") return PERIOD_W1;
   if(tf == "MN1") return PERIOD_MN1;
   return _Period;
}

string PeriodToText(const ENUM_TIMEFRAMES tf)
{
   if(tf == PERIOD_M1) return "M1";
   if(tf == PERIOD_M2) return "M2";
   if(tf == PERIOD_M3) return "M3";
   if(tf == PERIOD_M4) return "M4";
   if(tf == PERIOD_M5) return "M5";
   if(tf == PERIOD_M6) return "M6";
   if(tf == PERIOD_M10) return "M10";
   if(tf == PERIOD_M12) return "M12";
   if(tf == PERIOD_M15) return "M15";
   if(tf == PERIOD_M20) return "M20";
   if(tf == PERIOD_M30) return "M30";
   if(tf == PERIOD_H1) return "H1";
   if(tf == PERIOD_H2) return "H2";
   if(tf == PERIOD_H3) return "H3";
   if(tf == PERIOD_H4) return "H4";
   if(tf == PERIOD_H6) return "H6";
   if(tf == PERIOD_H8) return "H8";
   if(tf == PERIOD_H12) return "H12";
   if(tf == PERIOD_D1) return "D1";
   if(tf == PERIOD_W1) return "W1";
   if(tf == PERIOD_MN1) return "MN1";
   return EnumToString(tf);
}

//+------------------------------------------------------------------+
void DeleteLabObjects()
{
   for(int i = ObjectsTotal(0, -1, -1) - 1; i >= 0; i--)
   {
      string name = ObjectName(0, i, -1, -1);
      if(StringFind(name, InpObjectPrefix) == 0)
         ObjectDelete(0, name);
   }
}

string ObjName(const string id)
{
   return InpObjectPrefix + Sanitize(_Symbol) + "_" + Sanitize(EnumToString(_Period)) + "_" + Sanitize(id);
}

string Sanitize(string value)
{
   StringReplace(value, "#", "IDX");
   StringReplace(value, ".", "_");
   StringReplace(value, "/", "_");
   StringReplace(value, "\\", "_");
   StringReplace(value, " ", "_");
   StringReplace(value, ":", "_");
   return value;
}

color NodeColor(const string nodeType)
{
   if(nodeType == "LOW") return clrLime;
   if(nodeType == "HIGH") return clrTomato;
   return clrSilver;
}

color RtvColor(const double rtv)
{
   if(rtv >= InpStrongRtvLevel) return clrGold;
   if(rtv > 0.0 && rtv <= 0.90) return clrDeepPink;
   return clrAqua;
}

string Field(string &arr[], const int n, const int index)
{
   if(index < 0 || index >= n)
      return "";
   string value = arr[index];
   StringTrimLeft(value);
   StringTrimRight(value);
   return value;
}

datetime ToTime(const string value)
{
   if(value == "")
      return 0;
   return StringToTime(value);
}

double ToDouble(const string value)
{
   if(value == "")
      return 0.0;
   return StringToDouble(value);
}

int ToInt(const string value)
{
   if(value == "")
      return -1;
   return (int)StringToInteger(value);
}

bool ToBool(const string value)
{
   return (value == "1" || value == "true" || value == "True" || value == "yes" || value == "YES");
}
