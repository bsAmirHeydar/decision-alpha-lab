#ifndef GARTAL_NEWS_STORE_MQH
#define GARTAL_NEWS_STORE_MQH

void GT_ResetEvent(GT_NewsEvent &ev)
{
   ev.id = "";
   ev.sequence = 0;
   ev.time_source = 0;
   ev.time_utc = 0;
   ev.time_broker = 0;
   ev.day_start_broker = 0;
   ev.minute_of_day = 0;
   ev.day_offset = 0;
   ev.sort_rank = 0;
   ev.impact_rank = 0;
   ev.kind = GT_EVENT_KIND_ECONOMIC;
   ev.currency = "";
   ev.impact = GT_IMPACT_NONE;
   ev.title = "";
   ev.normalized_title = "";
   ev.actual = "";
   ev.forecast = "";
   ev.previous = "";
   ev.is_tentative = false;
   ev.is_speech = false;
   ev.is_holiday = false;
   ev.is_breaking = false;
   ev.is_relevant = false;
   ev.is_released = false;
   ev.is_today = false;
   ev.in_date_window = false;
   ev.status = GT_EVENT_UPCOMING;
   ev.source = "";
   ev.raw_hash = "";
   ev.notes = "";
}

void GT_ResetStore(GT_NewsStore &store)
{
   store.count = 0;
   store.source_ok = false;
   store.last_refresh = 0;
   store.source_status = "EMPTY";
   store.sample_profile = "";
   store.window_from_broker = 0;
   store.window_to_broker = 0;
   store.today_start_broker = GT_TodayBrokerMidnight();
   store.high_count = 0;
   store.medium_count = 0;
   store.low_count = 0;
   store.holiday_count = 0;
   store.speech_count = 0;
   store.breaking_count = 0;
   store.released_count = 0;
   store.upcoming_count = 0;
   store.active_count = 0;
   store.expired_count = 0;
   store.relevant_count = 0;
   store.visible_count = 0;
   store.next_event_index = -1;
   store.next_high_index = -1;
   store.checksum = "";
}

string GT_NormalizeTitle(string title)
{
   return GT_NormalizeWhitespace(title);
}

bool GT_TitleContains(string title, string needle)
{
   return (StringFind(GT_ToLower(title), GT_ToLower(needle)) >= 0);
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

   ev.is_holiday = GT_TitleContains(ev.title, "holiday");
   ev.is_tentative = GT_TitleContains(ev.title, "tentative");

   // Breaking news is sample/source-flag driven until the Stage 08 parser is active. Stage 08 parser will
   // infer it from source semantics when Forex Factory integration is active.
   if(ev.is_breaking)
      ev.kind = GT_EVENT_KIND_BREAKING;
   else if(ev.is_holiday)
      ev.kind = GT_EVENT_KIND_HOLIDAY;
   else if(ev.is_speech)
      ev.kind = GT_EVENT_KIND_SPEECH;
   else
      ev.kind = GT_EVENT_KIND_ECONOMIC;
}

string GT_MakeEventId(string currency, datetime broker_time, string title, int sequence)
{
   string key = GT_ToUpper(currency) + "_" + IntegerToString((int)broker_time) + "_" + IntegerToString(sequence) + "_" + title;
   return GT_SafeObjectName("", key);
}

