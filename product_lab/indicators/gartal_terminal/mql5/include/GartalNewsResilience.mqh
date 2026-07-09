#ifndef GARTAL_NEWS_RESILIENCE_MQH
#define GARTAL_NEWS_RESILIENCE_MQH

//+------------------------------------------------------------------+
//| Stage 09 Cache / Fallback / Resilience Layer                     |
//| Owns source sanity checks, cache bundle metadata, freshness       |
//| classification, failover accounting, and dashboard health text.   |
//+------------------------------------------------------------------+

string GT_SourceQualityText(int quality)
{
   if(quality == GT_SOURCE_QUALITY_LIVE)        return "LIVE";
   if(quality == GT_SOURCE_QUALITY_CACHE)       return "CACHE";
   if(quality == GT_SOURCE_QUALITY_STALE_CACHE) return "STALE_CACHE";
   if(quality == GT_SOURCE_QUALITY_SAMPLE)      return "SAMPLE_FALLBACK";
   if(quality == GT_SOURCE_QUALITY_FAILED)      return "FAILED";
   return "NONE";
}

string GT_CacheStateText(int state)
{
   if(state == GT_CACHE_STATE_MISS)        return "MISS";
   if(state == GT_CACHE_STATE_FRESH)       return "FRESH";
   if(state == GT_CACHE_STATE_STALE)       return "STALE";
   if(state == GT_CACHE_STATE_EXPIRED)     return "EXPIRED";
   if(state == GT_CACHE_STATE_UNKNOWN_AGE) return "UNKNOWN_AGE";
   return "NONE";
}

string GT_RawHashLite(string raw)
{
   int len = StringLen(raw);
   long acc = 146959810;
   for(int i=0; i<len; i+=13)
   {
      acc = acc ^ StringGetCharacter(raw, i);
      acc = acc * 16777619;
      if(acc < 0)
         acc = -acc;
      acc = acc % 2147483647;
   }
   return IntegerToString((int)acc) + ":" + IntegerToString(len);
}

int GT_CountToken(string raw, string token)
{
   if(GT_IsEmpty(raw) || GT_IsEmpty(token))
      return 0;

   int count = 0;
   int pos = 0;
   while(true)
   {
      int found = StringFind(raw, token, pos);
      if(found < 0)
         break;
      count++;
      pos = found + StringLen(token);
   }
   return count;
}

string GT_MetaGet(string meta, string key)
{
   string needle = key + "=";
   int start = StringFind(meta, needle);
   if(start < 0)
      return "";

   start += StringLen(needle);
   int end = StringFind(meta, "\n", start);
   if(end < 0)
      end = StringLen(meta);

   return GT_Trim(StringSubstr(meta, start, end - start));
}

int GT_MetaGetInt(string meta, string key, int fallback=0)
{
   string value = GT_MetaGet(meta, key);
   if(GT_IsEmpty(value))
      return fallback;
   return (int)StringToInteger(value);
}

bool GT_ResilienceRefreshAllowed(GT_Config &config, GT_RuntimeState &runtime, bool first_load)
{
   datetime now = TimeCurrent();
   if(first_load || config.source_min_refresh_seconds <= 0)
   {
      runtime.source_last_fetch_attempt_at = now;
      return true;
   }

   if(runtime.source_last_fetch_attempt_at > 0)
   {
      int elapsed = (int)(now - runtime.source_last_fetch_attempt_at);
      if(elapsed < config.source_min_refresh_seconds)
      {
         runtime.resilience_last_summary = "refresh throttled: elapsed=" + IntegerToString(elapsed) + "s min=" + IntegerToString(config.source_min_refresh_seconds) + "s";
         runtime.last_warning = runtime.resilience_last_summary;
         return false;
      }
   }

   runtime.source_last_fetch_attempt_at = now;
   return true;
}

bool GT_CheckRawCalendarHealth(string raw, GT_Config &config, GT_RuntimeState &runtime)
{
   int bytes = StringLen(raw);
   runtime.source_raw_bytes = bytes;
   runtime.source_raw_hash = GT_RawHashLite(raw);
   runtime.source_sanity_event_blocks = 0;
   runtime.source_health_score = 0;
   runtime.source_sanity_summary = "";

   if(bytes <= 0)
   {
      runtime.source_sanity_fail_count++;
      runtime.source_sanity_summary = "empty raw payload";
      runtime.source_last_error = runtime.source_sanity_summary;
      return false;
   }

   if(config.source_min_raw_bytes > 0 && bytes < config.source_min_raw_bytes)
   {
      runtime.source_sanity_fail_count++;
      runtime.source_sanity_summary = "raw payload too small: " + IntegerToString(bytes) + " bytes";
      runtime.source_last_error = runtime.source_sanity_summary;
      return false;
   }

   if(config.source_max_raw_bytes > 0 && bytes > config.source_max_raw_bytes)
   {
      runtime.source_sanity_fail_count++;
      runtime.source_sanity_summary = "raw payload too large: " + IntegerToString(bytes) + " bytes";
      runtime.source_last_error = runtime.source_sanity_summary;
      return false;
   }

   int event_blocks = GT_CountToken(raw, "<event>");
   if(event_blocks <= 0)
      event_blocks = GT_CountToken(raw, "<event ");

   runtime.source_sanity_event_blocks = event_blocks;

   if(config.source_require_event_blocks && event_blocks < config.source_min_event_blocks)
   {
      runtime.source_sanity_fail_count++;
      runtime.source_sanity_summary = "event block count below threshold: " + IntegerToString(event_blocks);
      runtime.source_last_error = runtime.source_sanity_summary;
      return false;
   }

   int score = 30;
   if(event_blocks >= config.source_min_event_blocks) score += 40;
   if(StringFind(raw, "<country>") >= 0) score += 10;
   if(StringFind(raw, "<title>") >= 0) score += 10;
   if(StringFind(raw, "<impact>") >= 0) score += 10;

   runtime.source_health_score = GT_ClampInt(score, 0, 100);
   runtime.source_sanity_summary = "ok bytes=" + IntegerToString(bytes) + " events=" + IntegerToString(event_blocks) + " score=" + IntegerToString(runtime.source_health_score) + " hash=" + runtime.source_raw_hash;
   return true;
}

