#ifndef GARTAL_NEWS_DASHBOARD_MQH
#define GARTAL_NEWS_DASHBOARD_MQH

//+------------------------------------------------------------------+
//| Stage 06 Dashboard Doctrine                                      |
//| This module renders the terminal surface and forwards object-click |
//| events to the runtime filter engine. The store remains read-only.  |
//+------------------------------------------------------------------+

void GT_ClearObjects(string prefix)
{
   int total = ObjectsTotal(0, 0, -1);
   for(int i=total-1; i>=0; i--)
   {
      string name = ObjectName(0, i, 0, -1);
      if(StringFind(name, prefix) == 0)
         ObjectDelete(0, name);
   }
}

void GT_SetCommonObjectProps(string name)
{
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
   ObjectSetInteger(0, name, OBJPROP_BACK, false);
}

void GT_Rect(string name, int corner, int x, int y, int width, int height, color bg, color border)
{
   if(ObjectFind(0, name) < 0)
      ObjectCreate(0, name, OBJ_RECTANGLE_LABEL, 0, 0, 0);

   ObjectSetInteger(0, name, OBJPROP_CORNER, corner);
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(0, name, OBJPROP_XSIZE, width);
   ObjectSetInteger(0, name, OBJPROP_YSIZE, height);
   ObjectSetInteger(0, name, OBJPROP_BGCOLOR, bg);
   ObjectSetInteger(0, name, OBJPROP_COLOR, border);
   ObjectSetInteger(0, name, OBJPROP_BORDER_TYPE, BORDER_FLAT);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, 1);
   GT_SetCommonObjectProps(name);
}

void GT_Label(string name, int corner, int x, int y, string text, color clr, int font_size=9, string font="Segoe UI")
{
   if(ObjectFind(0, name) < 0)
      ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0);

   ObjectSetInteger(0, name, OBJPROP_CORNER, corner);
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, font_size);
   ObjectSetString(0, name, OBJPROP_FONT, font);
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   GT_SetCommonObjectProps(name);
}

void GT_DashThinLine(string name, int corner, int x, int y, int width, color clr)
{
   GT_Rect(name, corner, x, y, width, 1, clr, clr);
}

void GT_DashBadge(string name, int corner, int x, int y, int width, string text, color bg, color border, color fg)
{
   GT_Rect(name + "_BG", corner, x, y, width, 20, bg, border);
   GT_Label(name + "_TXT", corner, x + 8, y + 4, text, fg, 8, "Segoe UI Semibold");
}

void GT_DashFilterButton(string name, int corner, int x, int y, int width, string text, bool active, color active_color, GT_Config &config, string tooltip)
{
   color border = active ? active_color : clrDimGray;
   color fg = active ? active_color : clrDimGray;
   color bg = clrBlack;

   GT_Rect(name + "_BG", corner, x, y, width, GT_FILTER_BUTTON_HEIGHT, bg, border);
   GT_Label(name + "_TXT", corner, x + 8, y + 4, text, fg, 8, "Segoe UI Semibold");
   ObjectSetString(0, name + "_BG", OBJPROP_TOOLTIP, tooltip);
   ObjectSetString(0, name + "_TXT", OBJPROP_TOOLTIP, tooltip);
}


void GT_DashMetric(string name, int corner, int x, int y, int width, string label, string value, color value_color, GT_Config &config)
{
   GT_Rect(name + "_BG", corner, x, y, width, 38, GT_DashPanel(config), GT_DashBorder(config));
   GT_Label(name + "_LBL", corner, x + 10, y + 6, label, GT_DashMuted(config), 7, "Segoe UI");
   GT_Label(name + "_VAL", corner, x + 10, y + 20, value, value_color, 10, "Segoe UI Semibold");
}

void GT_DashProgressBar(string name, int corner, int x, int y, int width, int percent, color fill, GT_Config &config)
{
   int p = GT_ClampInt(percent, 0, 100);
   int fill_width = (width * p) / 100;
   GT_Rect(name + "_BG", corner, x, y, width, 4, clrDarkSlateGray, clrDarkSlateGray);
   if(fill_width > 0)
      GT_Rect(name + "_FILL", corner, x, y, fill_width, 4, fill, fill);
}

