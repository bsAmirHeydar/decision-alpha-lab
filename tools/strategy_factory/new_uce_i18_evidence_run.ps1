param([string]$RunId = "")
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
if (-not $RunId) { $RunId = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ') }
if ($RunId -notmatch '^[A-Za-z0-9._-]+$') { throw "RunId contains unsafe characters." }
$RunRoot = Join-Path $Root ("local_evidence/uce_i18/" + $RunId)
if (Test-Path -LiteralPath $RunRoot) { throw "Evidence run already exists: $RunRoot" }
@('00_source','01_environment','02_compile','03_parity','04_tester','05_soak','06_chaos','07_recovery','08_reconciliation','09_security','10_paper','11_shadow','12_micro_live','13_rollback','14_incidents','15_release') | ForEach-Object { New-Item -ItemType Directory -Force -Path (Join-Path $RunRoot $_) | Out-Null }
Copy-Item -LiteralPath (Join-Path $Root 'lab/11_strategy_factory/implementation_program/universal_context_exploitation_engine/v3_implementation/artifacts/uce_i18/external_evidence_template.json') -Destination (Join-Path $RunRoot 'external_evidence_template.json')
$Claims = [ordered]@{
    requested_stage = "paper"
    source_commit = "REQUIRED"
    evaluated_at_ms = 0
    source_integrity_passed = $false
    source_integrity_evidence_hash = ""
    broker_reconciliation_passed = $false
    broker_reconciliation_evidence_hash = ""
    human_approval_id = ""
    human_approval_evidence_hash = ""
    limitations = @()
}
$Claims | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $RunRoot 'claims.template.json') -Encoding UTF8
@"
Normalized evaluator inputs belong at this run root as policy.json, environment.json,
compile.json, parity.json, tester.json, soak.json, chaos.json, recovery.json,
security.json, paper.json, shadow.json, optional live-tier JSON files, rollback.json,
and claims.json. Raw logs and screenshots remain in numbered subdirectories.
"@ | Set-Content -LiteralPath (Join-Path $RunRoot 'README.txt') -Encoding UTF8
Write-Host $RunRoot
