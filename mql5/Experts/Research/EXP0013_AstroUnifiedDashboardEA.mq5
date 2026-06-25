#property strict
#property description "Decision Alpha Lab - EXP0013 Raw Sky Cockpit EA"
#property description "Research-only raw sky dashboard. No trade, no iCustom, no interpretive market scores."
#property tester_file "astro_GMT3_M1_2026_to_now_mql.csv"
#property tester_file "astro\\astro_GMT3_M1_2026_to_now_mql.csv"
#property tester_file "astro_live_mql.csv"

#include <Research/DAL_AstroMapTypes.mqh>
#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroPureAstrologySignals.mqh>

enum DAL_AstroRawView
{
   ASTRO_RAW_OVERVIEW = 0,
   ASTRO_RAW_BODIES   = 1,
   ASTRO_RAW_ASPECTS  = 2,
   ASTRO_RAW_HOUSES   = 3,
   ASTRO_RAW_METRICS  = 4,
   ASTRO_RAW_NATAL    = 5,
   ASTRO_RAW_SIGNAL   = 6,
   ASTRO_RAW_TIMING   = 7
};

input string           InpAstroCsvFile          = "astro_live_mql.csv";
input double           InpBrokerGmtOffsetHours  = 0.0;
input bool             InpRequireExactBarTime   = true;
input int              InpReloadCsvEverySeconds = 10;
input int              InpRefreshSeconds        = 1;
input DAL_AstroRawView InpInitialView           = ASTRO_RAW_OVERVIEW;
input bool             InpUseTerminalComment    = false;
input string           InpBirthDate             = "";
input int              InpBirthHour             = 0;
input int              InpBirthMinute           = 0;
input double           InpBirthUtcOffsetHours   = 0.0;
input double           InpBirthLat              = 0.0;
input double           InpBirthLon              = 0.0;
input string           InpBirthLabel            = "";

input int              InpBaseX                 = 10;
input int              InpBaseY                 = 10;
input int              InpHeaderHeight          = 92;
input int              InpGap                   = 16;
input int              InpButtonW               = 96;
input int              InpButtonH               = 28;
input int              InpFontHero              = 13;
input int              InpFontTitle             = 12;
input int              InpFontBody              = 9;
input int              InpFontSmall             = 8;
input int              InpRowHeight             = 20;

input color            InpColorPanel            = C'11,14,18';
input color            InpColorCard             = C'18,22,28';
input color            InpColorBorder           = C'64,74,86';
input color            InpColorText             = clrWhite;
input color            InpColorMuted            = C'168,178,188';
input color            InpColorInfo             = C'86,208,255';
input color            InpColorLow              = C'255,111,97';
input color            InpColorMid              = C'255,199,87';
input color            InpColorHigh             = C'107,224,142';
input color            InpColorButtonOn         = C'31,91,63';
input color            InpColorButtonOff        = C'28,34,42';

DAL_AstroMapStore g_store;
bool              g_loaded = false;
datetime          g_last_load_time = 0;
string            g_prefix = "DAL_EXP0013_RAW_SKY_V14";
DAL_AstroRawView  g_view;
bool              g_minimized = false;
bool              g_force_rebuild = true;
int               g_last_w = 0;
int               g_last_h = 0;

struct DAL_UIGrid
{
   int chart_w;
   int chart_h;
   int x;
   int y;
   int header_w;
   int header_h;
   int main_x;
   int main_y;
   int main_w;
   int side_x;
   int side_y;
   int side_w;
   int panel_h;

   // Derived layout fields used by tab renderers.
   // These were accidentally left out of the V14 struct even though DAL_GetGrid()
   // and the panel drawing functions populate/read them.
   int card_w;
   int diag_w;
   int col1_x;
   int col2_x;
   int col3_x;
   int row1_y;
   int row2_y;
   int row3_y;
};

void DAL_DelPrefix(const string prefix)
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

void DAL_CleanupAll()
{
   DAL_DelPrefix("DAL_EXP0013_ASTRO");
   DAL_DelPrefix("DAL_EXP0013_RAW_ASTRO");
   DAL_DelPrefix("DAL_EXP0013_RAW_SKY");
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

void DAL_Line(const string name, const int x, const int y, const int w, const color clr)
{
   DAL_Rect(name, x, y, w, 1, clr, clr);
}

void DAL_Label(const string name, const string text, const int x, const int y, const color clr, const int font_size, const string font="Consolas")
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
   ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(chart_id, name, OBJPROP_HIDDEN, true);
}

string DAL_TimeText(const datetime t)
{
   if(t <= 0) return "n/a";
   return TimeToString(t, TIME_DATE | TIME_MINUTES);
}

string DAL_Short(const string s, const int max_len)
{
   int n = StringLen(s);
   if(n <= max_len || max_len <= 8) return s;
   int keep = (max_len - 3) / 2;
   return StringSubstr(s, 0, keep) + "..." + StringSubstr(s, n - keep);
}

string DAL_SignShort(const string sign)
{
   if(sign == "aries") return "Ari";
   if(sign == "taurus") return "Tau";
   if(sign == "gemini") return "Gem";
   if(sign == "cancer") return "Can";
   if(sign == "leo") return "Leo";
   if(sign == "virgo") return "Vir";
   if(sign == "libra") return "Lib";
   if(sign == "scorpio") return "Sco";
   if(sign == "sagittarius") return "Sag";
   if(sign == "capricorn") return "Cap";
   if(sign == "aquarius") return "Aqu";
   if(sign == "pisces") return "Pis";
   return "---";
}

string DAL_PosText(const DAL_AstroBodyState &b)
{
   return StringFormat("%05.2f %s", b.degree, DAL_SignShort(b.sign));
}

string DAL_LonSignText(const double lon)
{
   int si = (int)MathFloor(lon / 30.0) % 12;
   double deg = lon - si * 30.0;
   string signs[12] = {"Ari","Tau","Gem","Can","Leo","Vir","Lib","Sco","Sag","Cap","Aqu","Pis"};
   if(si < 0 || si > 11) return "n/a";
   return StringFormat("%05.2f %s", deg, signs[si]);
}

string DAL_RetroText(const DAL_AstroBodyState &b)
{
   return (b.retro == 1 ? "R" : "D");
}

string DAL_HouseText(const DAL_AstroBodyState &b)
{
   return (b.house >= 1 && b.house <= 12 ? IntegerToString(b.house) : "-");
}

string DAL_TransitNatalHouseText(const DAL_AstroMapRow &row, const int idx)
{
   if(idx < 0 || idx >= DAL_ASTRO_NATAL_CORE_COUNT)
      return "-";
   int h = row.transit_in_natal_house[idx];
   return (h >= 1 && h <= 12 ? IntegerToString(h) : "-");
}

