#ifndef GARTAL_NEWS_PARSER_MQH
#define GARTAL_NEWS_PARSER_MQH

string GT_StripCData(string value)
{
   string s = value;
   StringReplace(s, "<![CDATA[", "");
   StringReplace(s, "]]>", "");
   return s;
}

string GT_XmlDecode(string value)
{
   string s = GT_StripCData(value);
   StringReplace(s, "&amp;", "&");
   StringReplace(s, "&lt;", "<");
   StringReplace(s, "&gt;", ">");
   StringReplace(s, "&quot;", "\"");
   StringReplace(s, "&#39;", "'");
   StringReplace(s, "&apos;", "'");
   return GT_NormalizeWhitespace(s);
}

string GT_GetTagValue(string block, string tag)
{
   string left = "<" + tag + ">";
   string right = "</" + tag + ">";
   int p1 = StringFind(block, left);
   if(p1 < 0)
      return "";
   p1 += StringLen(left);
   int p2 = StringFind(block, right, p1);
   if(p2 < 0 || p2 < p1)
      return "";
   return GT_XmlDecode(StringSubstr(block, p1, p2 - p1));
}

string GT_MapFfCountryToCurrency(string country)
{
   string c = GT_ToUpper(GT_Trim(country));
   if(c == "US" || c == "USD") return "USD";
   if(c == "EU" || c == "EZ" || c == "EUR") return "EUR";
   if(c == "UK" || c == "GB" || c == "GBP") return "GBP";
   if(c == "JP" || c == "JPY") return "JPY";
   if(c == "CH" || c == "CHF") return "CHF";
   if(c == "CA" || c == "CAD") return "CAD";
   if(c == "AU" || c == "AUD") return "AUD";
   if(c == "NZ" || c == "NZD") return "NZD";
   if(c == "CN" || c == "CNY") return "CNY";
   if(StringLen(c) == 3) return c;
   return c;
}

int GT_ParseImpact(string value)
{
   string v = GT_ToLower(GT_Trim(value));
   if(StringFind(v, "high") >= 0)    return GT_IMPACT_HIGH;
   if(StringFind(v, "red") >= 0)     return GT_IMPACT_HIGH;
   if(StringFind(v, "medium") >= 0)  return GT_IMPACT_MEDIUM;
   if(StringFind(v, "orange") >= 0)  return GT_IMPACT_MEDIUM;
   if(StringFind(v, "low") >= 0)     return GT_IMPACT_LOW;
   if(StringFind(v, "yellow") >= 0)  return GT_IMPACT_LOW;
   if(StringFind(v, "holiday") >= 0) return GT_IMPACT_HOLIDAY;
   if(StringFind(v, "gray") >= 0)    return GT_IMPACT_HOLIDAY;
   return GT_IMPACT_NONE;
}

bool GT_ParseFfDate(string value, int &year, int &month, int &day)
{
   string d = GT_Trim(value);
   StringReplace(d, ".", "-");
   StringReplace(d, "/", "-");

   string parts[];
   ushort date_sep = StringGetCharacter("-", 0);
   int n = StringSplit(d, date_sep, parts);
   if(n < 3)
      return false;

   int a = (int)StringToInteger(parts[0]);
   int b = (int)StringToInteger(parts[1]);
   int c = (int)StringToInteger(parts[2]);

   if(a > 1900)
   {
      year = a; month = b; day = c;
   }
   else if(c > 1900)
   {
      year = c;
      // Forex Factory XML has historically used mm-dd-yyyy. If the first part
      // cannot be a month, fall back to dd-mm-yyyy.
      if(a > 12)
      {
         day = a; month = b;
      }
      else
      {
         month = a; day = b;
      }
   }
   else
      return false;

   if(year < 2000 || month < 1 || month > 12 || day < 1 || day > 31)
      return false;

   return true;
}

