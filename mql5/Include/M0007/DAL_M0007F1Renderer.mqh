#ifndef __DAL_M0007_F1_RENDERER_MQH__
#define __DAL_M0007_F1_RENDERER_MQH__
#property strict
#include <M0007/DAL_M0007F1Types.mqh>

// M0007 renderer contract:
// - Draws only the clean F1 schematic on the real chart.
// - No horizontal audit levels, no trigger/confirm vertical lines, and no internal node clutter by default.
// - Visual layer is schematic/audit-only and never changes the detector state.
// - Main schematic = one straight Leg 1 + one smooth curve from Leg 1 through correction into Leg 2.

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

// -----------------------------------------------------------------------------
// Clean schematic primitives
// -----------------------------------------------------------------------------

double M0007_CubicBezierValue(const double p0,
                              const double p1,
                              const double p2,
                              const double p3,
                              const double u)
{
   double v = 1.0 - u;
   return v*v*v*p0 + 3.0*v*v*u*p1 + 3.0*v*u*u*p2 + u*u*u*p3;
}

datetime M0007_TimeAt(const datetime a, const datetime b, const double ratio)
{
   return (datetime)((long)a + (long)MathRound(((double)((long)b - (long)a)) * ratio));
}

void M0007_DrawBezierCurve(const string name,
                           const datetime t0,
                           const double p0,
                           const datetime c1t,
                           const double c1p,
                           const datetime c2t,
                           const double c2p,
                           const datetime t3,
                           const double p3,
                           const color clr,
                           const int width,
                           const int segments)
{
   int n = MathMax(3, segments);
   datetime prev_t = t0;
   double   prev_p = p0;

   for(int i=1; i<=n; i++)
   {
      double u = (double)i / (double)n;
      datetime next_t = (datetime)MathRound(M0007_CubicBezierValue((double)((long)t0),
                                                                    (double)((long)c1t),
                                                                    (double)((long)c2t),
                                                                    (double)((long)t3),
                                                                    u));
      double next_p = M0007_CubicBezierValue(p0, c1p, c2p, p3, u);
      M0007_DrawTrendRaw(name + "_" + IntegerToString(i), prev_t, prev_p, next_t, next_p, clr, width, STYLE_SOLID);
      prev_t = next_t;
      prev_p = next_p;
   }
}

void M0007_DrawNodeDot(const string name, const datetime t, const double price, const color clr, const int font_size = 14)
{
   // A text dot is more stable across brokers than OBJ_BITMAP and keeps the patch self-contained.
   M0007_DrawTextRaw(name, t, price, "●", clr, font_size, ANCHOR_CENTER);
}

void M0007_DrawLocalLevel(const string name,
                          const datetime left_t,
                          const datetime right_t,
                          const double price,
                          const string label,
                          const color clr)
{
   M0007_DrawTrendRaw(name + "_LINE", left_t, price, right_t, price, clr, 1, STYLE_DASH);
   M0007_DrawTextRaw(name + "_TXT", left_t, price, label, clr, 9, ANCHOR_LEFT_LOWER);
}

