#ifndef GARTAL_NEWS_TIMELINE_MQH
#define GARTAL_NEWS_TIMELINE_MQH

void GT_DeleteObjectsByPrefix(string prefix)
{
   int total = ObjectsTotal(0, 0, -1);
   for(int i=total-1; i>=0; i--)
   {
      string name = ObjectName(0, i, 0, -1);
      if(StringFind(name, prefix) == 0)
         ObjectDelete(0, name);
   }
}

string GT_TimelinePrefix(GT_Config &config)
{
   return config.object_prefix + "TL_";
}

void GT_SetTimelineObjectBase(string name, bool back=true)
{
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
   ObjectSetInteger(0, name, OBJPROP_BACK, back);
}

color GT_TimelineLineColor(GT_NewsEvent &ev)
{
   if(ev.status == GT_EVENT_EXPIRED || ev.status == GT_EVENT_RELEASED)
      return clrDimGray;
   if(ev.is_breaking)
      return clrRed;
   return GT_ImpactColor(ev.impact);
}

int GT_TimelineLineWidth(GT_NewsEvent &ev)
{
   if(ev.is_breaking || ev.impact == GT_IMPACT_HIGH)
      return 2;
   return 1;
}

ENUM_LINE_STYLE GT_TimelineLineStyle(GT_NewsEvent &ev)
{
   if(ev.status == GT_EVENT_EXPIRED || ev.status == GT_EVENT_RELEASED)
      return STYLE_DOT;
   if(ev.impact == GT_IMPACT_HIGH || ev.is_breaking)
      return STYLE_SOLID;
   if(ev.impact == GT_IMPACT_MEDIUM)
      return STYLE_DASH;
   return STYLE_DOT;
}

bool GT_ShouldRenderTimelineEvent(GT_NewsEvent &ev, GT_Config &config, GT_FilterState &filters)
{
   if(!GT_EventPassesFilters(ev, filters))
      return false;
   if(!GT_EventInsideProjection(ev, config))
      return false;
   return true;
}

void GT_RenderTimelineVerticalLine(GT_Config &config, GT_NewsEvent &ev)
{
   if(!config.show_vertical_lines)
      return;

   string name = GT_SafeObjectName(GT_TimelinePrefix(config), "VLINE_" + ev.id);
   if(ObjectFind(0, name) < 0)
      ObjectCreate(0, name, OBJ_VLINE, 0, ev.time_broker, 0);

   ObjectMove(0, name, 0, ev.time_broker, 0);
   ObjectSetInteger(0, name, OBJPROP_COLOR, GT_TimelineLineColor(ev));
   ObjectSetInteger(0, name, OBJPROP_STYLE, GT_TimelineLineStyle(ev));
   ObjectSetInteger(0, name, OBJPROP_WIDTH, GT_TimelineLineWidth(ev));
   GT_SetTimelineObjectBase(name, true);

   if(config.show_timeline_tooltips)
      ObjectSetString(0, name, OBJPROP_TEXT, GT_TimelineTooltip(ev));
}

void GT_RenderTimelineDangerZone(GT_Config &config, GT_NewsEvent &ev)
{
   if(!config.show_danger_zones)
      return;
   if(ev.impact != GT_IMPACT_HIGH && !ev.is_breaking)
      return;
   if(config.pre_news_zone_minutes == 0 && config.post_news_zone_minutes == 0)
      return;

   datetime from_time = ev.time_broker - config.pre_news_zone_minutes * GT_SECONDS_PER_MINUTE;
   datetime to_time   = ev.time_broker + config.post_news_zone_minutes * GT_SECONDS_PER_MINUTE;
   if(to_time <= from_time)
      return;

   double top = GT_DangerZoneTopPrice();
   double bottom = GT_DangerZoneBottomPrice();

   string name = GT_SafeObjectName(GT_TimelinePrefix(config), "ZONE_" + ev.id);
   if(ObjectFind(0, name) < 0)
      ObjectCreate(0, name, OBJ_RECTANGLE, 0, from_time, top, to_time, bottom);

   ObjectMove(0, name, 0, from_time, top);
   ObjectMove(0, name, 1, to_time, bottom);
   ObjectSetInteger(0, name, OBJPROP_COLOR, ev.is_breaking ? clrRed : clrTomato);
   ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID);
   ObjectSetInteger(0, name, OBJPROP_WIDTH, 1);
   ObjectSetInteger(0, name, OBJPROP_FILL, true);
   GT_SetTimelineObjectBase(name, true);

   if(config.show_timeline_tooltips)
      ObjectSetString(0, name, OBJPROP_TEXT, "Danger zone | " + GT_TimelineTooltip(ev));
}

void GT_RenderTimelineEventLabel(GT_Config &config, GT_NewsEvent &ev, int render_index)
{
   if(!config.show_event_labels)
      return;

   int row = 0;
   if(config.timeline_label_rows > 0)
      row = render_index % config.timeline_label_rows;

   double price = GT_TimelineLabelPrice(row, config.timeline_label_rows);
   string name = GT_SafeObjectName(GT_TimelinePrefix(config), "LABEL_" + ev.id);
   if(ObjectFind(0, name) < 0)
      ObjectCreate(0, name, OBJ_TEXT, 0, ev.time_broker, price);

   ObjectMove(0, name, 0, ev.time_broker, price);
   ObjectSetInteger(0, name, OBJPROP_COLOR, GT_TimelineLineColor(ev));
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, ev.impact == GT_IMPACT_HIGH || ev.is_breaking ? 8 : 7);
   ObjectSetString(0, name, OBJPROP_FONT, "Consolas");
   ObjectSetString(0, name, OBJPROP_TEXT, GT_TimelineEventCaption(ev, config));
   ObjectSetDouble(0, name, OBJPROP_ANGLE, 90.0);
   GT_SetTimelineObjectBase(name, false);

   if(config.show_timeline_tooltips)
      ObjectSetString(0, name, OBJPROP_TOOLTIP, GT_TimelineTooltip(ev));
}

