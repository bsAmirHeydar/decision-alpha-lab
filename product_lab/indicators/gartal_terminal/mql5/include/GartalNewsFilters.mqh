#ifndef GARTAL_NEWS_FILTERS_MQH
#define GARTAL_NEWS_FILTERS_MQH

//+------------------------------------------------------------------+
//| Stage 06 Runtime Filter Engine                                   |
//| Owns mutable dashboard filter state. The dashboard renders buttons|
//| and forwards click object names here; this module mutates state.   |
//+------------------------------------------------------------------+

string GT_FilterPrefix(GT_Config &config)
{
   return config.object_prefix + "DASH_FLT_";
}

string GT_FilterStateText(bool enabled)
{
   return enabled ? "ON" : "OFF";
}

string GT_FilterButtonText(string label, bool enabled)
{
   return label + " " + GT_FilterStateText(enabled);
}

string GT_NormalizeCurrencyCsv(string csv)
{
   string parts[];
   string result = "";
   int n = StringSplit(csv, ',', parts);
   for(int i=0; i<n; i++)
   {
      string c = GT_ToUpper(GT_Trim(parts[i]));
      if(StringLen(c) == 0)
         continue;
      if(StringLen(c) > 6)
         c = StringSubstr(c, 0, 6);
      if(GT_CsvContains(result, c))
         continue;
      if(StringLen(result) > 0)
         result += ",";
      result += c;
   }
   return result;
}

string GT_CsvRemoveItem(string csv, string item)
{
   string parts[];
   string result = "";
   string needle = GT_ToUpper(GT_Trim(item));
   int n = StringSplit(csv, ',', parts);
   for(int i=0; i<n; i++)
   {
      string c = GT_ToUpper(GT_Trim(parts[i]));
      if(StringLen(c) == 0)
         continue;
      if(c == needle)
         continue;
      if(GT_CsvContains(result, c))
         continue;
      if(StringLen(result) > 0)
         result += ",";
      result += c;
   }
   return result;
}

string GT_CsvAddItem(string csv, string item)
{
   string clean = GT_NormalizeCurrencyCsv(csv);
   string needle = GT_ToUpper(GT_Trim(item));
   if(StringLen(needle) == 0)
      return clean;
   if(GT_CsvContains(clean, needle))
      return clean;
   if(StringLen(clean) > 0)
      clean += ",";
   clean += needle;
   return clean;
}

bool GT_ToggleCsvItem(string &csv, string item)
{
   string clean = GT_NormalizeCurrencyCsv(csv);
   if(GT_CsvContains(clean, item))
      csv = GT_CsvRemoveItem(clean, item);
   else
      csv = GT_CsvAddItem(clean, item);
   return true;
}

void GT_ResetRuntimeFiltersToConfig(GT_FilterState &filters, GT_Config &config)
{
   GT_InitFilterState(filters, config);
}

string GT_FilterSummary(GT_FilterState &filters)
{
   string impacts = "";
   if(filters.show_high) impacts += "RED ";
   if(filters.show_medium) impacts += "ORG ";
   if(filters.show_low) impacts += "YLW ";
   if(filters.show_holiday) impacts += "HOL ";
   if(GT_IsEmpty(impacts)) impacts = "none";

   string special = "";
   if(filters.show_speech) special += "speech ";
   if(filters.show_breaking) special += "breaking ";
   if(filters.show_tentative) special += "tentative ";
   if(filters.only_symbol) special += "symbol-only ";
   if(GT_IsEmpty(special)) special = "standard";

   return "impacts=" + GT_Trim(impacts) + " | special=" + GT_Trim(special) + " | ccy=" + GT_CompactTitle(filters.currencies_csv, 52);
}

string GT_FilterTooltip(GT_FilterState &filters)
{
   return "gartal terminal filters | " + GT_FilterSummary(filters);
}

bool GT_ObjectNameHas(string object_name, string token)
{
   return (StringFind(object_name, token) >= 0);
}