void M0007_DrawF1Schematic(const M0007_F1Event &e,
                            const string prefix,
                            const color clr,
                            const bool show_text_labels = true,
                            const bool show_badge = true)
{
   int sec = PeriodSeconds(_Period);
   if(sec <= 0) sec = 60;

   bool bullish = (e.direction == M0007_DIR_BULLISH);

   // Mechanical F1 anchors:
   // H1/L1 = end of the first leg.
   // W     = correction / protected waist.
   // H2/L2 = end of the second main leg.
   double h_left  = MathAbs(e.H1.price - e.W.price);
   double h_right = MathAbs(e.H2.price - e.W.price);
   double h = MathMax(h_left, h_right);
   if(h <= 0.0) h = MathMax(100.0 * _Point, MathAbs(e.H1.price) * 0.001);

   int dt_hw = (int)((long)e.W.time  - (long)e.H1.time);
   int dt_wh = (int)((long)e.H2.time - (long)e.W.time);
   if(dt_hw <= 0) dt_hw = sec * 6;
   if(dt_wh <= 0) dt_wh = sec * 8;

   // Synthetic visual start for Leg 1. The detector does not need this point;
   // it is only for showing the clean F1 grammar exactly like the reference sketch.
   datetime start_t = e.H1.time - (datetime)MathMax(sec * 4, (int)(dt_hw * 0.90));
   double start_p = bullish ? e.H1.price - 1.35 * h : e.H1.price + 1.35 * h;

   // One straight line = Leg 1.
   M0007_DrawTrendRaw(prefix + "LEG1_STRAIGHT", start_t, start_p, e.H1.time, e.H1.price, clr, 3, STYLE_SOLID);

   // One clean curve = correction into Leg 2.
   // This is drawn as two cubic Bezier curves that pass through W, so the correction is visually exact.
   datetime c1a_t = M0007_TimeAt(e.H1.time, e.W.time, 0.35);
   datetime c2a_t = M0007_TimeAt(e.H1.time, e.W.time, 0.70);
   datetime c1b_t = M0007_TimeAt(e.W.time, e.H2.time, 0.30);
   datetime c2b_t = M0007_TimeAt(e.W.time, e.H2.time, 0.68);

   double c1a_p, c2a_p, c1b_p, c2b_p;
   if(bullish)
   {
      c1a_p = e.H1.price - 0.10 * h_left;
      c2a_p = e.W.price  + 0.08 * h_left;
      c1b_p = e.W.price  + 0.06 * h_right;
      c2b_p = e.H2.price - 0.10 * h_right;
   }
   else
   {
      c1a_p = e.H1.price + 0.10 * h_left;
      c2a_p = e.W.price  - 0.08 * h_left;
      c1b_p = e.W.price  - 0.06 * h_right;
      c2b_p = e.H2.price + 0.10 * h_right;
   }

   M0007_DrawBezierCurve(prefix + "CURVE_A", e.H1.time, e.H1.price, c1a_t, c1a_p, c2a_t, c2a_p, e.W.time, e.W.price, clr, 3, 10);
   M0007_DrawBezierCurve(prefix + "CURVE_B", e.W.time, e.W.price, c1b_t, c1b_p, c2b_t, c2b_p, e.H2.time, e.H2.price, clr, 3, 10);

   // Main visual nodes.
   M0007_DrawNodeDot(prefix + "DOT_START", start_t, start_p, clr, 13);
   M0007_DrawNodeDot(prefix + "DOT_LEG1",  e.H1.time, e.H1.price, clr, 13);
   M0007_DrawNodeDot(prefix + "DOT_CORR",  e.W.time,  e.W.price,  clr, 13);
   M0007_DrawNodeDot(prefix + "DOT_LEG2",  e.H2.time, e.H2.price, clr, 13);

   double text_gap = MathMax(0.17 * h, 40.0 * _Point);
   double small_gap = MathMax(0.10 * h, 25.0 * _Point);

   if(show_text_labels)
   {
      // Labels matching the reference drawing.
      M0007_DrawTextRaw(prefix + "TXT_START", start_t, bullish ? start_p - small_gap : start_p + small_gap,
                        "Start", clr, 9, bullish ? ANCHOR_LEFT_UPPER : ANCHOR_LEFT_LOWER);

      datetime leg1_label_t = M0007_TimeAt(start_t, e.H1.time, 0.42);
      double leg1_label_p = (start_p + e.H1.price) * 0.5;
      M0007_DrawTextRaw(prefix + "TXT_LEG1", leg1_label_t,
                        bullish ? leg1_label_p + text_gap : leg1_label_p - text_gap,
                        "Leg 1", clr, 10, ANCHOR_CENTER);

      datetime correction_label_t = M0007_TimeAt(e.H1.time, e.H2.time, 0.48);
      double correction_label_p = bullish ? e.W.price + 0.70 * h : e.W.price - 0.70 * h;
      M0007_DrawTextRaw(prefix + "TXT_CORRECTION", correction_label_t, correction_label_p,
                        "Correction", clr, 10, bullish ? ANCHOR_CENTER : ANCHOR_CENTER);

      M0007_DrawTextRaw(prefix + "TXT_PULLBACK", e.W.time,
                        bullish ? e.W.price - text_gap : e.W.price + text_gap,
                        "Pullback / Correction", clr, 8,
                        bullish ? ANCHOR_CENTER : ANCHOR_CENTER);

      datetime leg2_label_t = M0007_TimeAt(e.W.time, e.H2.time, 0.74);
      double leg2_label_p = (e.W.price + e.H2.price) * 0.5;
      M0007_DrawTextRaw(prefix + "TXT_LEG2", leg2_label_t,
                        bullish ? leg2_label_p + text_gap : leg2_label_p - text_gap,
                        "Leg 2", clr, 10, ANCHOR_CENTER);

   }

   if(show_badge)
   {
      string badge = bullish ? "BULLISH F1" : "BEARISH F1";
      datetime badge_t = M0007_TimeAt(start_t, e.H2.time, 0.50);
      double badge_p = bullish ? MathMax(e.H1.price, e.H2.price) + 0.52 * h
                               : MathMin(e.H1.price, e.H2.price) - 0.52 * h;
      M0007_DrawTextRaw(prefix + "TXT_BADGE", badge_t, badge_p, badge, clr, 13, ANCHOR_CENTER);
   }
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

void M0007_DrawEvent(const M0007_F1Event &e,
                       const string prefix,
                       const int event_number,
                       const bool show_text_labels = true,
                       const bool show_badge = true)
{
   string p = prefix + IntegerToString(event_number) + "_";
   color schematic_clr = (e.direction == M0007_DIR_BULLISH ? clrLimeGreen : clrTomato);

   // Clean requested schematic only:
   // Start -> straight Leg 1 -> smooth correction curve -> Leg 2.
   // No horizontal levels, no internal H1/W/H2/R12/N labels, no vertical trigger bars.
   M0007_DrawF1Schematic(e, p, schematic_clr, show_text_labels, show_badge);
}

int M0007_DrawEvents(const M0007_F1Event &events[],
                       const int max_events,
                       const bool draw_only_confirmed,
                       const string prefix,
                       const bool show_text_labels = true,
                       const bool show_badge = true,
                       const bool show_status_panel = false)
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
      M0007_DrawEvent(events[i], prefix, drawn, show_text_labels, show_badge);
      drawn++;
   }

   if(show_status_panel)
      M0007_DrawStatusPanel(prefix, total, confirmed, invalidated, open_count, draw_only_confirmed, drawn);
   ChartRedraw(0);
   return drawn;
}

#endif
