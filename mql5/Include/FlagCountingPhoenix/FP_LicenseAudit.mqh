#ifndef __FP_LICENSE_AUDIT_MQH__
#define __FP_LICENSE_AUDIT_MQH__
#property strict

#include "FP_LicenseTypes.mqh"

// ============================================================================
// FlagCounting Phoenix - Offline License Audit
// ============================================================================

string FP_LicenseBoolName(const bool v)
{
   return (v ? "true" : "false");
}

void FP_PrintOfflineLicenseReport(const string prefix, const FP_OfflineLicenseReport &r)
{
   string msg = prefix;
   msg += " attempted=" + FP_LicenseBoolName(r.attempted);
   msg += " ok=" + FP_LicenseBoolName(r.ok);
   msg += " status=" + r.status;
   msg += " reason=" + r.reason;
   msg += " enabled=" + FP_LicenseBoolName(r.enabled);
   msg += " fail_closed=" + FP_LicenseBoolName(r.fail_closed);
   msg += " token_parsed=" + FP_LicenseBoolName(r.token_parsed);
   msg += " product_ok=" + FP_LicenseBoolName(r.product_ok);
   msg += " account_ok=" + FP_LicenseBoolName(r.account_ok);
   msg += " server_ok=" + FP_LicenseBoolName(r.server_ok);
   msg += " expiry_ok=" + FP_LicenseBoolName(r.expiry_ok);
   msg += " password_ok=" + FP_LicenseBoolName(r.password_ok);
   msg += " gates_ok=" + FP_LicenseBoolName(r.gates_ok);
   msg += " signature_ok=" + FP_LicenseBoolName(r.signature_ok);
   msg += " expired=" + FP_LicenseBoolName(r.expired);
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

void FP_PrintOfflineLicenseSamples(const string prefix, const FP_OfflineLicenseReport &r)
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

#endif // __FP_LICENSE_AUDIT_MQH__