string DAL_BodyDisplay(const string name)
{
   if(name == "true_node") return "true_node";
   if(name == "mean_node") return "mean_node";
   return name;
}

string DAL_Dignity(const DAL_AstroBodyState &b)
{
   int s = b.sign_index;
   string n = b.name;
   if(n == "sun")
   {
      if(s == 4) return "domicile";
      if(s == 0) return "exalt";
      if(s == 10) return "detriment";
      if(s == 6) return "fall";
      return "peregrine";
   }
   if(n == "moon")
   {
      if(s == 3) return "domicile";
      if(s == 1) return "exalt";
      if(s == 9) return "detriment";
      if(s == 7) return "fall";
      return "peregrine";
   }
   if(n == "mercury")
   {
      if(s == 2 || s == 5) return "domicile";
      if(s == 5) return "exalt";
      if(s == 8 || s == 11) return "detriment";
      if(s == 11) return "fall";
      return "peregrine";
   }
   if(n == "venus")
   {
      if(s == 1 || s == 6) return "domicile";
      if(s == 11) return "exalt";
      if(s == 7 || s == 0) return "detriment";
      if(s == 5) return "fall";
      return "peregrine";
   }
   if(n == "mars")
   {
      if(s == 0 || s == 7) return "domicile";
      if(s == 9) return "exalt";
      if(s == 6 || s == 1) return "detriment";
      if(s == 3) return "fall";
      return "peregrine";
   }
   if(n == "jupiter")
   {
      if(s == 8 || s == 11) return "domicile";
      if(s == 3) return "exalt";
      if(s == 2 || s == 5) return "detriment";
      if(s == 9) return "fall";
      return "peregrine";
   }
   if(n == "saturn")
   {
      if(s == 9 || s == 10) return "domicile";
      if(s == 6) return "exalt";
      if(s == 3 || s == 4) return "detriment";
      if(s == 0) return "fall";
      return "peregrine";
   }
   return "n/a";
}

color DAL_DignityColor(const string d)
{
   if(d == "domicile" || d == "exalt") return InpColorHigh;
   if(d == "detriment" || d == "fall") return InpColorLow;
   if(d == "peregrine") return InpColorMid;
   return InpColorMuted;
}

color DAL_OrbColor(const double orb)
{
   if(orb <= 1.0) return InpColorHigh;
   if(orb <= 3.0) return InpColorMid;
   return InpColorMuted;
}

color DAL_ScoreColor(const double value)
{
   if(value >= 67.0) return InpColorHigh;
   if(value >= 45.0) return InpColorMid;
   return InpColorLow;
}

void DAL_Pill(const string name, const string text, const int x, const int y, const int w, const color bg, const color fg)
{
   DAL_Rect(name, x, y, w, 18, bg, bg);
   DAL_Label(name + "_TXT", text, x + 6, y + 2, fg, InpFontSmall);
}

string DAL_BirthInputText()
{
   if(InpBirthDate == "")
      return "not_set";
   return InpBirthDate + " " + IntegerToString(InpBirthHour) + ":" + IntegerToString(InpBirthMinute);
}

bool DAL_LoadStore()
{
   g_last_load_time = TimeCurrent();
   g_loaded = DAL_AstroMapStore_LoadExcelCsv(g_store, InpAstroCsvFile, InpBrokerGmtOffsetHours, PeriodSeconds(_Period) / 60);
   Print("EXP0013 Raw Sky | CSV loaded=", g_loaded, " rows=", g_store.row_count, " source=", g_store.source_file);
   return g_loaded;
}

bool DAL_ShouldReload()
{
   if(InpReloadCsvEverySeconds <= 0) return false;
   if(g_last_load_time <= 0) return true;
   return (TimeCurrent() - g_last_load_time) >= InpReloadCsvEverySeconds;
}

bool DAL_FindRow(DAL_AstroMapRow &row, bool &exact, bool &fallback)
{
   exact = false;
   fallback = false;
   DAL_AstroMapRow_Reset(row);
   if(!g_loaded) return false;
   datetime t = iTime(_Symbol, _Period, 0);
   if(DAL_AstroMapStore_FindForCandleOpen(g_store, t, row, true))
   {
      exact = true;
      return true;
   }
   if(DAL_AstroMapStore_FindForCandleOpen(g_store, t, row, false))
   {
      fallback = true;
      return true;
   }
   return false;
}

void DAL_GetGrid(DAL_UIGrid &g)
{
   g.chart_w = (int)ChartGetInteger(ChartID(), CHART_WIDTH_IN_PIXELS, 0);
   g.chart_h = (int)ChartGetInteger(ChartID(), CHART_HEIGHT_IN_PIXELS, 0);
   g.x = InpBaseX;
   g.y = InpBaseY;
   g.header_w = MathMax(1040, g.chart_w - 30);
   g.header_h = (g_minimized ? 72 : InpHeaderHeight);
   g.side_w = MathMax(420, g.header_w / 3);
   g.main_w = g.header_w - g.side_w - InpGap;
   g.card_w = MathMax(420, (g.main_w - InpGap) / 2);
   g.diag_w = g.side_w;
   g.main_x = g.x;
   g.main_y = g.y + g.header_h + 12;
   g.side_x = g.x + g.main_w + InpGap;
   g.side_y = g.main_y;
   g.col1_x = g.x;
   g.col2_x = g.x + g.card_w + InpGap;
   g.col3_x = g.side_x;
   g.row1_y = g.main_y;
   g.row2_y = g.row1_y + 248 + InpGap;
   g.row3_y = g.row2_y + 248 + InpGap;
   g.panel_h = MathMax(520, g.chart_h - g.main_y - 80);
}