void GT_RenderFatalStatus(GT_Config &config, GT_RuntimeState &runtime)
{
   string prefix = config.object_prefix + "FATAL_";
   GT_Rect(prefix + "BG", CORNER_RIGHT_UPPER, 20, 28, 500, 96, clrBlack, clrTomato);
   GT_Label(prefix + "TITLE", CORNER_RIGHT_UPPER, 36, 42, "gartal terminal | INIT FAILED", clrTomato, 12, "Segoe UI Semibold");
   GT_Label(prefix + "TEXT", CORNER_RIGHT_UPPER, 36, 70, runtime.last_error, clrWhite, 9);
   GT_Label(prefix + "SUB", CORNER_RIGHT_UPPER, 36, 92, "Stage 05 startup guard blocked the product surface.", clrSilver, 8);
}

void GT_RenderShell(GT_Config &config, GT_RuntimeState &runtime)
{
   if(!config.show_dashboard)
      return;

   string prefix = config.object_prefix + "SHELL_";
   int width = config.dashboard_width;
   GT_Rect(prefix + "BG", config.dashboard_corner, config.dashboard_x, config.dashboard_y, width, 76, GT_DashBg(config), GT_DashBorder(config));
   GT_Label(prefix + "TITLE", config.dashboard_corner, config.dashboard_x + 16, config.dashboard_y + 12, "gartal terminal", GT_DashText(config), 13, "Segoe UI Semibold");
   GT_Label(prefix + "SUB", config.dashboard_corner, config.dashboard_x + 16, config.dashboard_y + 36, "Stage 05 luxury dashboard UI renderer booting...", GT_DashMuted(config), 8);
   GT_Label(prefix + "TIME", config.dashboard_corner, config.dashboard_x + 16, config.dashboard_y + 54, runtime.time_summary, clrDarkGray, 8, "Consolas");
}

string GT_EventRowText(GT_NewsEvent &ev)
{
   return GT_DashboardTableRow(ev);
}

void GT_RenderDashboardHeader(string prefix, int corner, int x, int y, int width, GT_Config &config, GT_NewsStore &store, GT_RuntimeState &runtime)
{
   if(!config.dashboard_show_header)
      return;

   color health = GT_DashboardHealthColor(store, runtime);
   string title = "gartal terminal";
   string subtitle = "macro news terminal  |  " + GT_DataModeText(config.data_mode) + "  |  " + GT_DashboardModeText(config.dashboard_mode) + "  |  Stage 05";

   GT_Label(prefix + "BRAND", corner, x + 16, y + 12, title, GT_DashText(config), 14, "Segoe UI Semibold");
   GT_Label(prefix + "SUBTITLE", corner, x + 16, y + 36, subtitle, GT_DashMuted(config), 8, "Segoe UI");
   GT_DashBadge(prefix + "HEALTH", corner, x + width - 118, y + 16, 96, GT_DashboardHealthText(store, runtime), clrBlack, health, health);
   GT_DashThinLine(prefix + "SEP_HEADER", corner, x + 14, y + 58, width - 28, GT_DashBorder(config));
}

void GT_RenderDashboardHealthBar(string prefix, int corner, int x, int y, int width, GT_Config &config, GT_NewsStore &store, GT_RuntimeState &runtime)
{
   if(!config.dashboard_show_health_bar)
      return;

   string left = "source=" + store.source_status + " | refresh=" + TimeToString(store.last_refresh, TIME_MINUTES) + " | attempts=" + IntegerToString(runtime.refresh_attempts);
   string right = "broker=" + GT_FormatGmtOffsetSeconds(config.broker_gmt_offset_seconds) + " | detected=" + GT_FormatGmtOffsetSeconds(runtime.broker_gmt_detected_seconds) + " | confidence=" + IntegerToString(runtime.broker_gmt_confidence);
   GT_Label(prefix + "HEALTH_LEFT", corner, x + 16, y, left, GT_DashMuted(config), 8, "Consolas");
   GT_Label(prefix + "HEALTH_RIGHT", corner, x + 16, y + 14, right, clrDarkGray, 8, "Consolas");
}

