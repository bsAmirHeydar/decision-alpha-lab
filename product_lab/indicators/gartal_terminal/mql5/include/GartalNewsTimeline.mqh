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
      ObjectSetString(0, name, OBJPROP_TEXT, ev.currency + " " + GT_ImpactText(ev.impact) + " " + GT_EventKindText(ev.kind) + " " + ev.title);
   }
}

void GT_RenderTimeline(GT_Config &config, GT_NewsStore &store, GT_FilterState &filters, GT_RuntimeState &runtime)
{
   if(!config.show_timeline)
      return;

   string prefix = config.object_prefix + "TIMELINE_";
   int width = 760;
   GT_Rect(prefix + "BG", CORNER_LEFT_LOWER, 18, 22, width, 54, clrBlack, clrDimGray);

   string text = "gartal timeline | visible=" + IntegerToString(store.visible_count) +
                 " | next=" + (store.next_event_index >= 0 ? TimeToString(store.events[store.next_event_index].time_broker, TIME_MINUTES) : "none") +
                 " | red=" + IntegerToString(store.high_count) +
                 " | stage 02 event store active";
   GT_Label(prefix + "INFO", CORNER_LEFT_LOWER, 32, 34, text, clrWhite, 8, "Segoe UI");

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
      tape += TimeToString(ev.time_broker, TIME_MINUTES) + " " + ev.currency + " " + GT_ImpactDot(ev.impact) + " " + GT_CompactTitle(ev.title, 22);
      shown++;
   }

   if(shown == 0)
      tape = "no upcoming visible events in configured window";

   GT_Label(prefix + "TAPE", CORNER_LEFT_LOWER, 32, 54, tape, clrSilver, 8, "Consolas");
}

#endif
