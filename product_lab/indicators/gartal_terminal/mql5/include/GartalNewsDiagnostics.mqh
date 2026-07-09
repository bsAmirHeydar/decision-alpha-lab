#ifndef GARTAL_NEWS_DIAGNOSTICS_MQH
#define GARTAL_NEWS_DIAGNOSTICS_MQH

void GT_ResetRuntime(GT_RuntimeState &runtime)
{
   runtime.boot_at = TimeCurrent();
   runtime.last_timer_at = 0;
   runtime.last_calculate_at = 0;
   runtime.last_refresh_started_at = 0;
   runtime.last_refresh_finished_at = 0;
   runtime.last_refresh_at = 0;
   runtime.last_refresh_ok = false;
   runtime.refresh_attempts = 0;

   runtime.timeline_last_visible_rendered = 0;
   runtime.timeline_last_vertical_lines = 0;
   runtime.timeline_last_labels = 0;
   runtime.timeline_last_zones = 0;
   runtime.timeline_last_render_at = 0;
   runtime.timeline_last_render_summary = "";

   runtime.dashboard_last_objects = 0;
   runtime.dashboard_last_rows = 0;
   runtime.dashboard_last_cards = 0;
   runtime.dashboard_last_render_at = 0;
   runtime.dashboard_last_render_summary = "";

   runtime.filter_change_count = 0;
   runtime.filter_last_change_at = 0;
   runtime.filter_last_action = "";

   runtime.alert_scan_count = 0;
   runtime.alert_last_scanned_events = 0;
   runtime.alert_last_visible_candidates = 0;
   runtime.alert_last_sent_count = 0;
   runtime.alert_last_suppressed_count = 0;
   runtime.alert_last_scan_at = 0;
   runtime.alert_last_sent_at = 0;
   runtime.alert_last_stage = "";
   runtime.alert_last_event_id = "";
   runtime.alert_last_message = "";
   runtime.alert_last_summary = "not scanned";

   runtime.time_normalization_ok = false;
   runtime.time_snapshot_server = 0;
   runtime.time_snapshot_gmt = 0;
   runtime.time_snapshot_local = 0;
   runtime.broker_gmt_detected_hours = 0;
   runtime.broker_gmt_detected_seconds = 0;
   runtime.broker_gmt_effective_seconds = 0;
   runtime.source_gmt_effective_seconds = 0;
   runtime.time_shift_effective_seconds = 0;
   runtime.server_gmt_raw_delta_seconds = 0;
   runtime.broker_gmt_confidence = 0;
   runtime.time_summary = "";

   runtime.source_fetch_status_code = 0;
   runtime.source_raw_bytes = 0;
   runtime.source_fetch_mode_used = GT_FETCH_LOCAL_FILE;
   runtime.source_format_detected = GT_SOURCE_FORMAT_AUTO;
   runtime.source_last_fetch_at = 0;
   runtime.source_last_url = "";
   runtime.source_last_file = "";
   runtime.source_last_error = "";
   runtime.source_permission_hint = "";

   runtime.parser_blocks_seen = 0;
   runtime.parser_events_added = 0;
   runtime.parser_events_skipped = 0;
   runtime.parser_last_run_at = 0;
   runtime.parser_last_summary = "not parsed";
   runtime.parser_last_warning = "";

   runtime.source_last_fetch_attempt_at = 0;
   runtime.source_sanity_event_blocks = 0;
   runtime.source_sanity_fail_count = 0;
   runtime.source_health_score = 0;
   runtime.source_raw_hash = "";
   runtime.source_sanity_summary = "not checked";
   runtime.source_quality_text = "NONE";
   runtime.source_quality = GT_SOURCE_QUALITY_NONE;

   runtime.cache_last_saved_at = 0;
   runtime.cache_last_loaded_at = 0;
   runtime.cache_age_seconds = -1;
   runtime.cache_state = GT_CACHE_STATE_NONE;
   runtime.cache_load_count = 0;
   runtime.cache_save_count = 0;
   runtime.cache_status = "none";
   runtime.cache_last_meta = "";

   runtime.source_using_cache = false;
   runtime.source_using_stale_cache = false;
   runtime.source_using_sample_fallback = false;
   runtime.resilience_failover_count = 0;
   runtime.resilience_last_summary = "not evaluated";

   runtime.product_version = "";
   runtime.product_release_channel = "";
   runtime.product_build_profile = "";
   runtime.product_license_status = "UNVERIFIED";
   runtime.product_build_summary = "not hardened";
   runtime.product_release_gate_summary = "not evaluated";
   runtime.product_last_gate_at = 0;
   runtime.product_release_warnings = 0;

   runtime.last_error = "";
   runtime.last_warning = "";
   runtime.last_info = "";
}

void GT_RuntimeLog(GT_RuntimeState &runtime, int level, string message)
{
   string prefix = "gartal terminal";

   if(level == GT_LOG_ERROR)
   {
      runtime.last_error = message;
      Print(prefix + " ERROR | " + message);
      return;
   }

   if(level == GT_LOG_WARNING)
   {
      runtime.last_warning = message;
      Print(prefix + " WARNING | " + message);
      return;
   }

   runtime.last_info = message;
   Print(prefix + " INFO | " + message);
}

string GT_RuntimeStatusText(GT_RuntimeState &runtime)
{
   if(!GT_IsEmpty(runtime.last_error))
      return "ERROR: " + runtime.last_error;
   if(!GT_IsEmpty(runtime.last_warning))
      return "WARN: " + runtime.last_warning;
   if(!GT_IsEmpty(runtime.last_info))
      return runtime.last_info;
   return "OK";
}

#endif
