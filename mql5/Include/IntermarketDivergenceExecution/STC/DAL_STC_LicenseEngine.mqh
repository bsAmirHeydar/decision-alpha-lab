#ifndef __DAL_STC_LICENSE_ENGINE_MQH__
#define __DAL_STC_LICENSE_ENGINE_MQH__
#property strict

#include "DAL_STC_LicenseCrypto.mqh"
#include "DAL_STC_LicenseAudit.mqh"

// ============================================================================
// Decision Alpha Lab - STC/SMT Cycles Offline License Engine
// ----------------------------------------------------------------------------
// Public facade: STC_CheckOfflineLicenseWithReport.
// The engine is fail-closed by default and must run before strategy init/pulse.
// ============================================================================

bool STC_LicIsBlank(const string s)
{
   string x = s;
   StringTrimLeft(x);
   StringTrimRight(x);
   return (StringLen(x) <= 0);
}

int STC_LicDateInt(const datetime t)
{
   if(t <= 0)
      return 0;
   MqlDateTime dt;
   TimeToStruct(t, dt);
   return dt.year * 10000 + dt.mon * 100 + dt.day;
}

datetime STC_LicDateFromInt(const int yyyymmdd)
{
   int y = yyyymmdd / 10000;
   int m = (yyyymmdd / 100) % 100;
   int d = yyyymmdd % 100;
   if(y < 2000 || y > 2099 || m < 1 || m > 12 || d < 1 || d > 31)
      return 0;
   MqlDateTime dt;
   dt.year = y;
   dt.mon = m;
   dt.day = d;
   dt.hour = 23;
   dt.min = 59;
   dt.sec = 59;
   return StructToTime(dt);
}

bool STC_ParseOfflineLicenseToken(const string token, STC_OfflineLicensePayload &p)
{
   STC_ResetOfflineLicensePayload(p);
   string t = token;
   StringTrimLeft(t);
   StringTrimRight(t);
   if(StringLen(t) <= 0)
      return false;

   string parts[];
   ushort sep = StringGetCharacter("|", 0);
   int n = StringSplit(t, sep, parts);
   if(n != 9)
      return false;

   for(int i=0; i<n; i++)
   {
      StringTrimLeft(parts[i]);
      StringTrimRight(parts[i]);
   }

   p.prefix = STC_LicUpperTrim(parts[0]);
   p.product_id = STC_LicUpperTrim(parts[1]);
   p.account_login = (long)StringToInteger(parts[2]);
   p.server_hash = STC_LicUpperTrim(parts[3]);
   p.expires_yyyymmdd = (int)StringToInteger(parts[4]);
   p.feature_flags = STC_LicUpperTrim(parts[5]);
   p.nonce = STC_LicUpperTrim(parts[6]);
   p.sig_a = STC_LicUpperTrim(parts[7]);
   p.sig_b = STC_LicUpperTrim(parts[8]);

   p.canonical_payload = p.prefix + "|" + p.product_id + "|" + IntegerToString((long)p.account_login) + "|" +
                         p.server_hash + "|" + IntegerToString(p.expires_yyyymmdd) + "|" +
                         p.feature_flags + "|" + p.nonce;

   p.parsed = (p.prefix == STC_LICENSE_TOKEN_PREFIX && p.product_id == STC_LICENSE_PRODUCT_ID && p.expires_yyyymmdd > 0);
   return p.parsed;
}

bool STC_OfflineLicenseTime(datetime &now, int &now_yyyymmdd)
{
   now = TimeTradeServer();
   if(now <= 0)
      now = TimeCurrent();
   if(now <= 0)
      return false;
   now_yyyymmdd = STC_LicDateInt(now);
   return (now_yyyymmdd > 0);
}

