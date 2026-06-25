#property strict
#property description "Decision Alpha Lab - EXP0013 Astro Unified Dashboard EA"
#property description "Research-only visual dashboard. No orders. No iCustom. No indicator loading."
#property tester_file "astro_GMT3_M1_2026_to_now_mql.csv"
#property tester_file "astro\\astro_GMT3_M1_2026_to_now_mql.csv"
#property tester_file "astro_live_mql.csv"

#include <Research/DAL_AstroMapTypes.mqh>
#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroPathCleanlinessMetrics.mqh>
#include <Research/DAL_AstroFractalPathMetrics.mqh>

enum DAL_AstroDashboardView
{
   ASTRO_VIEW_COCKPIT = 0,
   ASTRO_VIEW_FOCUS   = 1
};

enum DAL_AstroSection
{
   ASTRO_SEC_PATH   = 0,
   ASTRO_SEC_MICRO  = 1,
   ASTRO_SEC_REGIME = 2,
   ASTRO_SEC_MACRO  = 3,
   ASTRO_SEC_RAW    = 4,
   ASTRO_SEC_DIAG   = 5
};

input string               InpAstroCsvFile             = "astro_live_mql.csv";
input double               InpBrokerGmtOffsetHours     = 0.0;
input bool                 InpRequireExactBarTime      = true;
input int                  InpReloadCsvEverySeconds    = 10;
input int                  InpRefreshSeconds           = 1;
input DAL_AstroDashboardView InpInitialViewMode        = ASTRO_VIEW_COCKPIT;
input DAL_AstroSection     InpInitialFocusSection      = ASTRO_SEC_PATH;

input bool                 InpShowTextPanel            = true;
input bool                 InpShowOscillator           = true;
input bool                 InpUseTerminalComment       = false;

input int                  InpBaseX                    = 10;
input int                  InpBaseY                    = 10;
input int                  InpHeaderWidth              = 980;
input int                  InpHeaderHeight             = 92;
input int                  InpCardWidth                = 320;
input int                  InpCardGap                  = 12;
input int                  InpCardRowHeight            = 16;
input int                  InpCardTitleHeight          = 20;
input int                  InpCardValueWidth           = 52;
input int                  InpFontSize                 = 10;
input int                  InpButtonW                  = 84;
input int                  InpButtonH                  = 18;

input int                  InpOscHeight                = 220;
input int                  InpOscHistoryBars           = 80;
input int                  InpOscPointSize             = 2;
input bool                 InpOscShowCurrentBar        = true;

input color                InpColorBackground          = clrBlack;
input color                InpColorPanel               = C'8,8,8';
input color                InpColorCard                = C'12,12,12';
input color                InpColorBorder              = clrDimGray;
input color                InpColorText                = clrWhite;
input color                InpColorMuted               = clrSilver;
input color                InpColorGood                = clrLime;
input color                InpColorRisk                = clrTomato;
input color                InpColorWarn                = clrOrange;
input color                InpColorInfo                = clrAqua;
input color                InpColorButtonOn            = C'25,55,25';
input color                InpColorButtonOff           = C'35,35,35';

DAL_AstroMapStore g_store;
bool      g_loaded = false;
datetime  g_last_load_time = 0;
string    g_prefix = "DAL_EXP0013_ASTRO_COCKPIT";
DAL_AstroDashboardView g_view_mode;
DAL_AstroSection g_focus_section;
bool      g_show_text;
bool      g_show_osc;
bool      g_show_path = true;
bool      g_show_micro = true;
bool      g_show_regime = true;
bool      g_show_macro = true;
bool      g_show_raw = true;

void DAL_DeleteByPrefix(const string prefix)
{
   long chart_id = ChartID();
   int total = ObjectsTotal(chart_id, -1, -1);
   for(int i = total - 1; i >= 0; i--)
   {
      string name = ObjectName(chart_id, i, -1, -1);
      if(StringFind(name, prefix) == 0)
         ObjectDelete(chart_id, name);
   }
}

void DAL_Rect(const string name, const int x, const int y, const int w, const int h, const color bg, const color border)
{
   long chart_id = ChartID();
   if(ObjectFind(chart_id, name) < 0)
      ObjectCreate(chart_id, name, OBJ_RECTANGLE_LABEL, 0, 0, 0);
   ObjectSetInteger(chart_id, name, OBJPROP_CORNER, CORNER_LEFT_UPPER);
   ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(chart_id, name, OBJPROP_XSIZE, w);
   ObjectSetInteger(chart_id, name, OBJPROP_YSIZE, h);
   ObjectSetInteger(chart_id, name, OBJPROP_BGCOLOR, bg);
   ObjectSetInteger(chart_id, name, OBJPROP_BORDER_TYPE, BORDER_FLAT);
   ObjectSetInteger(chart_id, name, OBJPROP_COLOR, border);
   ObjectSetInteger(chart_id, name, OBJPROP_BACK, false);
   ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, false);
   ObjectSetInteger(chart_id, name, OBJPROP_HIDDEN, true);
}

