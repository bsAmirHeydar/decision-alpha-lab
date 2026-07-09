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

color GT_ImpactColor(int impact)
{
   if(impact == GT_IMPACT_HIGH)    return clrTomato;
   if(impact == GT_IMPACT_MEDIUM)  return clrOrange;
   if(impact == GT_IMPACT_LOW)     return clrGold;
   if(impact == GT_IMPACT_HOLIDAY) return clrSilver;
   return clrGray;
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

string GT_SafeObjectName(string prefix, string segment)
{
   string name = prefix + segment;
   StringReplace(name, " ", "_");
   StringReplace(name, ":", "_");
   StringReplace(name, "/", "_");
   StringReplace(name, "\\", "_");
   StringReplace(name, ".", "_");
   return name;
}

#endif
