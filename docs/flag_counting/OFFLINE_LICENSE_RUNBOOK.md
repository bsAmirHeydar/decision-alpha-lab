# FlagCounting Phoenix Offline License Runbook

This project now supports a fail-closed offline license layer for EX5 distribution.
The license check runs before Level 01 and again on a timer while the expert is attached.
It does not create, mutate, hide, reveal, confirm, invalidate, lock, or reinterpret market structure.

## Runtime input design

The visible MT5 inputs intentionally do not use obvious license names. The recipient fills these fields:

- `InpPhaseModelProfile` — signed offline token
- `InpRenderMemo` — passphrase/password
- `InpNodeModelSeed` — hidden numeric gate A
- `InpBoundaryModelSeed` — hidden numeric gate B
- `InpValidationModelSeed` — hidden numeric gate C
- `InpReleaseModelSeed` — hidden numeric gate D
- `InpSessionCacheDepth` — recheck interval in minutes

The token binds product, account, optional server hash, expiry date, feature flags, nonce, and signature.
The numeric gates are derived from the same signed payload and password. A copied token without the matching password and four numeric gates fails. A copied bundle on a different account fails when account binding is enabled.

## Token format

```text
FCPHX1|FCPHX|ACCOUNT|SERVER_HASH|YYYYMMDD|FEATURE|NONCE|SIG_A|SIG_B
```

`SERVER_HASH` is the uppercase hash of `AccountInfoString(ACCOUNT_SERVER)`, or `ANY` when server binding is intentionally disabled by the issuer.

## Generate a license bundle

Run from the repository root:

```powershell
python tools/flag_counting/offline_license_keygen.py `
  --account 12345678 `
  --server "Broker-Demo" `
  --expires 20260901
```

For a server-independent license:

```powershell
python tools/flag_counting/offline_license_keygen.py `
  --account 12345678 `
  --server-any `
  --expires 20260901
```

The tool prints exactly the fields that must be given to the recipient.
Keep `tools/flag_counting/offline_license_keygen.py` private. Do not ship it with commercial releases.

## Runtime behavior

The expert is fail-closed:

- missing token blocks `OnInit`
- wrong password blocks `OnInit`
- wrong hidden numeric gates block `OnInit`
- account mismatch blocks `OnInit`
- server mismatch blocks `OnInit` when server binding is active
- expired license blocks `OnInit`
- expiry during runtime stops future scans/redraws

The check uses broker/server time first via `TimeTradeServer()`, then `TimeCurrent()` as fallback. Local Windows time is not used as the authority.

## Security notes

Offline client-side licensing is never mathematically unbreakable because checks run on the client terminal. The goal is practical protection: prevent casual sharing, account copying, wrong-server copying, expired usage, and missing-password usage. Stronger revocation requires an online license server.
