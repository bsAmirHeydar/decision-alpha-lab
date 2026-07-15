param(
    [Parameter(Mandatory=$true)][string]$MetaEditorPath,
    [string]$EvidenceRoot = "local_evidence/uce_i19/metaeditor"
)
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
if (-not (Test-Path -LiteralPath $MetaEditorPath -PathType Leaf)) { throw "MetaEditor not found: $MetaEditorPath" }
$Targets = @(
    "mql5/Experts/AlphaLab/StrategyFactory/Diagnostics/EXP_UCE_I19_FailClosedCycleSelfTest.mq5",
    "mql5/Experts/AlphaLab/StrategyFactory/Diagnostics/EXP_UCE_I19_LeaseExpirySelfTest.mq5",
    "mql5/Experts/AlphaLab/StrategyFactory/Diagnostics/EXP_UCE_I19_ReconciliationSelfTest.mq5",
    "mql5/Experts/AlphaLab/StrategyFactory/Diagnostics/EXP_UCE_I19_RampAndRetirementSelfTest.mq5"
)
$Out = Join-Path $Root $EvidenceRoot
New-Item -ItemType Directory -Force -Path $Out | Out-Null
$Results = @()
foreach ($Relative in $Targets) {
    $Source = Join-Path $Root $Relative
    if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) { throw "Missing source: $Relative" }
    $Name = [IO.Path]::GetFileNameWithoutExtension($Source)
    $Log = Join-Path $Out ($Name + ".compile.log")
    & $MetaEditorPath "/compile:$Source" "/log:$Log"
    $Exit = $LASTEXITCODE
    if (-not (Test-Path -LiteralPath $Log)) { throw "Compile log missing: $Log" }
    $Text = Get-Content -LiteralPath $Log -Raw
    $ErrorCount = ([regex]::Matches($Text, '(?im)^.*\berror\b.*$')).Count
    $WarningCount = ([regex]::Matches($Text, '(?im)^.*\bwarning\b.*$')).Count
    $Results += [ordered]@{
        target = $Relative
        source_hash = (Get-FileHash -LiteralPath $Source -Algorithm SHA256).Hash.ToLowerInvariant()
        log_hash = (Get-FileHash -LiteralPath $Log -Algorithm SHA256).Hash.ToLowerInvariant()
        exit_code = $Exit
        errors = $ErrorCount
        warnings = $WarningCount
        compiled_at_utc = [DateTime]::UtcNow.ToString('o')
    }
    if ($Exit -ne 0 -or $ErrorCount -ne 0) { throw "MetaEditor compilation failed: $Relative" }
}
$Manifest = [ordered]@{
    phase_id = 'UCE-I19'
    authority_order = $false
    evidence_class = 'external_metaeditor_compile'
    metaeditor_path_hash = (Get-FileHash -LiteralPath $MetaEditorPath -Algorithm SHA256).Hash.ToLowerInvariant()
    results = $Results
}
$Manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $Out 'uce_i19_compile_manifest.json') -Encoding UTF8
