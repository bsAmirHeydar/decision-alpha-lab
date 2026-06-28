#ifndef __FP_LICENSE_TYPES_MQH__
#define __FP_LICENSE_TYPES_MQH__
#property strict

// ============================================================================
// FlagCounting Phoenix - Offline License Types
// ----------------------------------------------------------------------------
// Offline, fail-closed, signed-license contract for EX5 distribution.
// This layer is intentionally operational and must never create or reinterpret
// market structure. It only permits or blocks runtime execution.
// ============================================================================

#define FP_LICENSE_CONTRACT_VERSION "1.00"
#define FP_LICENSE_PRODUCT_ID       "FCPHX"
#define FP_LICENSE_TOKEN_PREFIX     "FCPHX1"

struct FP_OfflineLicenseConfig
{
   bool   enabled;
   bool   fail_closed;
   bool   bind_account;
   bool   bind_server;
   bool   require_password;
   bool   require_hidden_gates;
   bool   require_expiry;
   bool   print_sanity;
   bool   print_samples;
   int    check_interval_seconds;
   string product_id;
   string build_id;
   string token;
   string passphrase;
   long   gate_a;
   long   gate_b;
   long   gate_c;
   long   gate_d;
};

struct FP_OfflineLicensePayload
{
   bool   parsed;
   string prefix;
   string product_id;
   long   account_login;
   string server_hash;
   int    expires_yyyymmdd;
   string feature_flags;
   string nonce;
   string sig_a;
   string sig_b;
   string canonical_payload;
};

struct FP_OfflineLicenseReport
{
   bool     attempted;
   bool     ok;
   bool     enabled;
   bool     token_parsed;
   bool     product_ok;
   bool     account_ok;
   bool     server_ok;
   bool     expiry_ok;
   bool     password_ok;
   bool     gates_ok;
   bool     signature_ok;
   bool     fail_closed;
   bool     expired;
   long     account_login;
   string   server;
   string   server_hash;
   string   product_id;
   string   build_id;
   string   feature_flags;
   string   nonce;
   int      expires_yyyymmdd;
   int      now_yyyymmdd;
   int      seconds_until_recheck;
   datetime checked_at;
   datetime expires_at;
   string   status;
   string   reason;
};

void FP_DefaultOfflineLicenseConfig(FP_OfflineLicenseConfig &cfg)
{
   cfg.enabled = true;
   cfg.fail_closed = true;
   cfg.bind_account = true;
   cfg.bind_server = true;
   cfg.require_password = true;
   cfg.require_hidden_gates = true;
   cfg.require_expiry = true;
   cfg.print_sanity = true;
   cfg.print_samples = false;
   cfg.check_interval_seconds = 900;
   cfg.product_id = FP_LICENSE_PRODUCT_ID;
   cfg.build_id = "phoenix_18_licensed";
   cfg.token = "";
   cfg.passphrase = "";
   cfg.gate_a = 0;
   cfg.gate_b = 0;
   cfg.gate_c = 0;
   cfg.gate_d = 0;
}

void FP_ResetOfflineLicensePayload(FP_OfflineLicensePayload &p)
{
   p.parsed = false;
   p.prefix = "";
   p.product_id = "";
   p.account_login = 0;
   p.server_hash = "";
   p.expires_yyyymmdd = 0;
   p.feature_flags = "";
   p.nonce = "";
   p.sig_a = "";
   p.sig_b = "";
   p.canonical_payload = "";
}

void FP_ResetOfflineLicenseReport(FP_OfflineLicenseReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.enabled = true;
   r.token_parsed = false;
   r.product_ok = false;
   r.account_ok = false;
   r.server_ok = false;
   r.expiry_ok = false;
   r.password_ok = false;
   r.gates_ok = false;
   r.signature_ok = false;
   r.fail_closed = true;
   r.expired = false;
   r.account_login = 0;
   r.server = "";
   r.server_hash = "";
   r.product_id = "";
   r.build_id = "";
   r.feature_flags = "";
   r.nonce = "";
   r.expires_yyyymmdd = 0;
   r.now_yyyymmdd = 0;
   r.seconds_until_recheck = 0;
   r.checked_at = 0;
   r.expires_at = 0;
   r.status = "reset";
   r.reason = "reset";
}

#endif // __FP_LICENSE_TYPES_MQH__
