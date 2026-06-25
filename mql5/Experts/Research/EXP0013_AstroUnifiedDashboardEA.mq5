#property strict
#property description "Decision Alpha Lab - EXP0013 Astro Unified Dashboard EA"
#property description "Research-only astro dashboard. Enhanced header clarity and spacing."
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
   ASTRO_SEC_RAW    = 4
};

input string                 InpAstroCsvFile             = "astro_live_mql.csv";
input double                 InpBrokerGmtOffsetHours     = 0.0;
input bool                   InpRequireExactBarTime      = true;
input int                    InpReloadCsvEverySeconds    = 10;
input int                    InpRefreshSeconds           = 1;
input DAL_AstroDashboardView InpInitialViewMode          = ASTRO_VIEW_COCKPIT;
input DAL_AstroSection       InpInitialFocusSection      = ASTRO_SEC_PATH;
input bool                   InpShowTextPanel            = true;
input bool                   InpShowOscillator           = true;
input bool                   InpUseTerminalComment       = false;

input int                    InpBaseX                    = 10;
input int                    InpBaseY                    = 10;
input int                    InpFontHero                 = 13;
input int                    InpFontTitle                = 12;
input int                    InpFontBody                 = 10;
input int                    InpFontSmall                = 9;
input int                    InpHeaderHeight             = 100;
input int                    InpGap                      = 16;
input int                    InpCardTitleHeight          = 26;
input int                    InpCardRowHeight            = 24;
input int                    InpButtonW                  = 124;
input int                    InpButtonH                  = 30;
input int                    InpCompactHistoryBars       = 18;
input int                    InpSparkPointSize           = 2;

input color                  InpColorPanel               = C'7,7,7';
input color                  InpColorCard                = C'10,10,10';
input color                  InpColorBorder              = C'88,88,88';
input color                  InpColorText                = clrWhite;
input color                  InpColorMuted               = clrSilver;
input color                  InpColorInfo                = clrAqua;
input color                  InpColorLow                 = clrTomato;
input color                  InpColorMid                 = clrGold;
input color                  InpColorHigh                = clrLime;
input color                  InpColorButtonOn            = C'24,74,24';
input color                  InpColorButtonOff           = C'36,36,36';

DAL_AstroMapStore g_store;
bool     g_loaded = false;
datetime g_last_load_time = 0;
string   g_prefix = "DAL_EXP0013_ASTRO_V13";
bool     g_force_rebuild = false;
DAL_AstroDashboardView g_view_mode;
DAL_AstroSection g_focus_section;
bool g_show_text;
bool g_show_osc;
bool g_minimized = false;

struct DAL_Layout
{
   int chart_w;
   int chart_h;
   int x;
   int y;
   int header_w;
   int header_h;
   int diag_w;
   int left_w;
   int card_w;
   int card_h;
   int col1_x;
   int col2_x;
   int diag_x;
   int row1_y;
   int row2_y;
   int osc_x;
   int osc_y;
   int osc_w;
   int focus_w;
};

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