bool STC_CheckOfflineLicenseWithReport(const STC_OfflineLicenseConfig &cfg,
                                       STC_OfflineLicenseReport &report)
{
   STC_ResetOfflineLicenseReport(report);
   report.attempted = true;
   report.enabled = cfg.enabled;
   report.fail_closed = cfg.fail_closed;
   report.product_id = cfg.product_id;
   report.build_id = cfg.build_id;
   report.account_login = (long)AccountInfoInteger(ACCOUNT_LOGIN);
   report.server = AccountInfoString(ACCOUNT_SERVER);
   report.server_hash = STC_LicServerHash(report.server);
   int recheck_sec = cfg.check_interval_seconds;
   if(recheck_sec < 60)
      recheck_sec = 60;
   report.seconds_until_recheck = recheck_sec;

   if(!cfg.enabled)
   {
      report.ok = !cfg.fail_closed;
      report.status = (report.ok ? "disabled_open" : "disabled_closed");
      report.reason = report.status;
      return report.ok;
   }

   STC_OfflineLicensePayload p;
   report.token_parsed = STC_ParseOfflineLicenseToken(cfg.token, p);
   if(!report.token_parsed)
   {
      report.status = "blocked";
      report.reason = "license_token_parse_failed";
      return false;
   }

   report.feature_flags = p.feature_flags;
   report.nonce = p.nonce;
   report.expires_yyyymmdd = p.expires_yyyymmdd;
   report.expires_at = STC_LicDateFromInt(p.expires_yyyymmdd);
   report.licensed_account_login = p.account_login;
   report.licensed_server_hash = p.server_hash;
   report.account_any = (p.account_login == 0);
   report.server_any = (p.server_hash == "ANY");

   report.product_ok = (p.product_id == cfg.product_id && p.prefix == STC_LICENSE_TOKEN_PREFIX);

   report.account_ok = true;
   if(cfg.bind_account)
      report.account_ok = ((p.account_login == 0) || (p.account_login == report.account_login));

   report.server_ok = true;
   if(cfg.bind_server)
      report.server_ok = (p.server_hash == "ANY" || p.server_hash == report.server_hash);

   report.password_ok = true;
   if(cfg.require_password)
      report.password_ok = !STC_LicIsBlank(cfg.passphrase);

   datetime now;
   int now_i = 0;
   bool time_ok = STC_OfflineLicenseTime(now, now_i);
   report.checked_at = now;
   report.now_yyyymmdd = now_i;
   report.expiry_ok = true;
   report.expired = false;
   if(cfg.require_expiry)
   {
      report.expiry_ok = (time_ok && report.expires_at > 0 && now <= report.expires_at);
      report.expired = (time_ok && report.expires_at > 0 && now > report.expires_at);
   }

   string expected_a, expected_b;
   STC_LicSignatures(p.canonical_payload, cfg.passphrase, expected_a, expected_b);
   report.signature_ok = (p.sig_a == expected_a && p.sig_b == expected_b);

   report.gates_ok = true;
   if(cfg.require_hidden_gates)
   {
      long ga = STC_LicGateValue(p.canonical_payload, cfg.passphrase, 1);
      long gb = STC_LicGateValue(p.canonical_payload, cfg.passphrase, 2);
      long gc = STC_LicGateValue(p.canonical_payload, cfg.passphrase, 3);
      long gd = STC_LicGateValue(p.canonical_payload, cfg.passphrase, 4);
      report.gates_ok = (cfg.gate_a == ga && cfg.gate_b == gb && cfg.gate_c == gc && cfg.gate_d == gd);
   }

   report.ok = (report.product_ok && report.account_ok && report.server_ok && report.expiry_ok &&
                report.password_ok && report.signature_ok && report.gates_ok);
   report.status = (report.ok ? "active" : "blocked");

   if(report.ok)
      report.reason = "license_active";
   else if(!report.product_ok)
      report.reason = "product_mismatch";
   else if(!report.account_ok)
      report.reason = "account_mismatch";
   else if(!report.server_ok)
      report.reason = "server_mismatch";
   else if(!report.expiry_ok)
      report.reason = (report.expired ? "expired" : "expiry_time_unavailable");
   else if(!report.password_ok)
      report.reason = "passphrase_missing";
   else if(!report.signature_ok)
      report.reason = "signature_mismatch";
   else if(!report.gates_ok)
      report.reason = "hidden_gate_mismatch";
   else
      report.reason = "unknown_block";

   return report.ok;
}

#endif // __DAL_STC_LICENSE_ENGINE_MQH__