void DAL_Label(const string name, const string text, const int x, const int y, const color clr, const int font_size, const string font = "Consolas")
{
   long chart_id = ChartID();
   if(ObjectFind(chart_id, name) < 0)
      ObjectCreate(chart_id, name, OBJ_LABEL, 0, 0, 0);
   ObjectSetInteger(chart_id, name, OBJPROP_CORNER, CORNER_LEFT_UPPER);
   ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, y);
   ObjectSetString(chart_id, name, OBJPROP_TEXT, text);
   ObjectSetString(chart_id, name, OBJPROP_FONT, font);
   ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, font_size);
   ObjectSetInteger(chart_id, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, false);
   ObjectSetInteger(chart_id, name, OBJPROP_HIDDEN, true);
}

void DAL_Button(const string name, const string text, const int x, const int y, const int w, const int h, const bool active)
{
   long chart_id = ChartID();
   if(ObjectFind(chart_id, name) < 0)
      ObjectCreate(chart_id, name, OBJ_BUTTON, 0, 0, 0);
   ObjectSetInteger(chart_id, name, OBJPROP_CORNER, CORNER_LEFT_UPPER);
   ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(chart_id, name, OBJPROP_XSIZE, w);
   ObjectSetInteger(chart_id, name, OBJPROP_YSIZE, h);
   ObjectSetString(chart_id, name, OBJPROP_TEXT, text);
   ObjectSetString(chart_id, name, OBJPROP_FONT, "Consolas");
   ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, 8);
   ObjectSetInteger(chart_id, name, OBJPROP_COLOR, active ? InpColorGood : InpColorText);
   ObjectSetInteger(chart_id, name, OBJPROP_BGCOLOR, active ? InpColorButtonOn : InpColorButtonOff);
   ObjectSetInteger(chart_id, name, OBJPROP_BORDER_COLOR, InpColorBorder);
   ObjectSetInteger(chart_id, name, OBJPROP_HIDDEN, true);
   ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, false);
}

string DAL_TimeText(const datetime t)
{
   if(t <= 0) return "n/a";
   return TimeToString(t, TIME_DATE | TIME_MINUTES);
}

string DAL_Shorten(const string s, const int max_len)
{
   int len = StringLen(s);
   if(len <= max_len || max_len <= 7)
      return s;
   int keep = (max_len - 3) / 2;
   return StringSubstr(s, 0, keep) + "..." + StringSubstr(s, len - keep);
}

string DAL_Bucket(const double v)
{
   if(v < 20.0) return "very_low";
   if(v < 40.0) return "low";
   if(v < 60.0) return "mid";
   if(v < 80.0) return "high";
   return "very_high";
}

color DAL_ValueColor(const string name, const double v)
{
   bool inverse = (
      name == "Friction" || name == "Pressure" || name == "Transition" ||
      name == "PullbackRisk" || name == "ChopRisk" || name == "M1DirtyWindow" ||
      name == "MacroDrag" || name == "MacroPressure" || name == "MacroTransition" ||
      name == "OuterStation" || name == "MarsSatFriction" || name == "MercuryNoise" ||
      name == "MoonPressure" || name == "MoonDrag" || name == "MoonBoundary" ||
      name == "MicroNoise" || name == "SaturnResistance");
   if(inverse)
   {
      if(v >= 70.0) return InpColorRisk;
      if(v >= 45.0) return InpColorWarn;
      return InpColorGood;
   }
   if(v >= 70.0) return InpColorGood;
   if(v >= 45.0) return InpColorInfo;
   if(v >= 25.0) return InpColorWarn;
   return InpColorMuted;
}

bool DAL_LoadStore()
{
   g_last_load_time = TimeCurrent();
   g_loaded = DAL_AstroMapStore_LoadExcelCsv(
      g_store,
      InpAstroCsvFile,
      InpBrokerGmtOffsetHours,
      PeriodSeconds(_Period) / 60
   );
   if(!g_loaded)
   {
      Print("EXP0013 Astro Dashboard | CSV load failed | file=", InpAstroCsvFile);
      return false;
   }
   Print("EXP0013 Astro Dashboard | CSV loaded | rows=", g_store.row_count, " | source=", g_store.source_file);
   return true;
}

bool DAL_ShouldReload()
{
   if(InpReloadCsvEverySeconds <= 0) return false;
   if(g_last_load_time <= 0) return true;
   return (TimeCurrent() - g_last_load_time) >= InpReloadCsvEverySeconds;
}