void DAL_CleanupAllAstroObjects()
{
   DAL_DeleteByPrefix("DAL_EXP0013_ASTRO");
   DAL_DeleteByPrefix("DAL_EXP0013_ASTRO_");
   DAL_DeleteByPrefix("DAL_EXP0013_ASTRO_COCKPIT");
   DAL_DeleteByPrefix("DAL_EXP0013_ASTRO_PRO");
   DAL_DeleteByPrefix("DAL_EXP0013_ASTRO_V6");
   DAL_DeleteByPrefix("DAL_EXP0013_ASTRO_V7");
   DAL_DeleteByPrefix("DAL_EXP0013_ASTRO_V8");
   DAL_DeleteByPrefix("DAL_EXP0013_ASTRO_V9");
   DAL_DeleteByPrefix("DAL_EXP0013_ASTRO_V10");
   DAL_DeleteByPrefix("DAL_EXP0013_ASTRO_V11");
   DAL_DeleteByPrefix("DAL_EXP0013_ASTRO_V12");
   DAL_DeleteByPrefix("DAL_EXP0013_ASTRO_V13");
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

void DAL_LineH(const string name, const int x, const int y, const int w, const color clr)
{
   DAL_Rect(name, x, y, w, 1, clr, clr);
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
   ObjectSetInteger(chart_id, name, OBJPROP_COLOR, active ? InpColorHigh : InpColorText);
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
   if(len <= max_len || max_len <= 7) return s;
   int keep = (max_len - 3) / 2;
   return StringSubstr(s, 0, keep) + "..." + StringSubstr(s, len - keep);
}

string DAL_Bucket(const double v)
{
   if(v < 33.34) return "low";
   if(v < 66.67) return "mid";
   return "high";
}

color DAL_HeatColor(const double v)
{
   if(v < 33.34) return InpColorLow;
   if(v < 66.67) return InpColorMid;
   return InpColorHigh;
}

int DAL_MaxLabelLen(const string &names[], const int count)
{
   int max_len = 0;
   for(int i = 0; i < count; i++)
   {
      int len = StringLen(names[i]);
      if(len > max_len) max_len = len;
   }
   return max_len;
}

int DAL_LabelWidthPx(const int max_len)
{
   int px = max_len * 10 + 44;
   if(px < 188) px = 188;
   if(px > 310) px = 310;
   return px;
}

bool DAL_LoadStore()
{
   g_last_load_time = TimeCurrent();
   g_loaded = DAL_AstroMapStore_LoadExcelCsv(g_store, InpAstroCsvFile, InpBrokerGmtOffsetHours, PeriodSeconds(_Period) / 60);
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

string DAL_SectionTitle(const DAL_AstroSection s)
{
   if(s == ASTRO_SEC_PATH) return "PATH QUALITY";
   if(s == ASTRO_SEC_MICRO) return "MICRO M1";
   if(s == ASTRO_SEC_REGIME) return "REGIME ENGINE";
   if(s == ASTRO_SEC_MACRO) return "MACRO BACKGROUND";
   return "RAW AXES";
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
   names[0] = "MarsImpulse";    vals[0] = f.mars_impulse;
   names[1] = "MarsCleanImp";   vals[1] = f.mars_clean_impulse;
   names[2] = "MarsSatFrict";   vals[2] = f.mars_saturn_friction;
   names[3] = "MarsJupExp";     vals[3] = f.mars_jupiter_expansion;
   names[4] = "MercuryNoise";   vals[4] = f.mercury_noise;
   names[5] = "VenusMarsCoh";   vals[5] = f.venus_mars_cohesion;
   names[6] = "JupiterSupport"; vals[6] = f.jupiter_support;
   names[7] = "SaturnResist";   vals[7] = f.saturn_resistance;
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

void DAL_GetSectionData(const DAL_AstroSection s, const DAL_AstroFractalMetrics &f, string &names[], double &vals[], int &count)
{
   if(s == ASTRO_SEC_PATH) { DAL_FillPath(f, names, vals, count); return; }
   if(s == ASTRO_SEC_MICRO) { DAL_FillMicro(f, names, vals, count); return; }
   if(s == ASTRO_SEC_REGIME) { DAL_FillRegime(f, names, vals, count); return; }
   if(s == ASTRO_SEC_MACRO) { DAL_FillMacro(f, names, vals, count); return; }
   DAL_FillRaw(f, names, vals, count);
}

void DAL_GetLayout(DAL_Layout &L)
{
   L.chart_w = (int)ChartGetInteger(ChartID(), CHART_WIDTH_IN_PIXELS, 0);
   L.chart_h = (int)ChartGetInteger(ChartID(), CHART_HEIGHT_IN_PIXELS, 0);
   L.x = InpBaseX;
   L.y = InpBaseY;
   L.header_w = MathMax(980, L.chart_w - 30);
   L.header_h = (g_minimized ? 72 : InpHeaderHeight);
   L.diag_w = MathMax(500, L.header_w / 3);
   L.left_w = L.header_w - L.diag_w - InpGap;
   L.card_w = MathMax(430, (L.left_w - InpGap) / 2);
   L.card_h = InpCardTitleHeight + 16 + 8 * InpCardRowHeight + 14;
   L.col1_x = L.x;
   L.col2_x = L.x + L.card_w + InpGap;
   L.diag_x = L.x + L.left_w + InpGap;
   L.row1_y = L.y + L.header_h + 12;
   L.row2_y = L.row1_y + L.card_h + InpGap;
   L.osc_x = L.x;
   L.osc_y = L.row2_y + L.card_h + 16;
   L.osc_w = MathMin(920, L.left_w);
   L.focus_w = L.left_w;
}

void DAL_DrawHeader(const DAL_Layout &L, const bool have_row, const bool exact_match, const bool fallback_match, const DAL_AstroFractalMetrics &f)
{
   DAL_Rect(g_prefix + "_HDR_BG", L.x, L.y, L.header_w, L.header_h, InpColorPanel, InpColorBorder);

   string view_name = (g_view_mode == ASTRO_VIEW_COCKPIT ? "Cockpit" : DAL_SectionTitle(g_focus_section));
   string row_status = !g_loaded ? "CSV NOT LOADED" : (!have_row ? "ROW NOT FOUND" : (exact_match ? "EXACT ROW" : "FALLBACK ROW"));
   color row_clr = !g_loaded ? InpColorLow : (!have_row ? InpColorLow : (exact_match ? InpColorHigh : InpColorMid));

   DAL_Label(g_prefix + "_HDR0", "EXP0013 ASTRO COCKPIT", L.x + 16, L.y + 8, InpColorInfo, InpFontHero);
   DAL_Label(g_prefix + "_HDR0B", "Research dashboard", L.x + 16, L.y + 25, InpColorMuted, InpFontSmall);
   DAL_LineH(g_prefix + "_HDR_RULE", L.x + 14, L.y + 38, L.header_w - 28, InpColorBorder);

   int meta_y1 = L.y + 46;
   int meta_y2 = L.y + 66;
   DAL_Label(g_prefix + "_HDR1K1", "Symbol", L.x + 16, meta_y1, InpColorMuted, InpFontBody);
   DAL_Label(g_prefix + "_HDR1V1", _Symbol, L.x + 78, meta_y1, InpColorText, InpFontBody);
   DAL_Label(g_prefix + "_HDR1K2", "TF", L.x + 170, meta_y1, InpColorMuted, InpFontBody);
   DAL_Label(g_prefix + "_HDR1V2", EnumToString(_Period), L.x + 206, meta_y1, InpColorText, InpFontBody);
   DAL_Label(g_prefix + "_HDR1K3", "View", L.x + 280, meta_y1, InpColorMuted, InpFontBody);
   DAL_Label(g_prefix + "_HDR1V3", view_name, L.x + 326, meta_y1, InpColorText, InpFontBody);

   DAL_Label(g_prefix + "_HDR2K1", "Status", L.x + 16, meta_y2, InpColorMuted, InpFontBody);
   DAL_Label(g_prefix + "_HDR2V1", row_status, L.x + 78, meta_y2, row_clr, InpFontBody);
   DAL_Label(g_prefix + "_HDR2K2", "File", L.x + 280, meta_y2, InpColorMuted, InpFontBody);
   DAL_Label(g_prefix + "_HDR2V2", DAL_Shorten(InpAstroCsvFile, 30), L.x + 318, meta_y2, InpColorMid, InpFontBody);

   if(!g_minimized)
   {
      DAL_Label(g_prefix + "_HDR3K1", "Broker", L.x + 520, meta_y2, InpColorMuted, InpFontBody);
      DAL_Label(g_prefix + "_HDR3V1", have_row ? DAL_TimeText(f.broker_time) : DAL_TimeText(iTime(_Symbol, _Period, 0)), L.x + 580, meta_y2, InpColorText, InpFontBody);
      DAL_Label(g_prefix + "_HDR3K2", "UTC", L.x + 750, meta_y2, InpColorMuted, InpFontBody);
      DAL_Label(g_prefix + "_HDR3V2", have_row ? DAL_TimeText(f.utc_time) : "n/a", L.x + 790, meta_y2, InpColorText, InpFontBody);
   }

   int nav_gap = 8;
   int util_w = 124;
   int util_gap = 10;
   int bx = L.x + L.header_w - 6 * (InpButtonW + nav_gap) - 18;
   int by = L.y + 8;
   DAL_Button(g_prefix + "_BTN_COCKPIT", "COCKPIT", bx, by, InpButtonW, InpButtonH, g_view_mode == ASTRO_VIEW_COCKPIT); bx += InpButtonW + nav_gap;
   DAL_Button(g_prefix + "_BTN_PATH", "PATH", bx, by, InpButtonW, InpButtonH, g_view_mode == ASTRO_VIEW_FOCUS && g_focus_section == ASTRO_SEC_PATH); bx += InpButtonW + nav_gap;
   DAL_Button(g_prefix + "_BTN_MICRO", "MICRO", bx, by, InpButtonW, InpButtonH, g_view_mode == ASTRO_VIEW_FOCUS && g_focus_section == ASTRO_SEC_MICRO); bx += InpButtonW + nav_gap;
   DAL_Button(g_prefix + "_BTN_REGIME", "REGIME", bx, by, InpButtonW, InpButtonH, g_view_mode == ASTRO_VIEW_FOCUS && g_focus_section == ASTRO_SEC_REGIME); bx += InpButtonW + nav_gap;
   DAL_Button(g_prefix + "_BTN_MACRO", "MACRO", bx, by, InpButtonW, InpButtonH, g_view_mode == ASTRO_VIEW_FOCUS && g_focus_section == ASTRO_SEC_MACRO); bx += InpButtonW + nav_gap;
   DAL_Button(g_prefix + "_BTN_RAW", "RAW", bx, by, InpButtonW, InpButtonH, g_view_mode == ASTRO_VIEW_FOCUS && g_focus_section == ASTRO_SEC_RAW);

   bx = L.x + L.header_w - 4 * (util_w + util_gap) - 18;
   by = L.y + 44;
   DAL_Button(g_prefix + "_BTN_TEX", g_show_text ? "TEXT ON" : "TEXT OFF", bx, by, util_w, InpButtonH, g_show_text); bx += util_w + util_gap;
   DAL_Button(g_prefix + "_BTN_OSC", g_show_osc ? "OSC ON" : "OSC OFF", bx, by, util_w, InpButtonH, g_show_osc); bx += util_w + util_gap;
   DAL_Button(g_prefix + "_BTN_MIN", g_minimized ? "EXPAND" : "MINIMIZE", bx, by, util_w, InpButtonH, g_minimized); bx += util_w + util_gap;
   DAL_Button(g_prefix + "_BTN_RELD", "RELOAD", bx, by, util_w, InpButtonH, false);
}

void DAL_DrawMetricCard(const string key, const string title, const int x, const int y, const int w, const string &names[], const double &vals[], const int count)
{
   int h = InpCardTitleHeight + 18 + count * InpCardRowHeight + 16;
   DAL_Rect(g_prefix + "_CARD_BG_" + key, x, y, w, h, InpColorCard, InpColorBorder);
   DAL_Label(g_prefix + "_CARD_T_" + key, title, x + 16, y + 8, InpColorInfo, InpFontTitle);
   DAL_LineH(g_prefix + "_CARD_RULE_" + key, x + 14, y + InpCardTitleHeight + 2, w - 28, InpColorBorder);

   int label_x = x + 16;
   int label_w = DAL_LabelWidthPx(DAL_MaxLabelLen(names, count)) + 26;
   int val_x   = label_x + label_w + 12;
   int bucket_x= val_x + 60;
   int bar_w   = 92;
   int bar_x   = x + w - bar_w - 18;
   if(bucket_x > bar_x - 62) bucket_x = bar_x - 62;
   for(int i = 0; i < count; i++)
   {
      int ry = y + InpCardTitleHeight + 16 + i * InpCardRowHeight;
      color clr = DAL_HeatColor(vals[i]);
      DAL_Label(g_prefix + "_CARD_L_" + key + "_" + IntegerToString(i), names[i], label_x, ry, InpColorText, InpFontBody);
      DAL_Label(g_prefix + "_CARD_V_" + key + "_" + IntegerToString(i), DoubleToString(vals[i], 1), val_x, ry, clr, InpFontBody);
      DAL_Label(g_prefix + "_CARD_B_" + key + "_" + IntegerToString(i), DAL_Bucket(vals[i]), bucket_x, ry, InpColorMuted, InpFontBody);
      DAL_Rect(g_prefix + "_CARD_BG2_" + key + "_" + IntegerToString(i), bar_x, ry + 5, bar_w, 10, C'22,22,22', InpColorBorder);
      DAL_Rect(g_prefix + "_CARD_F_" + key + "_" + IntegerToString(i), bar_x, ry + 5, (int)MathRound(MathMax(0.0, MathMin(100.0, vals[i])) / 100.0 * bar_w), 10, clr, clr);
   }
}

void DAL_DrawDiagnosticsCard(const DAL_Layout &L, const bool have_row, const bool exact_match, const bool fallback_match, const DAL_AstroFractalMetrics &f)
{
   int x = L.diag_x;
   int y = L.row1_y;
   int w = L.diag_w;
   int h = 2 * L.card_h + InpGap;
   DAL_Rect(g_prefix + "_DIAG_BG", x, y, w, h, InpColorCard, InpColorBorder);
   DAL_Label(g_prefix + "_DIAG_T", "DIAGNOSTICS", x + 16, y + 8, InpColorInfo, InpFontTitle);
   DAL_LineH(g_prefix + "_DIAG_RULE", x + 14, y + InpCardTitleHeight + 2, w - 28, InpColorBorder);

   int label_x = x + 16;
   int val_x = x + 120;
   int step = 28;
   int ry = y + InpCardTitleHeight + 18;
   DAL_Label(g_prefix + "_DIAG_0", "CSV", label_x, ry, InpColorText, InpFontBody);
   DAL_Label(g_prefix + "_DIAGV_0", g_loaded ? "LOADED" : "NOT LOADED", val_x, ry, g_loaded ? InpColorHigh : InpColorLow, InpFontBody); ry += step;
   DAL_Label(g_prefix + "_DIAG_1", "Rows", label_x, ry, InpColorText, InpFontBody);
   DAL_Label(g_prefix + "_DIAGV_1", IntegerToString(g_store.row_count), val_x, ry, InpColorMuted, InpFontBody); ry += step;
   DAL_Label(g_prefix + "_DIAG_2", "Source", label_x, ry, InpColorText, InpFontBody);
   DAL_Label(g_prefix + "_DIAGV_2", DAL_Shorten(g_store.source_file, 30), val_x, ry, InpColorMuted, InpFontBody); ry += step;
   DAL_Label(g_prefix + "_DIAG_3", "Lookup", label_x, ry, InpColorText, InpFontBody);
   string lk = have_row ? (exact_match ? "exact" : (fallback_match ? "fallback" : "unknown")) : "row_not_found";
   DAL_Label(g_prefix + "_DIAGV_3", lk, val_x, ry, exact_match ? InpColorHigh : (fallback_match ? InpColorMid : InpColorLow), InpFontBody); ry += step;
   DAL_Label(g_prefix + "_DIAG_4", "Chart", label_x, ry, InpColorText, InpFontBody);
   DAL_Label(g_prefix + "_DIAGV_4", DAL_TimeText(iTime(_Symbol, _Period, 0)), val_x, ry, InpColorText, InpFontBody); ry += step;
   DAL_Label(g_prefix + "_DIAG_5", "Matched", label_x, ry, InpColorText, InpFontBody);
   DAL_Label(g_prefix + "_DIAGV_5", have_row ? DAL_TimeText(f.broker_time) : "n/a", val_x, ry, InpColorMuted, InpFontBody); ry += step;
   DAL_Label(g_prefix + "_DIAG_6", "Hint", label_x, ry, InpColorText, InpFontBody);
   DAL_Label(g_prefix + "_DIAGV_6", have_row ? "dashboard ok" : "extend live window / check GMT", val_x, ry, have_row ? InpColorHigh : InpColorMid, InpFontBody);
}

void DAL_DrawCompactOsc(const DAL_Layout &L, const DAL_AstroSection sec)
{
   if(!g_show_osc) return;

   bool ex0, fb0;
   DAL_AstroFractalMetrics f0;
   if(!DAL_FindFractalByShift(0, f0, ex0, fb0)) return;

   string names[8]; double vals[8]; int count;
   DAL_GetSectionData(sec, f0, names, vals, count);

   int x = L.osc_x;
   int y = L.osc_y;
   int w = L.osc_w;
   int title_h = 26;
   int row_h = 23;
   int h = title_h + count * row_h + 16;
   DAL_Rect(g_prefix + "_OSC_BG", x, y, w, h, InpColorPanel, InpColorBorder);
   DAL_Label(g_prefix + "_OSC_T", "COMPACT OSCILLATOR  ·  " + DAL_SectionTitle(sec), x + 16, y + 7, InpColorInfo, InpFontTitle);
   DAL_LineH(g_prefix + "_OSC_RULE", x + 14, y + title_h - 2, w - 28, InpColorBorder);

   int label_x = x + 16;
   int label_w = DAL_LabelWidthPx(DAL_MaxLabelLen(names, count)) + 24;
   int val_x   = label_x + label_w + 12;
   int bucket_x = val_x + 56;
   int bar_x   = bucket_x + 64;
   int bar_w   = 120;

   for(int r = 0; r < count; r++)
   {
      int ry = y + title_h + 2 + r * row_h;
      color clr = DAL_HeatColor(vals[r]);
      DAL_Label(g_prefix + "_OSC_L_" + IntegerToString(r), names[r], label_x, ry + 2, InpColorText, InpFontBody);
      DAL_Label(g_prefix + "_OSC_V_" + IntegerToString(r), DoubleToString(vals[r], 1), val_x, ry + 2, clr, InpFontBody);
      DAL_Label(g_prefix + "_OSC_B_" + IntegerToString(r), DAL_Bucket(vals[r]), bucket_x, ry + 2, InpColorMuted, InpFontBody);
      DAL_Rect(g_prefix + "_OSC_BARBG_" + IntegerToString(r), bar_x, ry + 6, bar_w, 10, C'22,22,22', InpColorBorder);
      DAL_Rect(g_prefix + "_OSC_BAR_" + IntegerToString(r), bar_x, ry + 6, (int)MathRound(MathMax(0.0, MathMin(100.0, vals[r])) / 100.0 * bar_w), 10, clr, clr);
   }
}

void DAL_DrawCockpit(const DAL_Layout &L, const DAL_AstroFractalMetrics &f, const bool have_row, const bool exact_match, const bool fallback_match)
{
   string names[8]; double vals[8]; int count;
   DAL_GetSectionData(ASTRO_SEC_PATH, f, names, vals, count);
   DAL_DrawMetricCard("PATH", "PATH QUALITY", L.col1_x, L.row1_y, L.card_w, names, vals, count);
   DAL_GetSectionData(ASTRO_SEC_MICRO, f, names, vals, count);
   DAL_DrawMetricCard("MICRO", "MICRO M1", L.col2_x, L.row1_y, L.card_w, names, vals, count);
   DAL_GetSectionData(ASTRO_SEC_MACRO, f, names, vals, count);
   DAL_DrawMetricCard("MACRO", "MACRO BACKGROUND", L.col1_x, L.row2_y, L.card_w, names, vals, count);
   DAL_GetSectionData(ASTRO_SEC_RAW, f, names, vals, count);
   DAL_DrawMetricCard("RAW", "RAW AXES", L.col2_x, L.row2_y, L.card_w, names, vals, count);
   DAL_DrawDiagnosticsCard(L, have_row, exact_match, fallback_match, f);
}

void DAL_DrawFocus(const DAL_Layout &L, const DAL_AstroFractalMetrics &f, const bool have_row, const bool exact_match, const bool fallback_match)
{
   string names[8]; double vals[8]; int count;
   DAL_GetSectionData(g_focus_section, f, names, vals, count);
   DAL_DrawMetricCard("FOCUS", DAL_SectionTitle(g_focus_section), L.col1_x, L.row1_y, L.focus_w, names, vals, count);
   DAL_DrawDiagnosticsCard(L, have_row, exact_match, fallback_match, f);
}

DAL_AstroSection DAL_CurrentOscSection()
{
   if(g_view_mode == ASTRO_VIEW_FOCUS) return g_focus_section;
   return ASTRO_SEC_PATH;
}

void DAL_Render()
{
   if(DAL_ShouldReload()) DAL_LoadStore();

   bool have_row = false, exact_match = false, fallback_match = false;
   DAL_AstroFractalMetrics f;
   DAL_AstroFM_Reset(f);
   if(g_loaded) have_row = DAL_FindFractalByShift(0, f, exact_match, fallback_match);

   if(g_force_rebuild)
   {
      DAL_CleanupAllAstroObjects();
      g_force_rebuild = false;
   }

   DAL_Layout L; DAL_GetLayout(L);
   DAL_DrawHeader(L, have_row, exact_match, fallback_match, f);

   if(g_minimized)
   {
      if(InpUseTerminalComment)
      {
         string status = !g_loaded ? "CSV NOT LOADED" : (!have_row ? "ROW NOT FOUND" : (exact_match ? "EXACT" : "FALLBACK"));
         Comment("EXP0013 Astro Dashboard | ", status, " | ", (have_row ? f.thesis : "no row"));
      }
      ChartRedraw(ChartID());
      return;
   }

   if(g_show_text)
   {
      if(have_row)
      {
         if(g_view_mode == ASTRO_VIEW_COCKPIT) DAL_DrawCockpit(L, f, have_row, exact_match, fallback_match);
         else DAL_DrawFocus(L, f, have_row, exact_match, fallback_match);
      }
      else DAL_DrawDiagnosticsCard(L, have_row, exact_match, fallback_match, f);
   }

   if(have_row) DAL_DrawCompactOsc(L, DAL_CurrentOscSection());

   if(InpUseTerminalComment)
   {
      string status = !g_loaded ? "CSV NOT LOADED" : (!have_row ? "ROW NOT FOUND" : (exact_match ? "EXACT" : "FALLBACK"));
      Comment("EXP0013 Astro Dashboard | ", status, " | ", (have_row ? f.thesis : "no row"));
   }
   ChartRedraw(ChartID());
}

int OnInit()
{
   g_prefix = "DAL_EXP0013_ASTRO_V13_" + IntegerToString((int)ChartID());
   g_view_mode = InpInitialViewMode;
   g_focus_section = InpInitialFocusSection;
   g_show_text = InpShowTextPanel;
   g_show_osc = InpShowOscillator;
   g_minimized = false;
   DAL_CleanupAllAstroObjects();
   g_force_rebuild = false;
   EventSetTimer(MathMax(1, InpRefreshSeconds));
   DAL_LoadStore();
   DAL_Render();
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   DAL_CleanupAllAstroObjects();
   if(InpUseTerminalComment) Comment("");
}

void OnTick() {}
void OnTimer() { DAL_Render(); }

void OnChartEvent(const int id, const long &lparam, const double &dparam, const string &sparam)
{
   if(id == CHARTEVENT_CHART_CHANGE)
   {
      // Rebuild only when layout dimensions may have changed.
      g_force_rebuild = true;
      DAL_Render();
      return;
   }

   if(id != CHARTEVENT_OBJECT_CLICK) return;

   bool layout_changed = false;
   if(sparam == g_prefix + "_BTN_COCKPIT") { g_view_mode = ASTRO_VIEW_COCKPIT; layout_changed = true; }
   else if(sparam == g_prefix + "_BTN_PATH") { g_view_mode = ASTRO_VIEW_FOCUS; g_focus_section = ASTRO_SEC_PATH; layout_changed = true; }
   else if(sparam == g_prefix + "_BTN_MICRO") { g_view_mode = ASTRO_VIEW_FOCUS; g_focus_section = ASTRO_SEC_MICRO; layout_changed = true; }
   else if(sparam == g_prefix + "_BTN_REGIME") { g_view_mode = ASTRO_VIEW_FOCUS; g_focus_section = ASTRO_SEC_REGIME; layout_changed = true; }
   else if(sparam == g_prefix + "_BTN_MACRO") { g_view_mode = ASTRO_VIEW_FOCUS; g_focus_section = ASTRO_SEC_MACRO; layout_changed = true; }
   else if(sparam == g_prefix + "_BTN_RAW") { g_view_mode = ASTRO_VIEW_FOCUS; g_focus_section = ASTRO_SEC_RAW; layout_changed = true; }
   else if(sparam == g_prefix + "_BTN_TEX") { g_show_text = !g_show_text; layout_changed = true; }
   else if(sparam == g_prefix + "_BTN_OSC") { g_show_osc = !g_show_osc; layout_changed = true; }
   else if(sparam == g_prefix + "_BTN_MIN") { g_minimized = !g_minimized; layout_changed = true; }
   else if(sparam == g_prefix + "_BTN_RELD") { DAL_LoadStore(); }

   if(layout_changed)
      g_force_rebuild = true;

   DAL_Render();
}