void DAL_DrawHeader(const DAL_UIGrid &g, const bool have_row, const bool exact, const bool fallback, const DAL_AstroMapRow &row)
{
   DAL_Rect(g_prefix + "_HDR_BG", g.x, g.y, g.header_w, g.header_h, InpColorPanel, InpColorBorder);
   DAL_Label(g_prefix + "_HDR_TITLE", "EXP0013 ASTRO TIMING COCKPIT", g.x + 16, g.y + 8, InpColorInfo, InpFontHero);
   DAL_Label(g_prefix + "_HDR_SUB", "Macro field, meso gates, micro triggers, minute windows, natal activations, and pure astro execution language", g.x + 16, g.y + 28, InpColorMuted, InpFontSmall);
   DAL_Line(g_prefix + "_HDR_RULE", g.x + 14, g.y + 43, g.header_w - 28, InpColorBorder);

   string row_status = !g_loaded ? "CSV NOT LOADED" : (!have_row ? "ROW NOT FOUND" : (exact ? "EXACT ROW" : "FALLBACK ROW"));
   color st_col = !g_loaded ? InpColorLow : (!have_row ? InpColorLow : (exact ? InpColorHigh : InpColorMid));
   int y2 = g.y + 52;
   DAL_Label(g_prefix + "_HDR_S1", "Symbol", g.x + 16, y2, InpColorMuted, InpFontBody);
   DAL_Label(g_prefix + "_HDR_S1V", _Symbol, g.x + 78, y2, InpColorText, InpFontBody);
   DAL_Label(g_prefix + "_HDR_S2", "TF", g.x + 160, y2, InpColorMuted, InpFontBody);
   DAL_Label(g_prefix + "_HDR_S2V", EnumToString(_Period), g.x + 192, y2, InpColorText, InpFontBody);
   DAL_Label(g_prefix + "_HDR_S3", "Status", g.x + 280, y2, InpColorMuted, InpFontBody);
   DAL_Label(g_prefix + "_HDR_S3V", row_status, g.x + 342, y2, st_col, InpFontBody);
   DAL_Label(g_prefix + "_HDR_S4", "File", g.x + 500, y2, InpColorMuted, InpFontBody);
   DAL_Label(g_prefix + "_HDR_S4V", DAL_Short(InpAstroCsvFile, 28), g.x + 540, y2, InpColorMid, InpFontBody);
   DAL_Label(g_prefix + "_HDR_S5", "Natal", g.x + 800, y2, InpColorMuted, InpFontBody);
   DAL_Label(g_prefix + "_HDR_S5V", have_row && row.natal_enabled ? DAL_Short(row.natal_label, 20) : DAL_Short(InpBirthLabel, 20), g.x + 848, y2, have_row && row.natal_enabled ? InpColorHigh : InpColorMid, InpFontBody);

   if(!g_minimized)
   {
      string tline = have_row ? ("Broker " + DAL_TimeText(row.broker_time) + "  |  UTC " + DAL_TimeText(row.utc_time) + "  |  JD " + DoubleToString(row.jd_ut, 5))
                              : ("Chart candle " + DAL_TimeText(iTime(_Symbol, _Period, 0)));
      DAL_Label(g_prefix + "_HDR_TIME", tline, g.x + 16, g.y + 74, InpColorMuted, InpFontBody);
   }

   int btn_w = 82;
   int bx = g.x + g.header_w - 8 * (btn_w + 8) - 18;
   int by = g.y + 10;
   DAL_Button(g_prefix + "_BTN_OVR", "OVERVIEW", bx, by, btn_w, InpButtonH, g_view == ASTRO_RAW_OVERVIEW); bx += btn_w + 8;
   DAL_Button(g_prefix + "_BTN_BODY", "BODIES", bx, by, btn_w, InpButtonH, g_view == ASTRO_RAW_BODIES); bx += btn_w + 8;
   DAL_Button(g_prefix + "_BTN_ASP", "ASPECTS", bx, by, btn_w, InpButtonH, g_view == ASTRO_RAW_ASPECTS); bx += btn_w + 8;
   DAL_Button(g_prefix + "_BTN_HOU", "HOUSES", bx, by, btn_w, InpButtonH, g_view == ASTRO_RAW_HOUSES); bx += btn_w + 8;
   DAL_Button(g_prefix + "_BTN_MET", "METRICS", bx, by, btn_w, InpButtonH, g_view == ASTRO_RAW_METRICS); bx += btn_w + 8;
   DAL_Button(g_prefix + "_BTN_NAT", "NATAL", bx, by, btn_w, InpButtonH, g_view == ASTRO_RAW_NATAL); bx += btn_w + 8;
   DAL_Button(g_prefix + "_BTN_SIG", "SIGNALS", bx, by, btn_w, InpButtonH, g_view == ASTRO_RAW_SIGNAL); bx += btn_w + 8;
   DAL_Button(g_prefix + "_BTN_TIM", "TIMING", bx, by, btn_w, InpButtonH, g_view == ASTRO_RAW_TIMING);

   bx = g.x + g.header_w - 2 * (128 + 10) - 18;
   by = g.y + 48;
   DAL_Button(g_prefix + "_BTN_MIN", g_minimized ? "EXPAND" : "MINIMIZE", bx, by, 128, InpButtonH, g_minimized); bx += 138;
   DAL_Button(g_prefix + "_BTN_RELOAD", "RELOAD", bx, by, 128, InpButtonH, false);
   if(have_row)
   {
      DAL_Pill(g_prefix + "_HDR_PILL_DOC", "DOC " + DAL_Short(row.doctrine_id, 22), g.x + 16, g.y + 52, 164, InpColorButtonOff, InpColorMid);
      DAL_Pill(g_prefix + "_HDR_PILL_SCHEMA", "SCHEMA " + DAL_Short(row.schema_version, 18), g.x + 186, g.y + 52, 162, InpColorButtonOff, InpColorInfo);
      DAL_Pill(g_prefix + "_HDR_PILL_ZODIAC", row.zodiac_mode, g.x + 354, g.y + 52, 88, InpColorButtonOff, InpColorText);
   }
}

void DAL_Card(const string key, const string title, const int x, const int y, const int w, const int h)
{
   DAL_Rect(g_prefix + "_CARD_" + key, x, y, w, h, InpColorCard, InpColorBorder);
   DAL_Label(g_prefix + "_CARD_T_" + key, title, x + 14, y + 8, InpColorInfo, InpFontTitle);
   DAL_Line(g_prefix + "_CARD_R_" + key, x + 12, y + 32, w - 24, InpColorBorder);
}

void DAL_Cell4(const string key, const int i, const int x, const int y, const int c1w, const int c2w, const int c3w, const string c1, const string c2, const string c3, const string c4, const color col2=clrWhite, const color col3=clrSilver, const color col4=clrSilver)
{
   int yy = y + i * InpRowHeight;
   DAL_Label(g_prefix + "_" + key + "_A_" + IntegerToString(i), c1, x, yy, InpColorText, InpFontBody);
   DAL_Label(g_prefix + "_" + key + "_B_" + IntegerToString(i), c2, x + c1w, yy, col2, InpFontBody);
   DAL_Label(g_prefix + "_" + key + "_C_" + IntegerToString(i), c3, x + c1w + c2w, yy, col3, InpFontBody);
   DAL_Label(g_prefix + "_" + key + "_D_" + IntegerToString(i), c4, x + c1w + c2w + c3w, yy, col4, InpFontBody);
}