bool DAL_FindFractalByShift(const int shift, DAL_AstroFractalMetrics &f, bool &exact_match, bool &fallback_match)
{
   DAL_AstroFM_Reset(f);
   exact_match = false;
   fallback_match = false;
   datetime candle_time = iTime(_Symbol, _Period, shift);
   if(candle_time <= 0) return false;

   DAL_AstroMapRow row;
   if(DAL_AstroMapStore_FindForCandleOpen(g_store, candle_time, row, true))
   {
      exact_match = true;
      return DAL_AstroFM_Calc(row, f) && f.valid;
   }

   if(DAL_AstroMapStore_FindForCandleOpen(g_store, candle_time, row, false))
   {
      fallback_match = true;
      return DAL_AstroFM_Calc(row, f) && f.valid;
   }
   return false;
}

void DAL_FillPath(const DAL_AstroFractalMetrics &f, string &names[], double &vals[], int &count)
{
   count = 8;
   names[0] = "CleanPath";      vals[0] = f.clean_path;
   names[1] = "CleanImpulse";   vals[1] = f.clean_impulse;
   names[2] = "SmoothCont";     vals[2] = f.smooth_continuation;
   names[3] = "BreakoutFT";     vals[3] = f.breakout_followthrough;
   names[4] = "PullbackRisk";   vals[4] = f.pullback_risk;
   names[5] = "ChopRisk";       vals[5] = f.chop_risk;
   names[6] = "M1CleanWindow";  vals[6] = f.m1_clean_window;
   names[7] = "M1DirtyWindow";  vals[7] = f.m1_dirty_window;
}

void DAL_FillMicro(const DAL_AstroFractalMetrics &f, string &names[], double &vals[], int &count)
{
   count = 8;
   names[0] = "MoonTempo";    vals[0] = f.moon_tempo;
   names[1] = "MoonPressure"; vals[1] = f.moon_pressure;
   names[2] = "MoonFlow";     vals[2] = f.moon_flow;
   names[3] = "MoonDrag";     vals[3] = f.moon_drag;
   names[4] = "MoonBoundary"; vals[4] = f.moon_boundary;
   names[5] = "MoonOOB";      vals[5] = f.moon_oob_intensity;
   names[6] = "MicroNoise";   vals[6] = f.micro_noise;
   names[7] = "MicroClean";   vals[7] = f.micro_cleanliness;
}

void DAL_FillRegime(const DAL_AstroFractalMetrics &f, string &names[], double &vals[], int &count)
{
   count = 8;
   names[0] = "MarsImpulse";      vals[0] = f.mars_impulse;
   names[1] = "MarsCleanImpulse"; vals[1] = f.mars_clean_impulse;
   names[2] = "MarsSatFriction";  vals[2] = f.mars_saturn_friction;
   names[3] = "MarsJupExpand";    vals[3] = f.mars_jupiter_expansion;
   names[4] = "MercuryNoise";     vals[4] = f.mercury_noise;
   names[5] = "VenusMarsCoh";     vals[5] = f.venus_mars_cohesion;
   names[6] = "JupiterSupport";   vals[6] = f.jupiter_support;
   names[7] = "SaturnResist";     vals[7] = f.saturn_resistance;
}

void DAL_FillMacro(const DAL_AstroFractalMetrics &f, string &names[], double &vals[], int &count)
{
   count = 8;
   names[0] = "MacroFlow";      vals[0] = f.macro_flow;
   names[1] = "MacroDrag";      vals[1] = f.macro_drag;
   names[2] = "MacroPressure";  vals[2] = f.macro_pressure;
   names[3] = "MacroTransition";vals[3] = f.macro_transition;
   names[4] = "Expansion";      vals[4] = f.macro_expansion;
   names[5] = "Compression";    vals[5] = f.macro_compression;
   names[6] = "OuterStation";   vals[6] = f.outer_station_risk;
   names[7] = "StructuralBias"; vals[7] = f.structural_bias;
}

void DAL_FillRaw(const DAL_AstroFractalMetrics &f, string &names[], double &vals[], int &count)
{
   count = 7;
   names[0] = "Flow";        vals[0] = f.raw_flow;
   names[1] = "Impulse";     vals[1] = f.raw_impulse;
   names[2] = "Friction";    vals[2] = f.raw_friction;
   names[3] = "Pressure";    vals[3] = f.raw_pressure;
   names[4] = "Transition";  vals[4] = f.raw_transition;
   names[5] = "MoonTempo";   vals[5] = f.raw_moon_tempo;
   names[6] = "SaturnDrag";  vals[6] = f.raw_saturn_drag;
}

