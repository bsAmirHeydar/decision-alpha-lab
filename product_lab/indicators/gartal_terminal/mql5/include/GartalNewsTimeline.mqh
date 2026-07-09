#ifndef GARTAL_NEWS_TIMELINE_MQH
#define GARTAL_NEWS_TIMELINE_MQH

void GT_RenderVerticalLines(GT_Config &config, GT_NewsStore &store, GT_FilterState &filters, GT_RuntimeState &runtime)
{
   if(!config.show_vertical_lines)
      return;

   for(int i=0; i<store.count; i++)
   {
      GT_NewsEvent ev = store.events[i];
      if(!GT_EventPassesFilters(ev, filters))
         continue;

      string name = GT_SafeObjectName(config.object_prefix, "VLINE_" + ev.id);
      if(ObjectFind(0, name) < 0)
         ObjectCreate(0, name, OBJ_VLINE, 0, ev.time_broker, 0);

      ObjectSetInteger(0, name, OBJPROP_TIME, ev.time_broker);
      ObjectSetInteger(0, name, OBJPROP_COLOR, GT_ImpactColor(ev.impact));
      ObjectSetInteger(0, name, OBJPROP_STYLE, ev.impact == GT_IMPACT_HIGH ? STYLE_SOLID : STYLE_DASH);
      ObjectSetInteger(0, name, OBJPROP_WIDTH, ev.impact == GT_IMPACT_HIGH ? 2 : 1);
      ObjectSetInteger(0, name, OBJPROP_BACK, true);
      ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
      ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
      ObjectSetString(0, name, OBJPROP_TEXT, ev.currency + " " + GT_ImpactText(ev.impact) + " " + ev.title);
   }
}

void GT_RenderTimeline(GT_Config &config, GT_NewsStore &store, GT_FilterState &filters, GT_RuntimeState &runtime)
{
   if(!config.show_timeline)
      return;

   string prefix = config.object_prefix + "TIMELINE_";
   int upcoming = 0;
   int high = 0;
   datetime now = TimeCurrent();

   for(int i=0; i<store.count; i++)
   {
      if(store.events[i].time_broker >= now && GT_EventPassesFilters(store.events[i], filters))
      {
         upcoming++;
         if(store.events[i].impact == GT_IMPACT_HIGH)
            high++;
      }
   }

   GT_Rect(prefix + "BG", CORNER_LEFT_LOWER, 18, 22, 520, 34, clrBlack, clrDimGray);
   string text = "gartal timeline | upcoming=" + IntegerToString(upcoming) + " | high=" + IntegerToString(high) + " | stage 01 object model active";
   GT_Label(prefix + "INFO", CORNER_LEFT_LOWER, 32, 36, text, clrWhite, 8, "Segoe UI");
}

#endif