bool GT_ParseFfClock(string value, int &hour, int &minute, bool &all_day, bool &tentative)
{
   string t = GT_ToLower(GT_Trim(value));
   all_day = false;
   tentative = false;
   hour = 0;
   minute = 0;

   if(GT_IsEmpty(t))
   {
      tentative = true;
      hour = 12;
      return true;
   }

   if(StringFind(t, "all") >= 0 && StringFind(t, "day") >= 0)
   {
      all_day = true;
      hour = 0;
      minute = 0;
      return true;
   }

   if(StringFind(t, "tent") >= 0)
   {
      tentative = true;
      hour = 12;
      minute = 0;
      return true;
   }

   bool is_pm = (StringFind(t, "pm") >= 0);
   bool is_am = (StringFind(t, "am") >= 0);
   StringReplace(t, "am", "");
   StringReplace(t, "pm", "");
   t = GT_Trim(t);

   string parts[];
   ushort time_sep = StringGetCharacter(":", 0);
   int n = StringSplit(t, time_sep, parts);
   if(n >= 1)
      hour = (int)StringToInteger(parts[0]);
   if(n >= 2)
      minute = (int)StringToInteger(parts[1]);

   if(is_pm && hour < 12)
      hour += 12;
   if(is_am && hour == 12)
      hour = 0;

   hour = GT_ClampInt(hour, 0, 23);
   minute = GT_ClampInt(minute, 0, 59);
   return true;
}

datetime GT_BuildSourceDateTime(int year, int month, int day, int hour, int minute)
{
   string stamp = IntegerToString(year) + "." + GT_TwoDigits(month) + "." + GT_TwoDigits(day) + " " + GT_TwoDigits(hour) + ":" + GT_TwoDigits(minute);
   return StringToTime(stamp);
}

bool GT_TitleLooksBreaking(string title)
{
   string t = GT_ToLower(title);
   if(StringFind(t, "trump") >= 0) return true;
   if(StringFind(t, "president") >= 0 && StringFind(t, "speaks") >= 0) return true;
   if(StringFind(t, "emergency") >= 0) return true;
   if(StringFind(t, "unscheduled") >= 0) return true;
   if(StringFind(t, "statement") >= 0 && StringFind(t, "president") >= 0) return true;
   return false;
}

int GT_DetectSourceFormat(string raw, GT_Config &config)
{
   if(config.source_format != GT_SOURCE_FORMAT_AUTO)
      return config.source_format;

   string head = GT_ToLower(StringSubstr(GT_Trim(raw), 0, 500));
   if(StringFind(head, "<weeklyevents") >= 0 || StringFind(head, "<event>") >= 0)
      return GT_SOURCE_FORMAT_XML;
   if(StringFind(head, "<html") >= 0 || StringFind(head, "calendar__row") >= 0)
      return GT_SOURCE_FORMAT_HTML;
   if(StringFind(head, "title,") >= 0 || StringFind(head, "country,") >= 0)
      return GT_SOURCE_FORMAT_CSV;
   return GT_SOURCE_FORMAT_XML;
}