string DAL_SectionTitle(const DAL_AstroSection s)
{
   if(s == ASTRO_SEC_PATH) return "PATH QUALITY";
   if(s == ASTRO_SEC_MICRO) return "MICRO M1";
   if(s == ASTRO_SEC_REGIME) return "REGIME ENGINE";
   if(s == ASTRO_SEC_MACRO) return "MACRO BACKGROUND";
   if(s == ASTRO_SEC_RAW) return "RAW AXES";
   return "DIAGNOSTICS";
}

void DAL_GetSectionData(const DAL_AstroSection s, const DAL_AstroFractalMetrics &f, string &names[], double &vals[], int &count)
{
   count = 0;
   if(s == ASTRO_SEC_PATH)   { DAL_FillPath(f, names, vals, count); return; }
   if(s == ASTRO_SEC_MICRO)  { DAL_FillMicro(f, names, vals, count); return; }
   if(s == ASTRO_SEC_REGIME) { DAL_FillRegime(f, names, vals, count); return; }
   if(s == ASTRO_SEC_MACRO)  { DAL_FillMacro(f, names, vals, count); return; }
   if(s == ASTRO_SEC_RAW)    { DAL_FillRaw(f, names, vals, count); return; }
}

bool DAL_IsSectionVisible(const DAL_AstroSection s)
{
   if(s == ASTRO_SEC_PATH) return g_show_path;
   if(s == ASTRO_SEC_MICRO) return g_show_micro;
   if(s == ASTRO_SEC_REGIME) return g_show_regime;
   if(s == ASTRO_SEC_MACRO) return g_show_macro;
   if(s == ASTRO_SEC_RAW) return g_show_raw;
   return true;
}

void DAL_SetSectionVisible(const DAL_AstroSection s, const bool v)
{
   if(s == ASTRO_SEC_PATH) g_show_path = v;
   else if(s == ASTRO_SEC_MICRO) g_show_micro = v;
   else if(s == ASTRO_SEC_REGIME) g_show_regime = v;
   else if(s == ASTRO_SEC_MACRO) g_show_macro = v;
   else if(s == ASTRO_SEC_RAW) g_show_raw = v;
}

void DAL_DrawCard(const string key, const string title, const int x, const int y, const int w, const string &names[], const double &vals[], const int count)
{
   int h = InpCardTitleHeight + 8 + count * InpCardRowHeight + 8;
   DAL_Rect(g_prefix + "_CARD_BG_" + key, x, y, w, h, InpColorCard, InpColorBorder);
   DAL_Label(g_prefix + "_CARD_TITLE_" + key, title, x + 8, y + 4, InpColorInfo, InpFontSize);
   int bar_x = x + w - 110;
   int bar_w = 90;
   for(int i = 0; i < count; i++)
   {
      int ry = y + InpCardTitleHeight + 6 + i * InpCardRowHeight;
      color clr = DAL_ValueColor(names[i], vals[i]);
      DAL_Label(g_prefix + "_CARD_L_" + key + "_" + IntegerToString(i), names[i], x + 8, ry, InpColorText, 8);
      DAL_Label(g_prefix + "_CARD_V_" + key + "_" + IntegerToString(i), DoubleToString(vals[i], 1), x + 126, ry, clr, 8);
      DAL_Rect(g_prefix + "_CARD_BARBG_" + key + "_" + IntegerToString(i), bar_x, ry + 2, bar_w, 10, C'25,25,25', InpColorBorder);
      int fill_w = (int)MathRound(MathMax(0.0, MathMin(100.0, vals[i])) / 100.0 * bar_w);
      DAL_Rect(g_prefix + "_CARD_BAR_" + key + "_" + IntegerToString(i), bar_x, ry + 2, fill_w, 10, clr, clr);
   }
}