void DAL_DrawBodiesTable(const string key, const string title, const int x, const int y, const int w, const int h, const DAL_AstroMapRow &row, const int start_idx, const int end_idx)
{
   DAL_Card(key, title, x, y, w, h);
   int yy = y + 42;
   int c1 = 118, c2 = 118, c3 = 122;
   DAL_Cell4(key, 0, x + 14, yy, c1, c2, c3, "body", "position", "speed/dir", "decl/house", InpColorMuted, InpColorMuted, InpColorMuted);
   int r = 1;
   for(int i = start_idx; i <= end_idx && i < DAL_ASTRO_BODY_COUNT; i++)
   {
      DAL_AstroBodyState b = row.body[i];
      string spd = StringFormat("%.4f %s", b.speed_lon, DAL_RetroText(b));
      string dh = StringFormat("%.2f  H%s", b.decl, DAL_HouseText(b));
      DAL_Cell4(key, r, x + 14, yy, c1, c2, c3, DAL_BodyDisplay(b.name), DAL_PosText(b), spd, dh, InpColorMid, b.retro == 1 ? InpColorLow : InpColorText, InpColorMuted);
      r++;
   }
}

void DAL_OrderAspects(const DAL_AstroMapRow &row, int &order[])
{
   ArrayResize(order, DAL_ASTRO_ASPECT_PAIR_COUNT);
   for(int i = 0; i < DAL_ASTRO_ASPECT_PAIR_COUNT; i++) order[i] = i;
   for(int a = 0; a < DAL_ASTRO_ASPECT_PAIR_COUNT - 1; a++)
   {
      for(int b = a + 1; b < DAL_ASTRO_ASPECT_PAIR_COUNT; b++)
      {
         if(row.aspect[order[b]].orb < row.aspect[order[a]].orb)
         {
            int tmp = order[a]; order[a] = order[b]; order[b] = tmp;
         }
      }
   }
}

void DAL_DrawAspectsTable(const string key, const int x, const int y, const int w, const int h, const DAL_AstroMapRow &row, const int max_rows)
{
   DAL_Card(key, "ASPECTS - sorted by tightest orb", x, y, w, h);
   int yy = y + 42;
   int c1 = 138, c2 = 108, c3 = 112;
   DAL_Cell4(key, 0, x + 14, yy, c1, c2, c3, "pair", "aspect", "orb/app", "angle", InpColorMuted, InpColorMuted, InpColorMuted);
   int order[];
   DAL_OrderAspects(row, order);
   for(int r = 0; r < max_rows && r < DAL_ASTRO_ASPECT_PAIR_COUNT; r++)
   {
      DAL_AstroAspectState a = row.aspect[order[r]];
      color oc = DAL_OrbColor(a.orb);
      DAL_Cell4(key, r + 1, x + 14, yy, c1, c2, c3, a.pair, a.aspect, StringFormat("%.2f %s", a.orb, a.applying == 1 ? "app" : "sep"), DoubleToString(a.angle, 2), InpColorText, oc, InpColorMuted);
   }
}

void DAL_DrawHousesTable(const string key, const int x, const int y, const int w, const int h, const DAL_AstroMapRow &row)
{
   DAL_Card(key, "HOUSES / ANGLES", x, y, w, h);
   int yy = y + 42;
   if(!row.houses_valid)
   {
      DAL_Label(g_prefix + "_" + key + "_NOH", "Houses unavailable. Rebuild CSV with --house-lat and --house-lon.", x + 14, yy, InpColorLow, InpFontBody);
      return;
   }
   int c1 = 90, c2 = 120, c3 = 90;
   DAL_Cell4(key, 0, x + 14, yy, c1, c2, c3, "system", row.house_system, "location", StringFormat("%.4f / %.4f", row.house_lat, row.house_lon), InpColorText, InpColorMuted, InpColorMuted);
   DAL_Cell4(key, 1, x + 14, yy, c1, c2, c3, "ASC", DAL_LonSignText(row.asc_lon), "MC", DAL_LonSignText(row.mc_lon), InpColorMid, InpColorMid, InpColorText);
   for(int hidx = 0; hidx < 12; hidx++)
   {
      DAL_Cell4(key, hidx + 2, x + 14, yy, c1, c2, c3, "H" + IntegerToString(hidx + 1), DAL_LonSignText(row.house_cusp[hidx]), "", "", InpColorText, InpColorMuted, InpColorMuted);
   }
}

void DAL_DrawDignityTable(const string key, const int x, const int y, const int w, const int h, const DAL_AstroMapRow &row)
{
   DAL_Card(key, "TRADITIONAL ESSENTIAL DIGNITY", x, y, w, h);
   int yy = y + 42;
   int c1 = 100, c2 = 86, c3 = 128;
   DAL_Cell4(key, 0, x + 14, yy, c1, c2, c3, "body", "sign", "dignity", "house", InpColorMuted, InpColorMuted, InpColorMuted);
   for(int i = 0; i < 7; i++)
   {
      DAL_AstroBodyState b = row.body[i];
      string d = DAL_Dignity(b);
      DAL_Cell4(key, i + 1, x + 14, yy, c1, c2, c3, b.name, DAL_SignShort(b.sign), d, "H" + DAL_HouseText(b), InpColorText, DAL_DignityColor(d), InpColorMuted);
   }
}

void DAL_DrawMetricsTable(const string key, const int x, const int y, const int w, const int h, const DAL_AstroMapRow &row)
{
   DAL_Card(key, "CANONICAL RAW METRICS", x, y, w, h);
   int retro = 0, oob = 0, tight1 = 0, tight3 = 0, applying = 0;
   string retro_list = "";
   string oob_list = "";
   for(int i = 0; i < DAL_ASTRO_BODY_COUNT; i++)
   {
      if(row.body[i].retro == 1)
      {
         retro++;
         if(retro_list != "") retro_list += ",";
         retro_list += row.body[i].name;
      }
      if(MathAbs(row.body[i].decl) > 23.4366)
      {
         oob++;
         if(oob_list != "") oob_list += ",";
         oob_list += row.body[i].name;
      }
   }
   for(int j = 0; j < DAL_ASTRO_ASPECT_PAIR_COUNT; j++)
   {
      if(row.aspect[j].orb <= 1.0) tight1++;
      if(row.aspect[j].orb <= 3.0) tight3++;
      if(row.aspect[j].applying == 1) applying++;
   }
   int yy = y + 42;
   int c1 = 134, c2 = 120, c3 = 116;
   DAL_Cell4(key, 0, x + 14, yy, c1, c2, c3, "Moon phase", row.moon_phase_bucket, "angle", DoubleToString(row.moon_phase_angle, 2), InpColorMid, InpColorText, InpColorMuted);
   DAL_Cell4(key, 1, x + 14, yy, c1, c2, c3, "Illumination", DoubleToString(row.moon_illumination_proxy, 4), "", "", InpColorText, InpColorMuted, InpColorMuted);
   DAL_Cell4(key, 2, x + 14, yy, c1, c2, c3, "Retrograde", IntegerToString(retro), DAL_Short(retro_list, 28), "", retro > 0 ? InpColorLow : InpColorText, InpColorMuted, InpColorMuted);
   DAL_Cell4(key, 3, x + 14, yy, c1, c2, c3, "OOB decl", IntegerToString(oob), DAL_Short(oob_list, 28), "", oob > 0 ? InpColorLow : InpColorText, InpColorMuted, InpColorMuted);
   DAL_Cell4(key, 4, x + 14, yy, c1, c2, c3, "Tight <=1", IntegerToString(tight1), "aspects", "", tight1 > 0 ? InpColorHigh : InpColorMuted, InpColorMuted, InpColorMuted);
   DAL_Cell4(key, 5, x + 14, yy, c1, c2, c3, "Tight <=3", IntegerToString(tight3), "aspects", "", tight3 > 0 ? InpColorMid : InpColorMuted, InpColorMuted, InpColorMuted);
   DAL_Cell4(key, 6, x + 14, yy, c1, c2, c3, "Applying", IntegerToString(applying), "pairs", "", InpColorText, InpColorMuted, InpColorMuted);
   DAL_Cell4(key, 7, x + 14, yy, c1, c2, c3, "Houses", row.houses_valid ? "available" : "missing", row.houses_valid ? row.house_system : "", row.houses_valid ? StringFormat("%.3f, %.3f", row.house_lat, row.house_lon) : "", row.houses_valid ? InpColorHigh : InpColorLow, InpColorMuted, InpColorMuted);
}

