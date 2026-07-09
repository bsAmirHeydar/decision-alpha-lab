#ifndef GARTAL_NEWS_PARSER_MQH
#define GARTAL_NEWS_PARSER_MQH

string GT_NormalizeTitle(string title)
{
   StringTrimLeft(title);
   StringTrimRight(title);
   return title;
}

bool GT_TitleContainsAny(string title, string a, string b, string c, string d)
{
   string t = StringToLower(title);
   return (StringFind(t, StringToLower(a)) >= 0 ||
           StringFind(t, StringToLower(b)) >= 0 ||
           StringFind(t, StringToLower(c)) >= 0 ||
           StringFind(t, StringToLower(d)) >= 0);
}

void GT_ClassifyEvent(GT_NewsEvent &ev)
{
   ev.is_speech = GT_TitleContainsAny(ev.title, "speech", "speaks", "testifies", "press conference");
   if(GT_TitleContainsAny(ev.title, "chair", "president", "fomc", "statement"))
      ev.is_speech = true;

   ev.is_holiday = (StringFind(StringToLower(ev.title), "holiday") >= 0);
   ev.is_breaking = false; // Set true by future BreakingFeedAdapter.
}

bool GT_ParseCalendar(string raw, GT_Config &config, GT_NewsStore &store)
{
   // Product scaffold:
   // Replace this sample parser with hardened Forex Factory adapter.
   // The adapter must extract rows, map impact classes/colors, parse time,
   // currency, title, actual, forecast, previous, tentative/speech/holiday.
   if(config.use_sample_data)
   {
      GT_LoadSampleEvents(store, config);
      return true;
   }

   // Minimal fail-safe until the real parser is implemented.
   // Returning false allows cache or warning mode.
   Print("gartal terminal parser scaffold: production Forex Factory parser not implemented yet.");
   return false;
}

void GT_LoadSampleEvents(GT_NewsStore &store, GT_Config &config)
{
   store.count = 0;
   datetime now = TimeCurrent();
   datetime today = StringToTime(TimeToString(now, TIME_DATE));

   GT_AddSampleEvent(store, today + 12*3600, "EUR", GT_IMPACT_MEDIUM, "ECB President Speaks", "", "", "");
   GT_AddSampleEvent(store, today + 15*3600 + 30*60, "USD", GT_IMPACT_HIGH, "CPI m/m", "", "0.2%", "0.1%");
   GT_AddSampleEvent(store, today + 17*3600, "USD", GT_IMPACT_HIGH, "Fed Chair Press Conference", "", "", "");
   GT_AddSampleEvent(store, today + 19*3600, "GBP", GT_IMPACT_LOW, "BRC Retail Sales Monitor", "", "", "");

   store.source_ok = true;
   store.source_status = "SAMPLE";
   store.last_refresh = TimeCurrent();
}

void GT_AddSampleEvent(GT_NewsStore &store, datetime broker_time, string cur, int impact, string title, string actual, string forecast, string previous)
{
   if(store.count >= GT_MAX_EVENTS)
      return;

   int i = store.count;
   store.events[i].time_broker = broker_time;
   store.events[i].time_utc = broker_time; // sample only
   store.events[i].currency = cur;
   store.events[i].impact = impact;
   store.events[i].title = title;
   store.events[i].actual = actual;
   store.events[i].forecast = forecast;
   store.events[i].previous = previous;
   store.events[i].id = cur + "_" + IntegerToString((int)broker_time) + "_" + title;
   store.events[i].source = "sample";
   store.events[i].is_tentative = false;
   store.events[i].is_released = (StringLen(actual) > 0);
   GT_ClassifyEvent(store.events[i]);
   store.count++;
}

void GT_MarkRelevance(GT_Config &config, GT_NewsStore &store)
{
   string sym = Symbol();
   string s = StringToUpper(sym);

   for(int i=0; i<store.count; i++)
   {
      string c = StringToUpper(store.events[i].currency);
      store.events[i].is_relevant = (StringFind(s, c) >= 0);

      if((StringFind(s, "XAU") >= 0 || StringFind(s, "GOLD") >= 0 || StringFind(s, "US30") >= 0 || StringFind(s, "NAS") >= 0) && c == "USD")
         store.events[i].is_relevant = true;
   }
}

bool GT_EventPassesFilters(GT_NewsEvent &ev, GT_FilterState &filters)
{
   if(filters.only_symbol && !ev.is_relevant)
      return false;

   if(ev.impact == GT_IMPACT_LOW && !filters.show_low)
      return false;
   if(ev.impact == GT_IMPACT_MEDIUM && !filters.show_medium)
      return false;
   if(ev.impact == GT_IMPACT_HIGH && !filters.show_high)
      return false;
   if(ev.is_holiday && !filters.show_holiday)
      return false;
   if(ev.is_speech && !filters.show_speech)
      return false;
   if(ev.is_breaking && !filters.show_breaking)
      return false;

   if(StringFind("," + filters.currencies_csv + ",", "," + ev.currency + ",") < 0)
      return false;

   return true;
}

#endif
