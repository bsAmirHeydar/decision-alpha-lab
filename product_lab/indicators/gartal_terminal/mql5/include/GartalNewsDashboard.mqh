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

int GT_NextEventIndex(GT_NewsStore &store, GT_FilterState &filters)
{
   datetime now = TimeCurrent();
   for(int i=0; i<store.count; i++)
   {
      if(store.events[i].time_broker >= now && GT_EventPassesFilters(store.events[i], filters))
         return i;
   }
   return -1;
}

int GT_FilteredEventCount(GT_NewsStore &store, GT_FilterState &filters)
{
   int count = 0;
   for(int i=0; i<store.count; i++)
      if(GT_EventPassesFilters(store.events[i], filters))
         count++;
   return count;
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
   GT_Label(prefix + "SUB", config.dashboard_corner, config.dashboard_x + 16, config.dashboard_y + 34, "Stage 01 core skeleton booting...", clrSilver, 8);
}

void GT_RenderDashboard(GT_Config &config, GT_NewsStore &store, GT_FilterState &filters, GT_RuntimeState &runtime)
{
   if(!config.show_dashboard)
      return;

   string prefix = config.object_prefix + "DASH_";
   int corner = config.dashboard_corner;
   int x = config.dashboard_x;
   int y = config.dashboard_y;
   int width = 520;
   int height = 118 + config.dashboard_rows * 20;

   GT_Rect(prefix + "BG", corner, x, y, width, height, clrBlack, store.source_ok ? clrDimGray : clrTomato);

   string gmt = "GMT" + IntegerToString(config.broker_gmt_offset_hours);
   if(config.broker_gmt_offset_hours >= 0)
      gmt = "GMT+" + IntegerToString(config.broker_gmt_offset_hours);

   string title = "gartal terminal  |  " + store.source_status + "  |  " + gmt;
   GT_Label(prefix + "HEADER", corner, x + 16, y + 12, title, clrWhite, 11, "Segoe UI Semibold");

   string sub = "events=" + IntegerToString(store.count) +
                " | visible=" + IntegerToString(GT_FilteredEventCount(store, filters)) +
                " | refresh=" + TimeToString(store.last_refresh, TIME_MINUTES) +
                " | " + GT_RuntimeStatusText(runtime);
   GT_Label(prefix + "SUB", corner, x + 16, y + 34, sub, clrSilver, 8);

   int next = GT_NextEventIndex(store, filters);
   if(next >= 0)
   {
      GT_NewsEvent evn = store.events[next];
      string next_text = "NEXT  " + TimeToString(evn.time_broker, TIME_MINUTES) + "  " + evn.currency + "  " + GT_ImpactText(evn.impact) + "  " + evn.title + "  |  " + GT_FormatMinutesRemaining(evn.time_broker, TimeCurrent());
      GT_Label(prefix + "NEXT", corner, x + 16, y + 58, next_text, GT_ImpactColor(evn.impact), 9, "Segoe UI Semibold");
   }
   else
   {
      GT_Label(prefix + "NEXT", corner, x + 16, y + 58, "NEXT  no visible upcoming events", clrSilver, 9, "Segoe UI Semibold");
   }

   GT_Label(prefix + "COLS", corner, x + 16, y + 84, "TIME      CCY   IMP   EVENT", clrDarkGray, 8, "Consolas");

   int row = 0;
   for(int i=0; i<store.count && row<config.dashboard_rows; i++)
   {
      GT_NewsEvent ev = store.events[i];
      if(!GT_EventPassesFilters(ev, filters))
         continue;

      string marker = ev.is_relevant ? "*" : " ";
      string t = TimeToString(ev.time_broker, TIME_MINUTES);
      string text = marker + " " + t + "   " + ev.currency + "   " + GT_ImpactText(ev.impact) + "   " + ev.title;
      color row_color = GT_ImpactColor(ev.impact);
      if(ev.status == GT_EVENT_EXPIRED)
         row_color = clrDarkGray;

      GT_Label(prefix + "ROW_" + IntegerToString(row), corner, x + 16, y + 104 + row*20, text, row_color, 8, "Consolas");
      row++;
   }

   while(row < config.dashboard_rows)
   {
      GT_Label(prefix + "ROW_" + IntegerToString(row), corner, x + 16, y + 104 + row*20, "", clrDarkGray, 8, "Consolas");
      row++;
   }
}

bool GT_HandleDashboardClick(string object_name, GT_FilterState &filters, GT_Config &config, GT_RuntimeState &runtime)
{
   // Stage 01: object-click pipeline is wired but no runtime toggle is activated yet.
   // Stage 06 will map button names to filter mutations.
   return false;
}

void GT_UpdateCountdowns(GT_Config &config, GT_NewsStore &store, GT_FilterState &filters, GT_RuntimeState &runtime)
{
   if(!config.show_dashboard)
      return;

   // Stage 01 keeps this intentionally light. The full countdown-only refresh
   // will be introduced after the dashboard component tree is finalized.
}

#endif
