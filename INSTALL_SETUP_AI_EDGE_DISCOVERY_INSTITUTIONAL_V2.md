---
title: Install — SAED V2 Institutional AI Edge Discovery Architecture
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- install
---

# Prerequisites

- Apply from the repository root.
- The archive is additive: it adds documentation, schemas, contracts, runbooks and governance artifacts.
- It does **not** modify UCEE engine code or grant production/trading authority.

# PowerShell installation

```powershell
$Zip = Get-ChildItem "$env:USERPROFILE\Downloads" `
    -File `
    -Filter "decision-alpha-lab-setup-ai-edge-discovery-institutional-v2.0.0*.zip" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $Zip) {
    throw "ZIP معماری SAED V2 داخل Downloads پیدا نشد."
}

Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force

Get-Content ".\SAED_V2_FILE_INDEX.txt" |
    Where-Object { $_.Trim() } |
    ForEach-Object { git add -- ":(literal)$_" }

git status --short
git commit -m "docs(strategy-factory): add institutional SAED V2 AI edge discovery architecture"
git push origin main
```

# Start in Obsidian

Open:

`docs/strategy_factory_setup_ai_edge_discovery_institutional_v2/00_START_HERE/00_Home.md`

Then use:

- `MOC_Deep_Design_Blueprints`
- `MOC_Operational_Runbooks`
- `06_Persian_Billion_Dollar_Architecture`
- `SAED_V2_Institutional_Architecture.canvas`

# Integrity

- `SAED_V2_FILE_INDEX.txt` is the exact stage list.
- `SAED_V2_FILE_HASHES.sha256` hashes every package file except the hash ledger itself.
- `SAED_V2_QA_REPORT.json` records validation results.
- `SAED_V2_PATCH_MANIFEST.json` records scope and boundaries.
