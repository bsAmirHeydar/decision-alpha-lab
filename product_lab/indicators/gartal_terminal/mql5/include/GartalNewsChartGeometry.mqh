#ifndef GARTAL_NEWS_CHART_GEOMETRY_MQH
#define GARTAL_NEWS_CHART_GEOMETRY_MQH

// Stage 04: chart-space helpers. These functions keep renderer code isolated from
// raw ChartGet* calls so later UI work can change placement without touching event logic.

bool GT_ChartPriceRange(double &price_min, double &price_max)
{
   price_min = 0.0;
   price_max = 0.0;

   if(!ChartGetDouble(0, CHART_PRICE_MIN, 0, price_min))
      return false;
   if(!ChartGetDouble(0, CHART_PRICE_MAX, 0, price_max))
      return false;

   if(price_max <= price_min)
      return false;

   return true;
}

double GT_ChartPriceAtPercent(double percent_from_bottom)
{
   double price_min = 0.0;
   double price_max = 0.0;
   if(!GT_ChartPriceRange(price_min, price_max))
      return SymbolInfoDouble(Symbol(), SYMBOL_BID);

   double p = percent_from_bottom;
   if(p < 0.0) p = 0.0;
   if(p > 100.0) p = 100.0;

   return price_min + (price_max - price_min) * (p / 100.0);
}

double GT_TimelineLabelPrice(int row, int max_rows)
{
   int safe_rows = GT_ClampInt(max_rows, 1, 6);
   int safe_row = GT_ClampInt(row, 0, safe_rows - 1);
   double base = 3.5;
   double step = 3.2;
   return GT_ChartPriceAtPercent(base + safe_row * step);
}

double GT_DangerZoneTopPrice()
{
   return GT_ChartPriceAtPercent(100.0);
}

double GT_DangerZoneBottomPrice()
{
   return GT_ChartPriceAtPercent(0.0);
}

int GT_ChartVisibleBarsSafe()
{
   long visible = ChartGetInteger(0, CHART_VISIBLE_BARS, 0);
   if(visible <= 0)
      return 120;
   if(visible > 5000)
      return 5000;
   return (int)visible;
}

int GT_PeriodSecondsSafe()
{
   int seconds = PeriodSeconds((ENUM_TIMEFRAMES)_Period);
   if(seconds <= 0)
      seconds = 60;
   return seconds;
}

datetime GT_RightProjectionLimit(GT_Config &config)
{
   datetime now = TimeCurrent();
   return now + config.timeline_projection_minutes * GT_SECONDS_PER_MINUTE;
}

bool GT_EventInsideProjection(GT_NewsEvent &ev, GT_Config &config)
{
   if(ev.time_broker > GT_RightProjectionLimit(config))
      return false;
   if(!config.show_released_timeline_objects && (ev.status == GT_EVENT_RELEASED || ev.status == GT_EVENT_EXPIRED))
      return false;
   return true;
}

string GT_TimelineEventCaption(GT_NewsEvent &ev, GT_Config &config)
{
   string title = ev.title;
   if(config.timeline_compact_titles)
      title = GT_CompactTitle(ev.title, 24);

   string special = "";
   if(ev.is_breaking) special = " BRK";
   else if(ev.is_speech) special = " SPC";
   else if(ev.is_holiday) special = " HOL";

   return TimeToString(ev.time_broker, TIME_MINUTES) + " " + ev.currency + " " + GT_ImpactDot(ev.impact) + special + " | " + title;
}

string GT_TimelineTooltip(GT_NewsEvent &ev)
{
   string tooltip = "gartal terminal\n";
   tooltip += ev.currency + " " + GT_ImpactText(ev.impact) + " " + GT_EventKindText(ev.kind) + "\n";
   tooltip += ev.title + "\n";
   tooltip += "Broker: " + TimeToString(ev.time_broker, TIME_DATE|TIME_MINUTES) + "\n";
   tooltip += "UTC: " + TimeToString(ev.time_utc, TIME_DATE|TIME_MINUTES) + "\n";
   tooltip += "Actual: " + (GT_IsEmpty(ev.actual) ? "-" : ev.actual) + " | Forecast: " + (GT_IsEmpty(ev.forecast) ? "-" : ev.forecast) + " | Previous: " + (GT_IsEmpty(ev.previous) ? "-" : ev.previous);
   return tooltip;
}

#endif
