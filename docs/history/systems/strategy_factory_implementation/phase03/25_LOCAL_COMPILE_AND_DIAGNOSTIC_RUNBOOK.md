---
title: "Local Compile and Diagnostic Runbook"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Prerequisites

- MetaEditor64 path;
- target terminal MQL5 root;
- Phase 01 and Phase 02 installed;
- Phase 03 patch extracted.

# Automated compile

Run:

```powershell
powershell -ExecutionPolicy Bypass `
  -File .\tools\strategy_factory\compile_sf03_market_services.ps1 `
  -MetaEditorPath "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  -TerminalMql5Root "C:\Users\<USER>\AppData\Roaming\MetaQuotes\Terminal\<INSTANCE>\MQL5"
```

# Required results

- self-test compile: 0 errors;
- diagnostic compile: 0 errors;
- self-test `OnInit`: success;
- no unexpected source errors.

# Diagnostic sequence

1. Run on the primary chart symbol.
2. Set the explicit broker UTC offset.
3. Confirm latest closed-bar UTC time.
4. Confirm specification generation and tick size.
5. Test one prefixed/suffixed symbol.
6. Test the intended intermarket pair.
7. Disconnect/reconnect and verify recovery behavior.
8. Change timeframe and verify no duplicate new-bar identity.

# Evidence

Save compile logs and terminal journal excerpts under a local acceptance artifact. Do not promote the phase based only on static scans.