string GT_BuildCacheMeta(GT_Config &config, string raw, GT_RuntimeState &runtime)
{
   datetime now = TimeCurrent();
   string meta = "";
   meta += "product=gartal_terminal\n";
   meta += "stage=09\n";
   meta += "saved_at_epoch=" + IntegerToString((int)now) + "\n";
   meta += "saved_at_text=" + TimeToString(now, TIME_DATE|TIME_SECONDS) + "\n";
   meta += "source_url=" + config.source_url + "\n";
   meta += "source_format=" + GT_SourceFormatText(runtime.source_format_detected) + "\n";
   meta += "raw_bytes=" + IntegerToString(StringLen(raw)) + "\n";
   meta += "raw_hash=" + GT_RawHashLite(raw) + "\n";
   meta += "event_blocks=" + IntegerToString(runtime.source_sanity_event_blocks) + "\n";
   meta += "parser_summary=" + runtime.parser_last_summary + "\n";
   return meta;
}

bool GT_SaveVerifiedCacheBundle(GT_Config &config, string raw, GT_RuntimeState &runtime)
{
   if(!config.use_cache)
      return false;
   if(StringLen(raw) <= 0)
      return false;

   bool raw_ok = GT_WriteTextFile(config.local_cache_file, raw, runtime);
   if(!raw_ok)
      return false;

   runtime.cache_save_count++;
   runtime.cache_last_saved_at = TimeCurrent();
   runtime.cache_state = GT_CACHE_STATE_FRESH;
   runtime.cache_age_seconds = 0;
   runtime.cache_status = "FRESH";

   if(config.cache_write_metadata)
   {
      string meta = GT_BuildCacheMeta(config, raw, runtime);
      runtime.cache_last_meta = meta;
      GT_WriteTextFile(config.cache_metadata_file, meta, runtime);
   }

   GT_RuntimeLog(runtime, GT_LOG_INFO, "Verified cache bundle saved: " + config.local_cache_file);
   return true;
}

bool GT_LoadCacheMetadata(GT_Config &config, GT_RuntimeState &runtime)
{
   runtime.cache_last_meta = "";
   if(!config.cache_write_metadata)
      return false;

   string meta = "";
   if(!GT_ReadTextFile(config.cache_metadata_file, meta, runtime, false))
      return false;

   runtime.cache_last_meta = meta;
   int saved_epoch = GT_MetaGetInt(meta, "saved_at_epoch", 0);
   if(saved_epoch > 0)
      runtime.cache_last_saved_at = (datetime)saved_epoch;

   return true;
}

bool GT_ClassifyLoadedCache(GT_Config &config, GT_RuntimeState &runtime)
{
   datetime now = TimeCurrent();
   runtime.cache_last_loaded_at = now;

   if(runtime.cache_last_saved_at <= 0)
   {
      runtime.cache_state = GT_CACHE_STATE_UNKNOWN_AGE;
      runtime.cache_age_seconds = -1;
      runtime.cache_status = "UNKNOWN_AGE";
      return config.cache_accept_unknown_age;
   }

   runtime.cache_age_seconds = (int)(now - runtime.cache_last_saved_at);
   if(runtime.cache_age_seconds < 0)
      runtime.cache_age_seconds = 0;

   if(runtime.cache_age_seconds <= config.cache_fresh_seconds)
   {
      runtime.cache_state = GT_CACHE_STATE_FRESH;
      runtime.cache_status = "FRESH age=" + IntegerToString(runtime.cache_age_seconds) + "s";
      return true;
   }

   if(runtime.cache_age_seconds <= config.cache_stale_after_seconds)
   {
      runtime.cache_state = GT_CACHE_STATE_STALE;
      runtime.cache_status = "STALE age=" + IntegerToString(runtime.cache_age_seconds) + "s";
      return config.cache_allow_stale;
   }

   if(runtime.cache_age_seconds <= config.cache_max_age_seconds)
   {
      runtime.cache_state = GT_CACHE_STATE_STALE;
      runtime.cache_status = "STALE_MAX age=" + IntegerToString(runtime.cache_age_seconds) + "s";
      return config.cache_allow_stale;
   }

   runtime.cache_state = GT_CACHE_STATE_EXPIRED;
   runtime.cache_status = "EXPIRED age=" + IntegerToString(runtime.cache_age_seconds) + "s";
   return config.cache_allow_expired;
}