void DAL_DrawDiagnostics(const int x, const int y, const int w, const bool have_row, const bool exact_match, const bool fallback_match, const DAL_AstroFractalMetrics &f)
{
   int count = 7;
   int h = InpCardTitleHeight + 8 + count * InpCardRowHeight + 8;
   DAL_Rect(g_prefix + "_CARD_BG_DIAG", x, y, w, h, InpColorCard, InpColorBorder);
   DAL_Label(g_prefix + "_CARD_TITLE_DIAG", "DIAGNOSTICS", x + 8, y + 4, InpColorInfo, InpFontSize);
   int ry = y + InpCardTitleHeight + 6;
   DAL_Label(g_prefix + "_DIAG_0", "CSV status", x + 8, ry, InpColorText, 8); DAL_Label(g_prefix + "_DIAGV_0", g_loaded ? "LOADED" : "NOT_LOADED", x + 116, ry, g_loaded ? InpColorGood : InpColorRisk, 8); ry += InpCardRowHeight;
   DAL_Label(g_prefix + "_DIAG_1", "rows", x + 8, ry, InpColorText, 8); DAL_Label(g_prefix + "_DIAGV_1", IntegerToString(g_store.row_count), x + 116, ry, InpColorMuted, 8); ry += InpCardRowHeight;
   DAL_Label(g_prefix + "_DIAG_2", "source", x + 8, ry, InpColorText, 8); DAL_Label(g_prefix + "_DIAGV_2", DAL_Shorten(g_store.source_file, 30), x + 116, ry, InpColorMuted, 8); ry += InpCardRowHeight;
   DAL_Label(g_prefix + "_DIAG_3", "chart candle", x + 8, ry, InpColorText, 8); DAL_Label(g_prefix + "_DIAGV_3", DAL_TimeText(iTime(_Symbol, _Period, 0)), x + 116, ry, InpColorText, 8); ry += InpCardRowHeight;
   DAL_Label(g_prefix + "_DIAG_4", "lookup", x + 8, ry, InpColorText, 8);
   string lk = have_row ? (exact_match ? "exact" : (fallback_match ? "fallback" : "unknown")) : "row_not_found";
   DAL_Label(g_prefix + "_DIAGV_4", lk, x + 116, ry, exact_match ? InpColorGood : (fallback_match ? InpColorWarn : InpColorRisk), 8); ry += InpCardRowHeight;
   DAL_Label(g_prefix + "_DIAG_5", "matched broker", x + 8, ry, InpColorText, 8); DAL_Label(g_prefix + "_DIAGV_5", have_row ? DAL_TimeText(f.broker_time) : "n/a", x + 116, ry, InpColorMuted, 8); ry += InpCardRowHeight;
   DAL_Label(g_prefix + "_DIAG_6", "hint", x + 8, ry, InpColorText, 8);
   string hint = have_row ? "dashboard ok" : "extend live window or check broker GMT";
   DAL_Label(g_prefix + "_DIAGV_6", DAL_Shorten(hint, 32), x + 116, ry, have_row ? InpColorGood : InpColorWarn, 8);
}

