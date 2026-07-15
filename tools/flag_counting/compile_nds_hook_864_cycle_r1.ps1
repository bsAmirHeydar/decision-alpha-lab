param(
    [string]$MetaEditorPath = "",
    [string]$EvidenceRoot = "local_evidence/nds_hook_864_cycle_r1/metaeditor"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path

if ([string]::IsNullOrWhiteSpace($MetaEditorPath)) {
    $Candidates = @(
        "$env:ProgramFiles\MetaTrader 5\metaeditor64.exe",
        "$env:ProgramFiles\MetaTrader 5\MetaEditor64.exe",
        "${env:ProgramFiles(x86)}\MetaTrader 5\metaeditor64.exe"
    )
    $MetaEditorPath = $Candidates |
        Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } |
        Select-Object -First 1
}

if ([string]::IsNullOrWhiteSpace($MetaEditorPath) -or
    -not (Test-Path -LiteralPath $MetaEditorPath -PathType Leaf)) {
    throw "MetaEditor64.exe not found. Pass -MetaEditorPath explicitly."
}

$Targets = @(
    "mql5/Experts/FlagCounting/NDSHook864CycleR1ContractSelfTest.mq5",
    "mql5/Experts/FlagCounting/NDSHookLimitF123Backtest.mq5",
    "mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5"
)

$OutputRoot = Join-Path $RepoRoot $EvidenceRoot
New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null
$IncludeRoot = Join-Path $RepoRoot "mql5/Include"
$Results = @()

foreach ($RelativePath in $Targets) {
    $SourcePath = Join-Path $RepoRoot $RelativePath
    if (-not (Test-Path -LiteralPath $SourcePath -PathType Leaf)) {
        throw "Compile target missing: $RelativePath"
    }

    $Leaf = [IO.Path]::GetFileNameWithoutExtension($SourcePath)
    $LogPath = Join-Path $OutputRoot ($Leaf + ".compile.log")

    & $MetaEditorPath "/compile:$SourcePath" "/inc:$IncludeRoot" "/log:$LogPath"
    $ExitCode = $LASTEXITCODE

    if (-not (Test-Path -LiteralPath $LogPath -PathType Leaf)) {
        throw "MetaEditor did not produce a compile log: $RelativePath"
    }

    $LogText = Get-Content -LiteralPath $LogPath -Raw
    $Clean = ($ExitCode -eq 0 -and $LogText -match '(?i)0 errors?,\s*0 warnings?')
    $Results += [ordered]@{
        target = $RelativePath
        source_sha256 = (Get-FileHash -LiteralPath $SourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
        log_sha256 = (Get-FileHash -LiteralPath $LogPath -Algorithm SHA256).Hash.ToLowerInvariant()
        exit_code = $ExitCode
        clean_zero_error_zero_warning = $Clean
        compiled_at_utc = [DateTime]::UtcNow.ToString('o')
    }

    if (-not $Clean) {
        throw "MetaEditor compilation is not clean for $RelativePath. Review $LogPath"
    }
}

$Manifest = [ordered]@{
    phase = "NDS-HOOK-864-CYCLE-R1"
    evidence_class = "external_windows_metaeditor_compile"
    activation_allowed = $false
    metaeditor_sha256 = (Get-FileHash -LiteralPath $MetaEditorPath -Algorithm SHA256).Hash.ToLowerInvariant()
    include_root = $IncludeRoot
    results = $Results
}
$ManifestPath = Join-Path $OutputRoot "compile_manifest.json"
$Manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $ManifestPath -Encoding UTF8
Write-Host "NDS Hook 86.4 Cycle R1 MetaEditor compile gate: PASS"
Write-Host $ManifestPath
