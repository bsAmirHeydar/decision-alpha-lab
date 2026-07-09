#ifndef GARTAL_NEWS_DASHBOARD_MQH
#define GARTAL_NEWS_DASHBOARD_MQH

color GT_ImpactColor(int impact)
{
   if(impact == GT_IMPACT_HIGH) return clrTomato;
   if(impact == GT_IMPACT_MEDIUM) return clrOrange;
   if(impact == GT_IMPACT_LOW) return clrGold;
   return clrGray;
}

string GT_ImpactText(int impact)
{
   if(impact == GT_IMPACT_HIGH) return "HIGH";
   if(impact == GT_IMPACT_MEDIUM) return "MED";
   if(impact == GT_IMPACT_LOW) return "LOW";
   return "HOL";
}

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

void GT_RenderShell(GT_Config &config)
{
   // Placeholder shell creation. Full renderer draws panels and filter buttons.
}

void GT_Label(string name, int x, int y, string text, color clr, int font_size=9)
{
   if(ObjectFind(0, name) < 0)
      ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0);

   ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_RIGHT_UPPER);
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, font_size);
   ObjectSetString(0, name, OBJPROP_FONT, "Segoe UI");
   ObjectSetString(0, name, OBJPROP_TEXT, text);
}

void GT_RenderDashboard(GT_Config &config, GT_NewsStore &store, GT_FilterState &filters)
{
   if(!config.show_dashboard)
      return;

   string prefix = config.object_prefix + "DASH_";
   string status = store.source_ok ? store.source_status : "SOURCE WARNING";

   GT_Label(prefix + "HEADER", 20, 30, "gartal terminal  |  " + status + "  |  GMT" + IntegerToString(config.broker_gmt_offset_hours), clrWhite, 10);

   int row = 0;
   for(int i=0; i<store.count && row<8; i++)
   {
      GT_NewsEvent ev = store.events[i];
      if(!GT_EventPassesFilters(ev, filters))
         continue;

      string t = TimeToString(ev.time_broker, TIME_MINUTES);
      string text = t + "  " + ev.currency + "  " + GT_ImpactText(ev.impact) + "  " + ev.title;
      if(ev.is_relevant) text = "* " + text;
      GT_Label(prefix + "ROW_" + IntegerToString(row), 20, 55 + row*18, text, GT_ImpactColor(ev.impact), 9);
      row++;
   }
}

bool GT_HandleDashboardClick(string object_name, GT_FilterState &filters, GT_Config &config)
{
   // Production version toggles currency/impact/range/alert buttons.
   return false;
}

void GT_UpdateCountdowns(GT_Config &config, GT_NewsStore &store, GT_FilterState &filters)
{
   // Production version updates next-event countdown labels without full redraw.
}

#endif