void DAL_DrawNatalTable(const string key, const int x, const int y, const int w, const int h, const DAL_AstroMapRow &row)
{
   DAL_Card(key, "NATAL / INCEPTION CHART", x, y, w, h);
   int yy = y + 42;
   if(!row.natal_enabled)
   {
      DAL_Label(g_prefix + "_" + key + "_NONE", "Natal chart is not embedded in this CSV. Build the file with natal inputs.", x + 14, yy, InpColorLow, InpFontBody);
      DAL_Label(g_prefix + "_" + key + "_CFG", "EA birth input: " + DAL_BirthInputText(), x + 14, yy + 20, InpColorMuted, InpFontBody);
      return;
   }

   int c1 = 110, c2 = 120, c3 = 120;
   DAL_Cell4(key, 0, x + 14, yy, c1, c2, c3, "label", row.natal_label, "local", DAL_TimeText(row.natal_local_time), InpColorHigh, InpColorMuted, InpColorMuted);
   DAL_Cell4(key, 1, x + 14, yy, c1, c2, c3, "utc", DAL_TimeText(row.natal_utc_time), "offset", DoubleToString(row.natal_utc_offset_hours, 2), InpColorText, InpColorMuted, InpColorMuted);
   DAL_Cell4(key, 2, x + 14, yy, c1, c2, c3, "loc", StringFormat("%.4f / %.4f", row.natal_house_lat, row.natal_house_lon), "ASC", DAL_LonSignText(row.natal_asc_lon), InpColorText, InpColorMid, InpColorMuted);
   DAL_Cell4(key, 3, x + 14, yy, c1, c2, c3, "MC", DAL_LonSignText(row.natal_mc_lon), "HouseSys", row.natal_house_system, InpColorMid, InpColorText, InpColorMuted);
   DAL_Cell4(key, 4, x + 14, yy, c1, c2, c3, "EA input", DAL_BirthInputText(), "label", InpBirthLabel, InpColorMuted, InpColorMuted, InpColorMuted);

   int r = 6;
   DAL_Cell4(key, 5, x + 14, yy, c1, c2, c3, "body", "natal position", "decl/house", "dir", InpColorMuted, InpColorMuted, InpColorMuted);
   for(int i = 0; i < DAL_ASTRO_BODY_COUNT; i++)
   {
      DAL_AstroBodyState b = row.natal_body[i];
      string dh = StringFormat("%.2f  H%s", b.decl, DAL_HouseText(b));
      DAL_Cell4(key, r, x + 14, yy, c1, c2, c3, DAL_BodyDisplay(b.name), DAL_PosText(b), dh, DAL_RetroText(b), InpColorMid, InpColorMuted, b.retro == 1 ? InpColorLow : InpColorText);
      r++;
      if(r >= 15)
         break;
   }
}

void DAL_DrawTransitNatalTable(const string key, const int x, const int y, const int w, const int h, const DAL_AstroMapRow &row)
{
   DAL_Card(key, "TRANSIT TO NATAL ACTIVATIONS", x, y, w, h);
   int yy = y + 42;
   if(!row.natal_enabled)
   {
      DAL_Label(g_prefix + "_" + key + "_NONE", "Transit-to-natal activations are unavailable because natal data is missing.", x + 14, yy, InpColorLow, InpFontBody);
      return;
   }

   int c1 = 142, c2 = 110, c3 = 104;
   DAL_Cell4(key, 0, x + 14, yy, c1, c2, c3, "pair", "aspect", "orb/app", "natal house", InpColorMuted, InpColorMuted, InpColorMuted);
   int order[];
   ArrayResize(order, DAL_ASTRO_TRANSIT_NATAL_ASPECT_COUNT);
   for(int i = 0; i < DAL_ASTRO_TRANSIT_NATAL_ASPECT_COUNT; i++) order[i] = i;
   for(int a = 0; a < DAL_ASTRO_TRANSIT_NATAL_ASPECT_COUNT - 1; a++)
   {
      for(int b = a + 1; b < DAL_ASTRO_TRANSIT_NATAL_ASPECT_COUNT; b++)
      {
         if(row.transit_natal_aspect[order[b]].orb < row.transit_natal_aspect[order[a]].orb)
         {
            int tmp = order[a]; order[a] = order[b]; order[b] = tmp;
         }
      }
   }

   for(int r = 0; r < 12 && r < DAL_ASTRO_TRANSIT_NATAL_ASPECT_COUNT; r++)
   {
      DAL_AstroAspectState a = row.transit_natal_aspect[order[r]];
      int transit_idx = order[r] / DAL_ASTRO_NATAL_CORE_COUNT;
      DAL_Cell4(key, r + 1, x + 14, yy, c1, c2, c3, a.pair, a.aspect, StringFormat("%.2f %s", a.orb, a.applying == 1 ? "app" : "sep"), "H" + DAL_TransitNatalHouseText(row, transit_idx), InpColorText, DAL_OrbColor(a.orb), InpColorMuted);
   }
}

