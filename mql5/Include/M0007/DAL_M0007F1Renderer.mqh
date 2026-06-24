#ifndef __DAL_M0007_F1_RENDERER_MQH__
#define __DAL_M0007_F1_RENDERER_MQH__
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

void M0007_SetCommonObjectProps(const string name)
{
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
}

bool M0007_DrawTrendRaw(const string name,
                        const datetime t1,
                        const double p1,
                        const datetime t2,
                        const double p2,
                        const color clr,
                        const int width,
                        const ENUM_LINE_STYLE style)
{
   ObjectDelete(0, name);
   ResetLastError();
   if(!ObjectCreate(0, name, OBJ_TREND, 0, t1, p1, t2, p2))
   {
      Print("M0007 renderer: ObjectCreate failed for ", name, " err=", GetLastError());
      return false;
   }

   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, width);
   ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, false);
   ObjectSetInteger(0, name, OBJPROP_RAY_LEFT, false);
   ObjectSetInteger(0, name, OBJPROP_BACK, false);
   M0007_SetCommonObjectProps(name);
   return true;
}

bool M0007_DrawTextRaw(const string name,
                       const datetime t,
                       const double price,
                       const string text,
                       const color clr,
                       const int font_size,
                       const ENUM_ANCHOR_POINT anchor = ANCHOR_LEFT_LOWER)
{
   ObjectDelete(0, name);
   ResetLastError();
   if(!ObjectCreate(0, name, OBJ_TEXT, 0, t, price))
   {
      Print("M0007 renderer: text ObjectCreate failed for ", name, " err=", GetLastError());
      return false;
   }

   ObjectSetString(0, name, OBJPROP_TEXT, text);
   ObjectSetString(0, name, OBJPROP_FONT, "Arial Bold");
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, font_size);
   ObjectSetInteger(0, name, OBJPROP_ANCHOR, anchor);
   ObjectSetInteger(0, name, OBJPROP_BACK, false);
   M0007_SetCommonObjectProps(name);
   return true;
}

void M0007_DrawHLine(const string name, const double price, const color clr, const ENUM_LINE_STYLE style, const string text)
{
   ObjectDelete(0, name);
   if(!ObjectCreate(0, name, OBJ_HLINE, 0, 0, price))
      return;
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, 1);
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   M0007_SetCommonObjectProps(name);
}

void M0007_DrawVLine(const string name, const datetime t, const color clr, const ENUM_LINE_STYLE style, const string text)
{
   ObjectDelete(0, name);
   if(!ObjectCreate(0, name, OBJ_VLINE, 0, t, 0))
      return;
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, 1);
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   M0007_SetCommonObjectProps(name);
}

void M0007_DrawNodeLabel(const string name, const M0007_F1Node &node, const string text, const color clr, const int font_size = 9)
{
   M0007_DrawTextRaw(name, node.time, node.price, text, clr, font_size, ANCHOR_LEFT_LOWER);
}

void M0007_DrawF1Schematic(const M0007_F1Event &e, const string prefix, const color clr)
{
   int sec = PeriodSeconds(_Period);
   if(sec <= 0) sec = 60;

   bool bullish = (e.direction == M0007_DIR_BULLISH);
   double h_left  = MathAbs(e.H1.price - e.W.price);
   double h_right = MathAbs(e.H2.price - e.W.price);
   double h = MathMax(h_left, h_right);
   if(h <= 0.0) h = 100.0 * _Point;

   int dt_hw = (int)(e.W.time - e.H1.time);
   int dt_wh = (int)(e.H2.time - e.W.time);
   if(dt_hw <= 0) dt_hw = sec * 6;
   if(dt_wh <= 0) dt_wh = sec * 8;

   datetime start_t = e.H1.time - (datetime)MathMax(sec * 4, (int)(dt_hw * 0.90));
   double start_p = (bullish ? e.H1.price - 1.35 * h : e.H1.price + 1.35 * h);

   // First clean straight leg into H1/L1.
   M0007_DrawTrendRaw(prefix + "SCHEMATIC_LEG", start_t, start_p, e.H1.time, e.H1.price, clr, 3, STYLE_SOLID);

   // Curve-like schematic from H1/L1 through the waist area into H2/L2.
   // MQL chart objects do not provide a stable native arc for this use case, so the curve is drawn as short clean segments.
   datetime t0 = e.H1.time;
   datetime t1 = e.H1.time + (datetime)(dt_hw * 0.32);
   datetime t2 = e.H1.time + (datetime)(dt_hw * 0.70);
   datetime t3 = e.W.time;
   datetime t4 = e.W.time  + (datetime)(dt_wh * 0.30);
   datetime t5 = e.W.time  + (datetime)(dt_wh * 0.64);
   datetime t6 = e.H2.time;

   double p0 = e.H1.price;
   double p1, p2, p3, p4, p5, p6;

   if(bullish)
   {
      p1 = e.H1.price - 0.50 * h_left;
      p2 = e.W.price  + 0.10 * h_left;
      p3 = e.W.price;
      p4 = e.W.price  + 0.12 * h_right;
      p5 = e.W.price  + 0.52 * h_right;
      p6 = e.H2.price;
   }
   else
   {
      p1 = e.H1.price + 0.50 * h_left;
      p2 = e.W.price  - 0.10 * h_left;
      p3 = e.W.price;
      p4 = e.W.price  - 0.12 * h_right;
      p5 = e.W.price  - 0.52 * h_right;
      p6 = e.H2.price;
   }

   M0007_DrawTrendRaw(prefix + "SCHEMATIC_CURVE_01", t0, p0, t1, p1, clr, 3, STYLE_SOLID);
   M0007_DrawTrendRaw(prefix + "SCHEMATIC_CURVE_02", t1, p1, t2, p2, clr, 3, STYLE_SOLID);
   M0007_DrawTrendRaw(prefix + "SCHEMATIC_CURVE_03", t2, p2, t3, p3, clr, 3, STYLE_SOLID);
   M0007_DrawTrendRaw(prefix + "SCHEMATIC_CURVE_04", t3, p3, t4, p4, clr, 3, STYLE_SOLID);
   M0007_DrawTrendRaw(prefix + "SCHEMATIC_CURVE_05", t4, p4, t5, p5, clr, 3, STYLE_SOLID);
   M0007_DrawTrendRaw(prefix + "SCHEMATIC_CURVE_06", t5, p5, t6, p6, clr, 3, STYLE_SOLID);

   double text_offset = MathMax(0.30 * h, 50.0 * _Point);
   datetime label_t = e.H2.time + (datetime)(sec * 2);
   double label_p = bullish ? MathMax(e.H1.price, e.H2.price) + text_offset
                            : MathMin(e.H1.price, e.H2.price) - text_offset;

   M0007_DrawTextRaw(prefix + "F1_LABEL", label_t, label_p, "F1", clr, 16,
                     bullish ? ANCHOR_LEFT_LOWER : ANCHOR_LEFT_UPPER);
}