void DAL_DrawHeader(const bool have_row, const bool exact_match, const bool fallback_match, const DAL_AstroFractalMetrics &f)
{
   DAL_Rect(g_prefix + "_HEADER_BG", InpBaseX, InpBaseY, InpHeaderWidth, InpHeaderHeight, InpColorPanel, InpColorBorder);
   DAL_Label(g_prefix + "_H0", "EXP0013 ASTRO COCKPIT  |  no-trade  |  no-iCustom  |  live/python-ready", InpBaseX + 8, InpBaseY + 6, InpColorInfo, 12);
   DAL_Label(g_prefix + "_H1", "Symbol=" + _Symbol + "   TF=" + EnumToString(_Period) + "   View=" + (g_view_mode == ASTRO_VIEW_COCKPIT ? "COCKPIT" : "FOCUS") + "   Focus=" + DAL_SectionTitle(g_focus_section), InpBaseX + 8, InpBaseY + 24, InpColorText, 10);
   string row_status = !g_loaded ? "CSV NOT LOADED" : (!have_row ? "ROW NOT FOUND" : (exact_match ? "EXACT ROW" : "FALLBACK ROW"));
   color row_clr = !g_loaded ? InpColorRisk : (!have_row ? InpColorRisk : (exact_match ? InpColorGood : InpColorWarn));
   DAL_Label(g_prefix + "_H2", row_status + "   file=" + DAL_Shorten(InpAstroCsvFile, 38), InpBaseX + 8, InpBaseY + 42, row_clr, 10);
   string line3 = have_row ? ("Broker=" + DAL_TimeText(f.broker_time) + "   UTC=" + DAL_TimeText(f.utc_time) + "   Thesis=" + DAL_Shorten(f.thesis, 54))
                           : ("Chart candle=" + DAL_TimeText(iTime(_Symbol, _Period, 0)) + "   ReloadSec=" + IntegerToString(InpReloadCsvEverySeconds));
   DAL_Label(g_prefix + "_H3", line3, InpBaseX + 8, InpBaseY + 60, have_row ? InpColorMuted : InpColorWarn, 9);

   int bx = InpBaseX + 560;
   int by = InpBaseY + 6;
   DAL_Button(g_prefix + "_BTN_COCKPIT", "COCKPIT", bx, by, InpButtonW, InpButtonH, g_view_mode == ASTRO_VIEW_COCKPIT); bx += InpButtonW + 4;
   DAL_Button(g_prefix + "_BTN_PATH", "PATH", bx, by, 54, InpButtonH, g_view_mode == ASTRO_VIEW_FOCUS && g_focus_section == ASTRO_SEC_PATH); bx += 58;
   DAL_Button(g_prefix + "_BTN_MICRO", "MICRO", bx, by, 54, InpButtonH, g_view_mode == ASTRO_VIEW_FOCUS && g_focus_section == ASTRO_SEC_MICRO); bx += 58;
   DAL_Button(g_prefix + "_BTN_REGIME", "REGIME", bx, by, 60, InpButtonH, g_view_mode == ASTRO_VIEW_FOCUS && g_focus_section == ASTRO_SEC_REGIME); bx += 64;
   DAL_Button(g_prefix + "_BTN_MACRO", "MACRO", bx, by, 58, InpButtonH, g_view_mode == ASTRO_VIEW_FOCUS && g_focus_section == ASTRO_SEC_MACRO); bx += 62;
   DAL_Button(g_prefix + "_BTN_RAW", "RAW", bx, by, 46, InpButtonH, g_view_mode == ASTRO_VIEW_FOCUS && g_focus_section == ASTRO_SEC_RAW);

   bx = InpBaseX + 560;
   by = InpBaseY + 30;
   DAL_Button(g_prefix + "_BTN_TEX", g_show_text ? "TEXT ON" : "TEXT OFF", bx, by, 70, InpButtonH, g_show_text); bx += 74;
   DAL_Button(g_prefix + "_BTN_OSC", g_show_osc ? "OSC ON" : "OSC OFF", bx, by, 64, InpButtonH, g_show_osc); bx += 68;
   DAL_Button(g_prefix + "_BTN_PTH", g_show_path ? "PTH" : "-PTH", bx, by, 44, InpButtonH, g_show_path); bx += 48;
   DAL_Button(g_prefix + "_BTN_MCR", g_show_micro ? "MIC" : "-MIC", bx, by, 44, InpButtonH, g_show_micro); bx += 48;
   DAL_Button(g_prefix + "_BTN_RGM", g_show_regime ? "REG" : "-REG", bx, by, 44, InpButtonH, g_show_regime); bx += 48;
   DAL_Button(g_prefix + "_BTN_MCG", g_show_macro ? "MAC" : "-MAC", bx, by, 44, InpButtonH, g_show_macro); bx += 48;
   DAL_Button(g_prefix + "_BTN_RAWT", g_show_raw ? "RAW" : "-RAW", bx, by, 44, InpButtonH, g_show_raw); bx += 48;
   DAL_Button(g_prefix + "_BTN_RELD", "RELOAD", bx, by, 60, InpButtonH, false);
}

void DAL_DrawFocusCard(const DAL_AstroSection sec, const DAL_AstroFractalMetrics &f)
{
   string names[8]; double vals[8]; int count;
   DAL_GetSectionData(sec, f, names, vals, count);
   DAL_DrawCard(IntegerToString((int)sec), DAL_SectionTitle(sec), InpBaseX, InpBaseY + InpHeaderHeight + 10, 420, names, vals, count);
}

void DAL_DrawCockpitCards(const bool have_row, const bool exact_match, const bool fallback_match, const DAL_AstroFractalMetrics &f)
{
   int start_y = InpBaseY + InpHeaderHeight + 10;
   int x1 = InpBaseX;
   int x2 = InpBaseX + InpCardWidth + InpCardGap;
   int x3 = InpBaseX + 2 * (InpCardWidth + InpCardGap);
   int y1 = start_y;
   int y2 = start_y;
   int y3 = start_y;

   string names[8]; double vals[8]; int count;
   if(g_show_path)
   {
      DAL_GetSectionData(ASTRO_SEC_PATH, f, names, vals, count);
      DAL_DrawCard("PATH", "PATH QUALITY", x1, y1, InpCardWidth, names, vals, count);
      y1 += InpCardTitleHeight + 8 + count * InpCardRowHeight + 20;
   }
   if(g_show_micro)
   {
      DAL_GetSectionData(ASTRO_SEC_MICRO, f, names, vals, count);
      DAL_DrawCard("MICRO", "MICRO M1", x2, y2, InpCardWidth, names, vals, count);
      y2 += InpCardTitleHeight + 8 + count * InpCardRowHeight + 20;
   }
   if(g_show_regime)
   {
      DAL_GetSectionData(ASTRO_SEC_REGIME, f, names, vals, count);
      DAL_DrawCard("REGIME", "REGIME ENGINE", x3, y3, InpCardWidth, names, vals, count);
      y3 += InpCardTitleHeight + 8 + count * InpCardRowHeight + 20;
   }
   if(g_show_macro)
   {
      DAL_GetSectionData(ASTRO_SEC_MACRO, f, names, vals, count);
      DAL_DrawCard("MACRO", "MACRO BACKGROUND", x1, y1, InpCardWidth, names, vals, count);
      y1 += InpCardTitleHeight + 8 + count * InpCardRowHeight + 20;
   }
   if(g_show_raw)
   {
      DAL_GetSectionData(ASTRO_SEC_RAW, f, names, vals, count);
      DAL_DrawCard("RAW", "RAW AXES", x2, y2, InpCardWidth, names, vals, count);
      y2 += InpCardTitleHeight + 8 + count * InpCardRowHeight + 20;
   }
   DAL_DrawDiagnostics(x3, y3, InpCardWidth, have_row, exact_match, fallback_match, f);
}