void DAL_DrawSignalTable(const string key, const int x, const int y, const int w, const int h, const DAL_AstroMapRow &row)
{
   DAL_Card(key, "PURE ASTRO SIGNAL LANGUAGE", x, y, w, h);
   int yy = y + 42;
   DAL_AstroPureSignal s;
   if(!DAL_AstroPureSignal_Calc(row, s) || !s.valid)
   {
      DAL_Label(g_prefix + "_" + key + "_FAIL", "Signal stack could not be derived from the current row.", x + 14, yy, InpColorLow, InpFontBody);
      return;
   }

   int c1 = 118, c2 = 120, c3 = 120;
   DAL_Cell4(key, 0, x + 14, yy, c1, c2, c3, "Direction", s.direction_name, "Regime", s.regime_name, InpColorHigh, InpColorMuted, InpColorMuted);
   DAL_Cell4(key, 1, x + 14, yy, c1, c2, c3, "Entry", s.entry_signal, "Exit", s.exit_signal, InpColorText, InpColorMuted, InpColorMuted);
   DAL_Cell4(key, 2, x + 14, yy, c1, c2, c3, "LongBias", DoubleToString(s.long_bias_score, 1), "ShortBias", DoubleToString(s.short_bias_score, 1), InpColorMid, InpColorMid, InpColorMuted);
   DAL_Cell4(key, 3, x + 14, yy, c1, c2, c3, "Path", DoubleToString(s.path_score, 1), "Friction", DoubleToString(s.friction_score, 1), InpColorText, InpColorLow, InpColorMuted);
   DAL_Cell4(key, 4, x + 14, yy, c1, c2, c3, "Macro", DoubleToString(s.macro_timing_score, 1), "Meso", DoubleToString(s.meso_timing_score, 1), DAL_ScoreColor(s.macro_timing_score), DAL_ScoreColor(s.meso_timing_score), InpColorMuted);
   DAL_Cell4(key, 5, x + 14, yy, c1, c2, c3, "Micro", DoubleToString(s.micro_timing_score, 1), "Minute", DoubleToString(s.minute_window_score, 1), DAL_ScoreColor(s.micro_timing_score), DAL_ScoreColor(s.minute_window_score), InpColorMuted);
   DAL_Cell4(key, 6, x + 14, yy, c1, c2, c3, "Exhaust", DoubleToString(s.minute_exhaustion_score, 1), "State", s.trigger_state, DAL_ScoreColor(100.0 - s.minute_exhaustion_score), InpColorInfo, InpColorMuted);
   DAL_Cell4(key, 7, x + 14, yy, c1, c2, c3, "Volatility", DoubleToString(s.volatility_score, 1), "NatalAct", DoubleToString(s.natal_activation_score, 1), InpColorText, InpColorMid, InpColorMuted);
   DAL_Cell4(key, 8, x + 14, yy, c1, c2, c3, "SignalText", row.astro_signal_text, "Key", DAL_Short(s.astro_trade_key, 34), InpColorMuted, InpColorMuted, InpColorMuted);
}

void DAL_DrawTimingSummaryCard(const string key, const int x, const int y, const int w, const int h, const string title, const string state_text, const double score1, const string label1, const double score2, const string label2, const color accent)
{
   DAL_Card(key, title, x, y, w, h);
   DAL_Label(g_prefix + "_" + key + "_STATE", state_text, x + 14, y + 42, accent, InpFontTitle);
   DAL_Label(g_prefix + "_" + key + "_A", label1 + " " + DoubleToString(score1, 1), x + 14, y + 70, DAL_ScoreColor(score1), InpFontBody);
   DAL_Label(g_prefix + "_" + key + "_B", label2 + " " + DoubleToString(score2, 1), x + 14, y + 92, DAL_ScoreColor(score2), InpFontBody);
}

void DAL_DrawTimingTable(const string key, const int x, const int y, const int w, const int h, const DAL_AstroMapRow &row)
{
   DAL_Card(key, "ASTRO TIMING DOCTRINE", x, y, w, h);
   int yy = y + 42;
   DAL_AstroTimingState t;
   if(!DAL_AstroTD_Calc(row, t) || !t.valid)
   {
      DAL_Label(g_prefix + "_" + key + "_FAIL", "Timing doctrine could not be derived from the current row.", x + 14, yy, InpColorLow, InpFontBody);
      return;
   }

   int c1 = 132, c2 = 120, c3 = 118;
   DAL_Cell4(key, 0, x + 14, yy, c1, c2, c3, "MacroDir", t.macro_direction, "State", t.trigger_state, DAL_ScoreColor(t.macro_alignment_score), InpColorInfo, InpColorMuted);
   DAL_Cell4(key, 1, x + 14, yy, c1, c2, c3, "MacroBias", DoubleToString(t.macro_bias_score, 1), "Align", DoubleToString(t.macro_alignment_score, 1), DAL_ScoreColor(t.macro_bias_score), DAL_ScoreColor(t.macro_alignment_score), InpColorMuted);
   DAL_Cell4(key, 2, x + 14, yy, c1, c2, c3, "MesoGate", DoubleToString(t.meso_gate_score, 1), "Angular", DoubleToString(t.meso_angularity_score, 1), DAL_ScoreColor(t.meso_gate_score), DAL_ScoreColor(t.meso_angularity_score), InpColorMuted);
   DAL_Cell4(key, 3, x + 14, yy, c1, c2, c3, "Resonance", DoubleToString(t.meso_resonance_score, 1), "MicroTrig", DoubleToString(t.micro_trigger_score, 1), DAL_ScoreColor(t.meso_resonance_score), DAL_ScoreColor(t.micro_trigger_score), InpColorMuted);
   DAL_Cell4(key, 4, x + 14, yy, c1, c2, c3, "Release", DoubleToString(t.micro_release_score, 1), "MinuteWin", DoubleToString(t.minute_window_score, 1), DAL_ScoreColor(t.micro_release_score), DAL_ScoreColor(t.minute_window_score), InpColorMuted);
   DAL_Cell4(key, 5, x + 14, yy, c1, c2, c3, "Exhaust", DoubleToString(t.minute_exhaustion_score, 1), "", "", DAL_ScoreColor(100.0 - t.minute_exhaustion_score), InpColorMuted, InpColorMuted);
   DAL_Cell4(key, 6, x + 14, yy, c1, c2, c3, "MacroCtx", DAL_Short(t.macro_context, 42), "", "", InpColorMuted, InpColorMuted, InpColorMuted);
   DAL_Cell4(key, 7, x + 14, yy, c1, c2, c3, "MesoCtx", DAL_Short(t.meso_context, 42), "", "", InpColorMuted, InpColorMuted, InpColorMuted);
   DAL_Cell4(key, 8, x + 14, yy, c1, c2, c3, "MicroCtx", DAL_Short(t.micro_context, 42), "", "", InpColorMuted, InpColorMuted, InpColorMuted);
   DAL_Cell4(key, 9, x + 14, yy, c1, c2, c3, "MinuteCtx", DAL_Short(t.minute_context, 42), "", "", InpColorMuted, InpColorMuted, InpColorMuted);
}

