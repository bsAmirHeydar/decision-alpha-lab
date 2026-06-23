#property strict
#include <M0007/DAL_M0007F1Types.mqh>

void M0007_DeleteObjectsByPrefix(const string prefix)
{
   for(int i=ObjectsTotal(0, -1, -1)-1; i>=0; i--)
   {
      string name = ObjectName(0, i, -1, -1);
      if(StringFind(name, prefix) == 0)
         ObjectDelete(0, name);
   }
}

void M0007_DrawHLine(const string name, const double price, const color clr, const ENUM_LINE_STYLE style, const string text)
{
   ObjectDelete(0, name);
   ObjectCreate(0, name, OBJ_HLINE, 0, 0, price);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, 1);
   ObjectSetString(0, name, OBJPROP_TEXT, text);
}

void M0007_DrawVLine(const string name, const datetime t, const color clr, const ENUM_LINE_STYLE style, const string text)
{
   ObjectDelete(0, name);
   ObjectCreate(0, name, OBJ_VLINE, 0, t, 0);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, 1);
   ObjectSetString(0, name, OBJPROP_TEXT, text);
}

void M0007_DrawText(const string name, const datetime t, const double price, const string text, const color clr)
{
   ObjectDelete(0, name);
   ObjectCreate(0, name, OBJ_TEXT, 0, t, price);
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 9);
   ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER);
}

void M0007_DrawSegment(const string name, const M0007_F1Node &a, const M0007_F1Node &b, const color clr)
{
   ObjectDelete(0, name);
   ObjectCreate(0, name, OBJ_TREND, 0, a.time, a.price, b.time, b.price);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, 2);
   ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, false);
}

void M0007_DrawEvent(const M0007_F1Event &e, const string prefix, const int event_number)
{
   string p = prefix + IntegerToString(event_number) + "_";
   color main_clr = (e.direction == M0007_DIR_BULLISH ? clrLime : clrTomato);

   M0007_DrawSegment(p+"seg_01", e.H1,  e.W,   main_clr);
   M0007_DrawSegment(p+"seg_02", e.W,   e.H2,  main_clr);
   M0007_DrawSegment(p+"seg_03", e.H2,  e.N1,  main_clr);
   M0007_DrawSegment(p+"seg_04", e.N1,  e.R12, main_clr);
   M0007_DrawSegment(p+"seg_05", e.R12, e.N2,  main_clr);

   M0007_DrawText(p+"H1",  e.H1.time,  e.H1.price,  (e.direction==M0007_DIR_BULLISH ? "H1" : "L1"), clrDodgerBlue);
   M0007_DrawText(p+"W",   e.W.time,   e.W.price,   "W", clrRed);
   M0007_DrawText(p+"H2",  e.H2.time,  e.H2.price,  (e.direction==M0007_DIR_BULLISH ? "H2" : "L2"), clrLimeGreen);
   M0007_DrawText(p+"N1",  e.N1.time,  e.N1.price,  "1", clrYellow);
   M0007_DrawText(p+"R12", e.R12.time, e.R12.price, "R12", clrAqua);
   M0007_DrawText(p+"N2",  e.N2.time,  e.N2.price,  "2", clrYellow);

   M0007_DrawHLine(p+"waist", e.W.price, clrRed, STYLE_DASH, "M0007 W protected waist");
   M0007_DrawHLine(p+"r12",   e.R12.price, clrDeepSkyBlue, STYLE_DOT, "M0007 R12 internal trigger");
   M0007_DrawHLine(p+"h2",    e.H2.price, clrLimeGreen, STYLE_DASHDOT, "M0007 H2/L2 final confirm");

   if(e.internal_trigger_index >= 0)
      M0007_DrawVLine(p+"trigger_bar", e.internal_trigger_time, clrDeepSkyBlue, STYLE_DOT, "M0007 internal trigger");

   if(e.confirm_index >= 0)
      M0007_DrawVLine(p+"confirm_bar", e.confirm_time, clrLimeGreen, STYLE_DASHDOT, "M0007 F1 confirmed");

   if(e.invalidation_index >= 0)
      M0007_DrawVLine(p+"invalid_bar", e.invalidation_time, clrRed, STYLE_DASH, "M0007 F1 invalidated");
}

void M0007_DrawEvents(const M0007_F1Event &events[], const int max_events, const bool draw_only_confirmed, const string prefix)
{
   int drawn = 0;
   for(int i=ArraySize(events)-1; i>=0 && drawn<max_events; i--)
   {
      if(draw_only_confirmed && events[i].status != M0007_STATUS_CONFIRMED)
         continue;
      M0007_DrawEvent(events[i], prefix, drawn);
      drawn++;
   }
   ChartRedraw(0);
}