DAL_AstroSection DAL_OscSection()
{
   if(g_view_mode == ASTRO_VIEW_FOCUS)
      return g_focus_section;
   if(g_show_path) return ASTRO_SEC_PATH;
   if(g_show_micro) return ASTRO_SEC_MICRO;
   if(g_show_regime) return ASTRO_SEC_REGIME;
   if(g_show_macro) return ASTRO_SEC_MACRO;
   return ASTRO_SEC_RAW;
}

void DAL_DrawOscillator(const DAL_AstroSection sec)
{
   if(!g_show_osc) return;
   int x = InpBaseX;
   int y = InpBaseY + InpHeaderHeight + 10;
   if(g_view_mode == ASTRO_VIEW_COCKPIT)
      y += 2 * (InpCardTitleHeight + 8 + 8 * InpCardRowHeight + 20);
   else
      y += InpCardTitleHeight + 8 + 8 * InpCardRowHeight + 30;

   string names[8]; double vals[8]; int count;
   bool exact0, fallback0; DAL_AstroFractalMetrics f0;
   if(!DAL_FindFractalByShift(0, f0, exact0, fallback0)) return;
   DAL_GetSectionData(sec, f0, names, vals, count);

   int legend_w = 120;
   int value_w = 46;
   int hist_w = 860 - legend_w - value_w - 18;
   int title_h = 22;
   int row_h = 20;
   int total_h = title_h + count * row_h + 10;
   DAL_Rect(g_prefix + "_OSC_BG", x, y, 860, total_h, InpColorPanel, InpColorBorder);
   DAL_Label(g_prefix + "_OSC_TITLE", "OSCILLATOR 0..100  |  " + DAL_SectionTitle(sec), x + 8, y + 4, InpColorInfo, 10);
   int bars = MathMax(10, MathMin(InpOscHistoryBars, 160));
   double step = (double)hist_w / (double)MathMax(1, bars - 1);

   for(int r = 0; r < count; r++)
   {
      int ry = y + title_h + r * row_h;
      DAL_Label(g_prefix + "_OSC_N_" + IntegerToString(r), names[r], x + 8, ry + 2, InpColorText, 8);
      DAL_Label(g_prefix + "_OSC_V_" + IntegerToString(r), DoubleToString(vals[r],1), x + 88, ry + 2, DAL_ValueColor(names[r], vals[r]), 8);
      int hist_x0 = x + legend_w;
      DAL_Rect(g_prefix + "_OSC_LINE_" + IntegerToString(r), hist_x0, ry + row_h/2, hist_w, 1, InpColorBorder, InpColorBorder);
      if(InpOscShowCurrentBar)
      {
         DAL_Rect(g_prefix + "_OSC_BARBG_" + IntegerToString(r), x + legend_w - 44, ry + 4, 34, 10, C'20,20,20', InpColorBorder);
         DAL_Rect(g_prefix + "_OSC_BAR_" + IntegerToString(r), x + legend_w - 44, ry + 4, (int)MathRound(MathMax(0.0, MathMin(100.0, vals[r]))/100.0*34), 10, DAL_ValueColor(names[r], vals[r]), DAL_ValueColor(names[r], vals[r]));
      }
      for(int i = 0; i < bars; i++)
      {
         bool ex, fb; DAL_AstroFractalMetrics ft;
         string hnames[8]; double hvals[8]; int hcount;
         if(!DAL_FindFractalByShift(bars - 1 - i, ft, ex, fb))
         {
            string ptname = g_prefix + "_OSC_P_" + IntegerToString(r) + "_" + IntegerToString(i);
            if(ObjectFind(ChartID(), ptname) >= 0) ObjectDelete(ChartID(), ptname);
            continue;
         }
         DAL_GetSectionData(sec, ft, hnames, hvals, hcount);
         double v = (r < hcount ? hvals[r] : 0.0);
         int px = hist_x0 + (int)MathRound(i * step);
         int py = ry + row_h - 4 - (int)MathRound(MathMax(0.0, MathMin(100.0, v)) / 100.0 * (row_h - 8));
         DAL_Rect(g_prefix + "_OSC_P_" + IntegerToString(r) + "_" + IntegerToString(i), px, py, InpOscPointSize, InpOscPointSize, DAL_ValueColor(names[r], v), DAL_ValueColor(names[r], v));
      }
   }
}