bool GT_ParseFfXmlCalendar(string raw, GT_Config &config, GT_NewsStore &store, GT_RuntimeState &runtime)
{
   runtime.parser_blocks_seen = 0;
   runtime.parser_events_added = 0;
   runtime.parser_events_skipped = 0;
   runtime.parser_last_run_at = TimeCurrent();
   runtime.source_format_detected = GT_SOURCE_FORMAT_XML;

   int pos = 0;
   while(true)
   {
      int p1 = StringFind(raw, "<event>", pos);
      if(p1 < 0)
         break;
      int p2 = StringFind(raw, "</event>", p1);
      if(p2 < 0)
         break;

      string block = StringSubstr(raw, p1, p2 - p1 + 8);
      pos = p2 + 8;
      runtime.parser_blocks_seen++;

      string title = GT_GetTagValue(block, "title");
      string country = GT_GetTagValue(block, "country");
      string date = GT_GetTagValue(block, "date");
      string time = GT_GetTagValue(block, "time");
      string impact_text = GT_GetTagValue(block, "impact");
      string forecast = GT_GetTagValue(block, "forecast");
      string previous = GT_GetTagValue(block, "previous");
      string actual = GT_GetTagValue(block, "actual");
      string url = GT_GetTagValue(block, "url");

      if(GT_IsEmpty(title) || GT_IsEmpty(country) || GT_IsEmpty(date))
      {
         runtime.parser_events_skipped++;
         if(config.parser_log_skipped_rows)
            GT_RuntimeLog(runtime, GT_LOG_WARNING, "Skipped FF XML event with missing title/country/date.");
         continue;
      }

      int year=0, month=0, day=0;
      if(!GT_ParseFfDate(date, year, month, day))
      {
         runtime.parser_events_skipped++;
         if(config.parser_log_skipped_rows)
            GT_RuntimeLog(runtime, GT_LOG_WARNING, "Skipped FF XML event with invalid date: " + date + " title=" + title);
         continue;
      }

      int hour=0, minute=0;
      bool all_day=false, tentative=false;
      GT_ParseFfClock(time, hour, minute, all_day, tentative);
      if(all_day && !config.parser_include_all_day)
      {
         runtime.parser_events_skipped++;
         continue;
      }

      int impact = GT_ParseImpact(impact_text);
      string currency = GT_MapFfCountryToCurrency(country);
      bool breaking = (config.parser_detect_breaking_titles && GT_TitleLooksBreaking(title));

      datetime source_time = GT_BuildSourceDateTime(year, month, day, hour, minute);
      string notes = "ff_xml date=" + date + " time=" + time + " impact=" + impact_text;
      if(tentative) notes += " tentative";
      if(all_day)   notes += " all_day";
      if(!GT_IsEmpty(url)) notes += " url=" + url;

      int before = store.count;
      GT_AddEventFromSource(store, config, source_time, currency, impact, title, actual, forecast, previous, "FF_XML", breaking, notes);
      if(store.count > before)
      {
         store.events[store.count-1].is_tentative = store.events[store.count-1].is_tentative || tentative;
         store.events[store.count-1].is_holiday = store.events[store.count-1].is_holiday || (impact == GT_IMPACT_HOLIDAY);
         GT_ClassifyEvent(store.events[store.count-1]);
         runtime.parser_events_added++;
      }
      else
         runtime.parser_events_skipped++;
   }

   runtime.parser_last_summary = "FF_XML blocks=" + IntegerToString(runtime.parser_blocks_seen) +
                                 " added=" + IntegerToString(runtime.parser_events_added) +
                                 " skipped=" + IntegerToString(runtime.parser_events_skipped);

   if(runtime.parser_events_added <= 0)
   {
      runtime.parser_last_warning = "FF XML parser found no usable events.";
      GT_RuntimeLog(runtime, GT_LOG_WARNING, runtime.parser_last_warning);
      return false;
   }

   GT_RuntimeLog(runtime, GT_LOG_INFO, runtime.parser_last_summary);
   return true;
}

bool GT_ParseCsvCalendar(string raw, GT_Config &config, GT_NewsStore &store, GT_RuntimeState &runtime)
{
   runtime.source_format_detected = GT_SOURCE_FORMAT_CSV;
   runtime.parser_last_run_at = TimeCurrent();
   runtime.parser_last_warning = "CSV parser is a Stage 08 guardrail only. Use FF XML for production path.";
   GT_RuntimeLog(runtime, GT_LOG_WARNING, runtime.parser_last_warning);
   return false;
}

bool GT_ParseHtmlCalendar(string raw, GT_Config &config, GT_NewsStore &store, GT_RuntimeState &runtime)
{
   runtime.source_format_detected = GT_SOURCE_FORMAT_HTML;
   runtime.parser_last_run_at = TimeCurrent();
   runtime.parser_last_warning = "Website HTML parsing is intentionally guarded. Use the Forex Factory/Fair Economy XML feed or EA bridge; the public website DOM is fragile.";
   GT_RuntimeLog(runtime, GT_LOG_WARNING, runtime.parser_last_warning);
   return false;
}

bool GT_ParseCalendar(string raw, GT_Config &config, GT_NewsStore &store, GT_RuntimeState &runtime)
{
   if(config.data_mode == GT_DATA_MODE_SAMPLE)
      return GT_LoadSampleEvents(store, config, runtime);

   if(StringLen(GT_Trim(raw)) <= 0)
   {
      runtime.parser_last_warning = "Parser received empty raw source.";
      GT_RuntimeLog(runtime, GT_LOG_WARNING, runtime.parser_last_warning);
      return false;
   }

   int format = GT_DetectSourceFormat(raw, config);
   runtime.source_format_detected = format;

   if(format == GT_SOURCE_FORMAT_XML)
      return GT_ParseFfXmlCalendar(raw, config, store, runtime);
   if(format == GT_SOURCE_FORMAT_CSV)
      return GT_ParseCsvCalendar(raw, config, store, runtime);
   if(format == GT_SOURCE_FORMAT_HTML)
      return GT_ParseHtmlCalendar(raw, config, store, runtime);

   runtime.parser_last_warning = "Unknown source format.";
   GT_RuntimeLog(runtime, GT_LOG_WARNING, runtime.parser_last_warning);
   return false;
}

#endif