bool GT_EventPassesFilters(GT_NewsEvent &ev, GT_FilterState &filters)
{
   if(!ev.in_date_window)
      return false;

   if(filters.only_symbol && !ev.is_relevant)
      return false;

   if(!filters.show_past_events && (ev.status == GT_EVENT_EXPIRED || ev.status == GT_EVENT_RELEASED))
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

void GT_AddEventEx(GT_NewsStore &store,
                   GT_Config &config,
                   datetime broker_time,
                   string currency,
                   int impact,
                   string title,
                   string actual,
                   string forecast,
                   string previous,
                   string source,
                   bool breaking,
                   string notes)
{
   if(store.count >= GT_MAX_EVENTS)
      return;

   bool in_window = GT_InConfiguredDateWindow(broker_time, config);
   if(!in_window)
      return;

   int i = store.count;
   GT_ResetEvent(store.events[i]);

   string clean_currency = GT_ToUpper(GT_Trim(currency));
   string clean_title = GT_NormalizeTitle(title);

   store.events[i].sequence = i;
   GT_UpdateEventTimeFields(store.events[i], config, broker_time);

   store.events[i].currency = clean_currency;
   store.events[i].impact = impact;
   store.events[i].impact_rank = GT_ImpactRank(impact);
   store.events[i].title = clean_title;
   store.events[i].normalized_title = GT_ToLower(clean_title);
   store.events[i].actual = GT_Trim(actual);
   store.events[i].forecast = GT_Trim(forecast);
   store.events[i].previous = GT_Trim(previous);
   store.events[i].source = GT_Trim(source);
   store.events[i].notes = GT_Trim(notes);
   store.events[i].is_breaking = breaking;
   store.events[i].is_released = (StringLen(store.events[i].actual) > 0);
   store.events[i].status = GT_EVENT_UPCOMING;
   store.events[i].raw_hash = IntegerToString((int)broker_time) + "|" + clean_currency + "|" + clean_title + "|" + store.events[i].actual;
   store.events[i].id = GT_MakeEventId(clean_currency, broker_time, clean_title, i);

   GT_ClassifyEvent(store.events[i]);
   store.events[i].sort_rank = (store.events[i].day_offset * 1440000) + (store.events[i].minute_of_day * 1000) - store.events[i].impact_rank;

   store.count++;
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
   GT_AddEventEx(store, config, broker_time, currency, impact, title, actual, forecast, previous, source, false, "");
}

void GT_AddEventFromSource(GT_NewsStore &store,
                           GT_Config &config,
                           datetime source_time,
                           string currency,
                           int impact,
                           string title,
                           string actual,
                           string forecast,
                           string previous,
                           string source,
                           bool breaking=false,
                           string notes="")
{
   datetime broker_time = GT_SourceToBrokerTime(source_time, config);
   GT_AddEventEx(store, config, broker_time, currency, impact, title, actual, forecast, previous, source, breaking, notes);
}

void GT_AddEventFromUtc(GT_NewsStore &store,
                        GT_Config &config,
                        datetime utc_time,
                        string currency,
                        int impact,
                        string title,
                        string actual,
                        string forecast,
                        string previous,
                        string source,
                        bool breaking=false,
                        string notes="")
{
   datetime broker_time = GT_UtcToBrokerTime(utc_time, config);
   GT_AddEventEx(store, config, broker_time, currency, impact, title, actual, forecast, previous, source, breaking, notes);
}

void GT_SortEventsByBrokerTime(GT_NewsStore &store)
{
   for(int i=0; i<store.count-1; i++)
   {
      for(int j=i+1; j<store.count; j++)
      {
         bool swap = false;
         if(store.events[j].time_broker < store.events[i].time_broker)
            swap = true;
         else if(store.events[j].time_broker == store.events[i].time_broker && store.events[j].impact_rank > store.events[i].impact_rank)
            swap = true;
         else if(store.events[j].time_broker == store.events[i].time_broker && store.events[j].impact_rank == store.events[i].impact_rank && StringCompare(store.events[j].currency, store.events[i].currency) < 0)
            swap = true;

         if(swap)
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
          StringFind(symbol_upper, "SPX") >= 0 ||
          StringFind(symbol_upper, "DOW") >= 0) && c == "USD")
      {
         store.events[i].is_relevant = true;
      }
   }
}

int GT_FilteredEventCount(GT_NewsStore &store, GT_FilterState &filters)
{
   int count = 0;
   for(int i=0; i<store.count; i++)
      if(GT_EventPassesFilters(store.events[i], filters))
         count++;
   return count;
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

int GT_NextHighEventIndex(GT_NewsStore &store, GT_FilterState &filters)
{
   datetime now = TimeCurrent();
   for(int i=0; i<store.count; i++)
   {
      if(store.events[i].time_broker >= now && store.events[i].impact == GT_IMPACT_HIGH && GT_EventPassesFilters(store.events[i], filters))
         return i;
   }
   return -1;
}

string GT_StoreChecksum(GT_NewsStore &store)
{
   string result = IntegerToString(store.count);
   for(int i=0; i<store.count; i++)
      result += "|" + store.events[i].id + ":" + IntegerToString(store.events[i].status);
   return result;
}

void GT_UpdateStoreMetrics(GT_NewsStore &store, GT_FilterState &filters)
{
   store.high_count = 0;
   store.medium_count = 0;
   store.low_count = 0;
   store.holiday_count = 0;
   store.speech_count = 0;
   store.breaking_count = 0;
   store.released_count = 0;
   store.upcoming_count = 0;
   store.active_count = 0;
   store.expired_count = 0;
   store.relevant_count = 0;
   store.visible_count = 0;
   store.next_event_index = GT_NextEventIndex(store, filters);
   store.next_high_index = GT_NextHighEventIndex(store, filters);

   for(int i=0; i<store.count; i++)
   {
      if(store.events[i].impact == GT_IMPACT_HIGH) store.high_count++;
      if(store.events[i].impact == GT_IMPACT_MEDIUM) store.medium_count++;
      if(store.events[i].impact == GT_IMPACT_LOW) store.low_count++;
      if(store.events[i].impact == GT_IMPACT_HOLIDAY) store.holiday_count++;
      if(store.events[i].is_speech) store.speech_count++;
      if(store.events[i].is_breaking) store.breaking_count++;
      if(store.events[i].is_relevant) store.relevant_count++;

      if(store.events[i].status == GT_EVENT_RELEASED) store.released_count++;
      if(store.events[i].status == GT_EVENT_UPCOMING) store.upcoming_count++;
      if(store.events[i].status == GT_EVENT_ACTIVE) store.active_count++;
      if(store.events[i].status == GT_EVENT_EXPIRED) store.expired_count++;

      if(GT_EventPassesFilters(store.events[i], filters))
         store.visible_count++;
   }

   store.checksum = GT_StoreChecksum(store);
}

void GT_FinalizeStore(GT_Config &config, GT_NewsStore &store, GT_FilterState &filters)
{
   datetime today = GT_TodayBrokerMidnight();
   store.today_start_broker = today;
   store.window_from_broker = GT_ConfigWindowFromBroker(config);
   store.window_to_broker = GT_ConfigWindowToBroker(config);

   GT_SortEventsByBrokerTime(store);
   GT_MarkRelevance(config, store);
   GT_UpdateEventStatuses(store, TimeCurrent());
   GT_UpdateStoreMetrics(store, filters);
}

#endif