bool GT_HandleImpactFilterClick(string object_name, GT_FilterState &filters)
{
   if(GT_ObjectNameHas(object_name, "FLT_HIGH"))
   {
      filters.show_high = !filters.show_high;
      return true;
   }
   if(GT_ObjectNameHas(object_name, "FLT_MEDIUM"))
   {
      filters.show_medium = !filters.show_medium;
      return true;
   }
   if(GT_ObjectNameHas(object_name, "FLT_LOW"))
   {
      filters.show_low = !filters.show_low;
      return true;
   }
   if(GT_ObjectNameHas(object_name, "FLT_HOLIDAY"))
   {
      filters.show_holiday = !filters.show_holiday;
      return true;
   }
   return false;
}

bool GT_HandleSpecialFilterClick(string object_name, GT_FilterState &filters)
{
   if(GT_ObjectNameHas(object_name, "FLT_SPEECH"))
   {
      filters.show_speech = !filters.show_speech;
      return true;
   }
   if(GT_ObjectNameHas(object_name, "FLT_BREAKING"))
   {
      filters.show_breaking = !filters.show_breaking;
      return true;
   }
   if(GT_ObjectNameHas(object_name, "FLT_TENTATIVE"))
   {
      filters.show_tentative = !filters.show_tentative;
      return true;
   }
   if(GT_ObjectNameHas(object_name, "FLT_PAST"))
   {
      filters.show_past_events = !filters.show_past_events;
      return true;
   }
   if(GT_ObjectNameHas(object_name, "FLT_SYMBOL"))
   {
      filters.only_symbol = !filters.only_symbol;
      return true;
   }
   return false;
}

bool GT_HandleCurrencyFilterClick(string object_name, GT_FilterState &filters)
{
   string tokens[9] = {"USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "NZD", "CNY"};
   for(int i=0; i<9; i++)
   {
      string token = "FLT_CCY_" + tokens[i];
      if(GT_ObjectNameHas(object_name, token))
      {
         GT_ToggleCsvItem(filters.currencies_csv, tokens[i]);
         return true;
      }
   }
   return false;
}

bool GT_HandleUtilityFilterClick(string object_name, GT_FilterState &filters, GT_Config &config)
{
   if(GT_ObjectNameHas(object_name, "FLT_ALL_IMPACT"))
   {
      filters.show_high = true;
      filters.show_medium = true;
      filters.show_low = true;
      filters.show_holiday = true;
      return true;
   }
   if(GT_ObjectNameHas(object_name, "FLT_RED_ONLY"))
   {
      filters.show_high = true;
      filters.show_medium = false;
      filters.show_low = false;
      filters.show_holiday = false;
      return true;
   }
   if(GT_ObjectNameHas(object_name, "FLT_MAJOR_CCY"))
   {
      filters.currencies_csv = "USD,EUR,GBP,JPY,CHF,CAD,AUD,NZD,CNY";
      return true;
   }
   if(GT_ObjectNameHas(object_name, "FLT_RESET"))
   {
      GT_ResetRuntimeFiltersToConfig(filters, config);
      return true;
   }
   return false;
}

bool GT_HandleRuntimeFilterClick(string object_name, GT_FilterState &filters, GT_Config &config, GT_RuntimeState &runtime)
{
   if(!config.dashboard_enable_click_filters)
      return false;

   bool changed = false;
   changed = changed || GT_HandleImpactFilterClick(object_name, filters);
   changed = changed || GT_HandleSpecialFilterClick(object_name, filters);

   if(config.dashboard_enable_currency_toggles)
      changed = changed || GT_HandleCurrencyFilterClick(object_name, filters);

   changed = changed || GT_HandleUtilityFilterClick(object_name, filters, config);

   if(changed)
   {
      filters.currencies_csv = GT_NormalizeCurrencyCsv(filters.currencies_csv);
      runtime.filter_last_change_at = TimeCurrent();
      runtime.filter_change_count++;
      runtime.filter_last_action = "click=" + object_name + " | " + GT_FilterSummary(filters);
      GT_RuntimeLog(runtime, GT_LOG_INFO, "Runtime filter changed: " + GT_FilterSummary(filters));
   }

   return changed;
}

#endif
