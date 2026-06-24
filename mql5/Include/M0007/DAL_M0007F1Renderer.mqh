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
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
}

void M0007_DrawTextEx(
   const string name,
   const datetime t,
   const double price,
   const string text,
   const color clr,
   const int font_size,
   const ENUM_ANCHOR_POINT anchor = ANCHOR_LEFT_LOWER
)
{
   ObjectDelete(0, name);
   ObjectCreate(0, name, OBJ_TEXT, 0, t, price);
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   ObjectSetString(0, name, OBJPROP_FONT, "Arial Bold");
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, font_size);
   ObjectSetInteger(0, name, OBJPROP_ANCHOR, anchor);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
}

void M0007_DrawTrendRaw(
   const string name,
   const datetime t1,
   const double p1,
   const datetime t2,
   const double p2,
   const color clr,
   const int width = 2,
   const ENUM_LINE_STYLE style = STYLE_SOLID
)
{
   ObjectDelete(0, name);
   ObjectCreate(0, name, OBJ_TREND, 0, t1, p1, t2, p2);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_STYLE, style);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, width);
   ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
}

void M0007_DrawSegment(const string name, const M0007_F1Node &a, const M0007_F1Node &b, const color clr)
{
   ObjectDelete(0, name);
   ObjectCreate(0, name, OBJ_TREND, 0, a.time, a.price, b.time, b.price);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, 2);
   ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, false);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
}

void M0007_DrawF1Schematic(const M0007_F1Event &e, const string p, const color schematic_clr)
{
   bool bullish = (e.direction == M0007_DIR_BULLISH);

   double h1_w = MathAbs(e.H1.price - e.W.price);
   double h2_w = MathAbs(e.H2.price - e.W.price);
   double height = MathMax(h1_w, h2_w);
   if(height <= 0.0)
      height = 100.0 * _Point;

   int sec = PeriodSeconds(_Period);
   if(sec <= 0)
      sec = 60;

   int dt_hw = (int)(e.W.time - e.H1.time);
   int dt_wh = (int)(e.H2.time - e.W.time);
   if(dt_hw <= 0)
      dt_hw = sec * 5;
   if(dt_wh <= 0)
      dt_wh = sec * 8;

   // This is a visual anchor only. It is intentionally schematic:
   // one clean leg into H1/L1, then a curved flag form into H2/L2.
   datetime start_time = (datetime)(e.H1.time - (sec * 12));
   double start_price = bullish
      ? e.H1.price - (1.45 * height)
      : e.H1.price + (1.45 * height);

   M0007_DrawTrendRaw(
      p + "schem_leg",
      start_time,
      start_price,
      e.H1.time,
      e.H1.price,
      schematic_clr,
      2,
      STYLE_SOLID
   );

   datetime c1_time = (datetime)(e.H1.time + (dt_hw / 2));
   datetime c2_time = e.W.time;
   datetime c3_time = (datetime)(e.W.time + (dt_wh / 2));

   double c1_price;
   double c2_price = e.W.price;
   double c3_price;

   if(bullish)
   {
      c1_price = e.H1.price - (0.85 * h1_w);
      c3_price = e.W.price + (0.35 * h2_w);
   }
   else
   {
      c1_price = e.H1.price + (0.85 * h1_w);
      c3_price = e.W.price - (0.35 * h2_w);
   }

   M0007_DrawTrendRaw(p + "schem_curve_01", e.H1.time, e.H1.price, c1_time, c1_price, schematic_clr, 2, STYLE_SOLID);
   M0007_DrawTrendRaw(p + "schem_curve_02", c1_time, c1_price, c2_time, c2_price, schematic_clr, 2, STYLE_SOLID);
   M0007_DrawTrendRaw(p + "schem_curve_03", c2_time, c2_price, c3_time, c3_price, schematic_clr, 2, STYLE_SOLID);
   M0007_DrawTrendRaw(p + "schem_curve_04", c3_time, c3_price, e.H2.time, e.H2.price, schematic_clr, 2, STYLE_SOLID);

   double text_offset = 0.28 * h2_w;
   if(text_offset <= 0.0)
      text_offset = 80.0 * _Point;

   datetime label_time = (datetime)(e.H2.time + sec);
   double label_price = bullish
      ? MathMax(e.H1.price, e.H2.price) + text_offset
      : MathMin(e.H1.price, e.H2.price) - text_offset;

   M0007_DrawTextEx(
      p + "schem_label_F1",
      label_time,
      label_price,
      "F1",
      schematic_clr,
      14,
      bullish ? ANCHOR_LEFT_LOWER : ANCHOR_LEFT_UPPER
   );
}

void M0007_DrawEvent(const M0007_F1Event &e, const string prefix, const int event_number)
{
   string p = prefix + IntegerToString(event_number) + "_";
   color main_clr = (e.direction == M0007_DIR_BULLISH ? clrLime : clrTomato);

   // Schematic view: one clean leg into H1/L1, then a curved F1 form into H2/L2.
   M0007_DrawF1Schematic(e, p, main_clr);

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
