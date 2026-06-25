#property strict
#property description "Decision Alpha Lab - EXP0013 Radical Raw Astro Dashboard EA"
#property description "Research-only raw sky dashboard. No trade, no iCustom, no interpretive scores."
#property tester_file "astro_GMT3_M1_2026_to_now_mql.csv"
#property tester_file "astro\\astro_GMT3_M1_2026_to_now_mql.csv"
#property tester_file "astro_live_mql.csv"

#include <Research/DAL_AstroMapTypes.mqh>
#include <Research/DAL_AstroExcelCandleReader.mqh>

enum DAL_AstroRawView
{
   ASTRO_RAW_OVERVIEW = 0,
   ASTRO_RAW_BODIES   = 1,
   ASTRO_RAW_ASPECTS  = 2,
   ASTRO_RAW_HOUSES   = 3,
   ASTRO_RAW_METRICS  = 4
};

input string         InpAstroCsvFile          = "astro_live_mql.csv";
input double         InpBrokerGmtOffsetHours  = 0.0;
input bool           InpRequireExactBarTime   = true;
input int            InpReloadCsvEverySeconds = 10;
input int            InpRefreshSeconds        = 1;
input DAL_AstroRawView InpInitialView         = ASTRO_RAW_OVERVIEW;
input bool           InpShowLowerOrbStrip     = true;
input bool           InpUseTerminalComment    = false;

input int            InpBaseX                 = 10;
input int            InpBaseY                 = 10;
input int            InpHeaderHeight          = 104;
input int            InpGap                   = 16;
input int            InpButtonW               = 108;
input int            InpButtonH               = 28;
input int            InpFontHero              = 14;
input int            InpFontTitle             = 12;
input int            InpFontBody              = 9;
input int            InpRowHeight             = 19;

input color          InpColorPanel            = C'7,7,7';
input color          InpColorCard             = C'10,10,10';
input color          InpColorBorder           = C'86,86,86';
input color          InpColorText             = clrWhite;
input color          InpColorMuted            = clrSilver;
input color          InpColorInfo             = clrAqua;
input color          InpColorLow              = clrTomato;
input color          InpColorMid              = clrGold;
input color          InpColorHigh             = clrLime;
input color          InpColorButtonOn         = C'22,72,22';
input color          InpColorButtonOff        = C'36,36,36';

DAL_AstroMapStore g_store;
bool              g_loaded = false;
datetime          g_last_load_time = 0;
string            g_prefix = "DAL_EXP0013_RAW_ASTRO";
DAL_AstroRawView  g_view;
bool              g_minimized = false;
bool              g_show_orb_strip = true;
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
   int card_w;
   int wide_w;
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

