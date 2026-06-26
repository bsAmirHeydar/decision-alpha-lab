#ifndef __DAL_M0007_F1_RENDERER_MQH__
#define __DAL_M0007_F1_RENDERER_MQH__
#property strict
#include <M0007/DAL_M0007F1Types.mqh>

// M0007 renderer contract:
// - Draw only the clean F1 grammar requested by the research note.
// - No horizontal guide levels, no vertical audit lines, no internal N/R labels by default.
// - The drawing follows the real detector anchors: Start -> Leg 1 -> Correction -> Leg 2.

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

void M0007_DrawNodeDot(const string name, const datetime t, const double price, const color clr, const int font_size = 13)
{
   M0007_DrawTextRaw(name, t, price, "●", clr, font_size, ANCHOR_CENTER);
}

void M0007_DrawF1Schematic(const M0007_F1Event &e,
                           const string prefix,
                           const color clr,
                           const bool show_text_labels,
                           const bool show_badge)
{
   bool bullish = (e.direction == M0007_DIR_BULLISH);

   double leg1_size = MathAbs(e.H1.price - e.Start.price);
   double corr_size = MathAbs(e.H1.price - e.W.price);
   double leg2_size = MathAbs(e.H2.price - e.W.price);
   double h = MathMax(MathMax(leg1_size, corr_size), leg2_size);
   if(h <= 0.0) h = MathMax(100.0 * _Point, MathAbs(e.H1.price) * 0.001);

   // One straight line = true origin to end of Leg 1.
   M0007_DrawTrendRaw(prefix + "LEG1_STRAIGHT", e.Start.time, e.Start.price, e.H1.time, e.H1.price, clr, 3, STYLE_SOLID);

   // One clean curved path = end of Leg 1 -> correction -> end of Leg 2.
   datetime c1a_t = M0007_TimeAt(e.H1.time, e.W.time, 0.35);
   datetime c2a_t = M0007_TimeAt(e.H1.time, e.W.time, 0.70);
   datetime c1b_t = M0007_TimeAt(e.W.time, e.H2.time, 0.30);
   datetime c2b_t = M0007_TimeAt(e.W.time, e.H2.time, 0.68);

   double c1a_p, c2a_p, c1b_p, c2b_p;
   if(bullish)
   {
      c1a_p = e.H1.price - 0.10 * corr_size;
      c2a_p = e.W.price  + 0.08 * corr_size;
      c1b_p = e.W.price  + 0.06 * leg2_size;
      c2b_p = e.H2.price - 0.10 * leg2_size;
   }
   else
   {
      c1a_p = e.H1.price + 0.10 * corr_size;
      c2a_p = e.W.price  - 0.08 * corr_size;
      c1b_p = e.W.price  - 0.06 * leg2_size;
      c2b_p = e.H2.price + 0.10 * leg2_size;
   }

   M0007_DrawBezierCurve(prefix + "CURVE_A", e.H1.time, e.H1.price, c1a_t, c1a_p, c2a_t, c2a_p, e.W.time, e.W.price, clr, 3, 10);
   M0007_DrawBezierCurve(prefix + "CURVE_B", e.W.time, e.W.price, c1b_t, c1b_p, c2b_t, c2b_p, e.H2.time, e.H2.price, clr, 3, 10);

   M0007_DrawNodeDot(prefix + "DOT_START", e.Start.time, e.Start.price, clr, 13);
   M0007_DrawNodeDot(prefix + "DOT_LEG1",  e.H1.time,   e.H1.price,   clr, 13);
   M0007_DrawNodeDot(prefix + "DOT_CORR",  e.W.time,    e.W.price,    clr, 13);
   M0007_DrawNodeDot(prefix + "DOT_LEG2",  e.H2.time,   e.H2.price,   clr, 13);

   if(show_text_labels)
   {
      double text_gap = MathMax(0.12 * h, 35.0 * _Point);
      double small_gap = MathMax(0.08 * h, 20.0 * _Point);

      M0007_DrawTextRaw(prefix + "TXT_START", e.Start.time,
                        bullish ? e.Start.price - small_gap : e.Start.price + small_gap,
                        "Start", clr, 9,
                        bullish ? ANCHOR_LEFT_UPPER : ANCHOR_LEFT_LOWER);

      datetime leg1_label_t = M0007_TimeAt(e.Start.time, e.H1.time, 0.45);
      double leg1_label_p = (e.Start.price + e.H1.price) * 0.5;
      M0007_DrawTextRaw(prefix + "TXT_LEG1", leg1_label_t,
                        bullish ? leg1_label_p + text_gap : leg1_label_p - text_gap,
                        "Leg 1", clr, 10, ANCHOR_CENTER);

      datetime correction_label_t = M0007_TimeAt(e.H1.time, e.H2.time, 0.45);
      double correction_label_p = bullish ? e.W.price + 0.45 * h : e.W.price - 0.45 * h;
      M0007_DrawTextRaw(prefix + "TXT_CORRECTION", correction_label_t, correction_label_p,
                        "Correction", clr, 10, ANCHOR_CENTER);

      M0007_DrawTextRaw(prefix + "TXT_PULLBACK", e.W.time,
                        bullish ? e.W.price - text_gap : e.W.price + text_gap,
                        "Pullback / Correction", clr, 8, ANCHOR_CENTER);

      datetime leg2_label_t = M0007_TimeAt(e.W.time, e.H2.time, 0.70);
      double leg2_label_p = (e.W.price + e.H2.price) * 0.5;
      M0007_DrawTextRaw(prefix + "TXT_LEG2", leg2_label_t,
                        bullish ? leg2_label_p + text_gap : leg2_label_p - text_gap,
                        "Leg 2", clr, 10, ANCHOR_CENTER);
   }

   if(show_badge)
   {
      string badge = bullish ? "BULLISH F1" : "BEARISH F1";
      datetime badge_t = M0007_TimeAt(e.Start.time, e.H2.time, 0.58);
      double badge_p = bullish ? MathMax(e.H1.price, e.H2.price) + 0.35 * h
                               : MathMin(e.H1.price, e.H2.price) - 0.35 * h;
      M0007_DrawTextRaw(prefix + "TXT_BADGE", badge_t, badge_p, badge, clr, 12, ANCHOR_CENTER);
   }
}

void M0007_DrawEvent(const M0007_F1Event &e,
                     const string prefix,
                     const int event_number,
                     const bool show_text_labels,
                     const bool show_badge)
{
   string p = prefix + IntegerToString(event_number) + "_";
   color schematic_clr = (e.direction == M0007_DIR_BULLISH ? clrLimeGreen : clrTomato);
   M0007_DrawF1Schematic(e, p, schematic_clr, show_text_labels, show_badge);
}

int M0007_DrawEvents(const M0007_F1Event &events[],
                     const int max_events,
                     const bool draw_only_confirmed,
                     const string prefix,
                     const bool show_text_labels,
                     const bool show_badge)
{
   int drawn = 0;
   int total = ArraySize(events);

   for(int i=total-1; i>=0 && drawn<max_events; i--)
   {
      if(draw_only_confirmed && events[i].status != M0007_STATUS_CONFIRMED)
         continue;
      M0007_DrawEvent(events[i], prefix, drawn, show_text_labels, show_badge);
      drawn++;
   }

   ChartRedraw(0);
   return drawn;
}

#endif
