#ifndef GARTAL_NEWS_TIMELINE_MQH
#define GARTAL_NEWS_TIMELINE_MQH

void GT_RenderVerticalLines(GT_Config &config, GT_NewsStore &store, GT_FilterState &filters)
{
   if(!config.show_vertical_lines)
      return;

   for(int i=0; i<store.count; i++)
   {
      GT_NewsEvent ev = store.events[i];
      if(!GT_EventPassesFilters(ev, filters))
         continue;

      string name = config.object_prefix + "VLINE_" + IntegerToString(i);
      if(ObjectFind(0, name) < 0)
         ObjectCreate(0, name, OBJ_VLINE, 0, ev.time_broker, 0);

      ObjectSetInteger(0, name, OBJPROP_TIME, ev.time_broker);
      ObjectSetInteger(0, name, OBJPROP_COLOR, GT_ImpactColor(ev.impact));
      ObjectSetInteger(0, name, OBJPROP_STYLE, ev.impact == GT_IMPACT_HIGH ? STYLE_SOLID : STYLE_DASH);
      ObjectSetInteger(0, name, OBJPROP_WIDTH, ev.impact == GT_IMPACT_HIGH ? 2 : 1);
      ObjectSetString(0, name, OBJPROP_TEXT, ev.currency + " " + GT_ImpactText(ev.impact) + " " + ev.title);
   }
}

void GT_RenderTimeline(GT_Config &config, GT_NewsStore &store, GT_FilterState &filters)
{
   if(!config.show_timeline)
      return;

   // Scaffold: production version maps event time to screen-space x positions.
   string name = config.object_prefix + "TIMELINE_INFO";
   int upcoming = 0;
   datetime now = TimeCurrent();

   for(int i=0; i<store.count; i++)
      if(store.events[i].time_broker >= now && GT_EventPassesFilters(store.events[i], filters))
         upcoming++;

   if(ObjectFind(0, name) < 0)
      ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0);

   ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_LEFT_LOWER);
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, 20);
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, 28);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clrWhite);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 9);
   ObjectSetString(0, name, OBJPROP_FONT, "Segoe UI");
   ObjectSetString(0, name, OBJPROP_TEXT, "gartal timeline | upcoming today: " + IntegerToString(upcoming));
}

#endif