void GT_RenderDashboardNextCard(string prefix, int corner, int x, int y, int width, GT_Config &config, GT_NewsStore &store)
{
   if(!config.dashboard_show_next_card)
      return;

   int next = store.next_event_index;
   GT_Rect(prefix + "NEXT_CARD", corner, x + 14, y, width - 28, 64, GT_DashPanel(config), GT_DashSoftBorder(config));

   if(next < 0)
   {
      GT_Label(prefix + "NEXT_LABEL", corner, x + 28, y + 10, "NEXT EVENT", GT_DashMuted(config), 8, "Segoe UI Semibold");
      GT_Label(prefix + "NEXT_TITLE", corner, x + 28, y + 30, "No visible upcoming event in the selected window", GT_DashText(config), 10, "Segoe UI Semibold");
      return;
   }

   GT_NewsEvent ev = store.events[next];
   color accent = ev.is_breaking ? clrRed : GT_ImpactColor(ev.impact);
   string countdown = GT_DashboardCountdown(ev.time_broker);

   GT_Rect(prefix + "NEXT_STRIPE", corner, x + 14, y, 5, 64, accent, accent);
   GT_Label(prefix + "NEXT_LABEL", corner, x + 28, y + 8, "NEXT EVENT", GT_DashMuted(config), 8, "Segoe UI Semibold");
   GT_Label(prefix + "NEXT_TIME", corner, x + width - 158, y + 8, TimeToString(ev.time_broker, TIME_MINUTES) + "  |  " + countdown, accent, 9, "Consolas");
   GT_Label(prefix + "NEXT_TITLE", corner, x + 28, y + 28, ev.currency + "  " + GT_ImpactText(ev.impact) + "  " + GT_DashboardEventTitle(ev, 58), GT_DashText(config), 10, "Segoe UI Semibold");

   string nums = "actual=" + (GT_IsEmpty(ev.actual) ? "-" : ev.actual) + " | forecast=" + (GT_IsEmpty(ev.forecast) ? "-" : ev.forecast) + " | previous=" + (GT_IsEmpty(ev.previous) ? "-" : ev.previous);
   GT_Label(prefix + "NEXT_NUMS", corner, x + 28, y + 48, nums, GT_DashMuted(config), 8, "Consolas");
}

void GT_RenderDashboardHighCard(string prefix, int corner, int x, int y, int width, GT_Config &config, GT_NewsStore &store)
{
   if(!config.dashboard_show_high_card || config.dashboard_mode != GT_DASHBOARD_MODE_PRO)
      return;

   int idx = store.next_high_index;
   GT_Rect(prefix + "HIGH_CARD", corner, x + 14, y, width - 28, 40, clrBlack, clrTomato);
   GT_Label(prefix + "HIGH_LABEL", corner, x + 28, y + 8, "NEXT RED", clrTomato, 8, "Segoe UI Semibold");

   if(idx < 0)
   {
      GT_Label(prefix + "HIGH_TEXT", corner, x + 112, y + 8, "No visible high-impact event", clrDarkGray, 8, "Segoe UI");
      return;
   }

   GT_NewsEvent ev = store.events[idx];
   string text = TimeToString(ev.time_broker, TIME_MINUTES) + "  " + ev.currency + "  " + GT_DashboardCountdown(ev.time_broker) + "  |  " + GT_DashboardEventTitle(ev, 54);
   GT_Label(prefix + "HIGH_TEXT", corner, x + 112, y + 8, text, clrWhite, 8, "Segoe UI Semibold");
   GT_DashProgressBar(prefix + "HIGH_BAR", corner, x + 112, y + 30, width - 160, 100, clrTomato, config);
}

void GT_RenderDashboardMetrics(string prefix, int corner, int x, int y, int width, GT_Config &config, GT_NewsStore &store)
{
   if(!config.dashboard_show_metrics)
      return;

   int gap = 8;
   int card_w = (width - 28 - gap * 5) / 6;
   int start_x = x + 14;

   GT_DashMetric(prefix + "M_HIGH", corner, start_x + (card_w + gap) * 0, y, card_w, "RED", IntegerToString(store.high_count), clrTomato, config);
   GT_DashMetric(prefix + "M_MED",  corner, start_x + (card_w + gap) * 1, y, card_w, "ORANGE", IntegerToString(store.medium_count), clrOrange, config);
   GT_DashMetric(prefix + "M_LOW",  corner, start_x + (card_w + gap) * 2, y, card_w, "YELLOW", IntegerToString(store.low_count), clrGold, config);
   GT_DashMetric(prefix + "M_SPC",  corner, start_x + (card_w + gap) * 3, y, card_w, "SPEECH", IntegerToString(store.speech_count), clrDeepSkyBlue, config);
   GT_DashMetric(prefix + "M_BRK",  corner, start_x + (card_w + gap) * 4, y, card_w, "BREAK", IntegerToString(store.breaking_count), clrRed, config);
   GT_DashMetric(prefix + "M_VIS",  corner, start_x + (card_w + gap) * 5, y, card_w, "VISIBLE", IntegerToString(store.visible_count), GT_DashText(config), config);
}

