#ifndef GARTAL_NEWS_UTILS_MQH
#define GARTAL_NEWS_UTILS_MQH

string GT_Trim(string value)
{
   string result = value;
   StringTrimLeft(result);
   StringTrimRight(result);
   return result;
}

string GT_ToUpper(string value)
{
   string result = value;
   StringToUpper(result);
   return result;
}

string GT_ToLower(string value)
{
   string result = value;
   StringToLower(result);
   return result;
}

bool GT_IsEmpty(string value)
{
   return (StringLen(GT_Trim(value)) == 0);
}

string GT_BoolText(bool value)
{
   return value ? "true" : "false";
}

int GT_ClampInt(int value, int min_value, int max_value)
{
   if(value < min_value) return min_value;
   if(value > max_value) return max_value;
   return value;
}

string GT_DataModeText(int data_mode)
{
   if(data_mode == GT_DATA_MODE_SAMPLE) return "SAMPLE";
   if(data_mode == GT_DATA_MODE_DIRECT) return "DIRECT";
   if(data_mode == GT_DATA_MODE_CACHE)  return "CACHE";
   return "UNKNOWN";
}

string GT_ImpactText(int impact)
{
   if(impact == GT_IMPACT_HIGH)    return "HIGH";
   if(impact == GT_IMPACT_MEDIUM)  return "MED";
   if(impact == GT_IMPACT_LOW)     return "LOW";
   if(impact == GT_IMPACT_HOLIDAY) return "HOL";
   return "NONE";
}

string GT_ImpactDot(int impact)
{
   if(impact == GT_IMPACT_HIGH)    return "RED";
   if(impact == GT_IMPACT_MEDIUM)  return "ORG";
   if(impact == GT_IMPACT_LOW)     return "YLW";
   if(impact == GT_IMPACT_HOLIDAY) return "GRY";
   return "---";
}

int GT_ImpactRank(int impact)
{
   if(impact == GT_IMPACT_HIGH)    return 400;
   if(impact == GT_IMPACT_MEDIUM)  return 300;
   if(impact == GT_IMPACT_LOW)     return 200;
   if(impact == GT_IMPACT_HOLIDAY) return 100;
   return 0;
}

color GT_ImpactColor(int impact)
{
   if(impact == GT_IMPACT_HIGH)    return clrTomato;
   if(impact == GT_IMPACT_MEDIUM)  return clrOrange;
   if(impact == GT_IMPACT_LOW)     return clrGold;
   if(impact == GT_IMPACT_HOLIDAY) return clrSilver;
   return clrGray;
}

string GT_EventStatusText(int status)
{
   if(status == GT_EVENT_UPCOMING) return "UPCOMING";
   if(status == GT_EVENT_ACTIVE)   return "ACTIVE";
   if(status == GT_EVENT_RELEASED) return "RELEASED";
   if(status == GT_EVENT_EXPIRED)  return "EXPIRED";
   return "UNKNOWN";
}

string GT_EventKindText(int kind)
{
   if(kind == GT_EVENT_KIND_ECONOMIC) return "ECON";
   if(kind == GT_EVENT_KIND_SPEECH)   return "SPEECH";
   if(kind == GT_EVENT_KIND_HOLIDAY)  return "HOLIDAY";
   if(kind == GT_EVENT_KIND_BREAKING) return "BREAKING";
   return "OTHER";
}

bool GT_CsvContains(string csv, string needle)
{
   string clean_csv = GT_ToUpper(GT_Trim(csv));
   string clean_needle = GT_ToUpper(GT_Trim(needle));

   if(StringLen(clean_needle) == 0)
      return false;

   string boxed = "," + clean_csv + ",";
   string item  = "," + clean_needle + ",";
   return (StringFind(boxed, item) >= 0);
}

string GT_FormatDateTime(datetime value)
{
   return TimeToString(value, TIME_DATE|TIME_MINUTES);
}

string GT_FormatMinutesRemaining(datetime future_time, datetime now)
{
   int seconds = (int)(future_time - now);
   if(seconds < 0)
      return "passed";

   int minutes = seconds / 60;
   int hours = minutes / 60;
   int rem = minutes % 60;

   if(hours > 0)
      return IntegerToString(hours) + "h " + IntegerToString(rem) + "m";
   return IntegerToString(minutes) + "m";
}

string GT_FormatMinuteOfDay(int minute_of_day)
{
   int clamped = GT_ClampInt(minute_of_day, 0, 1439);
   int h = clamped / 60;
   int m = clamped % 60;
   string hs = (h < 10 ? "0" : "") + IntegerToString(h);
   string ms = (m < 10 ? "0" : "") + IntegerToString(m);
   return hs + ":" + ms;
}

string GT_SafeObjectName(string prefix, string segment)
{
   string name = prefix + segment;
   StringReplace(name, " ", "_");
   StringReplace(name, ":", "_");
   StringReplace(name, "/", "_");
   StringReplace(name, "\\", "_");
   StringReplace(name, ".", "_");
   StringReplace(name, "|", "_");
   StringReplace(name, "%", "pct");
   return name;
}

string GT_CompactTitle(string title, int max_len)
{
   string clean = GT_Trim(title);
   if(StringLen(clean) <= max_len)
      return clean;
   if(max_len <= 3)
      return StringSubstr(clean, 0, max_len);
   return StringSubstr(clean, 0, max_len - 3) + "...";
}

string GT_NormalizeWhitespace(string value)
{
   string result = GT_Trim(value);
   while(StringFind(result, "  ") >= 0)
      StringReplace(result, "  ", " ");
   return result;
}

int GT_OffsetPartsToSeconds(int hours, int minutes)
{
   int sign = 1;
   if(hours < 0 || minutes < 0)
      sign = -1;

   int h = (int)MathAbs((double)hours);
   int m = (int)MathAbs((double)minutes);
   int seconds = sign * ((h * GT_SECONDS_PER_HOUR) + (m * GT_SECONDS_PER_MINUTE));
   return seconds;
}

string GT_TwoDigits(int value)
{
   int v = (int)MathAbs((double)value);
   return (v < 10 ? "0" : "") + IntegerToString(v);
}

string GT_FormatGmtOffsetSeconds(int offset_seconds)
{
   string sign = "+";
   int seconds = offset_seconds;
   if(seconds < 0)
   {
      sign = "-";
      seconds = -seconds;
   }

   int hours = seconds / GT_SECONDS_PER_HOUR;
   int minutes = (seconds % GT_SECONDS_PER_HOUR) / GT_SECONDS_PER_MINUTE;
   return "GMT" + sign + IntegerToString(hours) + ":" + GT_TwoDigits(minutes);
}

string GT_FormatDateWindow(datetime from_time, datetime to_time)
{
   return TimeToString(from_time, TIME_DATE|TIME_MINUTES) + " -> " + TimeToString(to_time, TIME_DATE|TIME_MINUTES);
}

#endif