void DAL_Render()
{
   if(DAL_ShouldReload()) DAL_LoadStore();

   bool have_row = false, exact_match = false, fallback_match = false;
   DAL_AstroFractalMetrics f;
   DAL_AstroFM_Reset(f);
   if(g_loaded) have_row = DAL_FindFractalByShift(0, f, exact_match, fallback_match);

   DAL_DrawHeader(have_row, exact_match, fallback_match, f);

   if(g_show_text)
   {
      if(g_view_mode == ASTRO_VIEW_COCKPIT)
         DAL_DrawCockpitCards(have_row, exact_match, fallback_match, f);
      else if(have_row)
      {
         DAL_DrawFocusCard(g_focus_section, f);
         DAL_DrawDiagnostics(InpBaseX + 440, InpBaseY + InpHeaderHeight + 10, 320, have_row, exact_match, fallback_match, f);
      }
      else
         DAL_DrawDiagnostics(InpBaseX, InpBaseY + InpHeaderHeight + 10, 420, have_row, exact_match, fallback_match, f);
   }

   if(have_row)
      DAL_DrawOscillator(DAL_OscSection());

   if(InpUseTerminalComment)
   {
      string status = !g_loaded ? "CSV NOT LOADED" : (!have_row ? "ROW NOT FOUND" : (exact_match ? "EXACT" : "FALLBACK"));
      Comment("EXP0013 Astro Dashboard | ", status, " | ", (have_row ? f.thesis : "no row"));
   }

   ChartRedraw(ChartID());
}

int OnInit()
{
   g_prefix = "DAL_EXP0013_ASTRO_" + IntegerToString((int)ChartID());
   g_view_mode = InpInitialViewMode;
   g_focus_section = InpInitialFocusSection;
   g_show_text = InpShowTextPanel;
   g_show_osc = InpShowOscillator;
   EventSetTimer(MathMax(1, InpRefreshSeconds));
   DAL_LoadStore();
   DAL_Render();
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   DAL_DeleteByPrefix(g_prefix);
   if(InpUseTerminalComment) Comment("");
}

void OnTick() {}

void OnTimer()
{
   DAL_Render();
}

void OnChartEvent(const int id, const long &lparam, const double &dparam, const string &sparam)
{
   if(id != CHARTEVENT_OBJECT_CLICK) return;
   if(sparam == g_prefix + "_BTN_COCKPIT") { g_view_mode = ASTRO_VIEW_COCKPIT; }
   else if(sparam == g_prefix + "_BTN_PATH") { g_view_mode = ASTRO_VIEW_FOCUS; g_focus_section = ASTRO_SEC_PATH; }
   else if(sparam == g_prefix + "_BTN_MICRO") { g_view_mode = ASTRO_VIEW_FOCUS; g_focus_section = ASTRO_SEC_MICRO; }
   else if(sparam == g_prefix + "_BTN_REGIME") { g_view_mode = ASTRO_VIEW_FOCUS; g_focus_section = ASTRO_SEC_REGIME; }
   else if(sparam == g_prefix + "_BTN_MACRO") { g_view_mode = ASTRO_VIEW_FOCUS; g_focus_section = ASTRO_SEC_MACRO; }
   else if(sparam == g_prefix + "_BTN_RAW") { g_view_mode = ASTRO_VIEW_FOCUS; g_focus_section = ASTRO_SEC_RAW; }
   else if(sparam == g_prefix + "_BTN_TEX") { g_show_text = !g_show_text; }
   else if(sparam == g_prefix + "_BTN_OSC") { g_show_osc = !g_show_osc; }
   else if(sparam == g_prefix + "_BTN_PTH") { g_show_path = !g_show_path; }
   else if(sparam == g_prefix + "_BTN_MCR") { g_show_micro = !g_show_micro; }
   else if(sparam == g_prefix + "_BTN_RGM") { g_show_regime = !g_show_regime; }
   else if(sparam == g_prefix + "_BTN_MCG") { g_show_macro = !g_show_macro; }
   else if(sparam == g_prefix + "_BTN_RAWT") { g_show_raw = !g_show_raw; }
   else if(sparam == g_prefix + "_BTN_RELD") { DAL_LoadStore(); }
   DAL_Render();
}
