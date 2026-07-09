#ifndef GARTAL_NEWS_SAMPLE_DATA_MQH
#define GARTAL_NEWS_SAMPLE_DATA_MQH

void GT_AddSampleAt(GT_NewsStore &store,
                    GT_Config &config,
                    int day_offset,
                    int hour,
                    int minute,
                    string currency,
                    int impact,
                    string title,
                    string actual,
                    string forecast,
                    string previous,
                    bool breaking=false,
                    string notes="")
{
   datetime t = GT_ConfiguredSampleBrokerTime(config, day_offset, hour, minute);
   string source_tag = "sample_stage03_" + GT_SampleTimeModeText(config.sample_time_mode);
   GT_AddEventEx(store, config, t, currency, impact, title, actual, forecast, previous, source_tag, breaking, notes);
}

bool GT_LoadSampleEvents(GT_NewsStore &store, GT_Config &config, GT_RuntimeState &runtime)
{
   GT_ResetStore(store);
   store.sample_profile = "stage03_time_normalized_macro_tape";

   // Previous day events exist to validate DaysBack and past-event filters.
   GT_AddSampleAt(store, config, -1, 10,  0, "EUR", GT_IMPACT_MEDIUM,  "German Flash Manufacturing PMI", "49.4", "48.9", "48.8");
   GT_AddSampleAt(store, config, -1, 15, 30, "USD", GT_IMPACT_HIGH,    "Core Retail Sales m/m", "0.3%", "0.2%", "0.1%");

   // Current day tape: deliberately mixed by impact, type, status, and currency.
   GT_AddSampleAt(store, config,  0,  1, 50, "JPY", GT_IMPACT_LOW,     "Monetary Base y/y", "0.6%", "", "0.4%");
   GT_AddSampleAt(store, config,  0,  3, 30, "AUD", GT_IMPACT_MEDIUM,  "Retail Sales m/m", "", "0.3%", "0.1%");
   GT_AddSampleAt(store, config,  0,  5, 45, "CNY", GT_IMPACT_MEDIUM,  "Caixin Services PMI", "", "52.8", "52.5");
   GT_AddSampleAt(store, config,  0,  8, 00, "CHF", GT_IMPACT_LOW,     "SECO Consumer Climate", "", "", "-36");
   GT_AddSampleAt(store, config,  0,  9, 15, "EUR", GT_IMPACT_MEDIUM,  "Spanish Services PMI", "", "56.4", "56.2");
   GT_AddSampleAt(store, config,  0, 10, 00, "EUR", GT_IMPACT_MEDIUM,  "ECB President Speaks", "", "", "", false, "speech classification sample");
   GT_AddSampleAt(store, config,  0, 10, 30, "GBP", GT_IMPACT_MEDIUM,  "Construction PMI", "", "54.1", "54.0");
   GT_AddSampleAt(store, config,  0, 12, 30, "GBP", GT_IMPACT_MEDIUM,  "BOE Gov Bailey Speaks", "", "", "", false, "speech classification sample");
   GT_AddSampleAt(store, config,  0, 13, 45, "USD", GT_IMPACT_LOW,     "Final Services PMI", "", "55.3", "55.3");
   GT_AddSampleAt(store, config,  0, 15, 30, "USD", GT_IMPACT_HIGH,    "CPI m/m", "", "0.2%", "0.1%");
   GT_AddSampleAt(store, config,  0, 15, 30, "USD", GT_IMPACT_HIGH,    "Core CPI m/m", "", "0.3%", "0.2%");
   GT_AddSampleAt(store, config,  0, 16, 30, "USD", GT_IMPACT_MEDIUM,  "Unemployment Claims", "", "235K", "233K");
   GT_AddSampleAt(store, config,  0, 17, 00, "CAD", GT_IMPACT_MEDIUM,  "Ivey PMI", "", "", "52.0");
   GT_AddSampleAt(store, config,  0, 17, 00, "USD", GT_IMPACT_HIGH,    "Fed Chair Press Conference", "", "", "", false, "high-impact speech sample");
   GT_AddSampleAt(store, config,  0, 19, 00, "USD", GT_IMPACT_HIGH,    "Unscheduled Presidential Remarks", "", "", "", true, "breaking red-news sample");
   GT_AddSampleAt(store, config,  0, 23, 45, "NZD", GT_IMPACT_MEDIUM,  "FPI m/m", "", "", "0.5%");

   // Holiday and tentative cases.
   GT_AddSampleAt(store, config,  0,  0,  0, "JPY", GT_IMPACT_HOLIDAY, "Bank Holiday", "", "", "");
   GT_AddSampleAt(store, config,  0, 18, 20, "USD", GT_IMPACT_MEDIUM,  "Treasury Currency Report Tentative", "", "", "");

   // Tomorrow events exist to validate DaysForward.
   GT_AddSampleAt(store, config,  1,  9, 00, "EUR", GT_IMPACT_MEDIUM,  "French Trade Balance", "", "-6.9B", "-7.1B");
   GT_AddSampleAt(store, config,  1, 15, 30, "USD", GT_IMPACT_HIGH,    "Non-Farm Employment Change", "", "189K", "175K");
   GT_AddSampleAt(store, config,  1, 15, 30, "USD", GT_IMPACT_HIGH,    "Unemployment Rate", "", "4.0%", "4.0%");

   store.source_ok = true;
   store.source_status = "SAMPLE_STAGE02";
   store.last_refresh = TimeCurrent();

   GT_RuntimeLog(runtime, GT_LOG_INFO, "Stage 03 time-normalized sample pipeline loaded. count=" + IntegerToString(store.count));
   return (store.count > 0);
}

#endif
