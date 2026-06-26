$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$LogDir = Join-Path $ProjectRoot "lab\03_experiments\EXP0013_astro_feature_store\compile_logs"

function Find-MetaEditor {
    $candidates = Get-ChildItem "C:\Program Files\Meta" -Directory -ErrorAction SilentlyContinue |
        Sort-Object Name |
        ForEach-Object { Join-Path $_.FullName "MetaEditor64.exe" }

    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate) {
            return $candidate
        }
    }

    throw "MetaEditor64.exe not found under C:\Program Files\Meta"
}

function Get-ExpectedArtifactPath {
    param(
        [string]$ProjectRoot,
        [string]$SourceFile
    )

    $sharedProjectsMarker = "\MQL5\Shared Projects\"
    $idx = $ProjectRoot.IndexOf($sharedProjectsMarker)
    if ($idx -lt 0) {
        return ""
    }

    $terminalRoot = $ProjectRoot.Substring(0, $idx)
    $repoName = Split-Path $ProjectRoot -Leaf
    $projectUri = New-Object System.Uri(($ProjectRoot.TrimEnd('\') + '\'))
    $sourceUri = New-Object System.Uri($SourceFile)
    $relativeSource = [System.Uri]::UnescapeDataString($projectUri.MakeRelativeUri($sourceUri).ToString()).Replace('/', '\')
    $artifactRelative = [System.IO.Path]::ChangeExtension($relativeSource, ".ex5")
    return Join-Path $terminalRoot ("MQL5\Experts\Shared Projects\" + $repoName + "\" + $artifactRelative)
}

function Invoke-MetaCompile {
    param(
        [string]$ProjectRoot,
        [string]$MetaEditor,
        [string]$SourceFile,
        [string]$LogFile
    )

    if (!(Test-Path -LiteralPath $SourceFile)) {
        throw "Source file not found: $SourceFile"
    }

    $arguments = @("/compile:$SourceFile", "/log:$LogFile")
    $proc = Start-Process -FilePath $MetaEditor -ArgumentList $arguments -PassThru -Wait -WindowStyle Hidden

    $status = [ordered]@{
        source = $SourceFile
        exit_code = $proc.ExitCode
        log_file = $LogFile
        log_exists = (Test-Path -LiteralPath $LogFile)
        artifact_file = (Get-ExpectedArtifactPath -ProjectRoot $ProjectRoot -SourceFile $SourceFile)
        artifact_exists = $false
        errors = @()
        warnings = @()
    }

    if ($status.artifact_file -ne "") {
        $status.artifact_exists = Test-Path -LiteralPath $status.artifact_file
    }

    if ($status.log_exists) {
        $lines = Get-Content -LiteralPath $LogFile -ErrorAction SilentlyContinue
        foreach ($line in $lines) {
            if ($line -match "\berror\b") { $status.errors += $line }
            if ($line -match "\bwarning\b") { $status.warnings += $line }
        }
    }

    [pscustomobject]$status
}

Push-Location $ProjectRoot
try {
    New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
    $metaEditor = Find-MetaEditor

    $targets = @(
        "mql5\Experts\Research\EXP0013_AstroUnifiedDashboardEA.mq5",
        "mql5\Experts\AstroExecution\A0001_AstroTransitTrendPulse.mq5",
        "mql5\Experts\AstroExecution\A0002_AstroNatalResonanceExecutor.mq5",
        "mql5\Experts\AstroExecution\A0003_AstroFrictionPolarityExecutor.mq5",
        "mql5\Experts\AstroExecution\A0004_AstroSectBeneficPressureExecutor.mq5",
        "mql5\Experts\AstroExecution\A0005_AstroMoonTimingWindowExecutor.mq5",
        "mql5\Experts\AstroExecution\A0006_AstroAngularActivationExecutor.mq5",
        "mql5\Experts\AstroExecution\A0007_AstroStationTransitionExecutor.mq5",
        "mql5\Experts\AstroExecution\A0090_AstroOrderShell.mq5"
    )

    $results = @()
    foreach ($target in $targets) {
        $sourceFile = Join-Path $ProjectRoot $target
        $logFile = Join-Path $LogDir ((Split-Path $target -Leaf) + ".log")
        $results += Invoke-MetaCompile -ProjectRoot $ProjectRoot -MetaEditor $metaEditor -SourceFile $sourceFile -LogFile $logFile
    }

    $reportPath = Join-Path $LogDir "compile_report.txt"
    $reportLines = @()
    $reportLines += "EXP0013 Astro Suite Compile Report"
    $reportLines += "MetaEditor: $metaEditor"
    $reportLines += "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    $reportLines += ""

    foreach ($result in $results) {
        $reportLines += "FILE: $($result.source)"
        $reportLines += "EXIT: $($result.exit_code)"
        $reportLines += "LOG:  $($result.log_file)"
        $reportLines += "LOG_EXISTS: $($result.log_exists)"
        $reportLines += "ARTIFACT: $($result.artifact_file)"
        $reportLines += "ARTIFACT_EXISTS: $($result.artifact_exists)"
        if ($result.errors.Count -gt 0) {
            $reportLines += "ERRORS:"
            $reportLines += $result.errors
        }
        if ($result.warnings.Count -gt 0) {
            $reportLines += "WARNINGS:"
            $reportLines += $result.warnings
        }
        $reportLines += ""
    }

    Set-Content -LiteralPath $reportPath -Value $reportLines -Encoding ASCII
    Write-Host "Compile report written to $reportPath" -ForegroundColor Green
}
finally {
    Pop-Location
}