void DAL_Line(const string name, const int x, const int y, const int w, const color clr)
{
   DAL_Rect(name, x, y, w, 1, clr, clr);
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

string DAL_BodyShort(const string name)
{
   if(name == "true_node") return "true_node";
   if(name == "mean_node") return "mean_node";
   return name;
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

bool DAL_LoadStore()
{
   g_last_load_time = TimeCurrent();
   g_loaded = DAL_AstroMapStore_LoadExcelCsv(g_store, InpAstroCsvFile, InpBrokerGmtOffsetHours, PeriodSeconds(_Period) / 60);
   Print("EXP0013 Raw Astro | CSV loaded=", g_loaded, " rows=", g_store.row_count, " source=", g_store.source_file);
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
   g.header_w = MathMax(1000, g.chart_w - 30);
   g.header_h = (g_minimized ? 74 : InpHeaderHeight);
   g.diag_w = MathMax(470, g.header_w / 3);
   int left_w = g.header_w - g.diag_w - InpGap;
   g.card_w = MathMax(420, (left_w - InpGap) / 2);
   g.wide_w = left_w;
   g.col1_x = g.x;
   g.col2_x = g.x + g.card_w + InpGap;
   g.col3_x = g.x + left_w + InpGap;
   g.row1_y = g.y + g.header_h + 12;
   g.row2_y = g.row1_y + 196 + InpGap;
   g.row3_y = g.row2_y + 196 + InpGap;
}

void DAL_DrawHeader(const DAL_UIGrid &g, const bool have_row, const bool exact, const bool fallback, const DAL_AstroMapRow &row)
{
   DAL_Rect(g_prefix + "_HDR_BG", g.x, g.y, g.header_w, g.header_h, InpColorPanel, InpColorBorder);
   DAL_Label(g_prefix + "_HDR_TITLE", "EXP0013 RADICAL RAW SKY", g.x + 16, g.y + 8, InpColorInfo, InpFontHero);
   DAL_Label(g_prefix + "_HDR_SUB", "no interpretation layer · raw positions / houses / aspects / canonical geometry", g.x + 16, g.y + 28, InpColorMuted, InpFontBody);
   DAL_Line(g_prefix + "_HDR_RULE", g.x + 14, g.y + 44, g.header_w - 28, InpColorBorder);

   string row_status = !g_loaded ? "CSV NOT LOADED" : (!have_row ? "ROW NOT FOUND" : (exact ? "EXACT ROW" : "FALLBACK ROW"));
   color st_col = !g_loaded ? InpColorLow : (!have_row ? InpColorLow : (exact ? InpColorHigh : InpColorMid));
   int y2 = g.y + 52;
   DAL_Label(g_prefix + "_HDR_META1", "Symbol", g.x + 16, y2, InpColorMuted, InpFontBody);
   DAL_Label(g_prefix + "_HDR_META1V", _Symbol, g.x + 78, y2, InpColorText, InpFontBody);
   DAL_Label(g_prefix + "_HDR_META2", "TF", g.x + 160, y2, InpColorMuted, InpFontBody);
   DAL_Label(g_prefix + "_HDR_META2V", EnumToString(_Period), g.x + 192, y2, InpColorText, InpFontBody);
   DAL_Label(g_prefix + "_HDR_META3", "Status", g.x + 280, y2, InpColorMuted, InpFontBody);
   DAL_Label(g_prefix + "_HDR_META3V", row_status, g.x + 342, y2, st_col, InpFontBody);
   DAL_Label(g_prefix + "_HDR_META4", "File", g.x + 500, y2, InpColorMuted, InpFontBody);
   DAL_Label(g_prefix + "_HDR_META4V", DAL_Short(InpAstroCsvFile, 34), g.x + 540, y2, InpColorMid, InpFontBody);

   if(!g_minimized)
   {
      string tline = have_row ? ("Broker " + DAL_TimeText(row.broker_time) + "  |  UTC " + DAL_TimeText(row.utc_time) + "  |  JD " + DoubleToString(row.jd_ut, 5))
                              : ("Chart candle " + DAL_TimeText(iTime(_Symbol, _Period, 0)));
      DAL_Label(g_prefix + "_HDR_TIME", tline, g.x + 16, g.y + 74, InpColorMuted, InpFontBody);
   }

   int bx = g.x + g.header_w - 5 * (InpButtonW + 8) - 18;
   int by = g.y + 10;
   DAL_Button(g_prefix + "_BTN_OVR", "OVERVIEW", bx, by, InpButtonW, InpButtonH, g_view == ASTRO_RAW_OVERVIEW); bx += InpButtonW + 8;
   DAL_Button(g_prefix + "_BTN_BODY", "BODIES", bx, by, InpButtonW, InpButtonH, g_view == ASTRO_RAW_BODIES); bx += InpButtonW + 8;
   DAL_Button(g_prefix + "_BTN_ASP", "ASPECTS", bx, by, InpButtonW, InpButtonH, g_view == ASTRO_RAW_ASPECTS); bx += InpButtonW + 8;
   DAL_Button(g_prefix + "_BTN_HOU", "HOUSES", bx, by, InpButtonW, InpButtonH, g_view == ASTRO_RAW_HOUSES); bx += InpButtonW + 8;
   DAL_Button(g_prefix + "_BTN_MET", "METRICS", bx, by, InpButtonW, InpButtonH, g_view == ASTRO_RAW_METRICS);

   bx = g.x + g.header_w - 3 * (128 + 10) - 18;
   by = g.y + 48;
   DAL_Button(g_prefix + "_BTN_STRIP", g_show_orb_strip ? "ORB STRIP ON" : "ORB STRIP OFF", bx, by, 128, InpButtonH, g_show_orb_strip); bx += 138;
   DAL_Button(g_prefix + "_BTN_MIN", g_minimized ? "EXPAND" : "MINIMIZE", bx, by, 128, InpButtonH, g_minimized); bx += 138;
   DAL_Button(g_prefix + "_BTN_RELOAD", "RELOAD", bx, by, 128, InpButtonH, false);
}

void DAL_Card(const string key, const string title, const int x, const int y, const int w, const int h)
{
   DAL_Rect(g_prefix + "_CARD_" + key, x, y, w, h, InpColorCard, InpColorBorder);
   DAL_Label(g_prefix + "_CARD_T_" + key, title, x + 14, y + 8, InpColorInfo, InpFontTitle);
   DAL_Line(g_prefix + "_CARD_R_" + key, x + 12, y + 30, w - 24, InpColorBorder);
}

void DAL_Row(const string key, const int i, const int x, const int y, const string c1, const string c2, const string c3, const string c4, const color col2=clrWhite, const color col3=clrSilver, const color col4=clrSilver)
{
   int yy = y + i * InpRowHeight;
   DAL_Label(g_prefix + "_" + key + "_A_" + IntegerToString(i), c1, x, yy, InpColorText, InpFontBody);
   DAL_Label(g_prefix + "_" + key + "_B_" + IntegerToString(i), c2, x + 118, yy, col2, InpFontBody);
   DAL_Label(g_prefix + "_" + key + "_C_" + IntegerToString(i), c3, x + 236, yy, col3, InpFontBody);
   DAL_Label(g_prefix + "_" + key + "_D_" + IntegerToString(i), c4, x + 360, yy, col4, InpFontBody);
}

void DAL_DrawBodiesCard(const string key, const string title, const int x, const int y, const int w, const DAL_AstroMapRow &row, const int start_idx, const int end_idx)
{
   int n = end_idx - start_idx + 1;
   int h = 42 + (n + 1) * InpRowHeight + 12;
   DAL_Card(key, title, x, y, w, h);
   int yy = y + 40;
   DAL_Row(key, 0, x + 14, yy, "body", "position", "speed/dir", "decl/house", InpColorMuted, InpColorMuted, InpColorMuted);
   for(int i = start_idx; i <= end_idx; i++)
   {
      DAL_AstroBodyState b = row.body[i];
      string spd = StringFormat("%.4f %s", b.speed_lon, DAL_RetroText(b));
      string dh = StringFormat("decl %.2f  H%s", b.decl, DAL_HouseText(b));
      DAL_Row(key, i - start_idx + 1, x + 14, yy, DAL_BodyShort(b.name), DAL_PosText(b), spd, dh, InpColorMid, b.retro == 1 ? InpColorLow : InpColorText, InpColorMuted);
   }
}

void DAL_DrawDignityCard(const string key, const int x, const int y, const int w, const DAL_AstroMapRow &row)
{
   int h = 42 + 8 * InpRowHeight + 12;
   DAL_Card(key, "ESSENTIAL DIGNITY (traditional categories)", x, y, w, h);
   int yy = y + 40;
   DAL_Row(key, 0, x + 14, yy, "body", "sign", "dignity", "house", InpColorMuted, InpColorMuted, InpColorMuted);
   for(int i = 0; i < 7; i++)
   {
      DAL_AstroBodyState b = row.body[i];
      string d = DAL_Dignity(b);
      DAL_Row(key, i + 1, x + 14, yy, b.name, DAL_SignShort(b.sign), d, "H" + DAL_HouseText(b), InpColorText, DAL_DignityColor(d), InpColorMuted);
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

void DAL_DrawAspectsCard(const string key, const int x, const int y, const int w, const DAL_AstroMapRow &row, const int max_rows)
{
   int h = 42 + (max_rows + 1) * InpRowHeight + 12;
   DAL_Card(key, "ASPECT GEOMETRY - sorted by tightest orb", x, y, w, h);
   int yy = y + 40;
   DAL_Row(key, 0, x + 14, yy, "pair", "aspect", "orb/app", "angle", InpColorMuted, InpColorMuted, InpColorMuted);
   int order[];
   DAL_OrderAspects(row, order);
   for(int r = 0; r < max_rows && r < DAL_ASTRO_ASPECT_PAIR_COUNT; r++)
   {
      DAL_AstroAspectState a = row.aspect[order[r]];
      color oc = a.orb <= 1.0 ? InpColorHigh : (a.orb <= 3.0 ? InpColorMid : InpColorMuted);
      DAL_Row(key, r + 1, x + 14, yy, a.pair, a.aspect, StringFormat("%.2f %s", a.orb, a.applying == 1 ? "app" : "sep"), DoubleToString(a.angle, 2), InpColorText, oc, InpColorMuted);
   }
}

void DAL_DrawHousesCard(const string key, const int x, const int y, const int w, const DAL_AstroMapRow &row)
{
   int h = 42 + 14 * InpRowHeight + 12;
   DAL_Card(key, "HOUSES / ANGLES", x, y, w, h);
   int yy = y + 40;
   if(!row.houses_valid)
   {
      DAL_Label(g_prefix + "_" + key + "_NOH", "Houses unavailable. Rebuild CSV with --house-lat and --house-lon.", x + 14, yy, InpColorLow, InpFontBody);
      return;
   }
   DAL_Row(key, 0, x + 14, yy, "system", row.house_system, "lat/lon", StringFormat("%.4f / %.4f", row.house_lat, row.house_lon), InpColorText, InpColorMuted, InpColorMuted);
   DAL_Row(key, 1, x + 14, yy, "ASC", DAL_LonSignText(row.asc_lon), "MC", DAL_LonSignText(row.mc_lon), InpColorMid, InpColorMid, InpColorText);
   for(int hidx = 0; hidx < 12; hidx++)
   {
      string left = "H" + IntegerToString(hidx + 1);
      DAL_Row(key, hidx + 2, x + 14, yy, left, DAL_LonSignText(row.house_cusp[hidx]), "", "", InpColorText, InpColorMuted, InpColorMuted);
   }
}

void DAL_DrawMetricsCard(const string key, const int x, const int y, const int w, const DAL_AstroMapRow &row)
{
   int h = 42 + 12 * InpRowHeight + 12;
   DAL_Card(key, "CANONICAL RAW METRICS (no narrative scoring)", x, y, w, h);
   int yy = y + 40;
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
   DAL_Row(key, 0, x + 14, yy, "Moon phase", row.moon_phase_bucket, "angle", DoubleToString(row.moon_phase_angle, 2), InpColorMid, InpColorText, InpColorMuted);
   DAL_Row(key, 1, x + 14, yy, "Illumination", DoubleToString(row.moon_illumination_proxy, 4), "", "", InpColorText, InpColorMuted, InpColorMuted);
   DAL_Row(key, 2, x + 14, yy, "Retrograde", IntegerToString(retro), DAL_Short(retro_list, 24), "", retro > 0 ? InpColorLow : InpColorText, InpColorMuted, InpColorMuted);
   DAL_Row(key, 3, x + 14, yy, "OOB decl", IntegerToString(oob), DAL_Short(oob_list, 24), "", oob > 0 ? InpColorLow : InpColorText, InpColorMuted, InpColorMuted);
   DAL_Row(key, 4, x + 14, yy, "Tight <=1", IntegerToString(tight1), "aspects", "", tight1 > 0 ? InpColorHigh : InpColorMuted, InpColorMuted, InpColorMuted);
   DAL_Row(key, 5, x + 14, yy, "Tight <=3", IntegerToString(tight3), "aspects", "", tight3 > 0 ? InpColorMid : InpColorMuted, InpColorMuted, InpColorMuted);
   DAL_Row(key, 6, x + 14, yy, "Applying", IntegerToString(applying), "pairs", "", InpColorText, InpColorMuted, InpColorMuted);
   DAL_Row(key, 7, x + 14, yy, "Houses", row.houses_valid ? "available" : "missing", row.houses_valid ? row.house_system : "", row.houses_valid ? StringFormat("%.3f, %.3f", row.house_lat, row.house_lon) : "", row.houses_valid ? InpColorHigh : InpColorLow, InpColorMuted, InpColorMuted);
   DAL_Row(key, 8, x + 14, yy, "Feature key", DAL_Short(row.feature_key, 36), "", "", InpColorMuted, InpColorMuted, InpColorMuted);
}

void DAL_DrawDiagnosticsCard(const string key, const int x, const int y, const int w, const int h, const DAL_AstroMapRow &row, const bool have_row, const bool exact, const bool fallback)
{
   DAL_Card(key, "DIAGNOSTICS", x, y, w, h);
   int yy = y + 40;
   DAL_Row(key, 0, x + 14, yy, "CSV", g_loaded ? "LOADED" : "NOT LOADED", "rows", IntegerToString(g_store.row_count), g_loaded ? InpColorHigh : InpColorLow, InpColorMuted, InpColorMuted);
   DAL_Row(key, 1, x + 14, yy, "Source", DAL_Short(g_store.source_file, 28), "", "", InpColorMuted, InpColorMuted, InpColorMuted);
   DAL_Row(key, 2, x + 14, yy, "Lookup", have_row ? (exact ? "exact" : (fallback ? "fallback" : "unknown")) : "not found", "", "", exact ? InpColorHigh : (fallback ? InpColorMid : InpColorLow), InpColorMuted, InpColorMuted);
   DAL_Row(key, 3, x + 14, yy, "Chart", DAL_TimeText(iTime(_Symbol, _Period, 0)), "matched", have_row ? DAL_TimeText(row.broker_time) : "n/a", InpColorText, InpColorMuted, InpColorMuted);
   DAL_Row(key, 4, x + 14, yy, "Time rule", "chart open", "= csv broker_time", "", InpColorMuted, InpColorMuted, InpColorMuted);
   DAL_Row(key, 5, x + 14, yy, "Claim", "raw sky only", "no causal UI", "", InpColorMid, InpColorMuted, InpColorMuted);
}

void DAL_DrawOrbStrip(const DAL_UIGrid &g, const DAL_AstroMapRow &row)
{
   if(!g_show_orb_strip) return;
   int x = g.x;
   int y = g.row3_y;
   int w = g.wide_w;
   int h = 42 + 8 * InpRowHeight + 12;
   DAL_Card("ORBSTRIP", "ORB TIGHTNESS STRIP - mathematical geometry only", x, y, w, h);
   int order[];
   DAL_OrderAspects(row, order);
   int yy = y + 42;
   for(int r = 0; r < 8 && r < DAL_ASTRO_ASPECT_PAIR_COUNT; r++)
   {
      DAL_AstroAspectState a = row.aspect[order[r]];
      double tight = MathMax(0.0, MathMin(100.0, (1.0 - MathMin(a.orb, 6.0) / 6.0) * 100.0));
      color c = tight >= 80.0 ? InpColorHigh : (tight >= 50.0 ? InpColorMid : InpColorLow);
      int ry = yy + r * InpRowHeight;
      DAL_Label(g_prefix + "_ORB_A_" + IntegerToString(r), a.pair, x + 14, ry, InpColorText, InpFontBody);
      DAL_Label(g_prefix + "_ORB_B_" + IntegerToString(r), a.aspect, x + 150, ry, InpColorText, InpFontBody);
      DAL_Label(g_prefix + "_ORB_C_" + IntegerToString(r), StringFormat("orb %.2f %s", a.orb, a.applying == 1 ? "app" : "sep"), x + 260, ry, c, InpFontBody);
      DAL_Rect(g_prefix + "_ORB_BG_" + IntegerToString(r), x + 430, ry + 5, 160, 10, C'22,22,22', InpColorBorder);
      DAL_Rect(g_prefix + "_ORB_F_" + IntegerToString(r), x + 430, ry + 5, (int)MathRound(tight / 100.0 * 160.0), 10, c, c);
   }
}

void DAL_DrawOverview(const DAL_UIGrid &g, const DAL_AstroMapRow &row, const bool have_row, const bool exact, const bool fallback)
{
   DAL_DrawBodiesCard("CORE", "CORE BODIES", g.col1_x, g.row1_y, g.card_w, row, 0, 6);
   DAL_DrawBodiesCard("OUTER", "OUTER / NODES", g.col2_x, g.row1_y, g.card_w, row, 7, 11);
   DAL_DrawAspectsCard("ASPECTS", g.col3_x, g.row1_y, g.diag_w, row, 8);
   DAL_DrawHousesCard("HOUSES", g.col1_x, g.row2_y, g.card_w, row);
   DAL_DrawMetricsCard("METRICS", g.col2_x, g.row2_y, g.card_w, row);
   DAL_DrawDiagnosticsCard("DIAG", g.col3_x, g.row2_y, g.diag_w, 196, row, have_row, exact, fallback);
   DAL_DrawOrbStrip(g, row);
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
      DAL_DrawDiagnosticsCard("DIAG_ONLY", g.col1_x, g.row1_y, g.diag_w, 196, row, have_row, exact, fallback);
      ChartRedraw(ChartID());
      return;
   }

   if(g_view == ASTRO_RAW_OVERVIEW)
      DAL_DrawOverview(g, row, have_row, exact, fallback);
   else if(g_view == ASTRO_RAW_BODIES)
   {
      DAL_DrawBodiesCard("ALLB1", "ALL BODIES 1/2", g.col1_x, g.row1_y, g.card_w, row, 0, 6);
      DAL_DrawBodiesCard("ALLB2", "ALL BODIES 2/2", g.col2_x, g.row1_y, g.card_w, row, 7, 11);
      DAL_DrawDignityCard("DIGNITY", g.col1_x, g.row2_y, g.wide_w, row);
   }
   else if(g_view == ASTRO_RAW_ASPECTS)
      DAL_DrawAspectsCard("ALLASP", g.col1_x, g.row1_y, g.wide_w, row, 15);
   else if(g_view == ASTRO_RAW_HOUSES)
   {
      DAL_DrawHousesCard("HOUSES_BIG", g.col1_x, g.row1_y, g.card_w, row);
      DAL_DrawBodiesCard("HOUSE_BODIES", "BODY HOUSE PLACEMENT", g.col2_x, g.row1_y, g.card_w, row, 0, 11);
   }
   else if(g_view == ASTRO_RAW_METRICS)
   {
      DAL_DrawMetricsCard("METRICS_BIG", g.col1_x, g.row1_y, g.card_w, row);
      DAL_DrawDignityCard("DIGNITY_BIG", g.col2_x, g.row1_y, g.card_w, row);
   }

   if(InpUseTerminalComment)
      Comment("EXP0013 raw sky | ", exact ? "exact" : (fallback ? "fallback" : "no row"), " | ", row.summary);

   ChartRedraw(ChartID());
}

int OnInit()
{
   g_prefix = "DAL_EXP0013_RAW_ASTRO_" + IntegerToString((int)ChartID());
   g_view = InpInitialView;
   g_show_orb_strip = InpShowLowerOrbStrip;
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
   else if(sparam == g_prefix + "_BTN_STRIP") { g_show_orb_strip = !g_show_orb_strip; changed = true; }
   else if(sparam == g_prefix + "_BTN_MIN") { g_minimized = !g_minimized; changed = true; }
   else if(sparam == g_prefix + "_BTN_RELOAD") { DAL_LoadStore(); }
   if(changed) g_force_rebuild = true;
   DAL_Render();
}