void M0007_DrawStatusPanel(const string prefix,
                           const int total,
                           const int confirmed,
                           const int invalidated,
                           const int open_count,
                           const bool draw_only_confirmed,
                           const int drawn)
{
   string txt = "M0007 F1 | total=" + IntegerToString(total) +
                " confirmed=" + IntegerToString(confirmed) +
                " invalidated=" + IntegerToString(invalidated) +
                " open=" + IntegerToString(open_count) +
                " drawn=" + IntegerToString(drawn) +
                " filterConfirmed=" + (draw_only_confirmed ? "true" : "false");

   datetime t = iTime(_Symbol, _Period, 0);
   double p = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   if(p <= 0.0) p = iClose(_Symbol, _Period, 0);
   M0007_DrawTextRaw(prefix + "STATUS_PANEL", t, p, txt, clrSilver, 9, ANCHOR_RIGHT_UPPER);
}

void M0007_DrawEvent(const M0007_F1Event &e, const string prefix, const int event_number)
{
   string p = prefix + IntegerToString(event_number) + "_";
   color schematic_clr = clrCrimson;
   color audit_clr = (e.direction == M0007_DIR_BULLISH ? clrLime : clrTomato);

   // Main requested schematic: one straight line + one curve-like F1 shape + F1 text.
   M0007_DrawF1Schematic(e, p, schematic_clr);

   // Compact audit labels. These do not replace the schematic.
   M0007_DrawNodeLabel(p+"H1",  e.H1,  (e.direction==M0007_DIR_BULLISH ? "H1" : "L1"), clrDodgerBlue, 8);
   M0007_DrawNodeLabel(p+"W",   e.W,   "W", clrRed, 8);
   M0007_DrawNodeLabel(p+"H2",  e.H2,  (e.direction==M0007_DIR_BULLISH ? "H2" : "L2"), clrLimeGreen, 8);
   M0007_DrawNodeLabel(p+"N1",  e.N1,  "1", clrYellow, 9);
   M0007_DrawNodeLabel(p+"R12", e.R12, "R12", clrAqua, 8);
   M0007_DrawNodeLabel(p+"N2",  e.N2,  "2", clrYellow, 9);

   // Thin audit levels.
   M0007_DrawHLine(p+"waist", e.W.price, clrRed, STYLE_DASH, "M0007 W protected waist");
   M0007_DrawHLine(p+"r12",   e.R12.price, clrDeepSkyBlue, STYLE_DOT, "M0007 R12 internal trigger");
   M0007_DrawHLine(p+"h2",    e.H2.price, audit_clr, STYLE_DASHDOT, "M0007 H2/L2 final confirm");

   if(e.internal_trigger_index >= 0)
      M0007_DrawVLine(p+"trigger_bar", e.internal_trigger_time, clrDeepSkyBlue, STYLE_DOT, "M0007 internal trigger");

   if(e.confirm_index >= 0)
      M0007_DrawVLine(p+"confirm_bar", e.confirm_time, clrLimeGreen, STYLE_DASHDOT, "M0007 F1 confirmed");

   if(e.invalidation_index >= 0)
      M0007_DrawVLine(p+"invalid_bar", e.invalidation_time, clrRed, STYLE_DASH, "M0007 F1 invalidated");
}

int M0007_DrawEvents(const M0007_F1Event &events[], const int max_events, const bool draw_only_confirmed, const string prefix)
{
   int drawn = 0;
   int total = ArraySize(events);
   int confirmed = 0;
   int invalidated = 0;
   int open_count = 0;

   for(int k=0; k<total; k++)
   {
      if(events[k].status == M0007_STATUS_CONFIRMED) confirmed++;
      else if(events[k].status == M0007_STATUS_INVALIDATED) invalidated++;
      else open_count++;
   }

   for(int i=total-1; i>=0 && drawn<max_events; i--)
   {
      if(draw_only_confirmed && events[i].status != M0007_STATUS_CONFIRMED)
         continue;
      M0007_DrawEvent(events[i], prefix, drawn);
      drawn++;
   }

   M0007_DrawStatusPanel(prefix, total, confirmed, invalidated, open_count, draw_only_confirmed, drawn);
   ChartRedraw(0);
   return drawn;
}

#endif