bool GT_LoadCacheBundle(GT_Config &config, string &raw, GT_RuntimeState &runtime)
{
   raw = "";
   if(!config.use_cache)
      return false;

   string cached = "";
   if(!GT_ReadTextFile(config.local_cache_file, cached, runtime, false))
   {
      runtime.cache_state = GT_CACHE_STATE_MISS;
      runtime.cache_status = "MISS";
      return false;
   }

   runtime.cache_load_count++;
   GT_LoadCacheMetadata(config, runtime);

   if(!GT_CheckRawCalendarHealth(cached, config, runtime))
   {
      runtime.cache_status = "CACHE_SANITY_FAILED: " + runtime.source_sanity_summary;
      return false;
   }

   bool usable = GT_ClassifyLoadedCache(config, runtime);
   if(!usable)
   {
      GT_RuntimeLog(runtime, GT_LOG_WARNING, "Cache rejected: " + runtime.cache_status);
      return false;
   }

   raw = cached;
   runtime.source_using_cache = true;
   runtime.source_using_stale_cache = (runtime.cache_state == GT_CACHE_STATE_STALE || runtime.cache_state == GT_CACHE_STATE_UNKNOWN_AGE);
   runtime.source_quality = runtime.source_using_stale_cache ? GT_SOURCE_QUALITY_STALE_CACHE : GT_SOURCE_QUALITY_CACHE;
   runtime.source_quality_text = GT_SourceQualityText(runtime.source_quality);
   runtime.resilience_last_summary = "cache accepted: " + runtime.cache_status;
   GT_RuntimeLog(runtime, GT_LOG_INFO, runtime.resilience_last_summary);
   return true;
}

void GT_MarkLiveSource(GT_RuntimeState &runtime)
{
   runtime.source_using_cache = false;
   runtime.source_using_stale_cache = false;
   runtime.source_using_sample_fallback = false;
   runtime.source_quality = GT_SOURCE_QUALITY_LIVE;
   runtime.source_quality_text = GT_SourceQualityText(runtime.source_quality);
   runtime.resilience_last_summary = "live source accepted: " + runtime.source_sanity_summary;
}

void GT_MarkSampleFallback(GT_RuntimeState &runtime)
{
   runtime.source_using_cache = false;
   runtime.source_using_stale_cache = false;
   runtime.source_using_sample_fallback = true;
   runtime.source_quality = GT_SOURCE_QUALITY_SAMPLE;
   runtime.source_quality_text = GT_SourceQualityText(runtime.source_quality);
   runtime.resilience_failover_count++;
   runtime.resilience_last_summary = "sample fallback engaged";
}

void GT_MarkSourceFailed(GT_RuntimeState &runtime)
{
   runtime.source_using_cache = false;
   runtime.source_using_stale_cache = false;
   runtime.source_using_sample_fallback = false;
   runtime.source_quality = GT_SOURCE_QUALITY_FAILED;
   runtime.source_quality_text = GT_SourceQualityText(runtime.source_quality);
   runtime.resilience_last_summary = "source failed: " + runtime.source_last_error;
}

void GT_ApplySourceQualityToStore(GT_NewsStore &store, GT_RuntimeState &runtime)
{
   store.using_cache = runtime.source_using_cache;
   store.using_stale_cache = runtime.source_using_stale_cache;
   store.using_sample_fallback = runtime.source_using_sample_fallback;
   store.source_quality = runtime.source_quality;
   store.source_quality_text = runtime.source_quality_text;

   if(runtime.source_quality == GT_SOURCE_QUALITY_LIVE)
      store.source_status = "LIVE";
   else if(runtime.source_quality == GT_SOURCE_QUALITY_CACHE)
      store.source_status = "CACHE";
   else if(runtime.source_quality == GT_SOURCE_QUALITY_STALE_CACHE)
      store.source_status = "STALE_CACHE";
   else if(runtime.source_quality == GT_SOURCE_QUALITY_SAMPLE)
      store.source_status = "SAMPLE_FALLBACK";
   else if(runtime.source_quality == GT_SOURCE_QUALITY_FAILED)
      store.source_status = "NO DATA";
}

string GT_ResilienceCompactSummary(GT_RuntimeState &runtime)
{
   string txt = "quality=" + runtime.source_quality_text;
   txt += " | cache=" + GT_CacheStateText(runtime.cache_state);
   if(runtime.cache_age_seconds >= 0)
      txt += " age=" + IntegerToString(runtime.cache_age_seconds / 60) + "m";
   txt += " | sanity=" + runtime.source_sanity_summary;
   txt += " | failovers=" + IntegerToString(runtime.resilience_failover_count);
   return txt;
}

#endif
