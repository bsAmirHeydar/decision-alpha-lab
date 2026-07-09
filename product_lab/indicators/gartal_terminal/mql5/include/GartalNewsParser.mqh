#ifndef GARTAL_NEWS_PARSER_MQH
#define GARTAL_NEWS_PARSER_MQH

bool GT_ParseCalendar(string raw, GT_Config &config, GT_NewsStore &store, GT_RuntimeState &runtime)
{
   // Stage 03 parser contract:
   // The event model and store pipeline are now production-shaped, but the real
   // Forex Factory HTML parser is still intentionally deferred to Stage 08.
   if(config.data_mode == GT_DATA_MODE_SAMPLE)
      return GT_LoadSampleEvents(store, config, runtime);

   GT_RuntimeLog(runtime, GT_LOG_WARNING, "Production parser is not implemented in Stage 03. Time-normalized event store is ready; direct Forex Factory parser begins in Stage 08.");
   return false;
}

#endif
