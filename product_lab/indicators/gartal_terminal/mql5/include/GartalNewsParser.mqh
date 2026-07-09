#ifndef GARTAL_NEWS_PARSER_MQH
#define GARTAL_NEWS_PARSER_MQH

void GT_AddEvent(GT_NewsStore &store,
                 GT_Config &config,
                 datetime broker_time,
                 string currency,
                 int impact,
                 string title,
                 string actual,
                 string forecast,
                 string previous,
                 string source);

bool GT_LoadSampleEvents(GT_NewsStore &store, GT_Config &config, GT_RuntimeState &runtime);
void GT_ResetStore(GT_NewsStore &store);
void GT_SortEventsByBrokerTime(GT_NewsStore &store);
void GT_MarkRelevance(GT_Config &config, GT_NewsStore &store);
bool GT_EventPassesFilters(GT_NewsEvent &ev, GT_FilterState &filters);

string GT_NormalizeTitle(string title)
{
   return GT_Trim(title);
}

bool GT_TitleContainsAny(string title, string a, string b, string c, string d)
{
   string t = GT_ToLower(title);
   return (StringFind(t, GT_ToLower(a)) >= 0 ||
           StringFind(t, GT_ToLower(b)) >= 0 ||
           StringFind(t, GT_ToLower(c)) >= 0 ||
           StringFind(t, GT_ToLower(d)) >= 0);
}

void GT_ClassifyEvent(GT_NewsEvent &ev)
{
   ev.is_speech = GT_TitleContainsAny(ev.title, "speech", "speaks", "testifies", "press conference");
   if(GT_TitleContainsAny(ev.title, "chair", "president", "fomc", "statement"))
      ev.is_speech = true;

   ev.is_holiday = (StringFind(GT_ToLower(ev.title), "holiday") >= 0);
   ev.is_breaking = false; // Stage 08+ will set this from source semantics.
   ev.is_tentative = (StringFind(GT_ToLower(ev.title), "tentative") >= 0);
}

void GT_ResetStore(GT_NewsStore &store)
{
   store.count = 0;
   store.source_ok = false;
   store.last_refresh = 0;
   store.source_status = "EMPTY";
}

bool GT_ParseCalendar(string raw, GT_Config &config, GT_NewsStore &store, GT_RuntimeState &runtime)
{
   // Stage 01 parser contract:
   // The function exists and is callable, but real Forex Factory HTML parsing is
   // deliberately deferred. This keeps compile and lifecycle work isolated.
   if(config.data_mode == GT_DATA_MODE_SAMPLE)
      return GT_LoadSampleEvents(store, config, runtime);

   GT_RuntimeLog(runtime, GT_LOG_WARNING, "Production parser is not implemented in Stage 01. Enable sample data or continue to Stage 08.");
   return false;
}

bool GT_LoadSampleEvents(GT_NewsStore &store, GT_Config &config, GT_RuntimeState &runtime)
{
   GT_ResetStore(store);

   datetime today = GT_TodayBrokerMidnight();

   GT_AddEvent(store, config, today + 8*3600 + 30*60,  "JPY", GT_IMPACT_LOW,    "Final Manufacturing PMI", "", "", "", "sample");
   GT_AddEvent(store, config, today + 10*3600,          "EUR", GT_IMPACT_MEDIUM, "ECB President Speaks", "", "", "", "sample");
   GT_AddEvent(store, config, today + 12*3600 + 30*60,  "GBP", GT_IMPACT_MEDIUM, "BOE Gov Bailey Speaks", "", "", "", "sample");
   GT_AddEvent(store, config, today + 15*3600 + 30*60,  "USD", GT_IMPACT_HIGH,   "CPI m/m", "", "0.2%", "0.1%", "sample");
   GT_AddEvent(store, config, today + 17*3600,          "USD", GT_IMPACT_HIGH,   "Fed Chair Press Conference", "", "", "", "sample");
   GT_AddEvent(store, config, today + 19*3600,          "CAD", GT_IMPACT_MEDIUM, "BOC Business Outlook Survey", "", "", "", "sample");
   GT_AddEvent(store, config, today + 21*3600,          "USD", GT_IMPACT_HIGH,   "Unscheduled Presidential Remarks", "", "", "", "sample");

   store.source_ok = true;
   store.source_status = "SAMPLE";
   store.last_refresh = TimeCurrent();
   GT_RuntimeLog(runtime, GT_LOG_INFO, "Sample event pipeline loaded. count=" + IntegerToString(store.count));
   return true;
}

void GT_AddEvent(GT_NewsStore &store,
                 GT_Config &config,
                 datetime broker_time,
                 string currency,
                 int impact,
                 string title,
                 string actual,
                 string forecast,
                 string previous,
                 string source)
{
   if(store.count >= GT_MAX_EVENTS)
      return;

   if(!GT_InConfiguredDateWindow(broker_time, config))
      return;

   int i = store.count;
   string clean_currency = GT_ToUpper(GT_Trim(currency));
   string clean_title = GT_NormalizeTitle(title);

   store.events[i].time_broker = broker_time;
   store.events[i].time_utc = GT_BrokerToUtcTime(broker_time, config);
   store.events[i].currency = clean_currency;
   store.events[i].impact = impact;
   store.events[i].title = clean_title;
   store.events[i].actual = GT_Trim(actual);
   store.events[i].forecast = GT_Trim(forecast);
   store.events[i].previous = GT_Trim(previous);
   store.events[i].source = source;
   store.events[i].is_relevant = false;
   store.events[i].is_released = (StringLen(store.events[i].actual) > 0);
   store.events[i].status = GT_EVENT_UPCOMING;
   store.events[i].raw_hash = IntegerToString((int)broker_time) + "_" + clean_currency + "_" + clean_title;
   store.events[i].id = clean_currency + "_" + IntegerToString((int)broker_time) + "_" + IntegerToString(store.count);

   GT_ClassifyEvent(store.events[i]);
   store.count++;
}

void GT_SortEventsByBrokerTime(GT_NewsStore &store)
{
   for(int i=0; i<store.count-1; i++)
   {
      for(int j=i+1; j<store.count; j++)
      {
         if(store.events[j].time_broker < store.events[i].time_broker)
         {
            GT_NewsEvent tmp = store.events[i];
            store.events[i] = store.events[j];
            store.events[j] = tmp;
         }
      }
   }
}

void GT_MarkRelevance(GT_Config &config, GT_NewsStore &store)
{
   string symbol_upper = GT_ToUpper(Symbol());

   for(int i=0; i<store.count; i++)
   {
      string c = GT_ToUpper(store.events[i].currency);
      store.events[i].is_relevant = (StringFind(symbol_upper, c) >= 0);

      if((StringFind(symbol_upper, "XAU") >= 0 ||
          StringFind(symbol_upper, "GOLD") >= 0 ||
          StringFind(symbol_upper, "US30") >= 0 ||
          StringFind(symbol_upper, "NAS") >= 0 ||
          StringFind(symbol_upper, "SPX") >= 0) && c == "USD")
      {
         store.events[i].is_relevant = true;
      }
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
   if(ev.impact == GT_IMPACT_HOLIDAY && !filters.show_holiday)
      return false;

   if(ev.is_holiday && !filters.show_holiday)
      return false;
   if(ev.is_speech && !filters.show_speech)
      return false;
   if(ev.is_tentative && !filters.show_tentative)
      return false;
   if(ev.is_breaking && !filters.show_breaking)
      return false;

   if(!GT_CsvContains(filters.currencies_csv, ev.currency))
      return false;

   return true;
}

#endif
