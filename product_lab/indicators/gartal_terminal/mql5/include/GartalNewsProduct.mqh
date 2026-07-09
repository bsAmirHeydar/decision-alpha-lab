#ifndef GARTAL_NEWS_PRODUCT_MQH
#define GARTAL_NEWS_PRODUCT_MQH

//+------------------------------------------------------------------+
//| Stage 10 Product Hardening Doctrine                              |
//| This module owns release profile, license hook, and packaging     |
//| diagnostics. It does not fetch, parse, render, filter, or alert.  |
//+------------------------------------------------------------------+

string GT_NormalizedChannel(string channel)
{
   string c = GT_ToLower(GT_Trim(channel));
   if(c == "dev" || c == "development") return "dev";
   if(c == "stable" || c == "release" || c == "production") return "stable";
   if(c == "internal" || c == "support") return "internal";
   return "beta";
}

int GT_ChannelId(string channel)
{
   string c = GT_NormalizedChannel(channel);
   if(c == "dev") return GT_RELEASE_CHANNEL_DEV;
   if(c == "stable") return GT_RELEASE_CHANNEL_STABLE;
   if(c == "internal") return GT_RELEASE_CHANNEL_INTERNAL;
   return GT_RELEASE_CHANNEL_BETA;
}

string GT_ChannelText(int channel_id)
{
   if(channel_id == GT_RELEASE_CHANNEL_DEV) return "DEV";
   if(channel_id == GT_RELEASE_CHANNEL_STABLE) return "STABLE";
   if(channel_id == GT_RELEASE_CHANNEL_INTERNAL) return "INTERNAL";
   return "BETA";
}

color GT_ChannelColor(int channel_id)
{
   if(channel_id == GT_RELEASE_CHANNEL_STABLE) return clrLimeGreen;
   if(channel_id == GT_RELEASE_CHANNEL_INTERNAL) return clrDeepSkyBlue;
   if(channel_id == GT_RELEASE_CHANNEL_DEV) return clrGold;
   return clrOrange;
}

string GT_LicenseModeText(int mode)
{
   if(mode == GT_LICENSE_MODE_REQUIRED) return "REQUIRED";
   if(mode == GT_LICENSE_MODE_OPTIONAL) return "OPTIONAL";
   return "OFF";
}

string GT_ProductBadge(GT_Config &config)
{
   return "gartal terminal " + config.product_version + " | " + GT_ChannelText(config.release_channel_id);
}

string GT_ProductBuildSummary(GT_Config &config, GT_RuntimeState &runtime)
{
   string s = GT_ProductBadge(config);
   s += " | profile=" + config.build_profile;
   s += " | license=" + runtime.product_license_status;
   s += " | mode=" + GT_DataModeText(config.data_mode);
   s += " | source=" + runtime.source_quality_text;
   return s;
}

void GT_ApplyReleaseProfile(GT_Config &config, GT_RuntimeState &runtime)
{
   config.release_channel = GT_NormalizedChannel(config.release_channel);
   config.release_channel_id = GT_ChannelId(config.release_channel);

   if(config.strict_release_mode || config.release_channel_id == GT_RELEASE_CHANNEL_STABLE)
   {
      if(config.hide_debug_in_release)
      {
         config.show_time_debug = false;
         config.show_timeline_debug = false;
         config.show_resilience_debug = false;
         config.parser_log_skipped_rows = false;
         config.alert_log_only = false;
      }

      config.dashboard_rows = GT_ClampInt(config.dashboard_rows, 3, config.max_dashboard_rows_release);
      config.dashboard_mode = GT_DASHBOARD_MODE_PRO;
      config.dashboard_show_header = true;
      config.dashboard_show_health_bar = true;
      config.dashboard_show_next_card = true;
      config.dashboard_show_metrics = true;
   }

   runtime.product_version = config.product_version;
   runtime.product_release_channel = GT_ChannelText(config.release_channel_id);
   runtime.product_build_profile = config.build_profile;
   runtime.product_last_gate_at = TimeCurrent();
   runtime.product_release_warnings = 0;
   runtime.product_release_gate_summary = "release profile applied";
   runtime.product_build_summary = GT_ProductBadge(config) + " | profile=" + config.build_profile + " | strict=" + (config.strict_release_mode ? "yes" : "no");
}

bool GT_ProductValidateLicense(GT_Config &config, GT_RuntimeState &runtime)
{
   if(config.license_mode == GT_LICENSE_MODE_OFF && !config.require_license)
   {
      config.license_status_text = "OFF";
      runtime.product_license_status = "OFF";
      return true;
   }

   if(config.license_mode == GT_LICENSE_MODE_OPTIONAL && GT_IsEmpty(config.license_key))
   {
      config.license_status_text = "DEMO";
      runtime.product_license_status = "DEMO";
      runtime.product_release_warnings++;
      runtime.product_release_gate_summary = "optional license missing; running as demo/audit build";
      return true;
   }

   if(GT_IsEmpty(config.license_key))
   {
      config.license_status_text = "MISSING";
      runtime.product_license_status = "MISSING";
      runtime.last_error = "License gate failed: missing license key.";
      return false;
   }

   // Stage 10 hook only. Final cryptographic validation must be implemented in the licensing stage.
   if(StringLen(config.license_key) < 8)
   {
      config.license_status_text = "INVALID";
      runtime.product_license_status = "INVALID";
      runtime.last_error = "License gate failed: license key is too short.";
      return false;
   }

   config.license_status_text = "ACCEPTED";
   runtime.product_license_status = "ACCEPTED";
   return true;
}

#endif
