
//+------------------------------------------------------------------+
//| Decision Alpha Lab — M0001 Python-Brain Visual Lab               |
//| MQL is visual only. The Python M0001 engine is the single source  |
//| of truth for backtest, validation, export and live visual output. |
//+------------------------------------------------------------------+
#property strict
#property version   "5.00"
#property description "Python-brain M0001 visual lab: MQL draws the Python visual contract only"

input string InpFileName          = "DecisionAlphaLab\\M0001\\GOLD_M15_visual.csv";
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

//+------------------------------------------------------------------+
int OnInit()
{
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
void OnTimer()
{
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

   int handle = FileOpen(InpFileName, FILE_READ | FILE_TXT | FILE_ANSI, '\n');
   if(handle == INVALID_HANDLE)
   {
      Print("Decision Alpha Lab: cannot open Python visual file: ", InpFileName, " error=", GetLastError());
      DrawMessage("NO_PYTHON_FILE", "Waiting for Python visual contract:\n" + InpFileName, clrTomato, 12, 18);
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

   ChartRedraw(0);
   Print("DAL M0001 PYTHON-BRAIN VISUAL | rows_drawn=", g_drawn, " events=", g_events_seen, " nodes=", g_nodes_seen, " file=", InpFileName);
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

void DrawSummaryPanel()
{
   double mean_rtv = (g_rtv_count > 0 ? g_rtv_sum / g_rtv_count : 0.0);
   string text = "Decision Alpha Lab | M0001 Python Brain"
               + "\nMQL mode: VISUAL ONLY"
               + "\nFile: " + InpFileName
               + "\nNodes: " + IntegerToString(g_nodes_seen)
               + " | Events: " + IntegerToString(g_events_seen)
               + " | Hunts: " + IntegerToString(g_hunts_seen)
               + "\nMean RTV: " + DoubleToString(mean_rtv, 3)
               + "\nPreset: " + IntegerToString(InpViewPreset);
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
