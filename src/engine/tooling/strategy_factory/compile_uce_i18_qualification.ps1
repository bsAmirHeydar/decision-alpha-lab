param(
    [Parameter(Mandatory=$true)][string]$MetaEditorPath,
    [string]$EvidenceDirectory = "",
    [switch]$CompileAllStrategyFactoryExperts
)
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
if (-not (Test-Path -LiteralPath $MetaEditorPath -PathType Leaf)) { throw "MetaEditor executable not found: $MetaEditorPath" }
if (-not $EvidenceDirectory) { $EvidenceDirectory = Join-Path $Root "local_evidence/uce_i18/compile" }
New-Item -ItemType Directory -Force -Path $EvidenceDirectory | Out-Null
$DiagnosticRoot = Join-Path $Root "mql5/Experts/AlphaLab/StrategyFactory/Diagnostics"
$Targets = @(Get-ChildItem -LiteralPath $DiagnosticRoot -Filter "EXP_UCE_I18_*.mq5" -File)
if ($CompileAllStrategyFactoryExperts) {
    $Targets += @(Get-ChildItem (Join-Path $Root "mql5/Experts/AlphaLab/StrategyFactory") -Filter "*.mq5" -File -Recurse)
}
$Targets = $Targets | Sort-Object FullName -Unique
if ($Targets.Count -eq 0) { throw "No UCE-I18 compile targets found." }
$Results = @()
foreach ($Target in $Targets) {
    $SafeName = ($Target.FullName.Substring($Root.Length + 1) -replace '[\/:*?"<>| ]','_')
    $LogPath = Join-Path $EvidenceDirectory ($SafeName + ".log")
    & $MetaEditorPath "/compile:$($Target.FullName)" "/log:$LogPath"
    $ExitCode = $LASTEXITCODE
    if (-not (Test-Path -LiteralPath $LogPath)) { throw "MetaEditor did not produce log for $($Target.FullName)" }
    $LogText = Get-Content -LiteralPath $LogPath -Raw
    $Errors = ([regex]::Matches($LogText,'(?im)\b[1-9][0-9]*\s+errors?\b')).Count
    $Warnings = ([regex]::Matches($LogText,'(?im)\b[1-9][0-9]*\s+warnings?\b')).Count
    $Ex5 = [System.IO.Path]::ChangeExtension($Target.FullName,'.ex5')
    $Results += [ordered]@{
        target = $Target.FullName.Substring($Root.Length + 1).Replace('\','/')
        source_hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $Target.FullName).Hash.ToLowerInvariant()
        compiler_build = (Get-Item -LiteralPath $MetaEditorPath).VersionInfo.FileVersion
        exit_code = $ExitCode
        errors = $Errors
        warnings = $Warnings
        log_hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $LogPath).Hash.ToLowerInvariant()
        output_hash = $(if (Test-Path -LiteralPath $Ex5) { (Get-FileHash -Algorithm SHA256 -LiteralPath $Ex5).Hash.ToLowerInvariant() } else { "0" * 64 })
        compiled_at_utc = [DateTime]::UtcNow.ToString('o')
    }
    if ($ExitCode -ne 0 -or $Errors -ne 0) { throw "Compilation failed: $($Target.FullName). See $LogPath" }
}
$Evidence = [ordered]@{
    schema_version = "1.0.0"
    artifact_id = "uce-i18-metaeditor-compile"
    artifact_hash = "pending_recompute_after_canonicalization"
    metaeditor_path = $MetaEditorPath
    generated_at_utc = [DateTime]::UtcNow.ToString('o')
    targets = $Results
}
$Output = Join-Path $EvidenceDirectory "compile_evidence.external.json"
$Evidence | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $Output -Encoding UTF8
Write-Host $Output