void GT_RenderDashboardFilterBar(string prefix, int corner, int x, int y, int width, GT_Config &config, GT_FilterState &filters)
{
   if(!config.dashboard_show_filter_bar)
      return;

   string tooltip = GT_FilterTooltip(filters);
   GT_Label(prefix + "FILTER_TITLE", corner, x + 16, y, "LIVE FILTERS", GT_DashMuted(config), 8, "Segoe UI Semibold");
   GT_Label(prefix + "FILTER_STATUS", corner, x + width - 258, y, "clickable=" + GT_BoolText(config.dashboard_enable_click_filters) + " | dashboard runtime controls", clrDarkGray, 8, "Consolas");

   int bx = x + 16;
   int by = y + 16;
   GT_DashFilterButton(prefix + "FLT_HIGH",   corner, bx, by, 76, GT_FilterButtonText("RED", filters.show_high), filters.show_high, clrTomato, config, tooltip); bx += 82;
   GT_DashFilterButton(prefix + "FLT_MEDIUM", corner, bx, by, 86, GT_FilterButtonText("ORANGE", filters.show_medium), filters.show_medium, clrOrange, config, tooltip); bx += 92;
   GT_DashFilterButton(prefix + "FLT_LOW",    corner, bx, by, 86, GT_FilterButtonText("YELLOW", filters.show_low), filters.show_low, clrGold, config, tooltip); bx += 92;
   GT_DashFilterButton(prefix + "FLT_HOLIDAY",corner, bx, by, 86, GT_FilterButtonText("HOL", filters.show_holiday), filters.show_holiday, clrSilver, config, tooltip); bx += 92;
   GT_DashFilterButton(prefix + "FLT_SPEECH", corner, bx, by, 88, GT_FilterButtonText("SPEECH", filters.show_speech), filters.show_speech, clrDeepSkyBlue, config, tooltip); bx += 94;
   GT_DashFilterButton(prefix + "FLT_BREAKING", corner, bx, by, 88, GT_FilterButtonText("BREAK", filters.show_breaking), filters.show_breaking, clrRed, config, tooltip);

   by += 26;
   bx = x + 16;
   GT_DashFilterButton(prefix + "FLT_TENTATIVE", corner, bx, by, 94, GT_FilterButtonText("TENT", filters.show_tentative), filters.show_tentative, clrMediumPurple, config, tooltip); bx += 100;
   GT_DashFilterButton(prefix + "FLT_PAST", corner, bx, by, 94, GT_FilterButtonText("PAST", filters.show_past_events), filters.show_past_events, clrLightSlateGray, config, tooltip); bx += 100;
   GT_DashFilterButton(prefix + "FLT_SYMBOL", corner, bx, by, 116, GT_FilterButtonText("SYMBOL", filters.only_symbol), filters.only_symbol, GT_DashAccent(config), config, tooltip);
   GT_Label(prefix + "FILTER_SUMMARY", corner, bx + 126, by + 4, GT_CompactTitle(GT_FilterSummary(filters), 70), clrDarkGray, 8, "Consolas");

   if(config.dashboard_show_currency_buttons)
   {
      by += 28;
      bx = x + 16;
      string ccy[9] = {"USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "NZD", "CNY"};
      for(int i=0; i<9; i++)
      {
         bool active = GT_CsvContains(filters.currencies_csv, ccy[i]);
         color c = active ? GT_DashAccent(config) : clrDimGray;
         GT_DashFilterButton(prefix + "FLT_CCY_" + ccy[i], corner, bx, by, 58, ccy[i], active, c, config, tooltip);
         bx += 64;
      }
   }

   if(config.dashboard_show_filter_utilities)
   {
      by += 28;
      bx = x + 16;
      GT_DashFilterButton(prefix + "FLT_RED_ONLY", corner, bx, by, 90, "RED ONLY", true, clrTomato, config, tooltip); bx += 96;
      GT_DashFilterButton(prefix + "FLT_ALL_IMPACT", corner, bx, by, 94, "ALL IMP", true, clrSilver, config, tooltip); bx += 100;
      GT_DashFilterButton(prefix + "FLT_MAJOR_CCY", corner, bx, by, 104, "ALL CCY", true, GT_DashAccent(config), config, tooltip); bx += 110;
      GT_DashFilterButton(prefix + "FLT_RESET", corner, bx, by, 82, "RESET", true, clrMediumSeaGreen, config, tooltip);
   }
}


void GT_RenderDashboardMiniTape(string prefix, int corner, int x, int y, int width, GT_Config &config, GT_NewsStore &store, GT_FilterState &filters)
{
   if(!config.dashboard_show_mini_tape)
      return;

   GT_Rect(prefix + "MINITAPE_BG", corner, x + 14, y, width - 28, 34, clrBlack, GT_DashBorder(config));
   string tape = "";
   int shown = 0;
   datetime now = TimeCurrent();
   for(int i=0; i<store.count && shown<6; i++)
   {
      GT_NewsEvent ev = store.events[i];
      if(ev.time_broker < now)
         continue;
      if(!GT_EventPassesFilters(ev, filters))
         continue;

      if(shown > 0)
         tape += "   |   ";
      tape += TimeToString(ev.time_broker, TIME_MINUTES) + " " + ev.currency + " " + GT_ImpactDot(ev.impact) + " " + GT_CompactTitle(ev.title, 16);
      shown++;
   }

   if(shown == 0)
      tape = "no upcoming visible events";

   GT_Label(prefix + "MINITAPE_TITLE", corner, x + 28, y + 4, "TODAY TAPE", GT_DashMuted(config), 7, "Segoe UI Semibold");
   GT_Label(prefix + "MINITAPE_TEXT", corner, x + 28, y + 18, tape, GT_DashText(config), 8, "Consolas");
}

void GT_RenderDashboardTable(string prefix, int corner, int x, int y, int width, GT_Config &config, GT_NewsStore &store, GT_FilterState &filters)
{
   if(!config.dashboard_show_event_table)
      return;

   GT_Label(prefix + "COLS", corner, x + 16, y, GT_DashboardTableHeader(), clrDarkGray, 8, "Consolas");
   int row_y = y + 20;
   int row = 0;

   for(int i=0; i<store.count && row<config.dashboard_rows; i++)
   {
      GT_NewsEvent ev = store.events[i];
      if(!GT_EventPassesFilters(ev, filters))
         continue;

      color row_color = GT_ImpactColor(ev.impact);
      if(ev.status == GT_EVENT_EXPIRED || ev.status == GT_EVENT_RELEASED)
         row_color = clrDarkGray;
      if(ev.status == GT_EVENT_ACTIVE)
         row_color = GT_DashText(config);
      if(ev.is_breaking)
         row_color = clrRed;

      if(row % 2 == 0)
         GT_Rect(prefix + "ROW_BG_" + IntegerToString(row), corner, x + 14, row_y + row * config.dashboard_row_height - 2, width - 28, config.dashboard_row_height, clrBlack, clrBlack);

      GT_Label(prefix + "ROW_" + IntegerToString(row), corner, x + 16, row_y + row * config.dashboard_row_height, GT_DashboardTableRow(ev), row_color, 8, "Consolas");
      row++;
   }

   while(row < config.dashboard_rows)
   {
      GT_Label(prefix + "ROW_" + IntegerToString(row), corner, x + 16, row_y + row * config.dashboard_row_height, "", clrDarkGray, 8, "Consolas");
      row++;
   }
}

void GT_RenderDashboardDebug(string prefix, int corner, int x, int y, int width, GT_Config &config, GT_NewsStore &store, GT_RuntimeState &runtime)
{
   if(!config.show_time_debug && !config.show_timeline_debug)
      return;

   string dbg = "window=" + GT_FormatDateWindow(store.window_from_broker, store.window_to_broker) +
                " | tl=" + runtime.timeline_last_render_summary +
                " | dash=" + runtime.dashboard_last_render_summary +
                " | filters=" + IntegerToString(runtime.filter_change_count) +
                " | last=" + runtime.filter_last_action;
   GT_Label(prefix + "DEBUG", corner, x + 16, y, GT_CompactTitle(dbg, 128), clrDarkSlateGray, 8, "Consolas");
}

void GT_RenderDashboard(GT_Config &config, GT_NewsStore &store, GT_FilterState &filters, GT_RuntimeState &runtime)
{
   if(!config.show_dashboard)
      return;

   string prefix = config.object_prefix + "DASH_";
   int corner = config.dashboard_corner;
   int x = config.dashboard_x;
   int y = config.dashboard_y;
   int width = config.dashboard_width;
   int height = GT_DashboardHeight(config);
   int cursor = y;

   runtime.dashboard_last_objects = 0;
   runtime.dashboard_last_rows = 0;
   runtime.dashboard_last_cards = 0;
   runtime.dashboard_last_render_at = TimeCurrent();

   GT_Rect(prefix + "BG", corner, x, y, width, height, GT_DashBg(config), store.source_ok ? GT_DashBorder(config) : clrTomato);
   runtime.dashboard_last_objects++;

   if(config.dashboard_show_header)
   {
      GT_RenderDashboardHeader(prefix, corner, x, cursor, width, config, store, runtime);
      cursor += 66;
      runtime.dashboard_last_cards++;
   }

   if(config.dashboard_show_health_bar)
   {
      GT_RenderDashboardHealthBar(prefix, corner, x, cursor, width, config, store, runtime);
      cursor += 30;
      runtime.dashboard_last_cards++;
   }

   if(config.dashboard_show_next_card)
   {
      GT_RenderDashboardNextCard(prefix, corner, x, cursor, width, config, store);
      cursor += 72;
      runtime.dashboard_last_cards++;
   }

   if(config.dashboard_show_high_card && config.dashboard_mode == GT_DASHBOARD_MODE_PRO)
   {
      GT_RenderDashboardHighCard(prefix, corner, x, cursor, width, config, store);
      cursor += 48;
      runtime.dashboard_last_cards++;
   }

   if(config.dashboard_show_metrics)
   {
      GT_RenderDashboardMetrics(prefix, corner, x, cursor, width, config, store);
      cursor += 48;
      runtime.dashboard_last_cards += 6;
   }

   if(config.dashboard_show_filter_bar)
   {
      GT_RenderDashboardFilterBar(prefix, corner, x, cursor + 4, width, config, filters);
      int filter_height = 48;
      if(config.dashboard_show_currency_buttons) filter_height += 28;
      if(config.dashboard_show_filter_utilities) filter_height += 28;
      cursor += filter_height;
      runtime.dashboard_last_cards++;
   }

   if(config.dashboard_show_mini_tape)
   {
      GT_RenderDashboardMiniTape(prefix, corner, x, cursor, width, config, store, filters);
      cursor += 42;
      runtime.dashboard_last_cards++;
   }

   if(config.dashboard_show_event_table)
   {
      GT_RenderDashboardTable(prefix, corner, x, cursor, width, config, store, filters);
      cursor += 28 + config.dashboard_rows * config.dashboard_row_height;
      runtime.dashboard_last_rows = config.dashboard_rows;
   }

   if(config.show_time_debug || config.show_timeline_debug)
      GT_RenderDashboardDebug(prefix, corner, x, cursor, width, config, store, runtime);

   runtime.dashboard_last_render_summary = "mode=" + GT_DashboardModeText(config.dashboard_mode) +
                                           " width=" + IntegerToString(width) +
                                           " height=" + IntegerToString(height) +
                                           " cards=" + IntegerToString(runtime.dashboard_last_cards) +
                                           " rows=" + IntegerToString(runtime.dashboard_last_rows) +
                                           " filters=" + IntegerToString(runtime.filter_change_count);
}

bool GT_HandleDashboardClick(string object_name, GT_FilterState &filters, GT_Config &config, GT_RuntimeState &runtime)
{
   if(StringFind(object_name, config.object_prefix + "DASH_") != 0)
      return false;

   return GT_HandleRuntimeFilterClick(object_name, filters, config, runtime);
}

void GT_UpdateCountdowns(GT_Config &config, GT_NewsStore &store, GT_FilterState &filters, GT_RuntimeState &runtime)
{
   if(!config.show_dashboard)
      return;

   // Stage 05 keeps countdowns live by repainting the dashboard surface on timer.
   // This is intentionally limited to dashboard objects; the chart timeline is
   // still refreshed only by GT_RedrawAll or calendar refresh.
   GT_RenderDashboard(config, store, filters, runtime);
}

#endif