void DAL_DrawDiagnostics(const DAL_UIGrid &g, const DAL_AstroMapRow &row, const bool have_row, const bool exact, const bool fallback)
{
   int h = MathMax(240, g.panel_h);
   DAL_Card("DIAG", "DIAGNOSTICS", g.side_x, g.side_y, g.side_w, h);
   int yy = g.side_y + 42;
   int c1 = 112, c2 = 146, c3 = 90;
   DAL_Cell4("DIAG", 0, g.side_x + 14, yy, c1, c2, c3, "CSV", g_loaded ? "LOADED" : "NOT LOADED", "rows", IntegerToString(g_store.row_count), g_loaded ? InpColorHigh : InpColorLow, InpColorMuted, InpColorMuted);
   DAL_Cell4("DIAG", 1, g.side_x + 14, yy, c1, c2, c3, "Source", DAL_Short(g_store.source_file, 34), "", "", InpColorMuted, InpColorMuted, InpColorMuted);
   DAL_Cell4("DIAG", 2, g.side_x + 14, yy, c1, c2, c3, "Lookup", have_row ? (exact ? "exact" : (fallback ? "fallback" : "unknown")) : "not found", "", "", exact ? InpColorHigh : (fallback ? InpColorMid : InpColorLow), InpColorMuted, InpColorMuted);
   DAL_Cell4("DIAG", 3, g.side_x + 14, yy, c1, c2, c3, "Chart", DAL_TimeText(iTime(_Symbol, _Period, 0)), "matched", have_row ? DAL_TimeText(row.broker_time) : "n/a", InpColorText, InpColorMuted, InpColorMuted);
   DAL_Cell4("DIAG", 4, g.side_x + 14, yy, c1, c2, c3, "Time rule", "chart open", "= csv broker_time", "", InpColorMuted, InpColorMuted, InpColorMuted);
   DAL_Cell4("DIAG", 5, g.side_x + 14, yy, c1, c2, c3, "Doctrine", have_row ? DAL_Short(row.doctrine_id, 20) : "n/a", "Schema", have_row ? row.schema_version : "n/a", InpColorMid, InpColorMuted, InpColorMuted);
   DAL_Cell4("DIAG", 6, g.side_x + 14, yy, c1, c2, c3, "Natal", have_row && row.natal_enabled ? row.natal_label : "not active", "Mode", have_row ? row.zodiac_mode : "n/a", have_row && row.natal_enabled ? InpColorHigh : InpColorMid, InpColorMuted, InpColorMuted);
}

void DAL_DrawSkySnapshot(const DAL_UIGrid &g, const DAL_AstroMapRow &row)
{
   DAL_AstroPureSignal s;
   DAL_AstroTimingState t;
   bool have_signal = DAL_AstroPureSignal_Calc(row, s) && s.valid;
   bool have_timing = DAL_AstroTD_Calc(row, t) && t.valid;

   int summary_h = 154;
   int half_gap = 10;
   int mini_w = (g.main_w - 3 * half_gap) / 4;
   DAL_DrawTimingSummaryCard("SUM_MACRO", g.main_x, g.main_y, mini_w, summary_h, "MACRO FIELD", have_timing ? t.macro_direction : "n/a", have_timing ? t.macro_bias_score : 0.0, "bias", have_timing ? t.macro_alignment_score : 0.0, "align", InpColorInfo);
   DAL_DrawTimingSummaryCard("SUM_MESO", g.main_x + mini_w + half_gap, g.main_y, mini_w, summary_h, "MESO GATE", have_timing ? DAL_AstroFM_Bucket(t.meso_gate_score) : "n/a", have_timing ? t.meso_gate_score : 0.0, "gate", have_timing ? t.meso_resonance_score : 0.0, "res", InpColorMid);
   DAL_DrawTimingSummaryCard("SUM_MICRO", g.main_x + 2 * (mini_w + half_gap), g.main_y, mini_w, summary_h, "MICRO TRIGGER", have_timing ? DAL_AstroFM_Bucket(t.micro_trigger_score) : "n/a", have_timing ? t.micro_trigger_score : 0.0, "trigger", have_timing ? t.micro_release_score : 0.0, "release", InpColorHigh);
   DAL_DrawTimingSummaryCard("SUM_MIN", g.main_x + 3 * (mini_w + half_gap), g.main_y, mini_w, summary_h, "MINUTE WINDOW", have_timing ? t.trigger_state : "n/a", have_timing ? t.minute_window_score : 0.0, "window", have_timing ? t.minute_exhaustion_score : 0.0, "exhaust", InpColorText);

   int h = 248;
   int snap_y = g.main_y + summary_h + InpGap;
   DAL_Card("SNAP", "SKY SNAPSHOT", g.main_x, snap_y, g.main_w, h);
   int yy = snap_y + 42;
   int c1 = 104, c2 = 130, c3 = 130;
   DAL_Cell4("SNAP", 0, g.main_x + 14, yy, c1, c2, c3, "Sun", DAL_PosText(row.body[0]), "Moon", DAL_PosText(row.body[1]), InpColorMid, InpColorMid, InpColorText);
   DAL_Cell4("SNAP", 1, g.main_x + 14, yy, c1, c2, c3, "Mercury", DAL_PosText(row.body[2]), "Venus", DAL_PosText(row.body[3]), InpColorText, InpColorText, InpColorText);
   DAL_Cell4("SNAP", 2, g.main_x + 14, yy, c1, c2, c3, "Mars", DAL_PosText(row.body[4]), "Jupiter", DAL_PosText(row.body[5]), InpColorText, InpColorText, InpColorText);
   DAL_Cell4("SNAP", 3, g.main_x + 14, yy, c1, c2, c3, "Saturn", DAL_PosText(row.body[6]), "Phase", row.moon_phase_bucket, InpColorText, InpColorMid, InpColorMuted);
   if(row.houses_valid)
   {
      DAL_Cell4("SNAP", 4, g.main_x + 14, yy, c1, c2, c3, "ASC", DAL_LonSignText(row.asc_lon), "MC", DAL_LonSignText(row.mc_lon), InpColorMid, InpColorMid, InpColorText);
      DAL_Cell4("SNAP", 5, g.main_x + 14, yy, c1, c2, c3, "House sys", row.house_system, "Loc", StringFormat("%.2f / %.2f", row.house_lat, row.house_lon), InpColorText, InpColorMuted, InpColorMuted);
   }
   else
   {
      DAL_Cell4("SNAP", 4, g.main_x + 14, yy, c1, c2, c3, "Houses", "missing", "", "", InpColorLow, InpColorMuted, InpColorMuted);
      DAL_Cell4("SNAP", 5, g.main_x + 14, yy, c1, c2, c3, "Fix", "run builder", "with lat/lon", "", InpColorMid, InpColorMuted, InpColorMuted);
   }
   if(have_signal)
      DAL_Cell4("SNAP", 6, g.main_x + 14, yy, c1, c2, c3, "Entry", s.entry_signal, "Exit", s.exit_signal, InpColorInfo, InpColorMuted, InpColorMuted);
   DAL_DrawMetricsTable("MET_OVR", g.main_x, snap_y + h + InpGap, g.card_w, 248, row);
   DAL_DrawAspectsTable("ASP_OVR", g.col2_x, snap_y + h + InpGap, g.card_w, 248, row, 8);
}

