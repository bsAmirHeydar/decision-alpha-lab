#ifndef GARTAL_NEWS_DASHBOARD_MQH
#define GARTAL_NEWS_DASHBOARD_MQH

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
   ObjectSetInteger(0, name, OBJPROP_BACK, false);
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

void GT_RenderFatalStatus(GT_Config &config, GT_RuntimeState &runtime)
{
   string prefix = config.object_prefix + "FATAL_";
   GT_Rect(prefix + "BG", CORNER_RIGHT_UPPER, 20, 28, 440, 90, clrBlack, clrTomato);
   GT_Label(prefix + "TITLE", CORNER_RIGHT_UPPER, 36, 42, "gartal terminal | INIT FAILED", clrTomato, 11, "Segoe UI Semibold");
   GT_Label(prefix + "TEXT", CORNER_RIGHT_UPPER, 36, 66, runtime.last_error, clrWhite, 9);
}

void GT_RenderShell(GT_Config &config, GT_RuntimeState &runtime)
{
   if(!config.show_dashboard)
      return;

   string prefix = config.object_prefix + "SHELL_";
   GT_Rect(prefix + "BG", config.dashboard_corner, config.dashboard_x, config.dashboard_y, 460, 56, clrBlack, clrDimGray);
   GT_Label(prefix + "TITLE", config.dashboard_corner, config.dashboard_x + 16, config.dashboard_y + 12, "gartal terminal", clrWhite, 12, "Segoe UI Semibold");
   GT_Label(prefix + "SUB", config.dashboard_corner, config.dashboard_x + 16, config.dashboard_y + 34, "Stage 02 event model booting...", clrSilver, 8);
}

string GT_EventRowText(GT_NewsEvent &ev)
{
   string marker = ev.is_relevant ? "*" : " ";
   string special = "";
   if(ev.is_breaking) special = " BRK";
   else if(ev.is_speech) special = " SPC";
   else if(ev.is_holiday) special = " HOL";

   string t = TimeToString(ev.time_broker, TIME_MINUTES);
   return marker + " " + t + " " + ev.currency + " " + GT_ImpactDot(ev.impact) + " " + GT_EventStatusText(ev.status) + special + "  " + GT_CompactTitle(ev.title, 48);
}

void GT_RenderDashboard(GT_Config &config, GT_NewsStore &store, GT_FilterState &filters, GT_RuntimeState &runtime)
{
   if(!config.show_dashboard)
      return;

   string prefix = config.object_prefix + "DASH_";
   int corner = config.dashboard_corner;
   int x = config.dashboard_x;
   int y = config.dashboard_y;
   int width = 610;
   int height = 148 + config.dashboard_rows * 20;

   GT_Rect(prefix + "BG", corner, x, y, width, height, clrBlack, store.source_ok ? clrDimGray : clrTomato);

   string gmt = "GMT" + IntegerToString(config.broker_gmt_offset_hours);
   if(config.broker_gmt_offset_hours >= 0)
      gmt = "GMT+" + IntegerToString(config.broker_gmt_offset_hours);

   string title = "gartal terminal  |  " + store.source_status + "  |  " + gmt + "  |  Stage 02";
   GT_Label(prefix + "HEADER", corner, x + 16, y + 12, title, clrWhite, 11, "Segoe UI Semibold");

   string sub = "events=" + IntegerToString(store.count) +
                " | visible=" + IntegerToString(store.visible_count) +
                " | high=" + IntegerToString(store.high_count) +
                " | med=" + IntegerToString(store.medium_count) +
                " | low=" + IntegerToString(store.low_count) +
                " | speech=" + IntegerToString(store.speech_count) +
                " | breaking=" + IntegerToString(store.breaking_count);
   GT_Label(prefix + "SUB", corner, x + 16, y + 34, sub, clrSilver, 8);

   string lifecycle = "upcoming=" + IntegerToString(store.upcoming_count) +
                      " | active=" + IntegerToString(store.active_count) +
                      " | released=" + IntegerToString(store.released_count) +
                      " | expired=" + IntegerToString(store.expired_count) +
                      " | refresh=" + TimeToString(store.last_refresh, TIME_MINUTES) +
                      " | " + GT_RuntimeStatusText(runtime);
   GT_Label(prefix + "LIFE", corner, x + 16, y + 52, lifecycle, clrDarkGray, 8);

   int next = store.next_event_index;
   if(next >= 0)
   {
      GT_NewsEvent evn = store.events[next];
      string next_text = "NEXT  " + TimeToString(evn.time_broker, TIME_MINUTES) + "  " + evn.currency + "  " + GT_ImpactText(evn.impact) + "  " + evn.title + "  |  " + GT_FormatMinutesRemaining(evn.time_broker, TimeCurrent());
      GT_Label(prefix + "NEXT", corner, x + 16, y + 76, next_text, GT_ImpactColor(evn.impact), 9, "Segoe UI Semibold");
   }
   else
   {
      GT_Label(prefix + "NEXT", corner, x + 16, y + 76, "NEXT  no visible upcoming events", clrSilver, 9, "Segoe UI Semibold");
   }

   int next_high = store.next_high_index;
   if(next_high >= 0)
   {
      GT_NewsEvent hv = store.events[next_high];
      string high_text = "NEXT RED  " + TimeToString(hv.time_broker, TIME_MINUTES) + "  " + hv.currency + "  " + hv.title + "  |  " + GT_FormatMinutesRemaining(hv.time_broker, TimeCurrent());
      GT_Label(prefix + "NEXTHIGH", corner, x + 16, y + 96, high_text, clrTomato, 8, "Segoe UI Semibold");
   }
   else
      GT_Label(prefix + "NEXTHIGH", corner, x + 16, y + 96, "NEXT RED  no visible red event", clrDarkGray, 8, "Segoe UI");

   GT_Label(prefix + "COLS", corner, x + 16, y + 122, "  TIME CCY IMP STATUS       EVENT", clrDarkGray, 8, "Consolas");

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
         row_color = clrWhite;
      if(ev.is_breaking)
         row_color = clrTomato;

      GT_Label(prefix + "ROW_" + IntegerToString(row), corner, x + 16, y + 142 + row*20, GT_EventRowText(ev), row_color, 8, "Consolas");
      row++;
   }

   while(row < config.dashboard_rows)
   {
      GT_Label(prefix + "ROW_" + IntegerToString(row), corner, x + 16, y + 142 + row*20, "", clrDarkGray, 8, "Consolas");
      row++;
   }
}

bool GT_HandleDashboardClick(string object_name, GT_FilterState &filters, GT_Config &config, GT_RuntimeState &runtime)
{
   // Stage 02 keeps runtime toggle wiring reserved. Stage 06 will mutate filters here.
   return false;
}

void GT_UpdateCountdowns(GT_Config &config, GT_NewsStore &store, GT_FilterState &filters, GT_RuntimeState &runtime)
{
   if(!config.show_dashboard)
      return;

   // Full countdown-only repaint is deferred until dashboard component IDs become
   // interactive in Stage 06. Stage 02 recalculates next indices on each timer.
}

#endif