void GT_RenderTimelineBottomTape(GT_Config &config, GT_NewsStore &store, GT_FilterState &filters, GT_RuntimeState &runtime)
{
   if(!config.show_timeline || !config.show_bottom_tape)
      return;

   string prefix = config.object_prefix + "TIMELINE_";
   int width = 940;
   int height = config.show_timeline_debug ? 82 : 62;
   GT_Rect(prefix + "BG", CORNER_LEFT_LOWER, 18, config.timeline_bottom_y, width, height, clrBlack, clrDimGray);

   string headline = "gartal timeline | visible=" + IntegerToString(store.visible_count) +
                     " | rendered=" + IntegerToString(runtime.timeline_last_visible_rendered) +
                     " | horizon=" + IntegerToString(config.timeline_projection_minutes) + "m" +
                     " | zones=" + IntegerToString(config.pre_news_zone_minutes) + "/" + IntegerToString(config.post_news_zone_minutes) + "m" +
                     " | broker=" + GT_FormatGmtOffsetSeconds(config.broker_gmt_offset_seconds) +
                     " | Stage 04";
   GT_Label(prefix + "INFO", CORNER_LEFT_LOWER, 32, config.timeline_bottom_y + 12, headline, clrWhite, 8, "Segoe UI Semibold");

   string tape = "";
   int shown = 0;
   datetime now = TimeCurrent();
   for(int i=0; i<store.count && shown<8; i++)
   {
      GT_NewsEvent ev = store.events[i];
      if(ev.time_broker < now)
         continue;
      if(!GT_ShouldRenderTimelineEvent(ev, config, filters))
         continue;

      if(shown > 0)
         tape += "   |   ";
      tape += TimeToString(ev.time_broker, TIME_MINUTES) + " " + ev.currency + " " + GT_ImpactDot(ev.impact) + " " + GT_CompactTitle(ev.title, 18);
      shown++;
   }

   if(shown == 0)
      tape = "no upcoming visible events in configured broker-time projection";

   GT_Label(prefix + "TAPE", CORNER_LEFT_LOWER, 32, config.timeline_bottom_y + 32, tape, clrSilver, 8, "Consolas");

   if(config.show_timeline_debug)
   {
      string dbg = "objects: lines=" + IntegerToString(runtime.timeline_last_vertical_lines) +
                   " labels=" + IntegerToString(runtime.timeline_last_labels) +
                   " zones=" + IntegerToString(runtime.timeline_last_zones) +
                   " | last=" + TimeToString(runtime.timeline_last_render_at, TIME_MINUTES) +
                   " | visibleBars=" + IntegerToString(GT_ChartVisibleBarsSafe()) +
                   " | periodSec=" + IntegerToString(GT_PeriodSecondsSafe());
      GT_Label(prefix + "DEBUG", CORNER_LEFT_LOWER, 32, config.timeline_bottom_y + 52, dbg, clrDarkGray, 8, "Consolas");
   }
}

void GT_RenderTimeline(GT_Config &config, GT_NewsStore &store, GT_FilterState &filters, GT_RuntimeState &runtime)
{
   if(!config.show_timeline && !config.show_vertical_lines)
      return;

   string render_prefix = GT_TimelinePrefix(config);
   GT_DeleteObjectsByPrefix(render_prefix);

   runtime.timeline_last_visible_rendered = 0;
   runtime.timeline_last_vertical_lines = 0;
   runtime.timeline_last_labels = 0;
   runtime.timeline_last_zones = 0;

   int rendered = 0;
   for(int i=0; i<store.count && rendered<config.timeline_max_events; i++)
   {
      GT_NewsEvent ev = store.events[i];
      if(!GT_ShouldRenderTimelineEvent(ev, config, filters))
         continue;

      if(config.show_danger_zones && (ev.impact == GT_IMPACT_HIGH || ev.is_breaking))
      {
         GT_RenderTimelineDangerZone(config, ev);
         if(config.pre_news_zone_minutes > 0 || config.post_news_zone_minutes > 0)
            runtime.timeline_last_zones++;
      }

      if(config.show_vertical_lines)
      {
         GT_RenderTimelineVerticalLine(config, ev);
         runtime.timeline_last_vertical_lines++;
      }

      if(config.show_event_labels)
      {
         GT_RenderTimelineEventLabel(config, ev, rendered);
         runtime.timeline_last_labels++;
      }

      rendered++;
   }

   runtime.timeline_last_visible_rendered = rendered;
   runtime.timeline_last_render_at = TimeCurrent();
   runtime.timeline_last_render_summary = "rendered=" + IntegerToString(rendered) +
                                          " lines=" + IntegerToString(runtime.timeline_last_vertical_lines) +
                                          " labels=" + IntegerToString(runtime.timeline_last_labels) +
                                          " zones=" + IntegerToString(runtime.timeline_last_zones);

   GT_RenderTimelineBottomTape(config, store, filters, runtime);
   ChartRedraw(0);
}

void GT_RenderVerticalLines(GT_Config &config, GT_NewsStore &store, GT_FilterState &filters, GT_RuntimeState &runtime)
{
   // Stage 04 merged vertical-line rendering into GT_RenderTimeline so that line,
   // label, and danger-zone cleanup share the same object namespace. This function
   // remains as a compatibility shim for older orchestration calls.
}

#endif