void DAL_Render()
{
   if(DAL_ShouldReload()) DAL_LoadStore();

   bool exact = false;
   bool fallback = false;
   DAL_AstroMapRow row;
   bool have_row = DAL_FindRow(row, exact, fallback);

   int cw = (int)ChartGetInteger(ChartID(), CHART_WIDTH_IN_PIXELS, 0);
   int ch = (int)ChartGetInteger(ChartID(), CHART_HEIGHT_IN_PIXELS, 0);
   if(cw != g_last_w || ch != g_last_h)
   {
      g_last_w = cw;
      g_last_h = ch;
      g_force_rebuild = true;
   }
   if(g_force_rebuild)
   {
      DAL_CleanupAll();
      g_force_rebuild = false;
   }

   DAL_UIGrid g;
   DAL_GetGrid(g);
   DAL_DrawHeader(g, have_row, exact, fallback, row);

   if(g_minimized)
   {
      ChartRedraw(ChartID());
      return;
   }

   if(!have_row)
   {
      DAL_DrawDiagnostics(g, row, have_row, exact, fallback);
      ChartRedraw(ChartID());
      return;
   }

   if(g_view == ASTRO_RAW_OVERVIEW)
      DAL_DrawSkySnapshot(g, row);
   else if(g_view == ASTRO_RAW_BODIES)
      DAL_DrawBodiesTable("BODIES_ALL", "ALL BODIES", g.main_x, g.main_y, g.main_w, g.panel_h, row, 0, 11);
   else if(g_view == ASTRO_RAW_ASPECTS)
      DAL_DrawAspectsTable("ASPECTS_ALL", g.main_x, g.main_y, g.main_w, g.panel_h, row, 15);
   else if(g_view == ASTRO_RAW_HOUSES)
   {
      DAL_DrawHousesTable("HOUSES_BIG", g.main_x, g.main_y, g.card_w, g.panel_h, row);
      DAL_DrawBodiesTable("HOUSE_BODIES", "BODY HOUSE PLACEMENT", g.col2_x, g.main_y, g.card_w, g.panel_h, row, 0, 11);
   }
   else if(g_view == ASTRO_RAW_METRICS)
   {
      DAL_DrawMetricsTable("METRICS_BIG", g.main_x, g.main_y, g.card_w, 280, row);
      DAL_DrawDignityTable("DIGNITY_BIG", g.col2_x, g.main_y, g.card_w, 240, row);
   }
   else if(g_view == ASTRO_RAW_NATAL)
   {
      DAL_DrawNatalTable("NATAL_BIG", g.main_x, g.main_y, g.card_w, g.panel_h, row);
      DAL_DrawTransitNatalTable("TNATAL_BIG", g.col2_x, g.main_y, g.card_w, g.panel_h, row);
   }
   else if(g_view == ASTRO_RAW_SIGNAL)
   {
      DAL_DrawSignalTable("SIGNALS_BIG", g.main_x, g.main_y, g.card_w, 260, row);
      DAL_DrawTransitNatalTable("TNATAL_SIG", g.col2_x, g.main_y, g.card_w, g.panel_h, row);
   }
   else if(g_view == ASTRO_RAW_TIMING)
   {
      DAL_DrawTimingTable("TIMING_BIG", g.main_x, g.main_y, g.card_w, g.panel_h, row);
      DAL_DrawSignalTable("SIGNALS_TIM", g.col2_x, g.main_y, g.card_w, 320, row);
   }

   DAL_DrawDiagnostics(g, row, have_row, exact, fallback);

   if(InpUseTerminalComment)
      Comment("EXP0013 raw sky | ", exact ? "exact" : (fallback ? "fallback" : "no row"), " | ", row.summary);

   ChartRedraw(ChartID());
}

int OnInit()
{
   g_prefix = "DAL_EXP0013_RAW_SKY_V14_" + IntegerToString((int)ChartID());
   g_view = InpInitialView;
   g_last_w = 0;
   g_last_h = 0;
   g_force_rebuild = true;
   DAL_CleanupAll();
   EventSetTimer(MathMax(1, InpRefreshSeconds));
   DAL_LoadStore();
   DAL_Render();
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   DAL_CleanupAll();
   if(InpUseTerminalComment) Comment("");
}

void OnTick() {}
void OnTimer() { DAL_Render(); }

void OnChartEvent(const int id, const long &lparam, const double &dparam, const string &sparam)
{
   if(id != CHARTEVENT_OBJECT_CLICK) return;
   bool changed = false;
   if(sparam == g_prefix + "_BTN_OVR") { g_view = ASTRO_RAW_OVERVIEW; changed = true; }
   else if(sparam == g_prefix + "_BTN_BODY") { g_view = ASTRO_RAW_BODIES; changed = true; }
   else if(sparam == g_prefix + "_BTN_ASP") { g_view = ASTRO_RAW_ASPECTS; changed = true; }
   else if(sparam == g_prefix + "_BTN_HOU") { g_view = ASTRO_RAW_HOUSES; changed = true; }
   else if(sparam == g_prefix + "_BTN_MET") { g_view = ASTRO_RAW_METRICS; changed = true; }
   else if(sparam == g_prefix + "_BTN_NAT") { g_view = ASTRO_RAW_NATAL; changed = true; }
   else if(sparam == g_prefix + "_BTN_SIG") { g_view = ASTRO_RAW_SIGNAL; changed = true; }
   else if(sparam == g_prefix + "_BTN_TIM") { g_view = ASTRO_RAW_TIMING; changed = true; }
   else if(sparam == g_prefix + "_BTN_MIN") { g_minimized = !g_minimized; changed = true; }
   else if(sparam == g_prefix + "_BTN_RELOAD") { DAL_LoadStore(); }
   if(changed) g_force_rebuild = true;
   DAL_Render();
}
