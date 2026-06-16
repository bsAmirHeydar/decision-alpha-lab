//+------------------------------------------------------------------+
//| Decision Alpha Lab — M0001 Visual Lab                            |
//| Reads Python-exported CSV visual contracts and draws them on MT5. |
//+------------------------------------------------------------------+
#property strict
#property version   "1.00"
#property description "M0001 RTV visual terminal for Decision Alpha Lab"

input string InpFileName          = "DecisionAlphaLab\\M0001\\GOLD_M15_visual.csv";
input string InpObjectPrefix      = "DAL_M0001_";
input bool   InpDeleteOldObjects  = true;
input bool   InpShowActual        = true;
input bool   InpShowRandom        = true;
input bool   InpShowNodes         = true;
input bool   InpShowTerritories   = true;
input bool   InpShowEvents        = true;
input bool   InpShowRtvLabels     = true;
input bool   InpShowHunts         = true;
input int    InpMaxObjects        = 3000;
input int    InpAutoReloadSeconds = 0;

int g_drawn = 0;

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

   int handle = FileOpen(InpFileName, FILE_READ | FILE_TXT | FILE_ANSI, '\n');
   if(handle == INVALID_HANDLE)
   {
      Print("Decision Alpha Lab: cannot open visual file: ", InpFileName, " error=", GetLastError());
      return;
   }

   bool header = true;
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

      string fields[];
      int n = StringSplit(line, ',', fields);
      if(n < 13)
         continue;

      string kind      = fields[0];
      string baseline  = fields[1];
      string id        = fields[2];
      string startStr  = fields[3];
      string endStr    = fields[4];
      string anchorStr = fields[5];
      double price     = ToDouble(fields[6]);
      double lower     = ToDouble(fields[7]);
      double upper     = ToDouble(fields[8]);
      string label     = fields[9];
      string nodeType  = fields[10];
      double rtv       = ToDouble(fields[11]);
      bool hunted      = (fields[12] == "1" || fields[12] == "true" || fields[12] == "True");

      if(!BaselineVisible(baseline))
         continue;
      if(!KindVisible(kind))
         continue;

      DrawRecord(kind, baseline, id, startStr, endStr, anchorStr, price, lower, upper, label, nodeType, rtv, hunted);
   }

   FileClose(handle);
   ChartRedraw(0);
   Print("Decision Alpha Lab: drawn ", g_drawn, " M0001 visual objects from ", InpFileName);
}

//+------------------------------------------------------------------+
void DrawRecord(
   string kind,
   string baseline,
   string id,
   string startStr,
   string endStr,
   string anchorStr,
   double price,
   double lower,
   double upper,
   string label,
   string nodeType,
   double rtv,
   bool hunted
)
{
   string name = InpObjectPrefix + id;
   color clr = ColorFor(kind, baseline, rtv, hunted);

   if(kind == "NODE")
   {
      datetime t = StringToTime(anchorStr);
      if(t <= 0 || price == 0.0)
         return;
      int arrow = (nodeType == "LOW") ? 217 : 218;
      ObjectCreate(0, name, OBJ_ARROW, 0, t, price);
      ObjectSetInteger(0, name, OBJPROP_ARROWCODE, arrow);
      ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
      ObjectSetInteger(0, name, OBJPROP_WIDTH, 2);
      ObjectSetString(0, name, OBJPROP_TOOLTIP, label);
      g_drawn++;
      return;
   }

   if(kind == "TERRITORY" || kind == "EVENT")
   {
      datetime t1 = StringToTime(startStr);
      datetime t2 = StringToTime(endStr);
      if(t1 <= 0 || t2 <= 0 || lower == 0.0 || upper == 0.0)
         return;
      ObjectCreate(0, name, OBJ_RECTANGLE, 0, t1, upper, t2, lower);
      ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
      ObjectSetInteger(0, name, OBJPROP_STYLE, kind == "TERRITORY" ? STYLE_SOLID : STYLE_DOT);
      ObjectSetInteger(0, name, OBJPROP_WIDTH, kind == "TERRITORY" ? 1 : 2);
      ObjectSetInteger(0, name, OBJPROP_BACK, true);
      ObjectSetInteger(0, name, OBJPROP_FILL, true);
      ObjectSetString(0, name, OBJPROP_TOOLTIP, label);
      g_drawn++;
      return;
   }

   if(kind == "RTV_LABEL")
   {
      datetime t = StringToTime(anchorStr);
      if(t <= 0 || price == 0.0)
         return;
      ObjectCreate(0, name, OBJ_TEXT, 0, t, price);
      ObjectSetString(0, name, OBJPROP_TEXT, label);
      ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
      ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 8);
      ObjectSetString(0, name, OBJPROP_FONT, "Arial Bold");
      ObjectSetString(0, name, OBJPROP_TOOLTIP, label);
      g_drawn++;
      return;
   }

   if(kind == "HUNT")
   {
      datetime t = StringToTime(anchorStr);
      if(t <= 0 || price == 0.0)
         return;
      ObjectCreate(0, name, OBJ_ARROW, 0, t, price);
      ObjectSetInteger(0, name, OBJPROP_ARROWCODE, 251);
      ObjectSetInteger(0, name, OBJPROP_COLOR, clrRed);
      ObjectSetInteger(0, name, OBJPROP_WIDTH, 3);
      ObjectSetString(0, name, OBJPROP_TOOLTIP, label);
      g_drawn++;
      return;
   }
}

//+------------------------------------------------------------------+
bool BaselineVisible(string baseline)
{
   if(baseline == "actual")
      return InpShowActual;
   if(baseline == "random")
      return InpShowRandom;
   return true;
}

//+------------------------------------------------------------------+
bool KindVisible(string kind)
{
   if(kind == "NODE")       return InpShowNodes;
   if(kind == "TERRITORY")  return InpShowTerritories;
   if(kind == "EVENT")      return InpShowEvents;
   if(kind == "RTV_LABEL")  return InpShowRtvLabels;
   if(kind == "HUNT")       return InpShowHunts;
   return true;
}

//+------------------------------------------------------------------+
color ColorFor(string kind, string baseline, double rtv, bool hunted)
{
   if(kind == "HUNT")
      return clrRed;

   if(baseline == "random")
   {
      if(kind == "RTV_LABEL") return clrOrange;
      if(kind == "EVENT")     return clrDarkOrange;
      return clrSandyBrown;
   }

   if(kind == "RTV_LABEL")
   {
      if(rtv >= 1.25) return clrGold;
      if(rtv <= 0.90) return clrDeepPink;
      return clrAqua;
   }

   if(kind == "EVENT")     return clrDodgerBlue;
   if(kind == "TERRITORY") return clrDarkSlateGray;
   if(kind == "NODE")      return clrWhite;

   return clrSilver;
}

//+------------------------------------------------------------------+
double ToDouble(string value)
{
   StringTrimLeft(value);
   StringTrimRight(value);
   if(value == "")
      return 0.0;
   return StringToDouble(value);
}

//+------------------------------------------------------------------+
void DeleteLabObjects()
{
   int total = ObjectsTotal(0, 0, -1);
   for(int i = total - 1; i >= 0; i--)
   {
      string name = ObjectName(0, i, 0, -1);
      if(StringFind(name, InpObjectPrefix) == 0)
         ObjectDelete(0, name);
   }
}
//+------------------------------------------------------------------+
