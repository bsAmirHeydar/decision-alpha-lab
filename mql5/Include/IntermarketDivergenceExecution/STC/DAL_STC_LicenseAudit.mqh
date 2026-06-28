#ifndef __DAL_STC_LICENSE_AUDIT_MQH__
#define __DAL_STC_LICENSE_AUDIT_MQH__
#property strict

#include "DAL_STC_LicenseTypes.mqh"

// ============================================================================
// Decision Alpha Lab - STC/SMT Cycles Offline License Audit
// ============================================================================

string STC_LicenseBoolName(const bool v)
{
   return (v ? "true" : "false");
}

void STC_PrintOfflineLicenseReport(const string prefix, const STC_OfflineLicenseReport &r)
{
   string msg = prefix;
   msg += " attempted=" + STC_LicenseBoolName(r.attempted);
   msg += " ok=" + STC_LicenseBoolName(r.ok);
   msg += " status=" + r.status;
   msg += " reason=" + r.reason;
   msg += " enabled=" + STC_LicenseBoolName(r.enabled);
   msg += " fail_closed=" + STC_LicenseBoolName(r.fail_closed);
   msg += " token_parsed=" + STC_LicenseBoolName(r.token_parsed);
   msg += " product_ok=" + STC_LicenseBoolName(r.product_ok);
   msg += " account_ok=" + STC_LicenseBoolName(r.account_ok);
   msg += " server_ok=" + STC_LicenseBoolName(r.server_ok);
   msg += " expiry_ok=" + STC_LicenseBoolName(r.expiry_ok);
   msg += " password_ok=" + STC_LicenseBoolName(r.password_ok);
   msg += " gates_ok=" + STC_LicenseBoolName(r.gates_ok);
   msg += " signature_ok=" + STC_LicenseBoolName(r.signature_ok);
   msg += " expired=" + STC_LicenseBoolName(r.expired);
   msg += " login=" + IntegerToString((long)r.account_login);
   msg += " server_hash=" + r.server_hash;
   msg += " product=" + r.product_id;
   msg += " build=" + r.build_id;
   msg += " feature=" + r.feature_flags;
   msg += " expires=" + IntegerToString(r.expires_yyyymmdd);
   msg += " now=" + IntegerToString(r.now_yyyymmdd);
   msg += " recheck_sec=" + IntegerToString(r.seconds_until_recheck);
   Print(msg);
}

void STC_PrintOfflineLicenseSamples(const string prefix, const STC_OfflineLicenseReport &r)
{
   string msg = prefix;
   msg += " sample=runtime_binding";
   msg += " login=" + IntegerToString((long)r.account_login);
   msg += " server=" + r.server;
   msg += " server_hash=" + r.server_hash;
   msg += " nonce=" + r.nonce;
   msg += " checked_at=" + TimeToString(r.checked_at, TIME_DATE|TIME_SECONDS);
   msg += " expires_at=" + TimeToString(r.expires_at, TIME_DATE|TIME_SECONDS);
   Print(msg);
}

#endif // __DAL_STC_LICENSE_AUDIT_MQH__
